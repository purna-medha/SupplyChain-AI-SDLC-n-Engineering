"""Call local SmolLM2 through the same LiteLLM interface as the OpenAI example.

First: ollama pull hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M
Try: change the question; compare the actual reply with 01_openai_call.py.
"""

from time import perf_counter
from litellm import completion

# Ollama runs the GGUF locally; LiteLLM provides the familiar response shape.
model = "ollama_chat/hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M"
question = "Briefly explain container dwell time in shipping."

started = perf_counter()
response = completion(
    model=model,
    api_base="http://localhost:11434",
    messages=[{"role": "user", "content": question}],
    max_tokens=100,
    temperature=0,
)
elapsed = perf_counter() - started

print(response.choices[0].message.content)
print(f"\nModel: {response.model}")
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Seconds: {elapsed:.3f}")
print("Provider API charge (USD): $0.00; local hardware/electricity excluded.")
# The first call can include model loading; repeat to observe a warm call.
# Check the answer: a successful call does not establish factual correctness.
