---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 27px; }
  h1 { font-size: 39px; }
  pre { font-size: 21px; }
  table { font-size: 24px; }
---
# B1 · Building an LLM feature

A model call becomes useful application behavior one step at a time.

1. Send a request and inspect the answer
2. Control instructions, facts and conversation history
3. Turn generated text into validated application data
4. Compare model quality, latency and usage

<!--
Begin with the learner's existing Python mental model: functions receive input and return output. A model call has that familiar interface, but the returned content is generated rather than guaranteed by a deterministic calculation. The module starts with that observable behavior. Learners need no PortOps checkout or database. Container names are tiny synthetic examples, so attention stays on the mechanism.
-->

---

# Generation creates a candidate, not a retrieved record

A normal lookup returns the value stored under a key. A model call generates text from its input.

For “What is dwell time?”, language generation is useful.
For “What is C1’s current fee?”, we first need the relevant record.

<!-- Establish the difference through two questions. Ask which needs current private evidence. No model internals are required. -->

---

# A message request returns generated text

```python
reply = completion(
    model=os.environ["COURSE_MODEL"],
    messages=[{"role": "user", "content": "What does container dwell time mean?"}],
)
print("Answer:", reply.choices[0].message.content)
```

A request goes to a model service. The response contains generated text.

Source: `teaching-snippets/b1/s01_model_call.py`

<!--
Use teaching snippet 01 after setup. The later request-input code-along composes the separate instruction and context mechanisms. Point at the request before showing the answer. completion is the actual LiteLLM library call, not a local workshop wrapper. The model name selects a configured model service. choices[0].message.content reads its first generated answer. Ask learners to replace the question and run again. They should see that this one operation already provides a useful language capability.
-->

---

# A model answer is a candidate

The same question can produce different wording.

- Training gives the model general language patterns and knowledge
- The request supplies the current task
- Generation produces a candidate answer

**Predict:** Which parts of two answers should stay consistent?

<!--
Do not turn this into a model-internals lecture. Learners need to distinguish variable wording from an incorrect meaning. Ask them to rerun the first card and compare answers. A change in phrasing is usually acceptable; an invented operational fact is different. Even settings that reduce sampling do not justify treating all outputs as deterministic. This creates the reason to specify inputs and inspect outputs in the following cards.
-->

---

# Predict what changes when only the instruction changes

The model and question remain fixed.

Request A: “Answer in one sentence.”
Request B: “Answer in three short bullets.”

Which property should change? Which meaning should remain?
Would either instruction establish C1’s current fee?

<!-- Collect predictions before teaching snippet 02. Do not reveal the conclusion on this slide. -->

---

# Message roles separate instruction from task

```python
messages = [
    {"role": "system", "content": instruction},
    {"role": "user", "content": question},
]
```

Keep the question fixed. Compare:

- “Explain in one short sentence.”
- “Answer in three short bullets.”

Source: `teaching-snippets/b1/s02_instructions.py`

<!--
The experimental variable is the instruction, not the question or model. Run both requests and ask learners what changed. System instructions express application behavior; user messages supply the task. They influence generation but are not executable Python constraints. The comparison makes the role distinction visible before introducing prompt terminology. Avoid saying the system role makes a model infallible or that every provider treats every role identically.
-->

---

# Instructions guide form; they do not add evidence

We expect different structure while preserving the supplied C1 fee. The actual service may still fail to follow the format.

Neither instruction supplied a container record.

If an exact format is required, inspect the reply and enforce a contract in application code.

<!-- Reveal after both runs. Discuss actual differences without inventing a guaranteed output. -->

---

# A prompt has several inputs

| Part | Example | Change it to affect |
| --- | --- | --- |
| Instruction | Explain for an operations trainee | Style and task behavior |
| Facts | C1 has a USD 1500 fee | Available evidence |
| Question | What is C1’s fee? | The requested answer |

A clear instruction cannot supply a missing fact.

<!--
Use the examples as separable inputs, not one long magic prompt. Ask whether changing the instruction to “be accurate” adds access to a port database. It does not. This is the bridge to context: the application's job includes choosing relevant facts before the call. When an answer goes wrong, inspect which input actually caused the problem instead of always rewriting the instruction.
-->

