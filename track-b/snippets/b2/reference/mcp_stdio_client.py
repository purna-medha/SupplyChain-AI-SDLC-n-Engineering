"""Initialise, discover and call a tool across a real MCP process boundary.

Try: request C2, then an unknown ID, and inspect the server-owned result.
"""

import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_path = Path(__file__).with_name("mcp_stdio_server.py")
    parameters = StdioServerParameters(command=sys.executable, args=[str(server_path)])
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("Discovered:", [tool.name for tool in tools.tools])
            for container_id in ["C1", "C9"]:
                result = await session.call_tool(
                    "get_status", {"container_id": container_id}
                )
                print("Requested:", container_id, "is_error:", result.is_error)
                for content in result.content:
                    if content.type == "text":
                        print(content.text)


asyncio.run(main())
