# B5 teaching outline · LOD 2

Module question: How do we distinguish a correct answer, a successful operation and a convincing explanation?

- Make requirements executable
  - Slide 1: B5 · Improvement needs evidence of changed behavior.
  - Slide 2: A requirement supplies the expected result.
  - Slide 3: An assertion turns one requirement into a check.
  - Slide 4: Predict the effect of excluding equality.
  - Slide 5: The boundary check exposes a specific defect.
  - Slide 6: A case table makes coverage inspectable.
  - Slide 7: Predict the case-level results before the score.
  - Slide 8: Two passing cases can hide the important failure.
  - Slide 9: Adding easy cases can inflate a misleading score.
- Trace and repair observable failures
  - Slide 10: A trace records execution, not a verdict.
  - Slide 11: Correlate actual outcomes across steps.
  - Slide 12: Predict a failed workflow step.
  - Slide 13: Preserve the error and stop dependent work.
  - Slide 14: Resource evidence needs real operations and explicit units.
  - Slide 15: Diagnosis connects an observation to a mechanism.
  - Slide 16: Predict a controlled repair.
  - Slide 17: The same cases isolate the improvement.
  - Slide 18: A regression test preserves a learned failure.
- Enforce actions and evaluate judgments
  - Slide 19: A proposed action remains data until dispatch.
  - Slide 20: An exact gate precedes the function call.
  - Slide 21: Predict which proposals reach the lookup.
  - Slide 22: Text cannot invent a callable in an exact registry.
  - Slide 23: Known facts and writing quality need different evidence.
  - Slide 24: Predict a flattering judgment on a wrong fee.
  - Slide 25: Known-rule failure stops the evaluation path.
  - Slide 26: A judge response is advisory evidence.
- Practice and transfer evidence
  - Slide 27: Repair the failing layer rather than polishing the symptom.
  - Slide 28: Practice moves from repair to unsupplied transfer.
  - Slide 29: Transfer begins by naming the evidence.
  - Slide 30: A claim must fit the evidence collected.

## Existing executable checkpoint map

1. `01_assertion_cases.py` — Assertions and case coverage.
2. `02_trace_tool.py` — Trace an actual operation.
3. `03_measure_repair.py` — Comparable before and after.
4. `04_allowlist.py` — Enforce allowed proposals.
5. `05_model_judge.py` — Advisory subjective evaluation.

The separate [seven teaching snippets](../../teaching-snippets/b5/README.md) expose the conceptual boundaries. The [three-activity plan](codealong-plan.md) maps them to these five snippets; an activity can use several snippets.
