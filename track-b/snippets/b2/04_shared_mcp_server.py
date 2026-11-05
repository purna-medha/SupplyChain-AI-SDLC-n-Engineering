"""Expose the same status function once; both agent applications can reuse it.

Run this before 05_openai_mcp_agent.py or the LlamaIndex extension.
Keep it in a separate terminal; stop with Ctrl+C.
"""

from mcp.server import MCPServer

server = MCPServer("Port operations classroom tools")


@server.tool()
def get_container_status(container_id: str) -> str:
    """Read a container's recorded status from the synthetic classroom records."""
    print("SERVER get_container_status:", container_id, flush=True)
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")


if __name__ == "__main__":
    server.run(transport="streamable-http", host="127.0.0.1", port=8765)