---

# Predict the answer when the record is missing

Both requests ask: “What is C1’s net fee?”

- A supplies no facts.
- B supplies C1, USD 1500 and a calculation date.

What can each answer justify? What would a confident number in A establish?

<!-- Wait for reasoning. A confident answer alone establishes no source for a private fee. Inspect the two cases in teaching snippet 03 after predictions. -->

---

# Context supplies current facts

```python
question = "What is the net fee for container C1?"
record = "C1: net fee USD 1500, as of 2026-09-22"
for facts in ["", record]:
    # The card sends the same question with each context.
```

Compare the actual answers with and without the supplied record.

Source: `teaching-snippets/b1/s03_context.py`

<!--
The comment summarizes the call shown fully in the card. This is a genuine controlled comparison over two real model requests. The instruction asks the model to say it does not know when evidence is absent. It may still guess; that failure is useful evidence. Change only the fee in the inline record and repeat. The model's weights did not change; the request did. Later modules replace the inline fact with a tool or data query.
-->

---

# A supported answer depends on supplied evidence

Request B supplies a basis for saying USD 1500 as of the stated date.

Request A should acknowledge missing information. If it guesses, confidence does not repair the missing evidence.

Changing the context changes the request; it does not train the model.

<!-- Separate expected behavior from observed generation. Ask learners to change only the fee and explain the causal change. -->

---

# Context has a size and a cost

Every request includes the text the application sends.

- More history and facts mean more input tokens
- A context window limits what fits in one call
- Irrelevant text can distract from the task

**Try:** Add unrelated facts. Does the answer become more useful?

<!--
Define a token as a model-specific text unit, not necessarily a whole word. A context window is a finite token budget, so indefinitely appending records is not an architecture. We are not introducing retrieval here. First establish why the simplest application should send only relevant facts. Later, reported usage from the actual API makes the token volume inspectable. Do not give fabricated token counts or claim that character count equals tokenizer output.
-->

---

# A follow-up needs history

First question:

> Container C1 has a USD 1500 charge. Restate that fact.

Follow-up:

> Which container does it apply to?

The word “it” depends on the earlier exchange.

<!--
Ask learners to answer the follow-up without the first message. They should feel the ambiguity before seeing code. A chat interface can make memory appear automatic, but the application normally decides what to send on the next request. This lesson uses a stateless chat-completions call, so conversation history is explicit data. It is not a claim about every provider's session API.
-->

---

# Predict what a fresh request loses

Send only this message to a stateless API:

> Which container does it apply to?

What information is missing? Would using the same model name restore it?

Write the minimum earlier information needed to resolve the reference.

<!-- Have learners identify C1 and the charge before showing message assembly. The same backend name is not a conversation store. -->

---

# Conversation history is a message list

```python
messages.append({
    "role": "assistant",
    "content": first.choices[0].message.content,
})
messages.append({"role": "user", "content": "Which container does it apply to?"})
second = completion(model=os.environ["COURSE_MODEL"], messages=messages)
```

Python resends the earlier user message and actual model reply.

Source: `teaching-snippets/b1/s04_history.py`

<!--
Print the message list before the second call and identify each role. The assistant message is the actual first response, not a prepared demonstration answer. Remove the first two messages and repeat to see what is lost. The lesson is about request assembly and state, not a memory library. It naturally explains why token usage can grow across a conversation.
-->

---

# The message list supplies continuity

The second call receives the first user message, the actual assistant reply and the follow-up. It can therefore resolve “it.”

Removing the earlier exchange removes that evidence. A plausible answer afterward is not proof of memory.

More retained history also uses more of the request budget.

<!-- Reveal after inspecting teaching snippet 04. Ask which component owns history and which older messages could eventually be omitted. -->

---

# Prose is awkward application data

A person can read:

> C1 missed its planned departure.

A downstream function needs named fields:

```json
{"container_id":"C1","status":"delayed"}
```

Structured output lets Python inspect a specific field.

