"""Trace one real SDK request and locate the incorrect observation.

Try: request C1 or unknown C9. Only synthetic payloads are captured locally.
"""

import os
from time import perf_counter
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, ModelSettings, RunConfig, Runner, function_tool
from agents import set_default_openai_key, set_trace_processors
from agents.tracing import Span
from agents.tracing.processors import BatchTraceProcessor, ConsoleSpanExporter

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])


class ReadableSpans(ConsoleSpanExporter):
    def export(self, items):
        for item in items:
            if not isinstance(item, Span):
                print("TRACE:", item.trace_id)
            else:
                print("SPAN:", item.span_data.type, item.span_id, "parent:", item.parent_id)
                if item.span_data.type == "function":
                    print("  Arguments:", item.span_data.input)
                    print("  Observation:", item.span_data.output)


processor = BatchTraceProcessor(ReadableSpans())
set_trace_processors([processor])  # Replace hosted export with local printing.


@function_tool
def read_fee(container_id: str) -> dict:
    """Read the recorded fee and the application's review decision."""
    fee = {"C1": 100, "C2": 200}.get(container_id)
    decision = "unknown" if fee is None else "review" if fee > 200 else "clear"
    return {"container_id": container_id, "fee": fee, "decision": decision}


agent = Agent(
    name="Fee assistant", model="gpt-4.1-mini", tools=[read_fee],
    model_settings=ModelSettings(temperature=0),
    instructions="Call read_fee. Report its fee and decision unchanged. Never invent a fee.",
)
container_id = "C2"
started = perf_counter()
try:
    result = Runner.run_sync(agent, f"Check {container_id}.", max_turns=4,
                             run_config=RunConfig(trace_include_sensitive_data=True))
    elapsed = perf_counter() - started
except MaxTurnsExceeded:
    print("INCOMPLETE: turn limit reached.")
    raise
finally:
    processor.force_flush()
print("ANSWER:", result.final_output)
print("POLICY EXPECTS:", {"C1": "clear", "C2": "review", "C9": "unknown"}[container_id])
print("Seconds:", round(elapsed, 3))
print("Token usage:", result.context_wrapper.usage.input_tokens,
      "input,", result.context_wrapper.usage.output_tokens, "output")
# ReadableSpans only formats native SDK spans. It does not create the execution record.
