---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 27px; padding: 44px 55px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 20px; }
  table { font-size: 23px; }
---
<!-- _class: lead -->

# B3 · Agents that manage a task

Investigate a shipment delay and prepare an update for review

Adaptive execution · Specialist coordination · State and human decisions

<!--
Lecture: 60 minutes. Suggested pacing, including selected code illustrations: slides 2–13, 20 minutes; 14–24, 20 minutes; 25–34, 17 minutes; 35–36, 3 minutes. Explain each requirement and concept before showing code. Use one synthetic shipment investigation throughout. The six core files illustrate separate mechanisms; the LlamaIndex and parallel examples are optional comparisons. B2 already established the agent loop and MCP. Retain that foundation instead of teaching their setup again. No lab design is included in this deck.
-->

---

# A larger request for the assistant

B2's assistant can obtain a recorded status through a tool.

Now the user asks:

> Investigate C1's delay, assess its implications, and prepare a customer update for review.

The task needs several observations and decisions about what to do next.

<!--
Begin at B2's achieved capability. Its runtime already supports repeated decisions; the new requirement is coordinating a larger investigation. Ask which facts a status alone leaves unanswered: cause and scheduled onward movement. Charge exposure is introduced with the charges specialist. Do not equate more tools with a new kind of model. The application exposes more capabilities and decides which choices to delegate.
-->

---

# Evidence for the investigation

| Required information | Synthetic classroom source |
| --- | --- |
| Current status | Shipment record |
| Cause of the delay | Tracking events |
| Scheduled onward movement | Departure record |

A useful update preserves the source facts and identifies what remains unknown.

<!--
All records, dates and calculation rules are supplied teaching fixtures. C1 is delayed after a customs hold and a missed planned departure. Its next departure is scheduled for 2026-11-05 at 18:00 UTC; that is not confirmed movement. C2 is on time; C9 is absent.
-->

---

# A prescribed sequence

When every case needs the same information, the application can specify the order:

```text
Read status → read events → assemble a report
```

Each step supplies input to the next. Ordinary application code owns the sequence.

<!--
Establish the simplest architecture first. A model could write the report while code retains the sequence; adding a model does not automatically delegate orchestration. Ask what happens when this sequence runs for an on-time shipment. It still reads events because those steps were prescribed. The next requirement motivates a branch.
-->

---

# A branch avoids unnecessary work

```text
Read status
  ├── delayed → inspect events
  ├── on_time → report the status
  └── unknown → request a corrected identifier
```

The developer defines these conditions and their next steps.

This is a conditional workflow, even if a model later writes the answer.

<!--
Have participants predict C1, C2 and C9 before opening code. Missing membership is not evidence for a delay. Explain the extra review branch in the full file for a status outside the known vocabulary. Routing from a fixed condition differs from asking a model to determine the next information need.
-->

---

# Routing in application code

The code implements the conditions already described.

```python
if status is None:
    route = "clarify"
elif status == "delayed":
    route = "investigate"
    print("Evidence:", get_tracking_events(container_id))
elif status == "on_time":
    route = "finish"
```

Illustration: [fixed and conditional workflows](../snippets/b3/01_workflow_patterns.py)

<!--
The complete file first executes a fixed sequence, then runs this routing example for C1/C2/C9. Its output is labelled scripted; no model executes. Run it after the predictions. Point at the event read that C2 skips and the absence C9 cannot turn into a recorded status. The full file also handles unfamiliar statuses explicitly.
-->

---

# Decisions delegated to the agent

For a less predictable investigation, the model can choose:

- Which available capability answers the next information need.
- Which arguments to request using evidence already obtained.
- Whether another observation is needed before drafting.

The application still selects the available capabilities and enforces execution limits.

<!--
Make autonomy concrete through these choices. The model operates inside a runtime and an available tool set; it does not gain arbitrary functions or permission to change records. B2's decision/feedback loop is the mechanism underneath this larger task. A complex workflow can also retain prescribed portions: a hybrid design is common.
-->

