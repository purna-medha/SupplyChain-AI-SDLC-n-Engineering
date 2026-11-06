"""Calibrate one LlamaIndex clarity rubric against prepared, labelled examples.

Try: change a reference label, then inspect the disagreement before trusting scores.
Drafts here are prepared fixtures, not newly generated agent answers.
"""

import os
from time import perf_counter

from dotenv import load_dotenv
from llama_index.core.evaluation import GuidelineEvaluator
from llama_index.llms.openai import OpenAI

MODEL = "gpt-4.1-mini"
QUERY = "Explain C2's recorded fee and whether review is required."
GUIDELINES = (
    "Judge explanation clarity only. Pass when the response plainly explains the fee "
    "and review decision in understandable language. Accept paraphrases and either "
    "USD 200 or 200 USD. Fail an unexplained code or jargon-only response. "
    "Do not use length as a proxy for clarity. Do not judge source truth or authorize actions."
)


def main():
    load_dotenv()
    evaluator = GuidelineEvaluator(
        llm=OpenAI(model=MODEL, temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
        guidelines=GUIDELINES,
    )
    # Author-assigned classroom labels for calibration, separate from repair cases.
    examples = [
        ("clear", 200, "review", "C2 has a recorded fee of USD 200 and requires review.", True),
        ("paraphrase", 200, "review", "The charge for C2 is 200 USD. A reviewer must check it.", True),
        ("jargon", 200, "review", "C2 F200 R1 XFLAG-A7.", False),
        ("wrong fact", 999, "review", "C2's fee is USD 999 and requires review.", None),
    ]
    agreements = 0
    judged = 0
    for name, fee, decision, text, expected in examples:
        # Direct fact gate comes before a model judge. This is a structured-fact check.
        if fee != 200 or decision != "review":
            print(name, "FACT FAIL; judge skipped")
            continue
        started = perf_counter()
        try:
            result = evaluator.evaluate(query=QUERY, response=text)
            judged += 1
            agreements += result.passing == expected
            print(name, "reference:", expected, "judge:", result.passing,
                  "feedback:", result.feedback,
                  "seconds:", round(perf_counter() - started, 3))
        except Exception as exc:
            judged += 1  # Errors stay in the attempted-evaluation denominator.
            print(name, "JUDGE ERROR:", type(exc).__name__, str(exc))
    print("CALIBRATION AGREEMENT:", agreements, "/", judged)
    print("Judge usage/cost: unknown in this recorder; account separately from agent calls.")
    print("GuidelineEvaluator sees query/response. It does not establish source grounding.")


if __name__ == "__main__":
    main()
