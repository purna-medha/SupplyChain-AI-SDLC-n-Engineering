"""Publish a normal status function through an MCP server.

Run mcp_stdio_client.py; it launches this server as a separate process.
"""

from mcp.server import MCPServer

server = MCPServer("Container status")
records = {"C1": "delayed", "C2": "on_time"}


@server.tool()
def get_status(container_id: str) -> dict:
    """Read the recorded status of C1 or C2."""
    if container_id not in records:
        raise ValueError("Unknown container")
    return {"container_id": container_id, "status": records[container_id]}


if __name__ == "__main__":
    server.run(transport="stdio")
