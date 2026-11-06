"""Counterpart to ../../07_judge_clarity.py. Prepared drafts; real judge calls.

GEval judges the same clarity criteria. Its algorithm differs from LlamaIndex's.
"""

import os
from dotenv import load_dotenv
from deepeval.metrics import GEval
from deepeval.models import OpenAIModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

load_dotenv()
evaluator = GEval(
    name="Clarity", strict_mode=True, async_mode=False,
    model=OpenAIModel(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
    criteria=("Pass if the response plainly explains the fee and review decision. "
              "Accept paraphrases and either USD 200 or 200 USD. "
              "Fail unexplained codes or jargon-only responses. Judge clarity only."),
    evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
)
query = "Explain C2's recorded fee and whether review is required."
examples = [
    ("C2 has a recorded fee of USD 200 and requires review.", True),
    ("The charge for C2 is 200 USD. A reviewer must check it.", True),
    ("C2 F200 R1 XFLAG-A7.", False),
]
for text, expected in examples:
    evaluator.measure(LLMTestCase(input=query, actual_output=text))
    print("\nDRAFT:", text)
    print("REFERENCE LABEL:", expected, "JUDGE:", evaluator.is_successful())
    print("SCORE:", evaluator.score, "FEEDBACK:", evaluator.reason)
# These three labels are classroom calibration probes, not established accuracy.
# Clarity cannot prove source grounding or authorize an action.
