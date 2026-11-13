# Standalone lab verification · 6 November 2026

Current pack: B1–B5 learner drafts. B4's database lab is unchanged. B5 now evaluates actual generated answers: cases, generation, evaluator configuration/invocation and a candidate prompt. Its former rule-testing lab is a [supporting reference](container_help_desk/B5-APPLICATION-CHECKS-REFERENCE.md), with [historical verification](reference/VERIFICATION-APPLICATION-CHECKS.md).

## Current checks

From the repository root:

```bash
track-b/.venv/bin/python -m unittest discover -s track-b/labs/tests -v
```

**24 tests passed.** These cover existing B1–B3 behavior, B4 scope/policy/query failure, preserved application-reference controls, the current B5 runner and five new snippet-control regressions. The new regressions were observed failing before the guard/error-handling fixes and passing afterward. They use controlled model/evaluator IO and make no real model calls; they verify application behavior, not judge accuracy or a provider outage.

Current B5 runner checks establish that references are not forwarded to generation, invalid/missing/nonfinite/out-of-range scores cannot pass, normalized relevance is handled without a `passing` field, one judge error does not erase later judgments, every generation failure remains in both comparison versions, and unfinished learner work stops as a TODO.

The delivered B4 and B5 starters each retain **five unimplemented functions**. Formal assessments and B6's lab remain deferred. [Current structured evidence](verification-b4-b5.json) contains hashes, actual run reports and limits.

## Revised B5 actual-model checks

Temporary completed copies exercised seven checkpoints/variations: offline cases, actual generation, one-answer evaluation, two-judge calibration, development dataset, full prompt comparison and selected-case repetition. All exited successfully, with actual text and evaluator feedback retained. The copies inherit the key from the existing repository environment; no key was copied into starters/reports. An initial temporary-runner key-loading mistake stopped before model work and was corrected without modifying the learner code.

The full comparison retained ten generated answers under fixed cases/judges/thresholds. Development acceptance tied at **3/4 for both prompts**, with held-out **1/1 for each**. Candidate's waiver answer passed correctness/grounding but received relevance 0.5 because the judge criticised not accepting the user's premise. It sees question/answer, not source context. The fixed pass threshold of 1 was retained; no higher score was manufactured.

A future-case repetition retained four attempts, two per prompt. Dataset/report evidence is separate from the core snippets' earlier comparison, which observed development 3/4→4/4. These are different actual generations and not pooled quality rates. Judge false positives, same-family correlation and small counts remain explicit limitations.

The lab saves actual answers, context/reference, per-metric score/status/feedback, errors, code hash, model IDs, thresholds and elapsed scope. Generation and judging both take resources; missing token usage stays unknown. A score of 0 is different from an invalid/error judgment with no score.

## Retained B4 verification

B4's nine completed-copy offline/variation checks and six actual-model checks remain in the structured record: metadata, owner-scoped reads, SQL-looking IDs, correct150/200 grain totals, policy/row-cap behavior, actual total/maximum/empty SQL results, agent evidence and one-turn stopping. A supplied unsafe SQL candidate was rejected by the actual database while public rows remained unchanged; that probe made no model call.

The trusted A projection and SQLite policy are classroom controls, not an identity-provider implementation or portable production isolation. Output caps, instruction budgets and agent turns constrain different work. No B4 implementation or model behavior changed during the B5 refocus.

## Environment and teaching limits

The existing Python 3.12.2 / SQLite 3.51.1 shared environment was reused. Lab requirement constraints match installed packages, including SQLAlchemy 2.1.8, Pydantic 2.14.2, openai-agents 0.20.0, openai 2.54.0, llama-index-core 0.14.25 and llama-index-llms-openai 0.8.3. No dependency upgrade was needed. A fresh isolated pip installation and Python 3.11 were not tested.

A fresh read-only review checked the core snippets, lab and teaching/evidence alignment. Its material score-range and per-judge-error findings were fixed with targeted regressions. B5's 36-slide deck was rendered/visually inspected and its Gamma text preserves visible content. Source syntax, command paths, local links and current evidence hashes were checked.

The proposed 60-minute lab timing remains unvalidated by an instructor dry run. Current generation/reference separation does not establish broad production reliability, permissions, concurrent recovery or delivery. No external messages, production records, commits or staging operations were involved.
