"""Let LlamaIndex package the same tool loop around a normal function.

Try: ask about C2 and inspect the actual TOOL print before the answer.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai_like import OpenAILike

load_dotenv()


def get_status(container_id: str) -> dict:
    """Read a recorded status for C1 or C2."""
    records = {"C1": "delayed", "C2": "on_time"}
    print("TOOL get_status:", container_id)
    if container_id not in records:
        raise ValueError("Unknown container")
    return {"container_id": container_id, "status": records[container_id]}


llm = OpenAILike(
    model="gpt-4.1-mini",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    is_chat_model=True,
    is_function_calling_model=True,
)
tool = FunctionTool.from_defaults(fn=get_status)
agent = FunctionAgent(
    tools=[tool],
    llm=llm,
    streaming=False,
    timeout=60,
    system_prompt="Use the status tool before reporting a recorded status.",
)


async def main():
    result = await agent.run(user_msg="What is C1's recorded status?", max_iterations=3)
    print("Answer:", result)


asyncio.run(main())
