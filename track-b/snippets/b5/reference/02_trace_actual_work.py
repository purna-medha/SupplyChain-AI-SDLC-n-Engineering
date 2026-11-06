"""Repeat live SDK trials, inspect native spans and repair one tool rule.

Try: set MAX_TURNS to 1. Incomplete trials remain in the denominator.
All records and policies are synthetic. Trace capture stays local.
"""

import json
import os
from time import perf_counter
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, StrictInt
from agents import Agent, MaxTurnsExceeded, ModelSettings, RunConfig, Runner, function_tool
from agents import set_default_openai_key, set_trace_processors
from agents.tracing import TracingProcessor

MODEL = "gpt-4.1-mini"
REPEATS = 2
MAX_TURNS = 4


class Answer(BaseModel):
    container_id: str
    fee: StrictInt | None
    decision: Literal["clear", "review", "unknown", "denied", "unavailable"]
    source: str | None
    text: str


def grade(expected, actual, calls, reads):
    """The structured contract, separately probeable from the live runtime."""
    checks = {key: type(actual.get(key)) is type(value) and actual.get(key) == value
              and key in actual for key, value in expected.items()}
    cid = expected["container_id"]
    checks["tool_evidence"] = bool(calls) and all(
        call == {"tool": "read_fee", "arguments": {"container_id": cid}} for call in calls
    )
    checks["permitted_reads"] = (bool(reads) and all(item == cid for item in reads)
                                 if expected["source"] else not reads)
    return checks


class LocalTrace(TracingProcessor):
    """Retain SDK-created spans without the default hosted exporter."""

    def __init__(self):
        self.spans = []

    def on_trace_start(self, trace):
        print("TRACE:", trace.trace_id)

    def on_trace_end(self, trace):
        pass

    def on_span_start(self, span):
        pass

    def on_span_end(self, span):
        self.spans.append(span.export())

    def shutdown(self):
        pass

    def force_flush(self):
        pass


def run_trial(case, repaired, recorder):
    name, caller, cid, unavailable, fee, decision, source = case
    # Fresh tool state AND conversation for every trial. Caller is trusted host context.
    reads = []
    recorder.spans.clear()

    @function_tool
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

    agent = Agent(
        name="Container enquiry", model=MODEL, output_type=Answer,
        model_settings=ModelSettings(temperature=0, parallel_tool_calls=False),
        instructions=("Call read_fee for the requested ID. Copy its fee, decision and source "
                      "without changing them. Explain briefly in text. Null stays null. "
                      "Stop on unknown, denied or unavailable. Prepare only, queue nothing."),
        tools=[read_fee],
    )
    started = perf_counter()
    row = {"case": name, "version": "candidate" if repaired else "baseline",
           "passed": False, "status": "error", "input_tokens": None, "output_tokens": None,
           "estimated_usd": None}
    try:
        result = Runner.run_sync(
            agent, f"Prepare a fee update for {cid}.", max_turns=MAX_TURNS,
            run_config=RunConfig(workflow_name="B5 fee evaluation",
                                 trace_include_sensitive_data=True),
        )
        actual = result.final_output.model_dump()
        expected = dict(container_id=cid, fee=fee, decision=decision, source=source)
        functions = [s for s in recorder.spans if s and s["span_data"]["type"] == "function"]
        calls = [{"tool": s["span_data"]["name"],
                  "arguments": json.loads(s["span_data"]["input"])} for s in functions]
        checks = grade(expected, actual, calls, reads)
        usage = result.context_wrapper.usage
        # Standard text rates, USD per million tokens, checked 2026-11-05.
        # https://developers.openai.com/api/docs/models/gpt-4.1-mini
        cached = usage.input_tokens_details.cached_tokens
        estimated_cost = ((usage.input_tokens - cached) * 0.40 + cached * 0.10
                          + usage.output_tokens * 1.60) / 1_000_000
        row.update(status="completed", actual=actual, checks=checks,
                   passed=all(checks.values()), input_tokens=usage.input_tokens,
                   output_tokens=usage.output_tokens, cached_tokens=cached,
                   estimated_usd=round(estimated_cost, 8), model_requests=usage.requests)
    except MaxTurnsExceeded:
        row["status"] = "incomplete: max_turns"
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
    row["seconds"] = round(perf_counter() - started, 3)
    row["reads"] = reads
    # Native parent relationships and actual function arguments/outputs.
    for span in recorder.spans:
        if span and span["span_data"]["type"] in {"agent", "function", "response"}:
            print("SPAN:", json.dumps(span))
    print("TRIAL:", json.dumps(row))
    return row


def main():
    load_dotenv()
    set_default_openai_key(os.environ["OPEN_AI_KEY"])
    recorder = LocalTrace()
    set_trace_processors([recorder])  # Replaces the default hosted exporter.
    print("CONFIG:", MODEL, "temperature=0", "repeats=", REPEATS, "max_turns=", MAX_TURNS)
    cases = [
        ("below", "A", "C1", False, 100, "clear", "fees-v1"),
        ("boundary", "A", "C2", False, 200, "review", "fees-v1"),
        ("missing", "A", "C9", False, None, "unknown", None),
        ("denied", "B", "C2", False, None, "denied", None),
        ("dependency", "A", "C2", True, None, "unavailable", None),
    ]
    for repaired in [False, True]:
        rows = [run_trial(case, repaired, recorder)
                for case in cases for _ in range(REPEATS)]
        for case in cases:
            trials = [row for row in rows if row["case"] == case[0]]
            print("SUCCESS FREQUENCY:", trials[0]["version"], case[0],
                  sum(row["passed"] for row in trials), "/", len(trials))
        print("SUITE:", sum(row["passed"] for row in rows), "/", len(rows),
              "errors/incomplete:", sum(row["status"] != "completed" for row in rows))
    held_out = ("held-out above", "A", "C3", False, 201, "review", "fees-v1")
    for repaired in [False, True]:
        run_trial(held_out, repaired, recorder)
    print("COST: standard text-token estimate only. Recheck rates; failed-run usage is unknown.")


if __name__ == "__main__":
    main()
