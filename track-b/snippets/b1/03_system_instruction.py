"""Add one system instruction to the same model-call shape.

Try: change one sentence to three numbered points; keep the question fixed.
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
question = "Briefly explain container dwell time in shipping."

response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=[
        {"role": "system", "content": "Answer in one short sentence."},
        {"role": "user", "content": question},
    ],
    max_tokens=100,
    temperature=0,
)
print(response.choices[0].message.content)
