# Deepen understanding within the same lab

Keep the application small. Use **predict → change one thing → run → inspect
→ explain** to investigate the mechanism already implemented.

Each module's lab budget includes implementation and exploration. Choose
two questions from the module guide, rather than completing the whole question
bank. Use the remaining questions for discussion, faster participants or later
practice. Prepare dependencies and service access before starting the clock.

## Record one short explanation per experiment

| Item | What to record |
| --- | --- |
| Prediction | What do you expect, and why? |
| One change | Which input, instruction or configuration did you change? |
| Observation | What actually happened? Include the relevant request, read log, state field or side effect. |
| Explanation | Which mechanism explains that observation? |
| Limit | What would this observation alone fail to establish? |

A surprising result is useful evidence. An unchanged answer can also be useful:
inspect what information remained available before concluding that a change
had no effect. Do not force two model calls to differ or replace an unavailable
service with a prepared successful response.

## Three levels of questions

**Observe:** Which messages were sent? Which tool executed? Which state field
changed? What did the outbox contain before and after review?

**Explain:** Where did the answer's facts come from? Why was a request rejected?
Which component owns the next step or enforces the decision?

**Transfer:** What happens if that information is absent, an operation fails,
or the same action is requested again? Which part of the current lab handles
that case, and which guarantee has not been implemented?

The completion goal is an explanation supported by evidence from the run, not
only a successful command or an answer that sounds plausible.

## Current lab question banks

- [B1: instructions, history and operating observations](container_help_desk/B1.md#explore-the-same-lab--choose-two)
- [B2: capability, observations and MCP ownership](container_help_desk/B2.md#explore-the-same-lab--choose-two)
- [B3: workflow, retained context and review](container_help_desk/B3.md#explore-the-same-lab--choose-two)
- [B4: row grain, bound values, query evidence and execution limits](container_help_desk/B4.md#explore-the-same-lab--choose-two)
- [B5: generated-answer judgments, false passes, matched prompts and held-out cases](container_help_desk/B5.md#explore-the-same-lab--choose-two)

## Questions for the later B6 lab

The B4/B5 prompts now have concrete commands in their guides. B6's prompt
remains a design note until its lab is built.

| Module | Same-lab exploration prompts | Evidence to inspect |
| --- | --- | --- |
| B6 | Did retrieval find relevant evidence or merely return similar text? Does increasing top-k improve this answer? Can reranking recover a passage absent from its candidate pool? | Actual retrieved passages, source/metadata scope, candidate membership and supported claims |

For optional B0 practice, use the existing Python snippets: why can a value
conflict with its type hint and still run; how does a missing dictionary key
differ from an unknown business record; and does formatting a number change
the stored value? Require an actual small run to support each explanation.

## Instructor debrief

Ask learners to point to the evidence before explaining the concept. Accept
different model wording when the explanation remains supported. If someone
copies a correct answer, ask them to predict one fresh variation and explain
its actual outcome. Add application features only when they introduce a useful
learning decision that cannot be explored by changing the existing lab.
