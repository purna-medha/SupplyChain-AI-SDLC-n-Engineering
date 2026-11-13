"""Generate real answers for a small case set; keep three judgments separate.

Try: inspect the failed answer/feedback before changing any prompt or threshold.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.core.evaluation import AnswerRelevancyEvaluator, CorrectnessEvaluator, FaithfulnessEvaluator
from llama_index.llms.openai import OpenAI

load_dotenv()
Settings.embed_model = None
generator = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=200,
                   api_key=os.environ["OPEN_AI_KEY"])
judge = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=512,
               api_key=os.environ["OPEN_AI_KEY"])
context = """Synthetic snapshot fees-v1, observed 2026-11-06T00:00:00Z.
C1: recorded fee USD 100; status on_time. C2: recorded fee USD 200; status delayed.
Recorded fees of USD 200 or more require review. C9 has no matching record.
No waiver, payment or release schedule information is supplied."""
cases = [
    ('known',
     "What is C2's recorded fee and is review needed?",
     'C2 has a recorded fee of USD 200 and requires review.'),
    ('missing',
     "What is C9's recorded fee?",
     'No matching C9 record is available in the snapshot; its fee cannot be stated and is not a known zero.'),
    ('future',
     'Will C2 be released tomorrow?',
     "The supplied information does not establish a release date; tomorrow's release cannot be confirmed."),
    ('premise',
     "C2's fee has been waived, so can I skip review?",
     'A waiver is not established. The recorded fee is USD 200 and requires review under the supplied policy.'),
]
judges = {"correctness": CorrectnessEvaluator(llm=judge),
          "grounding": FaithfulnessEvaluator(llm=judge),
          "relevance": AnswerRelevancyEvaluator(llm=judge)}
thresholds = {"correctness":4.0, "grounding":1.0, "relevance":1.0}
counts = {name:0 for name in judges}
for case_id, question, reference in cases:
    print("\nCASE:", case_id, "QUESTION:", question)
    try:
        answer = generator.complete(f"Answer the shipping enquiry.\nCONTEXT:\n{context}\nQUESTION: {question}").text
        print("GENERATED ANSWER:", answer)
    except Exception as error:
        print("GENERATION ERROR:", type(error).__name__, str(error))
        continue  # Still included in every len(cases) denominator below.
    for name, evaluator in judges.items():
        try:
            result = evaluator.evaluate(query=question, response=answer,
                                        reference=reference, contexts=[context])
            low, high = (1.0, 5.0) if name == "correctness" else (0.0, 1.0)
            valid = (not result.invalid_result and result.score is not None
                     and low <= result.score <= high)
            passed = valid and result.score >= thresholds[name]
            counts[name] += passed
            print(name, "SCORE:", result.score, "VALID:", valid, "PASS:", passed, "FEEDBACK:", result.feedback)
        except Exception as error:
            print(name, "JUDGE ERROR:", type(error).__name__, str(error))
for name in judges:
    print(name, "PASSES:", counts[name], "/", len(cases))
# Different score scales; thresholds are explicit teaching choices, not interchangeable scores.
