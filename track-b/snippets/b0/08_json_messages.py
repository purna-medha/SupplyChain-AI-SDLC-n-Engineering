"""Convert Python data to JSON and back. Try: append an assistant message."""

import json

messages = [{"role": "user", "content": "What is container dwell time?"}]
request_text = json.dumps(messages)
restored_messages = json.loads(request_text)

print("Wire representation:", request_text)
print("Decoded Python type:", type(restored_messages).__name__)
print("First message text:", restored_messages[0]["content"])