---

# Capabilities available to one investigator

| Tool | Observation it can supply |
| --- | --- |
| `get_shipment_status(id)` | Recorded status or unknown |
| `get_tracking_events(id)` | Recorded events |
| `get_next_departure(id)` | Scheduled departure or missing value |

Each tool supplies an observation. The agent chooses the next lookup from the evidence.

<!--
The tools read tiny fixtures so decision making stays visible. Tool descriptions establish their purpose and limits. Business APIs, databases and caller scope become B4's subject. Direct callables keep this illustration short; the same business capabilities could be exposed through the MCP arrangement already taught.
-->

---

# An observation changes the next step

Possible paths through the same investigator:

```text
C1: delayed → inspect events and implications → draft update
C2: on_time → explain the observed status
C9: unknown → ask for a corrected ID
```

The next choice uses the returned observation. These are intended paths to inspect in an actual run.

<!--
Label this as a schematic, not a captured trace or a guarantee of tool choice. An argument derived from one lookup must wait for that result. Our C1 capabilities can share the same known identifier after status is established; a richer example could return a booking ID needed by another tool. Ask what would be wrong with continuing a delay investigation for an absent C9.
-->

---

# A task plan can change

A short plan names intended work, such as checking the delay and collecting evidence for an update.

After an observation, the agent may revise that plan or finish earlier.

The plan is a proposal. Tool observations establish the operational facts; the execution record shows which steps actually happened.

<!--
A short proposed checklist can explain intended work without requesting private reasoning. The core investigation needs no separate plan-recording tool. Inspect actual tool calls to see how observations affect the next step. Ask how an on-time status should change the investigation. A proposed plan, and even fluent planning text, does not prove that a lookup executed.
-->

---

# One agent with several capabilities

The familiar SDK objects now support the larger task.

```python
agent = Agent(
    name="Shipment investigator", model="gpt-4.1-mini",
    instructions=instructions,
    tools=[get_shipment_status, get_tracking_events, get_next_departure],
)
result = Runner.run_sync(agent, task, max_turns=6)
```

Illustration: [complete shipment investigation](../snippets/b3/02_agent_investigation.py)

<!--
This shortened configuration names the full file's instruction string and user request as instructions/task. The file includes typed tools, dotenv, OPEN_AI_KEY, actual execution prints and the final reply. Run C1 and inspect TOOL entries before reading the answer. Then inspect one changed case. Do not repeat the decorator and SDK introduction from B2. Source: https://developers.openai.com/api/docs/guides/agents/running-agents
-->

---

# Read the execution before trusting the update

Did the investigator obtain C1's status, cause and scheduled departure?

Does its draft preserve those observations and describe the departure as scheduled?

For C2 and C9, did it avoid inventing a delay investigation?

A fluent final answer and a completed runtime call are different evidence from a supported investigation.

<!--
Use actual output from the full file. The tool prints establish invocation; inspect returned fixture values in the source alongside the reply. A concise answer may omit a detail or overstate a schedule, so call success alone is insufficient. The systematic evaluation of these behaviours belongs to the later evaluation module; establish the habit here.
-->

---

# Completion, interruption and limits

| Outcome | Meaning for the application |
| --- | --- |
| Supported draft | Review the result against the required facts |
| Missing information | Clarify, obtain evidence or report the gap |
| Turn limit reached | Retain an incomplete outcome |

Turn limits do not bound total tool calls, tokens or spend.

**Predict:** the last allowed model call requests a lookup. The tool returns, but no call remains. Is the task complete?

<!--
The example catches MaxTurnsExceeded and prints an explicit incomplete outcome. Set max_turns to 1 to demonstrate stopping without claiming success. A proposed plan is not a stopping guarantee. Service errors and denied operations need their own policies; repeating an unchanged request cannot correct an absent ID or create permission. Keep detailed retry machinery outside this lecture. Source: https://developers.openai.com/api/docs/guides/agents/running-agents

