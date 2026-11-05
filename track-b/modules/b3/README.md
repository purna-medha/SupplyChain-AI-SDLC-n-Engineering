# B3 · Agents that manage a task

Use the [B3 exploration notebook](../../notebooks/b3_workflows_state_and_approval.ipynb)
to investigate state ownership, execution limits and review; [setup](../../notebooks/README.md).

Use the [36-slide lecture](../../slides-md/b3-agentic-workflows.md) and [six core examples](../../snippets/b3/README.md). The progression is multi-step autonomy → specialist coordination → memory, task state and human review.

The running scenario is a synthetic shipment-delay investigation and a customer update awaiting review. OpenAI Agents SDK is the main path; LlamaIndex and explicit parallelism are optional comparisons. B2 supplies the agent-loop and MCP foundations.

See the [teaching outline](teaching-outline.md), [illustration map](codealong-plan.md) and [shared setup](../../SETUP.md). The [B3 lab entrypoint](lab.md) links standalone and PortOps TODO starters for a saved investigation and human-reviewed local outbox action. Specialist coordination and handoffs are optional lab extensions. Earlier assessments retain their previous scope.
