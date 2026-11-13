# Model configuration for the delivered examples

Follow [Track B setup](track-b/SETUP.md) first. The delivered scripts specify their model and client directly; they do not implement a universal gateway or `COURSE_MODEL` configuration.

| Examples | Credential | Environment and model path |
| --- | --- | --- |
| B1–B5 core | `OPEN_AI_KEY` | Locked Track B environment. B1 uses LiteLLM; B2/B3 use SDK/framework clients; B4/B5 use the clients shown in their files. Most examples select GPT-4.1-mini explicitly. |
| B1 local model | No hosted key for the local request | Ollama must be running with the model in the [B1 guide](track-b/snippets/b1/README.md#before-the-local-example). |
| B6 core | `OPENAI_API_KEY` | Separate B6 environment; LlamaIndex OpenAI-like chat and embedding adapters configured in each file. Chat uses GPT-4.1-mini; embeddings use text-embedding-3-small. |
| Older optional references | Check the file/run guide | Some retain `OPENAI_API_KEY`; they are not evidence of a shared gateway contract. |
| Labs/notebooks | `OPEN_AI_KEY` | Their own setup guides load local or parent `.env` files without overriding exported values. |
| PortOps | None | Deterministic application without LLM dependencies. |

## Prepare credentials

From `track-b`, copy the supplied template and replace its placeholders locally:

```bash
cp snippets/.env.example snippets/.env
```

B1–B5 read `OPEN_AI_KEY`. If running B6, set `OPENAI_API_KEY` too; both may contain the same approved key. Exported environment variables also work. Python examples call `load_dotenv()` to find a local or parent file. Do not put real keys in source, notebook outputs or verification reports.

Hosted generation and judging consume API usage. Model access, endpoint compatibility and current billing must be checked in the account used for delivery. B1's comparison deliberately selects a second model in its source; edit that model explicitly when adapting the example.

## Boundaries

The current files do not read `COURSE_MODEL`, `COURSE_EMBED_MODEL` or `COURSE_COMPARE_MODEL`. No LiteLLM gateway configuration or PortOps AI service is distributed. Adapting to a local gateway or another provider is a separate exercise requiring code/configuration changes and verification of chat, tool and embedding capabilities.

See [B1–B5 setup](track-b/SETUP.md), [B6 setup](track-b/SETUP.md#later-modules), [lab setup](track-b/labs/container_help_desk/README.md#prepare-once) and [notebook setup](track-b/notebooks/README.md#prepare-the-notebook-environment).