<!--
Give a concrete application decision: putting a container into the delayed queue. A natural-language paragraph would need fragile text interpretation, whereas named fields make the application's expectations explicit. This motivates JSON before schemas. The displayed JSON is an illustrative desired shape, not a claim about what a model returned in the classroom. The next card tests the actual response.
-->

---

# JSON parsing is the first boundary

```python
raw = reply.choices[0].message.content
try:
    parsed = json.loads(raw)
    print("Parsed Python value:", parsed)
except (json.JSONDecodeError, TypeError) as error:
    print("Cannot use this as JSON:", type(error).__name__)
```

Source: `teaching-snippets/b1/s05_json_boundary.py`

<!--
Read the actual raw text first. Markdown fences, surrounding prose or broken punctuation can cause parsing to fail. This card uses a plain instruction so the failure is visible; provider-specific constrained generation can improve format reliability but does not remove application validation. Do not strip arbitrary fragments until something parses. Ask what json.loads proves, then show the next slide's valid-but-wrong examples.
-->

---

# Predict what a JSON parser accepts

Which of these can `json.loads` read? Which could our application use as a container note?

```json
["C1", "delayed"]
{"container_id":"C1"}
{"container_id":"C1","status":"maybe"}
```

<!-- Let participants answer the two questions separately. The next slide reveals syntax versus shape. -->

---

# Syntax success does not establish the required shape

All three values are valid JSON:

```json
["C1", "delayed"]
{"container_id":"C1"}
{"container_id":"C1","status":"maybe"}
```

None satisfies the intended container-note contract.

<!--
Have learners explain the difference between syntax, field presence and permitted values. A parser can build Python values for all three examples. The downstream application still cannot safely assume it received a dictionary with the two expected fields and one of two valid statuses. This is the reason to introduce a schema. Avoid teaching JSON decoding and business authorization as one undifferentiated validation step.
-->

---

# A schema makes accepted structure explicit

```python
class ContainerNote(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    container_id: str
    status: Literal["delayed", "on_time"]
```

- Required fields have names and types
- `Literal` limits the status values
- Extra fields cause an error

Source: `teaching-snippets/b1/s06_schema.py`

<!--
Introduce Pydantic by showing what each line buys. BaseModel describes a typed structure; it is not the entire application. Literal makes the two accepted labels explicit. Strict mode avoids unexpected type coercion, while extra forbid makes an unrequested approved field visible as an error. The supplied candidates are validation exercises, intentionally independent of a model endpoint so learners can isolate the schema mechanism.
-->

---

# Predict the schema outcome before running

The contract requires `container_id` and a status of `delayed` or `on_time`; extra fields are forbidden.

1. C1, delayed
2. C1, maybe
3. C1, missing status

Which field or rule decides each result?

<!-- Run teaching snippet 06 only after learners predict each case. Permission follows in snippet 07. -->

---

# Validation produces usable evidence

```python
note = ContainerNote.model_validate(candidate)
print("Accepted:", note.model_dump())
```

Observed prepared-candidate outcomes:

| Candidate | Result |
| --- | --- |
| C1, delayed | Accepted |
| C1, maybe | Rejected |
| C1, missing status | Rejected |

Source: `teaching-snippets/b1/s06_schema.py`

<!--
Run teaching snippet 06 and read the field location and reason for both rejections. Ask learners to remove container_id or change it to an integer. They should predict the failure and then see it. This is an application-contract demonstration, not a test of whether a model can generate correct data. After understanding the contract, use the actual raw response from teaching snippet 05 as a new candidate and inspect the same boundary.
-->

---

# Predict whether a valid note may be used

Both notes satisfy the same schema:

```json
{"container_id":"C1","status":"delayed"}
{"container_id":"C2","status":"delayed"}
```

C1 belongs to importer A; C2 belongs to importer B. The caller is A. Does the schema know this?

<!-- Ask where owner data lives. Reveal the application lookup next. -->

---

# Business rules use external facts

```python
owners = {"C1": "importer_a", "C2": "importer_b"}
caller = "importer_a"
permitted = owners.get(note.container_id) == caller
```

Both C1 and C2 can pass the same schema.
Only one belongs to this caller.

