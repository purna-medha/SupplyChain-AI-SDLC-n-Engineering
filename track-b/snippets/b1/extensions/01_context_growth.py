"""Measure actual input growth while resending a local model's conversation.

Try: keep only the system message and newest question before each call.
Compare the replies and the reported input tokens with the full-history run.
"""

from time import perf_counter
from litellm import completion

model = "ollama_chat/hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M"
messages = [
    {
        "role": "system",
        "content": "Explain shipping and port operations terms briefly.",
    }
]
questions = [
    "What is container dwell time?",
    "How does that differ from detention?",
    "Summarise the distinction in one sentence.",
]
total_input_tokens = 0

for turn, question in enumerate(questions, start=1):
    messages.append({"role": "user", "content": question})
    # Try here: messages = [messages[0], messages[-1]]
    print(f"\nTurn {turn} request:", messages)
    started = perf_counter()
    response = completion(
        model=model,
        api_base="http://localhost:11434",
        messages=messages,
        max_tokens=64,
        temperature=0,
    )
    elapsed = perf_counter() - started
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    total_input_tokens += response.usage.prompt_tokens
    print("Actual reply:", reply)
    print("Input tokens:", response.usage.prompt_tokens)
    print("Output tokens:", response.usage.completion_tokens)
    print(f"Seconds: {elapsed:.3f}")

print("\nTotal input tokens processed across calls:", total_input_tokens)
print("Provider API charge (USD): $0.00; local hardware/electricity excluded.")
# Each request has a context limit. More history consumes more of that budget.
# Inspect answer quality: a small model can give incorrect explanations.
