"""Generate an actual answer, then judge it against a separate reference.

Try: change the question AND its independent reference; inspect actual feedback.
"""

import os
from dotenv import load_dotenv
from llama_index.core.evaluation import CorrectnessEvaluator
from llama_index.llms.openai import OpenAI

load_dotenv()
generator = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=200,
                   api_key=os.environ["OPEN_AI_KEY"])
judge = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=512,
               api_key=os.environ["OPEN_AI_KEY"])
context = """Synthetic snapshot fees-v1, observed 2026-11-06T00:00:00Z.
C2: recorded fee USD 200; status delayed.
Recorded fees of USD 200 or more require review.
No waiver, payment or release schedule information is supplied."""
question = "Explain C2's recorded fee, review requirement and whether it will be released tomorrow."
reference = "C2's recorded fee is USD 200 and requires review. Its release date cannot be determined from the supplied information."

# The reference is NOT part of the generation request.
answer = generator.complete(f"Answer the shipping enquiry.\nCONTEXT:\n{context}\nQUESTION: {question}").text
print("QUESTION:", question)
print("GENERATED ANSWER:", answer)
evaluator = CorrectnessEvaluator(llm=judge, score_threshold=4.0)
result = evaluator.evaluate(query=question, response=answer, reference=reference)
print("REFERENCE:", reference)
if result.invalid_result or result.score is None or not 1.0 <= result.score <= 5.0:
    raise RuntimeError("No valid in-range correctness judgment; inspect the evaluator failure.")
print("CORRECTNESS (1–5):", result.score, "PASS:", result.passing)
print("FEEDBACK:", result.feedback)
# A judge's score is evidence to inspect, not proof that every claim is correct.
