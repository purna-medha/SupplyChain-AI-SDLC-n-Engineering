"""Application adapter: change only the rule, leaving grading to Promptfoo."""


def call_api(prompt, options, context):
    fee = context["vars"]["fee"]
    repaired = options["config"]["repaired"]
    needs_review = fee >= 200 if repaired else fee > 200
    return {"output": "review" if needs_review else "clear"}
