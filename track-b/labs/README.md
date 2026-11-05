# B1–B3 application labs

Build a **container help desk assistant** in three increments. Start by helping
a new colleague understand shipping terms, connect recorded container facts,
then prepare and review an evidence-based update.

Choose one version for a cohort. These are two versions of the same lab, not
six separate assignments.

Before applying the mechanisms here, learners can use the [B1–B3 exploration
notebooks](../notebooks/README.md) to inspect subtle behavior with complete
experiments. These labs keep their learner functions unfinished.

| Version | Data and application | Start |
| --- | --- | --- |
| Standalone | Tiny supplied synthetic records; no backend needed | [Container help desk](container_help_desk/README.md) |
| PortOps capstone | The existing FastAPI container and demurrage endpoints | [PortOps help desk](../../project-supplychain-sandbox-PortOps/labs/ai_container_help_desk/README.md) |

Both versions use the same TODO functions and checkpoint commands. The
PortOps version supplies a different `records.py` adapter and real seed IDs.
It does not require rebuilding the backend or copying completed standalone
answers. Each module can start independently.

| Module | Core learner work | Result |
| --- | --- | --- |
| B1 | 3 small functions: model call, instruction/messages, follow-up history | A shipping-terminology conversation with actual measurements |
| B2 | 4 functions: status read, fee read, local tool agent, MCP agent | Answers grounded in application observations |
| B3 | 5 functions: route, investigator, task save, review agent, review decision | A saved draft and an approval-gated local outbox action |

B3 has two optional functions for coordinator/specialist and handoff
comparisons. Hosted/local inference and a second framework/client are also
extensions. Plan approximately one hour for each module's core with prepared
dependencies and credentials; use the observations to adjust pace.

Functions marked TODO deliberately raise `NotImplementedError`. Supplied CLI,
records, HTTP access, runtime calls, files and MCP startup are complete. Each
guide identifies what to edit, what to run and what to observe. No learner
implementation is supplied as an answer key.

The current [slides](../slides-md/README.md) explain concepts and the
[snippets](../snippets/README.md) illustrate mechanisms before these labs.
Scaffold checks are in [tests](tests/test_scaffolding.py); they verify supplied
behavior, not whether a participant's unfinished answers are correct.
See the [verification record](VERIFICATION.md) for executed model, MCP, API and
approval checks and their limits.

