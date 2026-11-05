# B2 · Tools and MCP

Complete [shared setup](../../SETUP.md), then run from `track-b`:

```bash
uv run python snippets/b2/01_status_function.py
```

Add a container-status tool to the chatbot. Records are synthetic: C1 is delayed, C2 is on time, and C9 is unknown.

| File | Concept | Try changing |
| --- | --- | --- |
| [01_status_function.py](01_status_function.py) | Ordinary Python function | Look up C2, then C9 |
| [02_openai_agent_with_tool.py](02_openai_agent_with_tool.py) | Model requests; runtime executes | Compare general and status questions |
| [03_llamaindex_agent.py](03_llamaindex_agent.py) | Same tool through another runtime | Compare printed tool execution |
| [04_shared_mcp_server.py](04_shared_mcp_server.py) | Publish a shared tool | Add C3 and restart the server |
| [05_openai_mcp_agent.py](05_openai_mcp_agent.py) | Discover and call MCP tools | Ask about C3 |

Run 01–03 individually. Files 04–05 form one server/client example.

## Run MCP in two terminals

From `track-b`, start terminal A:

```bash
uv run python snippets/b2/04_shared_mcp_server.py
```

Leave it running at `http://127.0.0.1:8765/mcp`. In terminal B:

```bash
uv run python snippets/b2/05_openai_mcp_agent.py
```

The client prints discovered tools; the server prints execution. Only the agent client needs the OpenAI key. Stop the server with **Ctrl+C** afterward.

## Continue

- [Slides](../../slides-md/b2-tools-and-mcp.md) · [Lab](../../modules/b2/lab.md)
- [Exploration notebook](../../notebooks/b2_tools_contracts_and_mcp.ipynb) · [Notebook setup](../../notebooks/README.md)
- [Extension: LlamaIndex client for the same MCP server](extensions/README.md)
- [Reference: schemas, manual tool calls and stdio MCP](reference/README.md)
- [Requirements](requirements.txt) for standalone copies
