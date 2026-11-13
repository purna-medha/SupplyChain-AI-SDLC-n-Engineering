"""Observe the same fee investigation through LlamaIndex.

Try: request C1 or unknown C9; compare its tool observation with example 04.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult
from llama_index.core.instrumentation import get_dispatcher
from llama_index.core.instrumentation.span_handlers import SimpleSpanHandler
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

load_dotenv()
spans = SimpleSpanHandler()
get_dispatcher().add_span_handler(spans)


def read_fee(container_id: str) -> dict:
    """Read the recorded fee and the application's review decision."""
    fee = {"C1": 100, "C2": 200}.get(container_id)
    decision = "unknown" if fee is None else "review" if fee > 200 else "clear"
    return {"container_id": container_id, "fee": fee, "decision": decision}


agent = FunctionAgent(
    llm=OpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
    tools=[FunctionTool.from_defaults(fn=read_fee)], streaming=False, timeout=30,
    system_prompt="Call read_fee. Report its fee and decision unchanged. Never invent a fee.",
)
container_id = "C2"


async def main():
    handler = agent.run(user_msg=f"Check {container_id}.", max_iterations=4)
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            print("TOOL:", event.tool_name, "Arguments:", event.tool_kwargs)
            print("OBSERVATION:", event.tool_output)
    result = await handler
    print("ANSWER:", result)
    print("POLICY EXPECTS:", {"C1": "clear", "C2": "review", "C9": "unknown"}[container_id])
    for span in spans.completed_spans:
        if span.parent_id is None or span.id_.startswith("OpenAI.achat-"):
            print("SPAN:", span.id_, "parent:", span.parent_id, "seconds:", round(span.duration, 3))


asyncio.run(main())
# Tool events supply payloads. Native SimpleSpanHandler supplies parents/timing.
