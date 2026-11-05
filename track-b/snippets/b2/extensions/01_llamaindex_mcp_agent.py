"""A second agent application uses the same running MCP server and records.

First: keep 04_shared_mcp_server.py running. No tool function is copied here.
Try: add C3 on the server, restart it, then ask both clients about C3.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

load_dotenv()


async def main():
    client = BasicMCPClient("http://127.0.0.1:8765/mcp")
    tools = await McpToolSpec(client=client).to_tool_list_async()
    print("Discovered:", [tool.metadata.name for tool in tools])
    agent = FunctionAgent(
        llm=OpenAI(model="gpt-4.1-mini", api_key=os.environ["OPEN_AI_KEY"]),
        tools=tools,
        system_prompt="Use get_container_status for recorded statuses. Never invent a status.",
        streaming=False,
    )
    result = await agent.run(user_msg="What is C2's recorded status?", max_iterations=4)
    print(result)


asyncio.run(main())
