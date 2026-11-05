# B5 standalone lab

Diagnose one failure, repair it, and preserve the evidence. This exercise has no model, server, seed file or capstone dependency.

## 1 · Worked example: inspect a controlled comparison

Run `snippets/b5/03_measure_repair.py` unchanged. Identify the one changed case and the two preserved cases. Explain why inputs, expectations and denominator remain fixed. This working example is your catch-up baseline; no earlier lab or live model is required.

## 2 · Guided practice: diagnose before editing

1. Save the starter below as `b5_lab.py` anywhere and run it.
2. Record the case-level results and 2/3 baseline. Explain the failure before editing.
3. Repair only the comparison, rerun identical cases and record 3/3.
4. Add an assertion over all cases; keep the boundary case as a regression test.
5. Choose one additional case after the repair and justify its expected result from the rule. Label it new evidence rather than silently adding it to the before/after denominator. Do not claim faster performance from these tiny timing samples.

```python
import time

cases = [(100, False), (200, True), (201, True)]

def needs_review(fee):
    return fee > 200  # Deliberate bug.

passed = 0
for fee, expected in cases:
    start = time.perf_counter()
    actual = needs_review(fee)
    elapsed_ms = (time.perf_counter() - start) * 1000
    passed += int(actual == expected)
    print(fee, actual, expected, round(elapsed_ms, 4))
print("passed:", passed, "/", len(cases))
# TODO: keep the same cases, repair the rule and assert every case passes.
```

## 3 · Independent extension: evaluate a changed policy

Start from your completed guided script. The new synthetic policy requires review only when a fee is at least 200 **and** the container is marked delayed. Design the function, a case table covering both sides of each decision, and a deliberately broken candidate that your cases expose. No implementation or expected-output table is supplied.

Write each expectation from the policy before running. Record case-level before/after results on the identical new case set; explain why the original three fee-only cases cannot establish this new behavior. Run `python3 b5_lab.py`: the broken candidate must have a named failing case and the repaired candidate must pass every new requirement. Retain the original rule checks separately rather than silently changing their meaning.

## Evidence to submit

Your completed script, before/after output where applicable, and two sentences explaining the mechanism. Before: False, False, True (2/3). After: False, True, True (3/3). Durations are measured and variable. Assertions should fail if the taught rule is broken; do not delete failing cases.

## Optional PortOps transfer

After the independent lab, identify a corresponding read or review rule in PortOps. Describe how you would preserve its real identity, policy and tests. The classroom amounts and >=200 rule do not replace PortOps business policy. No capstone change is needed to complete this lab.
