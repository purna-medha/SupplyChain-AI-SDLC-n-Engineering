# B2 teaching outline (LOD 2)

Module question: How can a model use an owned fact without acquiring execution authority?

- Capability and contract
  - Slide 1: B2 · A model proposes; the host executes.
  - Slide 2: A useful answer needs evidence outside the model.
  - Slide 3: Defining a function makes a capability available.
  - Slide 4: Predict which action performs a read.
  - Slide 5: Invocation crosses the capability boundary.
  - Slide 6: The model needs a contract it can read.
  - Slide 7: A schema describes the argument boundary.
  - Slide 8: Predict what advertising the schema executes.
  - Slide 9: Contract text does not execute or supply defaults.
- Request and host admission
  - Slide 10: The first model call returns a proposed operation.
  - Slide 11: A request carries identity as well as arguments.
  - Slide 12: Predict whether a plausible request should run.
  - Slide 13: Host admission is a sequence of distinct checks.
  - Slide 14: Validation must precede execution.
  - Slide 15: Diagnose a dispatcher that reads before checking.
  - Slide 16: Repair the order and measure the side effect.
  - Slide 17: Exact keys prevent accidental argument acceptance.
- Observation and correlation
  - Slide 18: The observation belongs to the execution owner.
  - Slide 19: The conversation must retain both sides of the call.
  - Slide 20: Predict the effect of losing the correlation ID.
  - Slide 21: Correlation identifies a request, not a container.
  - Slide 22: A second model call can interpret the observation.
- Process boundary and transfer
  - Slide 23: MCP moves a capability across a process boundary.
  - Slide 24: The server publishes; the client discovers.
  - Slide 25: Initialization precedes discovery and invocation.
  - Slide 26: Predict the result of a validly shaped unknown ID.
  - Slide 27: The server retains responsibility for record facts.
  - Slide 28: Practice transfers the boundary to ETA reads.
  - Slide 29: Trace ownership before adding another tool.

## Teaching mechanisms and composition

- [Ordinary capability](../../teaching-snippets/b2/s01_capability.py): snippet 1.
- [Tool contract](../../teaching-snippets/b2/s02_tool_contract.py): snippet 2.
- [Real proposed call](../../teaching-snippets/b2/s03_proposed_call.py): snippet 3.
- [Host admission and dispatch](../../teaching-snippets/b2/s04_admission_dispatch.py): snippet 4.
- [Return the observation](../../teaching-snippets/b2/s05_return_observation.py): snippet 5.
- [MCP server](../../teaching-snippets/b2/s06_mcp_server.py): snippet 6.
- [MCP client](../../teaching-snippets/b2/s07_mcp_client.py): snippet 7.

The [activity plan](codealong-plan.md) groups these into two activities and maps all five existing composition checkpoints. A snippet, activity and Python file are different units.
