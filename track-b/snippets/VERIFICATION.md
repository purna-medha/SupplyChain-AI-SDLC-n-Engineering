# B1/B2 verification · 4 November 2026

All 21 scripts passed default-example execution and selected output checks after reorganization: 11 core files and 10 extensions/references.

A fresh Python 3.12.2 environment was installed from both module requirements files. All 107 installed packages passed the dependency compatibility check. Model calls were real OpenAI/Ollama requests. Both MCP servers were exercised through their clients and stopped afterward.

| File | Result |
| --- | --- |
| [b1/01_openai_call.py](b1/01_openai_call.py) | PASS |
| [b1/02_ollama_call.py](b1/02_ollama_call.py) | PASS |
| [b1/03_system_instruction.py](b1/03_system_instruction.py) | PASS |
| [b1/04_conversation_history.py](b1/04_conversation_history.py) | PASS |
| [b1/05_text_to_token_ids.py](b1/05_text_to_token_ids.py) | PASS |
| [b1/06_compare_models.py](b1/06_compare_models.py) | PASS |
| [b1/extensions/01_context_growth.py](b1/extensions/01_context_growth.py) | PASS |
| [b1/reference/json_output.py](b1/reference/json_output.py) | PASS |
| [b1/reference/supply_context.py](b1/reference/supply_context.py) | PASS |
| [b1/reference/validate_schema.py](b1/reference/validate_schema.py) | PASS |
| [b2/01_status_function.py](b2/01_status_function.py) | PASS |
| [b2/02_openai_agent_with_tool.py](b2/02_openai_agent_with_tool.py) | PASS |
| [b2/03_llamaindex_agent.py](b2/03_llamaindex_agent.py) | PASS |
| [b2/04_shared_mcp_server.py](b2/04_shared_mcp_server.py) | PASS |
| [b2/05_openai_mcp_agent.py](b2/05_openai_mcp_agent.py) | PASS |
| [b2/extensions/01_llamaindex_mcp_agent.py](b2/extensions/01_llamaindex_mcp_agent.py) | PASS |
| [b2/reference/agent_without_tools.py](b2/reference/agent_without_tools.py) | PASS |
| [b2/reference/function_and_tool_schema.py](b2/reference/function_and_tool_schema.py) | PASS |
| [b2/reference/mcp_stdio_client.py](b2/reference/mcp_stdio_client.py) | PASS |
| [b2/reference/mcp_stdio_server.py](b2/reference/mcp_stdio_server.py) | PASS |
| [b2/reference/tool_round_trip.py](b2/reference/tool_round_trip.py) | PASS |

## Fix and limitations

The first run passed 20/21. The JSON reference received Markdown-fenced JSON that json.loads rejected. Requesting JSON mode fixed the response format; its live rerun parsed successfully and contained the expected container identifier and fields. The other 20 files were unchanged.

SmolLM2 runs successfully but its shipping explanations were inaccurate and sometimes truncated by the configured output limit. Execution success does not establish answer quality.

Both GPT-4.1-mini and GPT-5-nano returned answers and usage/cost estimates. Hosted calls require credentials and model access; local calls require Ollama and the downloaded model. The legacy manual tool reference uses OPENAI_API_KEY; revised core scripts use OPEN_AI_KEY. Both were configured for these runs.

The HTTP server handled calls from both agent clients. The stdio pair returned a successful C1 lookup and the expected C9 error. Suggested learner edits and all possible model outputs have not been exhaustively tested.

## Resolved direct dependencies

| Package | Version |
| --- | --- |
| litellm | 1.108.0 |
| openai | 2.54.0 |
| openai-agents | 0.20.0 |
| llama-index-core | 0.14.25 |
| llama-index-llms-openai | 0.8.3 |
| llama-index-tools-mcp | 0.6.0 |
| mcp | 2.3.0 |
| python-dotenv | 1.2.4 |
| tiktoken | 0.14.0 |
| pydantic | 2.14.2 |
