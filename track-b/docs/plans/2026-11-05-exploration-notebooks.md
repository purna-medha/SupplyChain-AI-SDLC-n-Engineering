# B1–B3 exploration notebooks

Create three complete, incremental Jupyter notebooks alongside the short
snippets and TODO application labs. Each experiment supplies a question,
prediction, small runnable code cell, interpretation and one controlled change.
Keep APIs visible and use synthetic shipping records. Notebook async calls
use top-level await. No learner solution from the application labs is filled.

- B1: tokenizer boundaries and bytes; message roles; actual response/usage;
  history versus isolated follow-ups; output limits; repeated calls and
  measurement; optional hosted/local comparison.
- B2: callable versus contract; proposal versus invocation; schema validation
  versus membership/permission; actual agent observations; MCP discovery,
  invocation and error results; optional MCP agent.
- B3: prescribed routes versus agent selection; turn limits and side effects;
  coordinator versus handoff ownership; session versus task data versus SDK
  state; explicit approval and resumption; checkpoint serialization.

Default runs execute deterministic experiments and explicitly skip actual
model/MCP calls. A single visible RUN_LIVE switch enables real inference;
missing credentials and service failures are not replaced by prepared output.
MCP, local inference and delegation each have separate opt-in switches.
Outputs are cleared in distributed notebooks and actual executions are kept
only in temporary verification artifacts. Explain notebook cell state and
restart/run-all before interpreting changed experiments.

- [x] Author notebooks, setup instructions, requirements and experiment map.
- [x] Validate notebook schema and execute all default paths from clean kernels.
- [x] Execute actual model paths and selected optional integrations with the
  prepared versions, distinguishing observations from guaranteed behavior.
- [x] Review educational/API correctness, fix findings and link the notebooks
  from the snippet/module/lab entrypoints.
