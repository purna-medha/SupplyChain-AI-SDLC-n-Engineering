"""Request JSON mode, then decode the actual returned text with Python.

Try: remove response_format and inspect what the parser receives.
"""

import json
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    response_format={"type": "json_object"},  # JSON syntax; schema checks are separate.
    messages=[
        {"role": "system", "content": "Return JSON only: container_id and status."},
        {"role": "user", "content": "Container C1 missed its planned departure."},
    ],
)
raw = response.choices[0].message.content
print("Raw reply:", raw)
try:
    note = json.loads(raw)
    print("Python value:", note, "type:", type(note).__name__)
except (json.JSONDecodeError, TypeError) as error:
    print("Cannot use this as JSON:", error)
