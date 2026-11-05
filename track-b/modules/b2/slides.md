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
# B2 · A model proposes; the host executes

How can a language model use a recorded fact without owning the data?

Follow one container read through capability, contract, request, admission and observation.

<!-- Begin with the module question. Ask learners to name the process that owns the records; return to their answer at the end. -->

---

# A useful answer needs evidence outside the model

The question is “What is C1’s recorded status?”

Our Python process owns `C1: delayed` and `C2: on_time`. The model receives neither row until we expose it through a tool result.

<!-- Avoid claiming these toy rows are live operational data. They represent the evidence boundary at classroom scale. -->

---

# Defining a function makes a capability available

```python
rows = {"C1": "delayed", "C2": "on_time"}
def get_status(container_id):
    return {"container_id": container_id,
            "status": rows[container_id]}
```

The body specifies a read. Calling the function determines when that read happens.

<!-- Snippet s01 has the complete runnable version with type and membership checks. Point at the read expression. -->

---

# Predict which action performs a read

We define `get_status`, print its name, then call `get_status("C2")`.

Which action reads `rows`? What changes if the final call uses C9?

Explain your prediction before running snippet s01.

<!-- Pause before advancing. Ask learners to distinguish definition, reference and invocation; do not supply the result here. -->

---

# Invocation crosses the capability boundary

Only the call executes the body. C2 returns `on_time`.

Change the s01 invocation to C9: its guard rejects the unknown record. A type hint alone would not reject a non-string value.

<!-- Run snippet s01. The earlier slide uses a shortened function; explain that full card checks avoid an accidental KeyError interface. -->

---

# The model needs a contract it can read

A Python callable is not automatically a model tool.

We describe the operation as data: a stable name, a purpose and accepted arguments. The host keeps the implementation.

<!-- Snippet s02. Ask why sending a function name without its meaning is ambiguous. Keep capability and description distinct. -->

---

# A schema describes the argument boundary

```json
{"type": "object",
 "properties": {"container_id": {
   "type": "string", "enum": ["C1", "C2"]}},
 "required": ["container_id"],
 "additionalProperties": false}
```

One required known ID; no invented extra fields.

<!-- Excerpt from snippet s02, nested under function parameters. Explain required separately from properties: defining a property alone does not require it. -->

---

# Predict what advertising the schema executes

Snippet s02 prints the schema with `json.dumps`; s01 separately invokes the function.

How many reads should occur? If `required` is removed, does Python gain a default container ID?

<!-- Collect both answers. Ask learners to justify the difference between a description and function invocation. -->

---

# Contract text does not execute or supply defaults

Advertising the contract executes zero function calls. The later explicit calls do execute.

Removing `required` loosens the advertised contract; it does not modify the Python signature. A request and implementation can now disagree.

<!-- Compare snippet s02 contract data with the explicit invocation in s01. Explain schema/implementation alignment. -->

---

# The first model call returns a proposed operation

```python
response = completion(
    model=os.environ["COURSE_MODEL"],
    messages=messages, tools=tools,
    tool_choice={"type": "function",
                 "function": {"name": "get_status"}})
```

Snippet s03 asks the provider for a real tool request.

<!-- Messages and schema are shown in the complete card. Named tool choice isolates the request mechanism; it does not execute Python. -->

---

# A request carries identity as well as arguments

Inspect the actual call’s `id`, `function.name` and `function.arguments`.

Arguments are JSON text to decode. The call ID lets the host associate a later observation with this particular request.

<!-- Run live if configured. Otherwise show the explicit SKIPPED result and explain the protocol without inventing a model transcript. -->

---

# Predict whether a plausible request should run

Prepared candidates, not model output:

`get_status({"container_id":"C1"})`
`delete_container({"container_id":"C1"})`
`get_status({"container_id":"C9"})`

Which cross the host boundary, and why?

<!-- These are supplied prediction cases, not promised model outputs. Locate their admission checks in snippet s04; obtain reasons before revealing. -->

---

# Host admission is a sequence of distinct checks

C1 with the allowed name passes. The deletion name fails admission. C9 fails record membership.

Valid JSON establishes syntax only. Even a provider-constrained request still reaches host-owned checks.

<!-- Snippet s03 inspects a real proposal; s04 isolates deterministic admission. Use the lab starter and completed admission checks for deterministic malformed/unknown/extra-input cases: one read and four rejections. -->

---

# Validation must precede execution

```python
if name != "get_status":
    raise ValueError("unknown tool")
arguments = json.loads(raw_arguments)
if not isinstance(arguments, dict):
    raise ValueError("expected an object")
```

After shape and value checks, the host calls the admitted function.

<!-- Excerpt isolates the first checks. Full card also checks exact keys and membership; do not imply this excerpt is the complete dispatcher. -->

---

# Diagnose a dispatcher that reads before checking

```python
arguments = json.loads(raw_arguments)
result = get_status(arguments["container_id"])
if name != "get_status":
    raise ValueError("unknown tool")
```

A rejected operation still printed EXECUTING. Locate the cause.

