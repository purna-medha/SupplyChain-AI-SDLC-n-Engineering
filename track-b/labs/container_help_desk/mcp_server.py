"""Supplied MCP scaffolding: publish the SAME B2 functions in another process."""

import argparse

from mcp.server import MCPServer

from b2 import read_fee, read_status
from records import MCP_PORT

server = MCPServer("Container help desk")
server.tool()(read_status)
server.tool()(read_fee)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=MCP_PORT)
    args = parser.parse_args()
    print("Complete B2.1/B2.2 before invoking these tools. Stop with Ctrl+C.", flush=True)
    server.run(transport="streamable-http", host="127.0.0.1", port=args.port)

