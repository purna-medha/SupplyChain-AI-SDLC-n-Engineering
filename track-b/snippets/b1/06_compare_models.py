"""Compare two models on one unchanged task and inspect actual usage.

Try: repeat the comparison; check the explanation before comparing speed.
"""

import os
from time import perf_counter
from dotenv import load_dotenv
from litellm import completion, completion_cost

load_dotenv()
messages = [
    {
        "role": "user",
        "content": "In one sentence, explain the difference between container dwell time and detention.",
    }
]

for model in ["openai/gpt-4.1-mini", "openai/gpt-5-nano"]:
    started = perf_counter()
    response = completion(
        model=model,
        api_key=os.environ["OPEN_AI_KEY"],
        messages=messages,
    )
    elapsed = perf_counter() - started
    print("Model:", model, "seconds:", round(elapsed, 3))
    print("Usage:", response.usage)
    print("Reply:", response.choices[0].message.content)
    cost_usd = completion_cost(completion_response=response, model=model)
    print(f"Estimated cost (USD): ${cost_usd:.8f}\n")

# Reasoning tokens count towards output usage and cost, even when not displayed.
# Repeat under similar conditions; one call is not a latency/quality benchmark.