<!-- Controlled faulty excerpt, not runnable baseline. Ask what evidence proves the boundary was crossed too early. -->

---

# Repair the order and measure the side effect

Move all admission checks before `get_status`. Put a read counter inside the function.

Rerun the unknown-tool candidate: rejection plus zero reads demonstrates the repair for that case.

<!-- Have learners make the ordering change in a scratch copy, then compare with snippet s04. A rejection message alone is insufficient evidence. -->

---

# Exact keys prevent accidental argument acceptance

Add `"approve": true` to a prepared get_status request.

The host rejects it because the accepted interface contains only `container_id`. Ignoring extras would hide mistakes and blur the contract.

<!-- Run this changed case. For deeper discussion, ask when explicit extra-field acceptance might be appropriate and how its contract would change. -->

---

# The observation belongs to the execution owner

```python
observation = {"container_id": args["container_id"],
               "status": rows[args["container_id"]]}
```

The host constructs evidence from the read result. The model request does not establish the status.

<!-- Snippet s05 after validation. Ask which source determines delayed: the prompt, the arguments, or the owned row. -->

---

# The conversation must retain both sides of the call

```python
messages.append(message.model_dump(exclude_none=True))
messages.append({
    "role": "tool", "tool_call_id": call.id,
    "content": json.dumps(observation)})
```

The assistant message contains the request; the tool message carries its result.

<!-- Snippet s05 handles every returned call before the next model request. Explain why a batch needs one result per call. -->

---

# Predict the effect of losing the correlation ID

Two requests ask for C1 and C2. Both observations use the first call’s ID.

Can the protocol reliably associate each observation with its request? What must the host preserve?

<!-- Pause for explanation, not provider-specific error wording. Do not promise all providers reject malformed histories identically. -->

---

# Correlation identifies a request, not a container

Each observation must use its own `call.id`. A container ID identifies a record; a call ID identifies a conversation event.

Repeated reads of C1 can be distinct calls. Reusing a call ID breaks that relationship.

<!-- Reveal the reason. The model may reject or misinterpret a malformed history depending on provider; the host must construct it correctly. -->

---

# A second model call can interpret the observation

Snippet s05 appends correlated results, then calls the model with `tool_choice="none"`.

This produces the answer phase of one round trip. Compare the actual answer with the observed C1 row; fluent wording alone is not verification.

<!-- Run live only if configured. Change C1 to on_time and compare evidence and answer. The full composition remains within 40 lines. -->

---

# MCP moves a capability across a process boundary

A client cannot call a Python object inside another process directly. MCP supplies discovery and invocation messages.

`client → protocol → server function → protocol result`

The model is optional for this boundary.

<!-- Connect back to the same read. MCP does not by itself add a reasoning loop or authorize all discovered tools. -->

---

# The server publishes; the client discovers

```python
@server.tool()
def get_status(container_id: str) -> dict:
    if container_id not in rows:
        raise ValueError("unknown container")
    return {"container_id": container_id,
            "status": rows[container_id]}
```

Snippet s06 publishes the contract derived from this function.

<!-- Server startup is in the complete card. stdout carries stdio protocol traffic; diagnostic logs must use stderr. -->

---

# Initialization precedes discovery and invocation

```python
await session.initialize()
discovered = await session.list_tools()
result = await session.call_tool(
    "get_status", {"container_id": "C1"})
```

Snippet s07 starts the real child server and closes it afterward.

<!-- Run snippet s07; it starts the adjacent server automatically. The adjacent two-file dependency is intentional and unrelated to the capstone. -->

---

# Predict the result of a validly shaped unknown ID

The MCP client changes C1 to C9. The argument is still text.

Will discovery detect the missing record? Where should failure occur? What result field should you inspect?

<!-- Ask learners to locate membership ownership in snippet s06. The generated schema describes a string, not the live row set. -->

---

# The server retains responsibility for record facts

Discovery supplies a schema; C9 fails when the server checks membership during invocation.

Inspect `result.is_error` and its content. A discovered tool is not a guarantee that every call succeeds.

<!-- Snippet s07 already calls C1 and C9; inspect both outcomes. Ask how a host should handle the error before requesting a final answer. -->

---

# Practice transfers the boundary to ETA reads

Worked: trace the admission boundary in snippet s04. Guided: complete the ETA dispatcher in the lab. Independent: add a changed contract and prove rejected requests cause zero reads.

Explain where a real model request or MCP call could connect without changing admission ownership.

<!-- Direct learners to lab.md. Keep answers to the independent extension unsupplied; assess explanation and read-count evidence. -->

---

# Trace ownership before adding another tool

For an ETA question, identify who owns the contract, proposal, admission, record and answer.

Then explain why an accepted request is neither a verified fact nor blanket authority to act.

<!-- Exit transfer. Require a specific boundary and failure example rather than a list of API names. Use assessment question 5 for changed-process reasoning. -->

<!-- Teaching sources: ../../teaching-snippets/b2/README.md. Composition activities: codealong-plan.md. The s05 get_status contract preserves argument shape and caller checks while introducing correlation. -->
