# B5 assessment

Answer before consulting the instructor guide. Each question is worth 4 points: 2 for the correct behavior and 2 for its mechanism and limits (20 total). Explain predictions; a bare result is incomplete evidence.

1. For the rule “fee at least 200 requires review,” write an assertion that catches > used instead of >=. Explain why checking only 201 would miss the defect.
2. Cases 100, 200, 201 expect False, True, True. The implementation uses >200. State its outputs and pass rate. What is this rate measuring?
3. Name four fields in the tool trace. Why does a successful trace not establish business correctness, and why are its tiny duration samples not a benchmark?
4. A repair passes 3/3 where the original passed 2/3. What must remain unchanged for a valid comparison? What can this result not prove?
5. Explain why an injection-shaped tool name is rejected before dispatch. Then explain the order of deterministic field checks and an advisory model judge, including what the judge must never override.
