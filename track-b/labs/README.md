# B1–B5 · Learner lab starters

Only the **standalone container help desk** is currently available. It uses supplied synthetic records and needs no PortOps backend.

These are delivered learner starters, not completed solutions or formal assessments. B1–B3 target 30–40 minutes;
B4/B5 target a 60-minute session including implementation, two experiments and
debrief. Prepare setup beforehand and validate timing in an instructor dry run.

Use the [same-lab exploration method](EXPLORATION.md): predict, change one thing,
run, inspect evidence and explain. The question banks deepen the existing
exercise without requiring extra application features.

| Module | Learner work | Instructions |
| --- | --- | --- |
| B1 | Model call, instructions and follow-up history | [B1](container_help_desk/B1.md) |
| B2 | Status/fee reads, tool agent and MCP agent | [B2](container_help_desk/B2.md) |
| B3 | Routing, investigation, saved task and reviewed local outbox | [B3](container_help_desk/B3.md) |
| B4 | Scoped SQLAlchemy reads, LlamaIndex SQL queries, correct totals and agent integration | [B4](container_help_desk/B4.md) |
| B5 | Real answer generation, correctness/grounding/relevance evaluation, judge calibration and prompt comparison | [B5](container_help_desk/B5.md) |

Start with the [lab setup](container_help_desk/README.md). The runner and fixtures are supplied; TODO functions remain unfinished. Each module starts independently. Specialist coordination and handoff are optional B3 extensions. Use the [exploration method](EXPLORATION.md) for experiments within the same lab.

The PortOps lab variant has been removed. B6's lab and formal assessments remain deferred. Teach B6 before B5 in the course; B5's lab can run independently without a B6 implementation.

See the [course map](../README.md), [B1–B3 checks](tests/test_scaffolding.py), [B4/B5 scaffold checks](tests/test_b4_b5_scaffolding.py), [current B5 checks](tests/test_b5_llm_scaffolding.py), [snippet reporting checks](tests/test_b5_snippet_controls.py) and [verification record](VERIFICATION.md). These validate supplied behavior, not learner answers or formal assessments.
