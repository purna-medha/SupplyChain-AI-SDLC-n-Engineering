"""Repair the observed rule and rerun unchanged cases. No model call.

Try: change only the repaired condition; keep cases and references fixed.
"""


def review_decision(fee, repaired):
    requires_review = fee >= 200 if repaired else fee > 200
    return "review" if requires_review else "clear"


cases = [(100, "clear"), (200, "review")]
for repaired in [False, True]:
    print("\nCANDIDATE" if repaired else "\nBASELINE")
    for fee, expected in cases:
        actual = review_decision(fee, repaired)
        print("Fee:", fee, "expected:", expected, "actual:", actual,
              "PASS" if actual == expected else "FAIL")

# An additional above-boundary case, separate from the repair examples.
for repaired in [False, True]:
    actual = review_decision(201, repaired)
    print("Additional case, repaired:", repaired, "fee: 201", "expected: review", "actual:", actual)