Reasoning check: The lookup observation is progress, not a final answer based on that observation. If no model call remains to interpret it, report an incomplete run rather than success. Preserve the distinction between a model-turn limit and tool-call, token, spending or workflow-time budgets.
-->

---

# When a specialist helps

An operations investigation and a charge assessment may need different instructions, context and tools.

A specialist gives one responsibility a clear boundary.

Start with one agent. Add a specialist when that separation improves the task enough to justify additional calls and coordination.

<!--
Introduce specialization through a growing task requirement, before naming multi-agent APIs. In this tiny fixture a single agent can do the work; specialization is an architectural comparison, not a claim of improved accuracy. The useful distinction is separated responsibilities and tool sets. A differently named object calling the same prompt does not establish a meaningful specialist. Source: https://developers.openai.com/api/docs/guides/agents/orchestration
-->

---

# A coordinator retains the final answer

```text
User → Coordinator
         ├── Operations specialist → operational evidence
         └── Charges specialist    → illustrative exposure
              ↓ results return to coordinator
         Coordinator → combined customer update
```

The coordinator decides which specialist to call and combines the returned results.

<!--
Trace the return path. A specialist runs its own model/tool interaction; it is not merely an ordinary Python worker renamed as an agent. The coordinator remains responsible for the final user-facing reply. If only one kind of information is requested, invoking both specialists may be unnecessary. Context passing and tool access should match each responsibility.
-->

---

# The delegation contract

| Define before delegating | Example |
| --- | --- |
| Task and identifier | Assess C1's charge exposure |
| Available evidence and tools | Synthetic charge calculator |
| Expected result | Amount, units and limitations |
| Missing or failed evidence | Return the gap to the coordinator |

The coordinator must preserve uncertainty when assembling the result.

<!--
The worked example returns text from each specialist; a structured result schema would be a later refinement. Passing an identifier is not permission to access a production record. Specialist prose is still generated text, even when grounded in a tool result. Missing or disagreeing results need an explicit application policy; do not resolve conflict by treating the most confident wording as truth.
-->

---

# A specialist exposed as a tool

The SDK packages a specialist run as a capability of the coordinator.

```python
coordinator = Agent(
    name="Coordinator", model="gpt-4.1-mini",
    instructions=instructions,
    tools=[operations.as_tool(
        "investigate_operations", "Obtain operational evidence.",
        max_turns=4,
    )],
)
```

Illustration: [coordinator with two specialists](../snippets/b3/03_agents_as_tools.py)

<!--
The excerpt selects one of the full file's two specialist tools and shortens its description. Each specialist has its own tools and performs real model calls. Run the full file, inspect OPERATIONS TOOL and CHARGES TOOL, then FINAL OWNER. The coordinator remains the owner. Each nested specialist has a turn limit; the coordinator's outer limit does not bound the sum of all nested work. Source: https://developers.openai.com/api/docs/guides/agents/orchestration
-->

---

# A handoff transfers the conversation

Suppose the user asks specifically about charge exposure.

```text
User → Triage → Charges specialist → user-facing answer
```

The specialist becomes the active agent for that branch.

**Predict:** a specialist returns findings as a tool; another receives a handoff. Who should own the final answer in each arrangement?

<!--
Make the ownership distinction explicit before code. A handoff is not merely a specialist function returning a string. Available instructions and tools change with the active agent. Conversation context may transfer; a real application should choose what each specialist receives. This mechanism can also route to another narrow workflow, not only to a departmental persona. Source: https://developers.openai.com/api/docs/guides/agents/orchestration

Reasoning check: For the specialist-as-tool arrangement, results return to the coordinator, which owns the combined answer. With a handoff, the specialist becomes active and owns the response for that branch. Compare FINAL OWNER in the two complete examples after participants state their predictions.
-->

---

# Route to the agent that should answer

