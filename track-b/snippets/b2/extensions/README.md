# B2 · Optional MCP reuse demonstration

This example extends the [five-file core sequence](../README.md).

[01_llamaindex_mcp_agent.py](01_llamaindex_mcp_agent.py) connects a different agent application to the same MCP server. Start the core server once and leave it running.

From `track-b`, in terminal A:

```bash
uv run python snippets/b2/04_shared_mcp_server.py
```

In terminal B, with the same environment active:

```bash
uv run python snippets/b2/05_openai_mcp_agent.py
uv run python snippets/b2/extensions/01_llamaindex_mcp_agent.py
```

Inspect both actual calls in the server terminal. Add C3 on the server and restart it, then change both questions to C3. The clients do not need a copied status function or record dictionary.
