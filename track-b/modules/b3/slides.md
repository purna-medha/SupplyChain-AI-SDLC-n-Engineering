---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 27px; padding: 44px 55px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 22px; }
---
# B3 · Control flow belongs to the application

How does a useful tool conversation become a workflow that stops honestly and respects review?

We will vary the next step, bound repetition and preserve decisions.

<!-- Retrieve B2: model proposes, host validates and executes. The new problem is coordinating multiple steps. -->

---

# A chain is appropriate when every case needs every step

```python
result = review(draft(read(container_id)))
```

The dependencies fix `read → draft → review`. Data can change while the execution order stays the same.

<!-- Snippet s01. Ask learners to unpack the nested calls into three named assignments if needed. -->

---

# Predict whether on-time data skips drafting

Snippet s01 receives C1 delayed and C2 on_time.

Will both print `1 read`, `2 draft`, `3 review`? Identify the code that could skip a step if you think one is skipped.

<!-- Pause. Require a branch condition as evidence; do not accept a business intuition as proof of code behavior. -->

---

# Different data does not create a branch

Both rows visit all three functions because the expression is unconditional.

If on-time rows need no draft, the program needs an explicit decision about the next action.

<!-- Run snippet s01. Link the observed unnecessary draft to the need for routing. -->

---

# State is evidence available to the next decision

```python
state = {"container_id": "C1", "status": "delayed"}
```

State records what is known. A route records what to do next. Keeping these separate lets us explain a decision from its inputs.

<!-- Snippet s02. Ask learners why a missing status differs from an explicit on_time value. -->

---

# Routing turns known facts into a next action

```python
if "status" not in state:
    return "lookup"
if state["status"] == "delayed":
    return "review"
if state["status"] == "on_time":
    return "done"
return "manual_check"
```

<!-- Snippet s02 excerpt. The router selects a name and does not execute lookup or review; ask who must consume its result. -->

---

# Predict the route for missing and unfamiliar facts

Compare `{ "container_id": "C3" }` with a record whose status is `cancelled`.

Should both take the same route? Explain what additional information or decision each needs.

<!-- Do not reveal the routes on this slide. Have learners write a reason alongside each choice. -->

---

# Missing evidence and unfamiliar evidence need different responses

Missing status routes to lookup. Unrecognized status routes to manual_check.

Treating every non-delayed case as done would silently convert an unsupported status into successful completion.

<!-- Run snippet s02 and inspect each selected route, including cancelled. The fallback is deliberate uncertainty handling, not evidence that cancellation is safe. -->

---

# A state machine repeats decisions after state changes

Snippet s03 starts with only an ID. One iteration adds status; another adds draft. A later iteration can recognize completion.

The control rule is deterministic. No model generated these transitions.

<!-- Trace successive dictionaries on the board. Establish what one iteration means before introducing the budget. -->

---

# Predict whether two iterations are enough

The budget is two iterations.

Iteration 1 reads; iteration 2 drafts. Does snippet s03 report done or budget_exhausted? Identify when the completion check runs.

<!-- Snippet s03 runs both budgets; trace each completion check. Ask for a trace rather than intuition. -->

---

# A completed artifact is not always a completed workflow

Two iterations create the draft but never reach the completion branch. The loop ends without `break`, so its `else` records budget_exhausted.

With three iterations, the final check records done.

<!-- Run both budgets. Explain Python for-else precisely: it runs when the loop finishes without break, not whenever a condition is false. -->

---

# Diagnose a misleading success report

```python
for step in range(max_steps):
    perform_one_step(state)
print("done")
```

This prints done even when the budget interrupts useful work. Which evidence is missing?

<!-- Deliberately faulty pseudocode. Learners should ask whether a completion condition was observed, not merely whether the loop ended. -->

---

# Record completion and exhaustion as different outcomes

Place success on the observed completion path. Record budget exhaustion on the no-break path.

A partial draft may be retained for inspection, but its existence must not overwrite the stop reason.

<!-- Repair by comparison to snippet s03. Ask learners to explain why honest partial progress helps recovery and diagnosis. -->

---

# An agent loop lets observations influence the next request

A real model sees the growing conversation and can request another read or produce an answer.

The host retains admission checks, execution and stopping. Model choice changes the proposed next operation, not ownership of the loop.

<!-- Introduce snippet s04 after deterministic control flow is understood. Its no-argument read_c1 contract keeps attention on repeated decisions; B2 already taught argument validation. -->

---

# Automatic tool choice permits either a request or an answer

```python
response = completion(
    model=os.environ["COURSE_MODEL"], messages=messages,
    tools=tools, tool_choice="auto",
    timeout=30, num_retries=0)
```

B2 forced one tool phase. Here each actual model response can choose its form.

<!-- The card uses actual LiteLLM inference. If offline, show the explicit skip; do not relabel prepared fixtures as a model trace. -->

---

# Observations must enter the next iteration’s input

Preserve the assistant request and append one matching tool message per returned call.

Only then call the model again. Rejected requests become error observations so the model can propose a correction.

<!-- Retrieve B2 IDs. Ask why printing an observation to the console does not provide it to the model. -->

---

