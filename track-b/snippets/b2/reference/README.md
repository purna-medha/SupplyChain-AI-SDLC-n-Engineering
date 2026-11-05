# B2 · Supporting references

Use the [five-file teaching sequence](../README.md) first. These examples illustrate a preliminary wrapper and lower-level mechanisms. Their filenames describe the topic; they are not additional numbered lessons.

| File | Reference purpose |
| --- | --- |
| [agent_without_tools.py](agent_without_tools.py) | Wrap B1's no-tool behaviour in SDK objects |
| [function_and_tool_schema.py](function_and_tool_schema.py) | Inspect an ordinary function and an explicit advertised schema |
| [tool_round_trip.py](tool_round_trip.py) | Inspect proposal, argument checks, execution and correlated tool results |
| [mcp_stdio_server.py](mcp_stdio_server.py) | Expose a capability through a stdio server |
| [mcp_stdio_client.py](mcp_stdio_client.py) | Launch the adjacent server and perform discovery/invocation |

Keep the stdio pair together. The client resolves its server beside its own file. This pair is distinct from the core example's independently running shared HTTP server. The manual model example uses the earlier `OPENAI_API_KEY` configuration variable; the no-tool SDK wrapper uses `OPEN_AI_KEY`.