```python
triage = Agent(
    name="Triage", model="gpt-4.1-mini",
    instructions="Hand the request to the appropriate specialist.",
    handoffs=[operations, charges],
)
result = Runner.run_sync(triage, question, max_turns=6)
print("FINAL OWNER:", result.last_agent.name)
```

Illustration: [complete handoff example](../snippets/b3/04_handoff.py)

<!--
The file supplies both specialists, distinct tools and handoff descriptions. The excerpt shortens triage instructions and names the question. Ask participants to predict the final owner for a charge question, then run it. Change the question to scheduled departure and inspect actual routing. A handoff declaration does not guarantee a particular routing choice; inspect the specialist's tool execution and final owner.
-->

---

# The same responsibilities in LlamaIndex

| Responsibility | OpenAI Agents SDK | LlamaIndex |
| --- | --- | --- |
| Specialist definition | `Agent` | `FunctionAgent` |
| Permitted handoff targets | `handoffs` | `can_handoff_to` |
| Starting agent and execution | `Runner` | `AgentWorkflow` |

The architecture is the responsibility transfer. Framework objects implement that transfer.

<!--
B2 already compared basic agent runtimes. This comparison focuses only on the new handoff architecture. Both projects are open source and can use a hosted model; framework choice is separate from model access. The optional LlamaIndex example implements the charges branch, not an additional required application. Source: https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent/
-->

---

# A compact LlamaIndex handoff

The permitted target and starting agent express the same arrangement.

```python
triage = FunctionAgent(
    name="Triage", llm=llm,
    system_prompt="Hand charge questions to Charges.",
    can_handoff_to=["Charges"], streaming=False,
)
workflow = AgentWorkflow(agents=[triage, charges],
                         root_agent="Triage", timeout=60)
```

Comparison: [complete LlamaIndex handoff](../snippets/b3/extensions/02_llamaindex_handoff.py)

<!--
The full file supplies a description, the Charges agent, a real charge-reading tool, the explicit OpenAI adapter and an awaited workflow.run with an iteration limit. The shortened excerpt isolates orchestration. Running the SDK path is sufficient for the main explanation; use this comparison to map familiar responsibilities, rather than conduct another framework setup walkthrough. Inspect CHARGES TOOL and the real final result if run.
-->

---

# Dependencies determine what can overlap

A tracking lookup that needs an identifier from a previous observation must wait for that result.

Once the required inputs are available, independent operations and charge assessments can overlap.

Parallel execution can reduce waiting. It does not reduce the number of requests or guarantee a cheaper or more accurate result.

<!--
Explain dependency before concurrency syntax. A model can request several independent tools, and a runtime may execute them concurrently when supported. The next optional example uses explicit application-controlled concurrency. Distinguish parallel function calls, parallel model calls and multiple agents: these are related choices, not synonyms. Avoid claiming a speedup without comparable measurements.
-->

---

# Aggregate every outcome

```python
results = await asyncio.gather(
    run_specialist("operations", operations, operational_facts),
    run_specialist("charges", charges, charge_facts),
    return_exceptions=True,
)
```

Associate each result with its source. A failed branch makes the aggregate partial.

Illustration: [independent specialist calls](../snippets/b3/extensions/01_parallel_specialists.py)

<!--
The complete example supplies labelled synthetic facts to two real model calls. It does not pretend to perform live shipment reads. The excerpt gives those input strings descriptive variable names. START prints precede awaiting each run; COMPLETED order is not guaranteed. gather preserves input order, and the full file uses names to associate outcomes. return_exceptions=True preserves individual failures for aggregation; it does not recover them. This is a compact comparison, not another required run in the lecture.
-->

---

# Choose control from the task

| Need | Useful arrangement |
| --- | --- |
| Known order or conditions | Prescribed sequence or routing |
| Next information need varies | One agent with several tools |
| Separate bounded expertise | Coordinator calling specialists |
| Specialist should own the response | Handoff |
| Independent work can overlap | Parallel execution and aggregation |

