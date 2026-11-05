# B1 · Model calls, messages and tokens

Complete [shared setup](../../SETUP.md), then run from `track-b`:

```bash
uv run python snippets/b1/01_openai_call.py
```

Build a chatbot that answers general shipping questions. Run the six files in order; change one thing at a time.

| File | Concept | Try changing |
| --- | --- | --- |
| [01_openai_call.py](01_openai_call.py) | Hosted model call | Ask another shipping question |
| [02_ollama_call.py](02_ollama_call.py) | Local open-weight model call | Compare its answer with OpenAI's |
| [03_system_instruction.py](03_system_instruction.py) | Instructions shape the answer | Request three numbered points |
| [04_conversation_history.py](04_conversation_history.py) | History supplies follow-up context | Remove the previous exchange |
| [05_text_to_token_ids.py](05_text_to_token_ids.py) | Token IDs, counts and decoding | Add punctuation |
| [06_compare_models.py](06_compare_models.py) | Quality, tokens, latency and estimated cost | Repeat the same comparison |

## Before the local example

Install [Ollama](https://ollama.com/download) and keep its app running, or run `ollama serve` in another terminal. Download the model before class:

```bash
ollama pull hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M
uv run python snippets/b1/02_ollama_call.py
```

Check answer quality: this tiny model can misunderstand shipping terms. Run the tokenizer once online before class to cache its vocabulary; it uses GPT-4.1-mini's tokenizer.

## Continue

- [Slides](../../slides-md/b1-llm-applications.md) · [Lab](../../modules/b1/lab.md)
- [Exploration notebook](../../notebooks/b1_messages_tokens_and_generation.ipynb) · [Notebook setup](../../notebooks/README.md)
- [Extension: context growth](extensions/README.md)
- [Reference: grounding, JSON and schemas](reference/README.md)
- [Requirements](requirements.txt) for standalone copies
