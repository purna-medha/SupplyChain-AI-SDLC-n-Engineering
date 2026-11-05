"""Inspect configuration without revealing a key. Try: set PORTOPS_URL."""

import os
import sys

portops_url = os.environ.get("PORTOPS_URL", "http://127.0.0.1:8002")
has_model_key = bool(os.environ.get("OPEN_AI_KEY"))

print("Python executable:", sys.executable)
print("Configured PortOps URL:", portops_url)
print("Model key is configured:", has_model_key)
# A .env text file is not loaded automatically by Python; B1 uses python-dotenv.