Keep the simplest arrangement that meets the requirement.

<!--
Use this table to consolidate mechanisms already taught. Ask participants to explain why the shipment case could remain a single-agent design, and what requirement would justify specialists. The architecture choices can be combined, but every combination adds state, observations and failure outcomes to understand. Do not turn the comparison into a claim that more autonomy is always desirable.
-->

---

# Retaining context and progress

The investigator produces evidence and a draft. A user may return later or ask a follow-up.

| What must survive? | Example |
| --- | --- |
| Conversation context | What “that shipment” refers to |
| Application task state | Findings, draft and review status |
| An interrupted run | A pending tool call awaiting approval |

These related stores serve different purposes.

<!--
Begin the third section with the concrete need to continue. B1 taught explicit history; here the application also has task artifacts and a paused execution. A saved transcript alone does not establish a review decision or replay safety. A task-state JSON file alone does not serialize the SDK's pending tool call. Sources: https://developers.openai.com/api/docs/guides/agents/results ; https://developers.llamaindex.ai/python/framework/understanding/agent/state/
-->

---

# A follow-up uses earlier conversation

First request:

> Investigate C1 and draft one sentence.

Follow-up:

> Which shipment were we discussing?

A session can retain the earlier messages for the next request. This supplies context without changing the model's learned weights.

<!--
Reactivate B1's message-history explanation. The identifier-only follow-up isolates conversational reference from another factual lookup. A session is a storage/conversation mechanism, not a guarantee that the model will use history correctly. Context limits still apply; long conversations require retention choices, and unrelated users need separate scopes.
-->

---

# A session carries conversation history

```python
session = SQLiteSession("shipment-C1")
first = Runner.run_sync(agent, "Investigate C1 and draft one sentence.",
                        session=session, max_turns=4)
second = Runner.run_sync(agent, follow_up,
                         session=session, max_turns=4)
```

The same session supplies earlier messages to the second call.

Illustration: [conversation and task state](../snippets/b3/05_memory_and_state.py)

<!--
The full file uses the session's default in-memory storage. It supplies the exact follow-up question and prints the actual answer. Keep conversation retention distinct from disk persistence. Changing the second call to a new session lets participants inspect what context disappears. Source: https://developers.openai.com/api/docs/guides/agents/running-agents
-->

---

# Task state records what the application knows

```text
shipment_id: C1
findings:    observed shipment facts
draft:       actual generated update
review:      pending
```

Tool execution can record findings. Application code stores the draft and maintains its review status.

Generated prose saying “approved” does not change that status.

<!--
This is a schematic of application fields, not a prepared successful model reply. The complete file appends the actual tool result and stores first.final_output. State is a normal Python dictionary outside the prompt; the model receives facts through returned observations and the session, not by automatically seeing every application variable. Review is initialized by application code and remains pending.
-->

---

# Task data stays in the application

```python
state["draft"] = first.final_output
print("FINDINGS:", state["findings"])
print("REVIEW:", state["review"])
```

The session retains conversation messages. The dictionary retains findings, the actual draft and its pending review status.

Illustration: [conversation and task state](../snippets/b3/05_memory_and_state.py)

<!--
The tool records its observed fact in the application's dictionary; the model receives that fact through its tool observation. Application code stores the actual generated draft. These values remain in memory for this example. Ask which data answers a conversational reference and which determines review status. File-backed storage and reload are a separate follow-on example.
-->

---

# A checkpoint needs the right information

Saving a draft lets the application recover that draft.

Resuming a paused tool call also needs its pending arguments and the runtime's execution state.

After a restart, agent definitions, tools and external application state must be available again. Repeating a request can repeat an action.

Follow-ons: [persist task data](../snippets/b3/extensions/03_persist_task_state.py) · [save a pending approval](../snippets/b3/extensions/04_saved_approval.py)

