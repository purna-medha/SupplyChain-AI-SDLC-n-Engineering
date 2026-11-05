"""Make one OpenAI model call and show token usage and estimated USD cost.

Try: change the question and inspect the new reply.
"""

import os
from dotenv import load_dotenv
from litellm import completion, completion_cost

load_dotenv()

model = "openai/gpt-4.1-mini"
question = "Briefly explain container dwell time in shipping."

response = completion(
    model=model,
    api_key=os.environ["OPEN_AI_KEY"],
    messages=[{"role": "user", "content": question}],
    max_tokens=100,
    temperature=0,
)
print(response.choices[0].message.content)

print(f"\nModel: {response.model}")
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
# Estimate from actual usage and LiteLLM's model pricing; billing may differ.
cost_usd = completion_cost(completion_response=response, model=model)
print(f"Estimated cost (USD): ${cost_usd:.8f}")


# Model families seen in this key's OpenAI model list (2026-11-04).
# Set model to "openai/" + one of these names; for example, "openai/gpt-5-nano".
# GPT-4.1: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano.
# GPT-4o:  gpt-4o, gpt-4o-mini.
# GPT-5:   gpt-5, gpt-5-mini, gpt-5-nano, gpt-5.1, gpt-5.2,
#          gpt-5.4, gpt-5.5.
# GPT-6:   gpt-6-astra, gpt-6-luna, gpt-6-sol, gpt-6.1-sol, gpt-6.1-terra.
# Listing does not guarantee a successful call; model/endpoint support can differ.
# OpenAI's docs mark gpt-4.1-nano as shut down despite its presence in the list.
#
# Cheap testing options: standard USD per 1M text tokens, input / output:
# gpt-5-nano:  $0.05 / $0.40 (lowest token rates here; deprecated).
# gpt-6-luna:  $0.10 / $0.50 (current low-cost option).
# gpt-4o-mini: $0.15 / $0.60 (simple chat, JSON and tool-call tests; deprecated).
# Reasoning tokens also cost money, so compare the printed cost per request.
# For gpt-6-luna tool calling via completion(), add reasoning_effort="none".
# Prices/status: https://developers.openai.com/api/docs/models (2026-11-04).
