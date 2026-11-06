"""Use one narrow LlamaIndex rubric on prepared explanations.

Try: predict each judgment, then compare it with the actual feedback.
"""

import os
from dotenv import load_dotenv
from llama_index.core.evaluation import GuidelineEvaluator
from llama_index.llms.openai import OpenAI

load_dotenv()
evaluator = GuidelineEvaluator(
    llm=OpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
    guidelines=("Pass if the response plainly explains the fee and review decision. "
                "Accept paraphrases and either USD 200 or 200 USD. "
                "Fail unexplained codes or jargon-only responses. Judge clarity only."),
)
query = "Explain C2's recorded fee and whether review is required."
examples = [
    ("C2 has a recorded fee of USD 200 and requires review.", True),
    ("The charge for C2 is 200 USD. A reviewer must check it.", True),
    ("C2 F200 R1 XFLAG-A7.", False),
]
for text, expected in examples:
    result = evaluator.evaluate(query=query, response=text)
    print("\nDRAFT:", text)
    print("REFERENCE LABEL:", expected, "JUDGE:", result.passing)
    print("FEEDBACK:", result.feedback)

# These are classroom calibration labels, not established judge accuracy.
# This query/response evaluator does not verify source facts or authorize an action.
