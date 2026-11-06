"""Apply the same fee cases and criteria through LlamaIndex.

Try: change max_iterations to 1. Inspect events and incomplete outcomes.
Native spans provide timing/parents; tool events provide arguments/results.
"""

import asyncio
import json
import os
from time import perf_counter
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, StrictInt
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult
from llama_index.core.instrumentation import get_dispatcher
from llama_index.core.instrumentation.span_handlers import SimpleSpanHandler
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

MODEL = "gpt-4.1-mini"
REPEATS = 2
MAX_ITERATIONS = 4


class Answer(BaseModel):
    container_id: str
    fee: StrictInt | None
    decision: Literal["clear", "review", "unknown", "denied", "unavailable"]
    source: str | None
    text: str


def grade(expected, actual, calls, reads):
    """The same structured contract as the SDK example, with explicit evidence."""
    checks = {key: type(actual.get(key)) is type(value) and actual.get(key) == value
              and key in actual for key, value in expected.items()}
    cid = expected["container_id"]
    checks["tool_evidence"] = bool(calls) and all(
        call == {"tool": "read_fee", "arguments": {"container_id": cid}} for call in calls
    )
    checks["permitted_reads"] = (bool(reads) and all(item == cid for item in reads)
                                 if expected["source"] else not reads)
    return checks


async def run_trial(case, repaired, spans):
    name, caller, cid, unavailable, fee, decision, source = case
    reads = []
    events = []
    spans.completed_spans.clear()
    spans.dropped_spans.clear()

    def read_fee(container_id: str) -> dict:
        """Read the permitted recorded fee and its review decision. Never infer absent data."""
        records = {"C1": ("A", 100), "C2": ("A", 200), "C3": ("A", 201)}
        result = dict(container_id=container_id, fee=None, decision="unknown", source=None)
        record = records.get(container_id)
        if record is None:
            return result
        if caller != record[0]:
            return {**result, "decision": "denied"}
        if unavailable:
            return {**result, "decision": "unavailable"}
        reads.append(container_id)
        amount = record[1]
        review = amount >= 200 if repaired else amount > 200
        return {**result, "fee": amount, "decision": "review" if review else "clear",
                "source": "fees-v1"}

    # A new agent/context each trial, with no inherited conversation or task state.
    agent = FunctionAgent(
        llm=OpenAI(model=MODEL, temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
        tools=[FunctionTool.from_defaults(fn=read_fee)], output_cls=Answer,
        system_prompt=("Call read_fee for the requested ID. Copy its fee, decision and source "
                       "without changing them. Explain briefly in text. Null stays null. "
                       "Stop on unknown, denied or unavailable. Prepare only, queue nothing."),
        streaming=False, allow_parallel_tool_calls=False, timeout=45,
    )
    started = perf_counter()
    row = {"case": name, "version": "candidate" if repaired else "baseline",
           "passed": False, "status": "error", "input_tokens": None, "output_tokens": None}
    try:
        handler = agent.run(user_msg=f"Prepare a fee update for {cid}.",
                            max_iterations=MAX_ITERATIONS)
        async for event in handler.stream_events():
            if isinstance(event, ToolCallResult):
                observation = dict(tool=event.tool_name, arguments=event.tool_kwargs,
                                   output=str(event.tool_output), error=event.tool_output.is_error)
                events.append(observation)
                print("TOOL EVENT:", json.dumps(observation))
        result = await handler
        actual = Answer.model_validate(result.structured_response).model_dump()
        expected = dict(container_id=cid, fee=fee, decision=decision, source=source)
        calls = [{"tool": event["tool"], "arguments": event["arguments"]}
                 for event in events if not event["error"]]
        checks = grade(expected, actual, calls, reads)
        checks["tool_errors"] = not any(event["error"] for event in events)
        row.update(status="completed", actual=actual, checks=checks, passed=all(checks.values()))
    except Exception as exc:
        # Includes bounded-workflow errors. Keep the concrete type and failed trial.
        row["error"] = f"{type(exc).__name__}: {exc}"
        if "max" in str(exc).lower() or "timeout" in type(exc).__name__.lower():
            row["status"] = "incomplete"
    row["seconds"] = round(perf_counter() - started, 3)
    row["reads"] = reads
    print("SPAN COUNTS:", len(spans.completed_spans), "completed,",
          len(spans.dropped_spans), "dropped")
    for span in spans.completed_spans[-5:]:
        print("NATIVE SPAN:", span.id_, "parent:", span.parent_id,
              "seconds:", round(span.duration, 4))
    print("TRIAL:", json.dumps(row))
    return row


async def main():
    load_dotenv()
    spans = SimpleSpanHandler()
    get_dispatcher().add_span_handler(spans)
    print("CONFIG:", MODEL, "temperature=0", "repeats=", REPEATS,
          "max_iterations=", MAX_ITERATIONS)
    cases = [
        ("below", "A", "C1", False, 100, "clear", "fees-v1"),
        ("boundary", "A", "C2", False, 200, "review", "fees-v1"),
        ("missing", "A", "C9", False, None, "unknown", None),
        ("denied", "B", "C2", False, None, "denied", None),
        ("dependency", "A", "C2", True, None, "unavailable", None),
    ]
    for repaired in [False, True]:
        rows = []
        for case in cases:
            for _ in range(REPEATS):
                rows.append(await run_trial(case, repaired, spans))
        for case in cases:
            trials = [row for row in rows if row["case"] == case[0]]
            print("SUCCESS FREQUENCY:", trials[0]["version"], case[0],
                  sum(row["passed"] for row in trials), "/", len(trials))
        print("SUITE:", sum(row["passed"] for row in rows), "/", len(rows),
              "errors/incomplete:", sum(row["status"] != "completed" for row in rows))
    held_out = ("held-out above", "A", "C3", False, 201, "review", "fees-v1")
    for repaired in [False, True]:
        await run_trial(held_out, repaired, spans)
    print("USAGE/COST: unknown in this recorder, not zero. Structured formatting also uses the LLM.")


if __name__ == "__main__":
    asyncio.run(main())
