"""Wrap the B1 chatbot in an OpenAI Agent. No tools yet.

Try: change the instructions to answer in three short bullet points.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)

agent = Agent(
    name="Port operations assistant",
    instructions="Explain shipping and port terms in one short sentence.",
    model="gpt-4.1-mini",
)

result = Runner.run_sync(agent, "What is container dwell time?", max_turns=3)
print(result.final_output)
