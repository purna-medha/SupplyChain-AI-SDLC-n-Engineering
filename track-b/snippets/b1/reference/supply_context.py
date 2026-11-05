"""Supply a synthetic record as evidence for a specific question.

Try: change only the fee, then remove the record. Inspect the actual answers.
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
record = "Container C1 has a USD 1500 fee as of 2026-09-22."

response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=[
        {
            "role": "system",
            "content": "Use supplied facts. Say when evidence is missing.",
        },
        {"role": "user", "content": f"Record: {record}\nWhat is C1's fee?"},
    ],
)
print(response.choices[0].message.content)
