"""Trace an actual data read and model explanation under one run ID.

Try: change the requested ID; inspect the observation before judging the reply.
"""

import json
import os
from time import perf_counter
from uuid import uuid4
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
run_id = str(uuid4())
records = {"C1": 100, "C2": 200}
container_id = "C1"
facts = {"container_id": container_id, "fee": records[container_id]}
print(json.dumps({"run_id": run_id, "step": "read_fee", "result": facts}))

started = perf_counter()
response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    messages=[{"role": "user", "content": f"Explain these supplied facts: {facts}"}],
)
event = {
    "run_id": run_id,
    "step": "explain",
    "parent": "read_fee",
    "elapsed_seconds": perf_counter() - started,
    "input_tokens": getattr(response.usage, "prompt_tokens", None),
    "output_tokens": getattr(response.usage, "completion_tokens", None),
    "reply": response.choices[0].message.content,
}
print(json.dumps(event))
# A successful trace shows execution; it does not establish factual correctness.