# Predict what a one-call budget can deliver

The first model response requests a lookup. The host returns its observation. The budget allows one model call.

Does the loop get a model answer based on that observation? What should it report?

<!-- Conditional scenario, not a promise about model behavior. Learners must distinguish a tool result from a later model answer. -->

---

# An observation is progress, not a final answer

In that scenario, no call remains to interpret the result. Snippet s04 reports budget_exhausted.

If a response has no tool calls, the loop terminates; that protocol condition alone does not prove answer accuracy.

<!-- Run live only if configured. Explain that a model could answer immediately, so the prediction stated a particular first response. -->

---

# Budget units determine what is actually bounded

`max_steps=4` bounds model calls. One response can contain multiple tool requests.

A per-call timeout bounds a different resource. Neither setting alone is a total workflow deadline or a tool-count limit.

<!-- Have learners calculate two requests in each of four responses: up to eight tool executions in that scenario. Avoid asserting a universal batch maximum. -->

---

# Retry requires a reason the same input may succeed later

A temporary communication failure can recover. An invalid container ID remains invalid when repeated unchanged.

Retry policy classifies the failure before spending another attempt.

<!-- Snippet s05 uses supplied outcomes, not real network reliability evidence. Ask learners which party could repair an invalid ID. -->

---

# Predict the attempts used by three failure sequences

A: timeout, then a result.
B: unknown-ID ValueError.
C: timeout, timeout, timeout.

The attempt budget is three. Predict attempt count and final outcome for each.

<!-- Pause and record predictions. The successful attempt counts toward the total; three attempts does not mean three retries. -->

---

# Bounded retries distinguish recovery from repeated failure

A takes two attempts and succeeds. B stops after one because input needs repair. C uses three and reports retry_budget_exhausted.

An outer model loop still needs its own bound: it could request new operations indefinitely.

<!-- Run snippet s05. For advanced learners, discuss why repeating a write after an ambiguous timeout can duplicate an effect. -->

---

# A review gate separates drafting from release

A draft begins pending. A supplied human decision can make it approved or rejected.

Visibility is derived from `status == "approved"`; persuasive text cannot change that status by itself.

<!-- Snippet s06. The reviewer string is a classroom fixture, not authenticated identity. Keep note release separate from an operational write. -->

---

# A guarded transition checks the prior state

```python
if record["status"] != "pending":
    raise ValueError("already decided")
if decision not in {"approved", "rejected"}:
    raise ValueError("invalid decision")
```

Snippet s06 also checks a nonempty note and a trusted reviewer fixture.

<!-- Explain why a valid target state alone is insufficient: transitions depend on the current state too. -->

---

# Predict the second decision on an approved draft

A pending draft is approved by the classroom reviewer. The same record is then rejected.

Should the second decision overwrite the first, silently succeed, or fail under this card’s policy?

<!-- Require learners to cite the guard. Production reversal policies could differ, but this teaching example has one decision per record. -->

---

# The guard preserves the one-decision policy

The second decision fails because the record is no longer pending.

A rejection from a fresh pending draft is allowed and remains hidden. An unchanged nonempty reviewer label does not bypass the state guard.

<!-- Run snippet s06. For a rejection experiment use a fresh pending draft; do not weaken the guard to make the example pass. -->

---

# Saving preserves the decision already made

```python
path.write_text(json.dumps(draft), encoding="utf-8")
restored = json.loads(path.read_text(encoding="utf-8"))
```

Snippet s07 saves and reloads supplied pending and approved states. Serialization does not approve either note.

<!-- Run snippet s07 and inspect reloads. TemporaryDirectory performs real file I/O but removes the file at exit; distinguish the boundary demonstration from production durability. -->

---

# Diagnose a visibility rule that trusts text

A reloaded record is pending, but its text contains “approved”. A filter searches the text and releases it.

Repair the filter to inspect the dedicated decision field. Check pending, rejected and approved cases after reload.

<!-- Learners identify the wrong source of authority, then propose status == approved. Ask how a restart exposes a rule that only lived in UI state. -->

---

# Practice combines decisions without hiding them in a framework

Worked: trace routing and one guarded approval. Guided: complete route, decision and reload checks. Independent: add a new review outcome with explicit policy and evidence.

Keep input facts, workflow route and review status distinguishable.

<!-- Use lab.md. An operational delayed status and review pending status serve different purposes; nesting or distinct names avoids accidental overwriting. -->

---

# Independent workers need an aggregation policy

Snippet s08 runs three ordinary read functions concurrently: C1 and C2 succeed; C9 fails. The orchestrator retains successes and marks the aggregate **partial**.

Predict: must one failure discard every result? Add C3 and replace C9; explain why the aggregate becomes complete.

Function workers are not model agents. A model-based worker must actually invoke a model; concurrency alone adds no agency.

<!-- Run ../../teaching-snippets/b3/s08_fanout_aggregation.py. The barrier exposes real overlapping workers; completion order is unspecified. Compare partial-results policy with fail-all policy. Then ask which earlier case needs a chain, router or adaptive model loop. This is activity 3 in codealong-plan.md; existing five files are additional snippets for activities 1 and 2. -->
