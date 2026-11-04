# Shared model interface for Maersk courseware

All newly authored Maersk lessons use an **OpenAI-compatible API**. Choose hosted OpenAI or a local LiteLLM gateway backed by Ollama. The lesson code stays the same; endpoint, key and model names change. This standard applies to Track B, its PortOps AI reference extension, and future Track A model examples. Envestnet and the original non-AI PortOps project remain source references.

## One configuration contract

| Variable | Meaning |
| --- | --- |
| `OPENAI_API_BASE` | API base ending in `/v1`, not `/chat/completions` |
| `OPENAI_API_KEY` | Key for that API endpoint; gateway key for local LiteLLM |
| `COURSE_MODEL` | Chat model with LiteLLM's `openai/` routing prefix |
| `COURSE_EMBED_MODEL` | Embedding model name, with no LiteLLM prefix |
| `COURSE_COMPARE_MODEL` | Optional second chat model, also with `openai/` prefix |

The prefix selects the OpenAI-compatible protocol in LiteLLM; it does not mean the underlying model must be hosted by OpenAI. LlamaIndex and the reference HTTP client remove that routing prefix before sending a model name to the endpoint.

## Option A: hosted OpenAI

Set these in the terminal running the lessons. Replace the placeholders with model IDs available to your account. Set the real key through your shell or secret manager rather than committing it.

```bash
export OPENAI_API_BASE='https://api.openai.com/v1'
export OPENAI_API_KEY='<your-key>'
export COURSE_MODEL='openai/<your-chat-model-id>'
export COURSE_EMBED_MODEL='<your-embedding-model-id>'
```

Choose a chat model supporting Chat Completions and native tool calling for B2/B3/B6. RAG needs an embeddings model in addition to the chat model. The two are different capabilities; do not put the chat model ID in the embedding setting.

## Option B: local Ollama behind LiteLLM

The route is **lesson → OpenAI-compatible LiteLLM endpoint → Ollama**. Ollama serves the models; LiteLLM presents the common API. First install Ollama and pull a chat model with tool support plus an embedding model that fit your machine. This repository does not download weights or start servers automatically.

Install the gateway in its own environment to keep server dependencies separate from lesson dependencies:

```bash
python3 -m venv .venv-gateway
source .venv-gateway/bin/activate
python -m pip install 'litellm[proxy]>=1.97,<2'
```

In the gateway terminal, replace both model placeholders with the exact locally installed model tags. The route prefixes are intentional:

```bash
export OLLAMA_API_BASE='http://127.0.0.1:11434'
export OLLAMA_CHAT_ROUTE='ollama_chat/<installed-chat-tag>'
export OLLAMA_EMBED_ROUTE='ollama/<installed-embedding-tag>'
export LITELLM_MASTER_KEY='<your-local-gateway-key>'
litellm --config model-config/litellm-ollama.yaml --host 127.0.0.1 --port 4000
```

Ollama must already be running. In the separate lesson terminal, select the teaching environment and set:

```bash
export OPENAI_API_BASE='http://127.0.0.1:4000/v1'
export OPENAI_API_KEY='<same-local-gateway-key>'
export COURSE_MODEL='openai/course-chat'
export COURSE_EMBED_MODEL='course-embed'
```

The gateway key protects the gateway; it is not a hosted OpenAI credential. Tool support must be checked on the actual selected model; a capability flag or schema cannot manufacture it. Do not enable parameter dropping to hide incompatibilities.

For B1's two-model comparison, configure a second chat alias in the gateway or choose a second hosted model, then set `COURSE_COMPARE_MODEL`. Reusing one alias twice measures repeated calls, not two models.

## How examples use the interface

B1–B5 call `litellm.completion(model=os.environ['COURSE_MODEL'], ...)`. LiteLLM reads the shared endpoint/key environment variables. B6 uses LlamaIndex's `OpenAILike` and `OpenAILikeEmbedding` adapters with the same values explicitly supplied. No native Ollama or implicit default OpenAI embedding adapter is hidden in a lesson.

The optional `track-b/portops_ai` reference sends the same Chat Completions JSON over HTTP using these settings. Its constructor remains usable by tests, but its environment configuration uses the shared contract.

## Before a classroom session

Run the first model-call card and inspect actual text, then run B6's embeddings/retrieval card and inspect actual ranked nodes. B2's proposal/dispatch card verifies the next protocol capability. Record the exact backend/model tags used. A successful text response alone does not prove embeddings or tools work.

Rebuild a vector index when changing embedding models: document and query vectors must share a compatible space. A chat model change does not automatically require re-embedding documents.

`COURSEWARE_OFFLINE=1` explicitly skips network-dependent cards. It never substitutes successful model text or vectors. Offline structural checks and prepared evaluation fixtures are not live model validation.

## Implementation references

- [LiteLLM gateway configuration](https://docs.litellm.ai/docs/proxy/configs)
- [LiteLLM Ollama routes and tool support](https://docs.litellm.ai/docs/providers/ollama)
- [LlamaIndex OpenAI-like embeddings](https://developers.llamaindex.ai/python/framework-api-reference/embeddings/openai_like/)
