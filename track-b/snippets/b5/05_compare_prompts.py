"""Compare fresh answers under two prompts; keep the same cases and judges.

Try: increase repeats. A tie or regression is a result; do not manufacture improvement.
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
    ('development', 'known',
     "What is C2's recorded fee and is review needed?",
     'C2 has a recorded fee of USD 200 and requires review.'),
    ('development', 'missing',
     "What is C9's recorded fee?",
     'No matching C9 record is available; its fee is unavailable, not a known zero.'),
    ('development', 'future',
     'Will C2 be released tomorrow?',
     "The supplied information does not establish a release date; tomorrow's release cannot be confirmed."),
    ('development', 'premise',
     "C2's fee has been waived, so can I skip review?",
     "A waiver is not established. C2's recorded fee is USD 200 and requires review."),
    ('held_out', 'comparison',
     "Compare C1 and C2's recorded fees and review requirements.",
     'C1 has a recorded fee of USD 100, below the review threshold. C2 has USD 200 and requires review.'),
]
prompts = {
    "baseline": "Answer the shipping enquiry helpfully.",
    "candidate": ("Answer using only supplied facts and policy. Correct unsupported premises. "
                  "Say when information is unavailable; do not infer waivers, balances or release dates. "
                  "Answer every requested part, preserving units and distinguishing observations from guarantees."),
}
judges = {"correctness": CorrectnessEvaluator(llm=judge),
          "grounding": FaithfulnessEvaluator(llm=judge),
          "relevance": AnswerRelevancyEvaluator(llm=judge)}
thresholds = {"correctness":4.0, "grounding":1.0, "relevance":1.0}
repeats = 1  # Each attempt makes a new generation request; increase for repeated evidence.
if repeats < 1:
    raise ValueError("repeats must be positive")
totals = {(version, split):[0,0] for version in prompts for split in ["development","held_out"]}
for version, instruction in prompts.items():
    for split, case_id, question, reference in cases:
        for attempt in range(repeats):
            totals[version, split][1] += 1  # Count errors/invalid judgments as unsuccessful attempts.
            print("\nVERSION:", version, "SPLIT:", split, "CASE:", case_id, "ATTEMPT:", attempt+1)
            try:
                answer = generator.complete(f"{instruction}\nCONTEXT:\n{context}\nQUESTION: {question}").text
                print("GENERATED ANSWER:", answer)
            except Exception as error:
                print("GENERATION ERROR:", type(error).__name__, str(error))
                continue  # Attempt already counted; there is no answer to judge.
            passes = []
            for name, evaluator in judges.items():
                try:
                    result = evaluator.evaluate(query=question, response=answer,
                                                reference=reference, contexts=[context])
                    low, high = (1.0, 5.0) if name == "correctness" else (0.0, 1.0)
                    valid = (not result.invalid_result and result.score is not None
                             and low <= result.score <= high)
                    passed = valid and result.score >= thresholds[name]
                    passes.append(passed)
                    print(name, "SCORE:", result.score, "VALID:", valid,
                          "PASS:", passed, "FEEDBACK:", result.feedback)
                except Exception as error:
                    passes.append(False)
                    print(name, "JUDGE ERROR:", type(error).__name__, str(error))
            totals[version, split][0] += all(passes)
for (version, split), (passed, attempted) in totals.items():
    print("SUMMARY:", version, split, passed, "/", attempted)
# Judge/rubric/model/cases stay fixed. Held-out feedback must not be used to tune this candidate.
# All-three pass is a declared summary; inspect each metric and case before concluding improvement.
