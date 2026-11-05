# Exploration notebook verification · 5 November 2026

Three notebooks contain **39 code cells** in total: B1 has 11, B2 has 11 and
B3 has 17. Each was validated with nbformat and executed from a clean Jupyter
kernel. Distributed notebooks retain no outputs or execution counts.

| Path | Executed result |
| --- | --- |
| Default Run All | All 39 cells completed; model/local/MCP branches explicitly reported skips |
| B1 live inference | Actual response/usage, history comparison, output cap and repeated requests passed |
| B2 deterministic boundaries | SDK argument rejections, unknown membership and scope rejection behaved as described |
| B2 live inference | No-tool/tool comparison and actual runtime items inspected |
| B2 MCP | Real discovery, direct invocation, unknown result, tool-error result and remote agent passed |
| B3 storage | Separate in-memory stores, shared temporary file store and task JSON round trip passed |
| B3 live inference | Actual investigation, session follow-ups and exhausted-turn observations inspected |
| B3 delegation | Coordinator retained the final reply; handoff ended with the charges specialist |
| B3 review | Actual SDK interruption, JSON snapshot restoration, rejection and approval both passed |
| Rejected-candidate regression | A scripted SDK model proposed a mismatched payload; running later cells could not execute it |

The approval regression was reproduced before its fix: a failed payload check
left a result available to later notebook cells. The proposal cell now clears
stale state, publishes only validated candidates and the review cell rechecks
the payload. Published/restored state is consumed to avoid accidental reuse.
The same regression probe then passed.

## Example observations from the live run

- B1's content-only input count was 20; the provider reported 31 request input
  tokens. The local count did not encode the complete formatted conversation.
- The follow-up with actual history recovered “Harbor Orion”; the isolated
  follow-up said it lacked that information.
- A three-token output cap returned `1. **` with finish reason `length`.
- Two temperature-zero repeats produced different wording. Neither matching
  nor differing outputs are guaranteed by a classroom repetition count.
- MCP returned an ordinary unknown result for C9 and an error result for a
  missing required argument.
- The one-turn agent run stopped as incomplete after its status-read tool
  had already executed.

These are observations from specific runs, not fixed expected answers or
promises about future model behavior.

## Environment and artifacts

The kernel used LiteLLM 1.108.0, OpenAI Agents 0.20.0, MCP 2.3.0, tiktoken
0.14.0 and ipykernel 7.4.0. The execution driver used nbformat 5.10.4 and
nbclient 0.10.2. Live calls used the configured workshop key and GPT-4.1-mini.
The MCP check started the existing classroom server on a temporary port.
Neither PortOps storage nor a customer messaging system was used.

Execution notebooks, logs and the regression probe are local temporary
artifacts under `/private/tmp/maersk-exploration-notebooks-20261105/`. They were
not written into the distributed teaching notebooks. Execution used actual
IPython kernels and top-level await, rather than only parsing the code cells.

One initial approval-path execution encountered provider DNS resolution failure
(`APIConnectionError`). A fresh retry passed; no prepared response replaced
the failed request. The temporary kernel also emitted its upstream TCP
transport warning; this did not produce a cell error.

## Limits

The optional Ollama cell was not executed in this check. It requires the
runtime/model preparation described in the B1 snippet guide. The notebooks
teach mechanisms and inspect small cases; these checks are not a production
quality, performance or reliability evaluation. Default skips establish no
evidence of successful inference or a successful MCP connection.
