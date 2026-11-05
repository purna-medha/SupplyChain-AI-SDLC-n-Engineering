# B3 · Preserved earlier examples

Use the [six current teaching examples](../README.md) first. These files preserve the earlier mechanisms outside the required lecture path.

| File | Earlier purpose |
| --- | --- |
| [chain_and_route.py](chain_and_route.py) | Fixed/routed execution using prepared records |
| [manual_agent_loop.py](manual_agent_loop.py) | A manual model/tool exchange with a turn limit |
| [basic_framework_agent.py](basic_framework_agent.py) | A basic LlamaIndex status agent, substantially covered by B2 |
| [prepared_review_state.py](prepared_review_state.py) | Save a supplied review decision as JSON |

The shared uv environment includes their model libraries and compatibility adapter. These files retain their original credential setup. The model examples use OPENAI_API_KEY, LiteLLM or the OpenAI-compatible LlamaIndex adapter. For standalone use outside the shared uv project, the framework reference needs the requirements-rag.txt adapter dependencies in addition to the shared teaching dependencies. The prepared review fixture does not implement a human interruption or resumable SDK execution; the current [approval example](../06_human_approval.py) does.
