"""Judge whether an actual generated explanation is supported by its context.

Try: ask about tomorrow's release. No release schedule is supplied.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.llms.openai import OpenAI

load_dotenv()
Settings.embed_model = None  # Context evaluation needs no vector retrieval.
generator = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=200,
                   api_key=os.environ["OPEN_AI_KEY"])
judge = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=512,
               api_key=os.environ["OPEN_AI_KEY"])
context = """Synthetic snapshot fees-v1, observed 2026-11-06T00:00:00Z.
C2: recorded fee USD 200; status delayed.
Recorded fees of USD 200 or more require review.
No waiver, payment or release schedule information is supplied."""
question = "Explain C2's situation and what is known about its release date."
answer = generator.complete(f"Answer the shipping enquiry.\nCONTEXT:\n{context}\nQUESTION: {question}").text
print("CONTEXT:", context)
print("GENERATED ANSWER:", answer)
result = FaithfulnessEvaluator(llm=judge).evaluate(response=answer, contexts=[context])
if result.invalid_result or result.score not in (0.0, 1.0):
    raise RuntimeError("No valid binary grounding judgment.")
print("GROUNDED:", result.passing, "SCORE:", result.score)
print("FEEDBACK:", result.feedback)
# Grounding checks support for claims. It does not establish completeness or relevance.
