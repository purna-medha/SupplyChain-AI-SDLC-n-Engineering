"""Run the same model, function and question through LlamaIndex.

Try: ask for C2, then C9; compare with 02_openai_agent_with_tool.py.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

load_dotenv()


def get_container_status(container_id: str) -> str:
    """Read a container's recorded status from the synthetic classroom records."""
    print("TOOL get_container_status:", container_id)
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")


agent = FunctionAgent(
    llm=OpenAI(model="gpt-4.1-mini", api_key=os.environ["OPEN_AI_KEY"]),
    tools=[FunctionTool.from_defaults(fn=get_container_status)],
    system_prompt="Use get_container_status for recorded statuses. Never invent a status.",
    streaming=False,
)


async def main():
    result = await agent.run(user_msg="What is C1's recorded status?", max_iterations=4)
    print(result)


asyncio.run(main())
