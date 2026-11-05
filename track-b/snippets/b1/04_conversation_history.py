"""Resend the actual first exchange to make a follow-up understandable.

Try: send only the final user message on the second call. What is lost?
"""

import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()
messages = [{"role": "user", "content": "What is container dwell time? Answer in one sentence."}]

first = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=messages,
)
messages.append({"role": "assistant", "content": first.choices[0].message.content})
messages.append({"role": "user", "content": "How does that differ from detention?"})

second = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=messages,
)
print("Second request:", messages)
print("Reply:", second.choices[0].message.content)
