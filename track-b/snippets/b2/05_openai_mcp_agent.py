"""Replace the in-process function with tools discovered from the MCP server.

First: run 04_shared_mcp_server.py in another terminal.
Try: ask for C2; observe the tool call printed in the server terminal.
"""

import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


async def main():
    async with MCPServerStreamableHttp(
        name="Port operations tools",
        params={"url": "http://127.0.0.1:8765/mcp"},
    ) as server:
        tools = await server.list_tools()
        print("Discovered:", [tool.name for tool in tools])
        agent = Agent(
            name="Port operations assistant",
            instructions="Use get_container_status for recorded statuses. Never invent a status.",
            model="gpt-4.1-mini",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "What is C1's recorded status?", max_turns=4)
        print(result.final_output)


asyncio.run(main())