<!--
Connect the limits of a plain data snapshot to the next approval requirement. SDK state is serializable, but arbitrary service state and side effects are not thereby restored. A conversation ID, application task ID and run checkpoint are different identifiers/resources. Reliable retries and duplicate-action protection belong to the later integration/reliability work. Source: https://developers.openai.com/api/docs/guides/agents/results
-->

---

# A proposed action needs a human decision

The assistant has prepared a customer update. The next capability would place that message in a demonstration outbox.

Before execution, the reviewer sees the intended shipment, exact text and operation.

Approval authorizes that proposal. Rejection leaves the action unexecuted; a changed proposal needs another review.

<!--
Use a local in-memory outbox so the real effect is visible without sending messages to anyone. The standalone approval example uses a supplied draft to isolate review from generation; the earlier examples generated their own drafts. The terminal reviewer input is a classroom mechanism, not enterprise identity or a Maersk release policy. Source: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
-->

---

# Pause before executing the tool

```text
Model requests an outbox action
             ↓
Runtime returns a pending approval
             ↓
Application presents the exact proposed payload
             ↓
Human approves or rejects → resume the same run
```

The tool body waits for the decision.

<!--
Teach the lifecycle before code. An interruption is expected incomplete execution, unlike a failed run or completed final answer. The result supplies pending approvals and resumable state. After rejection, the resumed model receives the denied outcome; it must not silently substitute another action. Source: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
-->

---

# Mark the action for approval

```python
@function_tool(needs_approval=True)
def queue_customer_update(container_id: str, text: str) -> str:
    outbox.append({"container_id": container_id, "text": text})
    return "Recorded in the local demo outbox."
```

The application inspects `result.interruptions` before continuing.

Illustration: [real approval interruption](../snippets/b3/06_human_approval.py)

<!--
The complete function also prints when its body executes. Run the full file and inspect OUTBOX BEFORE: 0 plus the PENDING payload. The decorator requests runtime review before execution; an instruction to ask permission is not the enforcement mechanism. Do not approve unseen arguments. The file accepts approve/reject from the actual terminal input and rejects any other response.
-->

---

# Apply the decision and resume

```python
state = result.to_state()
for item in state.get_interruptions():
    if decision == "approve":
        state.approve(item)
    else:
        state.reject(item)
resumed = Runner.run_sync(agent, state, max_turns=4)
```

Illustration: [review and resume the same run](../snippets/b3/06_human_approval.py)

<!--
The core file obtains an actual terminal decision and resumes the pending in-memory run. Inspect one outbox entry after approval and none after rejection. Additional interruptions require a new review. Saving that pending run for a later process is a separate follow-on: extensions/04_saved_approval.py writes and restores SDK state before applying the same decision. Source: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
-->

---

# The investigation and its control points

```text
User task → plan → observed facts → further decisions
                         ↓
             optional specialist work
                         ↓
                draft + task state
                         ↓
              pending action + run state
                         ↓
             human decision → continuation
```

The model selects work. The application retains evidence and controls execution.

<!--
This assembles the conceptual architecture; the linked examples isolate its mechanisms rather than claiming a complete production shipment system. Ask who owns the final answer in each delegation arrangement, what has actually survived a pause, and which exact action was authorized. MCP can supply the capabilities without changing these orchestration responsibilities. Enterprise service/data integration is the next boundary.
-->

---

# B3 · What the application now manages

It can investigate through several observations, coordinate specialist work, retain progress and pause for a human decision.

**Explain:** what changes between a specialist called as a tool and a handoff?

**Next:** connect these familiar capabilities to business APIs, databases and controlled actions.

<!--
Close by asking participants to trace a C1 investigation, a C9 clarification and a rejected outbox action. Check causal understanding: a plan does not establish facts, an extra agent does not guarantee quality, stored conversation is not approval authority, and a resumed run still needs its tools/application state. B4 will replace classroom capabilities with enterprise integrations. Lab design remains separate from this lecture.
-->