Source: `teaching-snippets/b1/s07_permission.py`

<!--
Run both candidates to show a schema success followed by different permission outcomes. Ownership is an external business fact, not a constraint the schema can infer from the identifier's type. The caller string is a classroom input supplied outside the model. Authentication is a later deployment concern; this small example teaches where business permission belongs without needing an identity framework.
-->

---

# Three checks answer different questions

| Check | Question |
| --- | --- |
| JSON parser | Can Python read the text? |
| Schema | Are the required fields and values present? |
| Business rule | Is this data usable for this request? |

A further review asks whether the generated explanation is accurate and useful.

<!--
Ask learners to place failures at the right boundary: broken punctuation, missing status, another importer's container, and misleading prose. The last one may need task-specific evaluation or human judgment. The purpose is to build a layered mental model, not to claim that adding one validator solves quality. Later modules will add tools and evaluation on top of these same distinctions.
-->

---

# Diagnose the boundary before repairing the answer

A reply contains valid JSON with `status="maybe"`.

The parser succeeds; the schema rejects it.

Keep the rejected raw reply for diagnosis. Fix the allowed-status instruction or generation method, then validate the new actual reply. Do not silently relabel it as delayed.

<!-- Worked recovery. Ask why changing the parser would not address this failure and why a guessed replacement loses evidence. -->

---

# Model selection starts with a task

For the same representative request, compare:

- Whether the answer preserves the supplied facts
- Measured latency
- Reported input and output tokens
- The operating and data constraints

Model size is a starting hypothesis to test, not a quality score.

<!--
Avoid prescribing a provider or fixed ranking. A small model may handle a narrow classification well while failing a more demanding tool task. Larger models can also fail without the right context. Explain that local deployment adds hardware and serving constraints, while hosted deployment adds a service/data boundary. Tie all these choices to the particular application rather than a generic leaderboard.
-->

---

# The same request makes a fairer comparison

```python
start = perf_counter()
reply = completion(model=model, messages=messages)
print("Model:", model, "Seconds:", round(perf_counter() - start, 3))
print("Usage:", reply.usage)
print("Answer:", reply.choices[0].message.content)
```

Keep the request fixed. Inspect each answer alongside its measurements.

Source: `teaching-snippets/b1/s08_model_comparison.py`

<!--
The card sends the same request to two configured models. Use repeated runs before interpreting a single latency measurement as typical. Ask learners to assess preservation of C1, eight overdue days and the fee, then clarity. Token volume is observable usage; currency cost additionally needs applicable rates. Neither a lower token count nor a faster response proves that the task was completed well.
-->

---

# A faster answer can fail the task

Prepared comparison, not measured model output:

| Candidate | Time | Stated fee |
| --- | --- | --- |
| A | 0.4 s | USD 150 |
| B | 1.2 s | USD 1500 |

The supplied fee is USD 1500. Which candidate satisfies this requirement? What else must be measured before choosing?

<!-- Discuss accuracy before speed. Explain these illustrative measurements are not benchmark evidence. Repeat actual comparisons over representative cases. -->

---

# Lab · A container-note extractor

Given a short operational message:

1. Request `container_id` and `status`
2. Inspect and parse the actual reply
3. Validate the schema
4. Check the caller’s permitted container
5. Explain a failure at each boundary

The lab uses two inline containers. No capstone project is required.

<!--
Hand learners the lab document. They first build the deterministic parser/schema/business path using supplied candidates, then connect the actual model request if an endpoint is available. This keeps missing model access from obscuring the validation concept. The completed feature is small enough to understand as one script and combines only mechanisms already demonstrated.
-->

---

# Applying the concepts to PortOps later

Replace inline facts with the application’s trusted data.

Keep the same sequence:

**request → generated text → parse → schema → business check**

Next: B2 lets the model request facts through ordinary Python functions.

<!--
Make this the only required capstone transfer moment in the module. Learners should be able to explain every mechanism before opening the full project. Ask which inline values would eventually come from PortOps and which checks must remain in application code. Do not introduce the reference gateway or review store as prerequisites. The next module starts with a plain Python function and builds toward tools.
-->
