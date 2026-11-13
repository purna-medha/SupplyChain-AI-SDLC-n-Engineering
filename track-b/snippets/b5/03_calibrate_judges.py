"""Check model judges on explicitly prepared, independently labelled answers.

These are calibration inputs, NOT claimed outputs from the generation model.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings
from llama_index.core.evaluation import CorrectnessEvaluator, FaithfulnessEvaluator
from llama_index.llms.openai import OpenAI

load_dotenv()
Settings.embed_model = None
judge = OpenAI(model="gpt-4.1-mini", temperature=0, max_tokens=512,
               api_key=os.environ["OPEN_AI_KEY"])
context = """Synthetic snapshot: C2 has a recorded fee of USD 200.
Recorded fees of USD 200 or more require review.
No release schedule information is supplied."""
question = "Explain C2's recorded fee, review requirement and release date."
reference = "C2 has a recorded fee of USD 200 and requires review. The supplied information does not establish a release date."
probes = [
    ("correct", reference, True),
    ("wrong amount", "C2 has a recorded fee of USD 999 and needs review. Its release date is unknown.", False),
    ("unsupported date", "C2 has a recorded fee of USD 200 and needs review. It will be released tomorrow.", False),
    ("unsupported denial", "C2 has a recorded fee of USD 200 and needs review. It will not be released tomorrow.", False),
    ("paraphrase", "The record lists 200 US dollars for C2, so review is needed. We cannot determine a release date from these facts.", True),
]
judges = {"correctness": CorrectnessEvaluator(llm=judge),
          "grounding": FaithfulnessEvaluator(llm=judge)}
thresholds = {"correctness":4.0, "grounding":1.0}
agreement = {name:0 for name in judges}
for label, answer, expected in probes:
    print("\nPREPARED PROBE:", label, "EXPECTED ACCEPTANCE:", expected)
    for name, evaluator in judges.items():
        try:
            result = evaluator.evaluate(query=question, response=answer,
                                        reference=reference, contexts=[context])
            low, high = (1.0, 5.0) if name == "correctness" else (0.0, 1.0)
            valid = (not result.invalid_result and result.score is not None
                     and low <= result.score <= high)
            accepted = result.score >= thresholds[name] if valid else None
            agreement[name] += valid and accepted == expected
            print(name, "SCORE:", result.score, "ACCEPTED:", accepted,
                  "MATCH:", valid and accepted == expected, "FEEDBACK:", result.feedback)
        except Exception as error:
            print(name, "ERROR:", type(error).__name__, str(error))
for name in judges:
    print(name, "AGREEMENT:", agreement[name], "/", len(probes))
# Disagreements/errors stay visible. Five classroom labels cannot establish judge accuracy.
