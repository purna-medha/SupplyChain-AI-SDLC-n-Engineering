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

# B0 · Python for supply-chain applications

Read, run and change the Python used in Track B

Container records · Functions and objects · Application boundaries

<!--
Preparatory module before B1. Adapted from the BFSI M0 progression, using
synthetic supply-chain examples and the existing Track B environment. Do not
assume a new teaching-hour allocation. Slides through configuration establish
the language subset; the marked application bridge is a follow-on for learners
who need SQL, API, decorator, async or testing orientation. Experienced Python
developers can use the snippets as a readiness check. Explain concepts before
opening their illustrations. No model call or key is required in B0.
-->

---

# The Python behind an AI feature

A container service desk may read a record, calculate a quote, call a model and return an answer.

Python expresses the application steps and connects them to libraries.

Track B uses this ordinary software around model calls: data structures, functions, objects and explicit decisions.

<!--
Connect to the business need before syntax. Python does not provide current
company knowledge by itself; a connected source must supply it. The first
examples do ordinary deterministic work. B1 introduces actual inference.
-->

---

# The application owns the workflow

```text
Question → application code → permitted source or model
                  ↓
         inspect the returned value
                  ↓
           display or continue
```

The developer defines which component supplies each fact and what happens when that component fails.

<!--
Use the diagram as a motivation for the specific Python constructs that follow.
A model can draft language while ordinary code controls calculations, data
access and continuation. We will learn enough Python to inspect that boundary.
-->

---

# Run a small file first

From `track-b`, run the first complete illustration:

```bash
python3 snippets/b0/01_values_and_arithmetic.py
```

Python executes the file's statements in order. Read the output, change one input and run the file again.

All numbered B0 snippets use the Python standard library.

<!--
Python 3.11 or later is the supported course baseline. The plain python3 path
needs no model dependencies. If the shared environment is already prepared,
uv run python followed by the same path also works. Avoid beginning with an
installation exercise when the first file requires no third-party package.
-->

---

# Scripts and notebooks hold state differently

A fresh script process starts again with the values defined in the file.

A notebook kernel retains variables between cells. Editing an earlier cell does not automatically rerun its dependents.

Use a clean run when comparing results: rerun the script, or restart the notebook kernel and Run All.

<!--
This prepares learners for the exploration notebooks without requiring a new
B0 notebook. Demonstrate how an old notebook value can survive an edited cell.
Do not claim that scripts cannot store state: a file or database can persist it.
-->

---

# Values have names and types

A synthetic pickup quote needs a count, a rate and a budget:

```python
container_count = 3
usd_per_container = 120.0
budget_usd = 500.0
```

These values are an integer and two floating-point numbers. A name lets later code refer to the value.

<!--
This is a flat transport quote for teaching arithmetic, not a PortOps demurrage
tariff. Explain assignment before using expressions. Python determines the
runtime type of each value; an annotation is not required to create it.
-->

---

# Expressions produce a new value

The quote is count multiplied by rate. Remaining budget is budget minus quote.

```python
quote_usd = container_count * usd_per_container
budget_left_usd = budget_usd - quote_usd
print("Transport quote (USD):", quote_usd)
```

Illustration: [values and arithmetic](../snippets/b0/01_values_and_arithmetic.py)

<!--
Predict USD 360 and USD 140 remaining before running. Ask what changing count
to four should do. The complete file prints both values. A print displays a
value; it does not save a business record or send a customer quote.
-->

---

# Strings and formatted output

```python
quote_usd = 360.0
print(f"Transport quote: USD {quote_usd:.2f}")
```

The `f` prefix allows expressions inside braces. `:.2f` displays this number with two decimal places.

Formatting produces readable text; it does not change the stored value.

<!--
The supplied value is the first quote's result. Explain interpolation before
learners encounter the same print in the function illustration. Ask them to
replace the first snippet's plain print with this formatting and rerun it.
No new business calculation has been introduced.
-->

---

# A dictionary names the fields of a record

```python
container = {"container_id": "C1", "status": "delayed"}
print(container["container_id"])
```

The strings on the left are keys. Looking up a key retrieves its value.

The dictionary is supplied classroom data. Creating it does not query an operational system.

<!--
Point out quotes, braces and the colon. The identifier and status are both
strings. A dictionary can contain other kinds of values as well. This is the
same shape learners will see in messages, tool arguments and task state.
-->

---

# Missing fields need an explicit interpretation

```python
departure = container.get("scheduled_departure")
print(departure)
```

`get` returns `None` when this key is absent and no default is supplied. `None` represents the absence of a value here.

An absent departure is not evidence that a container has departed.

Illustration: [records and collections](../snippets/b0/02_lists_and_dictionaries.py)

<!--
Contrast container["missing"] raising KeyError with get returning a default.
Neither choice supplies the missing operational fact. Let learners change the
key, inspect the actual result and choose whether absence should stop work.
-->

---

# A list retains an ordered collection

```python
containers = [container, {"container_id": "C2", "status": "on_time"}]
print(containers[0])
print(len(containers))
```

Index zero selects the first element. `len` reports how many elements are present.

The list's order will also matter when it holds conversation messages.

<!--
Run the complete collections snippet. Ask learners to append C3 and predict
the new length. containers[0] refers to the dictionary already assigned to
container; this is not an independent deep copy. Avoid a full mutability
digression unless a learner changes one and observes the other.
-->

---

# Conditions choose a path

A delayed container needs investigation. An on-time record can finish this small status check.

```python
if container["status"] == "delayed":
    next_step = "investigate"
elif container["status"] == "on_time":
    next_step = "finish"
else:
    next_step = "clarify"
```

<!--
Explain == as a comparison and = as assignment. Indentation defines which
statements belong to each branch. This deliberately small policy sends all
other statuses to clarification; it is not a complete PortOps state machine.
-->

---

# A loop applies the decision to each record

```python
for container in containers:
    # Select the next step from this container's status.
    ...
```

Each iteration assigns the next list element to `container` and runs the indented body.

Illustration: [the complete loop and branches](../snippets/b0/03_conditions_and_loops.py)

<!--
The ellipsis is a shortened excerpt, not the runnable solution; open the
complete file before execution. It supplies three records and the complete
branch body. Have learners predict C1/C2/C9 and then change one status.
-->

---

# A function names one reusable operation

A quote calculation can be called from a terminal, an API or a later tool.

Its parameters describe the inputs. Its return value supplies the result to the caller.

Defining a function does not run its body; a call supplies the arguments and executes it.

<!--
Establish definition versus execution before opening code. The same distinction
will matter when B2 advertises a callable as a model-facing tool. Keep the
calculation separate from presentation and record access.
-->

---

# A readable function states its contract

```python
def quote_transport(container_count: int, usd_per_container: float) -> float:
    """Return a synthetic flat transport quote for positive inputs."""
    if container_count <= 0 or usd_per_container <= 0:
        raise ValueError("Count and rate must be positive.")
    return container_count * usd_per_container
```

Illustration: [function, checks and returned result](../snippets/b0/04_functions_and_hints.py)

<!--
Identify def, parameters, annotations, docstring, explicit input checks and
return in that order. The annotated integer count is an intended interface;
the positivity check does not enforce that the count is an integer.
-->

---

# Positional and named arguments call the same operation

```python
quote_transport(3, 120.0)
quote_transport(container_count=3, usd_per_container=120.0)
```

The first call matches by position. The second matches by parameter name.

B1's model calls use named arguments such as `model`, `messages` and `max_tokens` to make configuration readable.

<!--
Let learners change the complete function snippet to the second call. Explain
that a misspelled keyword is an error; an arbitrary extra name is not accepted
unless a function explicitly supports it. Do not teach **kwargs yet.
-->

---

# Type hints and runtime checks do different work

`container_count: int` tells readers and analysis tools the intended type.

The `if` statement executes and rejects nonpositive values. Python does not enforce ordinary annotations by itself.

For example, `quote_transport(1.5, 120.0)` passes the supplied positivity check even though it conflicts with the intended integer count.

<!--
Use the actual function to show this distinction. Additional runtime validation
would be needed to enforce integer counts. Avoid presenting the type hint as
a complete validator; that misconception later confuses tool schemas and
application permission checks.
-->

---

# An expected error needs a caller decision

```python
try:
    quote_usd = quote_transport(count, 120.0)
    print("Quoted:", count, "containers for USD", quote_usd)
except ValueError as error:
    print("Booking needs correction:", error)
```

Illustration: [valid and invalid booking inputs](../snippets/b0/05_handling_errors.py)

<!--
The complete file supplies count=3 and count=0. An invalid booking does not
receive a zero-price success result. Catch the expected failure where the
caller can do something useful; do not silently catch every exception.
-->

---

# A class gives related data a name

A transport quote has a count and a rate. A `TransportQuote` instance keeps those values together.

```python
@dataclass
class TransportQuote:
    container_count: int
    usd_per_container: float
```

The standard-library `dataclass` decorator generates common object setup code.

<!--
The full snippet imports dataclass and includes the method introduced next.
Explain a class as a definition and an instance as one concrete quote. No
inheritance hierarchy is needed. The decorator notation is opened later in
the application bridge. Dataclass annotations also do not validate values.
-->

---

# Attributes and methods belong to an instance

```python
quote = TransportQuote(container_count=3, usd_per_container=120.0)
print(quote.container_count)
print(quote.total_usd())
```

An attribute holds data. A method is a function accessed through the object; `self` refers to that instance in its method definition.

Illustration: [the complete quote class](../snippets/b0/06_classes_and_methods.py)

<!--
Open the method body and trace self.container_count to this object. Create a
second quote with different inputs. Later response.message.content and
result.final_output use the same attribute-access syntax, although their
classes are supplied by libraries rather than by this course.
-->

---

# Imports reuse another module's definitions

```python
from datetime import date
discharge_date = date(2026, 11, 1)
```

`datetime` is a standard-library module. `date` is one definition imported from it.

An import makes the definition available. The following call constructs a date value.

<!--
Compare import json, from datetime import date and import os in the next
examples. A Python import name and a package installation name are related
but need not be identical; python-dotenv is imported as dotenv in B1.
-->

---

# Date objects support a clear calculation

```python
dwell_days = max(0, (calculation_date - discharge_date).days)
overdue_days = max(0, dwell_days - free_days)
```

Subtracting dates produces a duration. `.days` reads its day count. `max` keeps these example counts at least zero.

Illustration: [fixed-date dwell calculation](../snippets/b0/07_imports_and_dates.py)

<!--
The fixed classroom dates produce seven dwell days and two overdue days. This
does not connect to a live container or calculate a PortOps fee. Its as-of date
is supplied rather than taken from today's clock, keeping the run reproducible.
-->

---

# JSON text and Python objects are different representations

```python
request_text = json.dumps(messages)
restored_messages = json.loads(request_text)
```

`dumps` encodes supported Python data as JSON text. `loads` parses JSON text back into Python values.

Illustration: [a message list and its JSON form](../snippets/b0/08_json_messages.py)

<!--
The full file imports json and defines the same list/dictionary message shape
used by B1. Print the decoded type, then access index zero and content. JSON
text does not become a validated or authorized operational record merely
because it parses. No request is sent by this snippet.
-->

---

# Configuration comes from the process environment

```python
portops_url = os.environ.get("PORTOPS_URL", "http://127.0.0.1:8002")
has_model_key = bool(os.environ.get("OPEN_AI_KEY"))
```

The first lookup has a default. The second checks presence without displaying a credential.

Illustration: [configuration and the active interpreter](../snippets/b0/09_environment_variables.py)

<!--
Python does not automatically load a .env text file. B1's load_dotenv provides
that separate step. Show that an exported environment value changes the URL
while editing no Python. Never ask learners to print their key to prove setup.
-->

---

# Packages belong to a Python environment

Standard-library examples run with Python itself. B1 adds installed packages such as LiteLLM and python-dotenv.

From `track-b`, prepare the existing course environment once:

```bash
uv sync --locked
uv run python snippets/b1/01_openai_call.py
```

`uv run` uses this project's environment. The lockfile records its resolved dependency versions.

<!--
Follow SETUP.md; do not run uv init inside this existing project or uv add
every package named in a slide. The second command is the B1 handoff and
requires a configured key. The environment snippet's sys.executable helps
diagnose installing a package into a different interpreter from the one used.
-->

---
<!-- _class: lead -->

# Application bridge · Python used after B1

Storage · Function wrappers · HTTP routes · Async calls · Logs and tests

Use the following illustrations when those mechanisms are new to the learner.

<!--
This section is a follow-on, not a requirement to learn every library before
making a first model call. The selected Python patterns make B2/B3 SDK code
and the PortOps application easier to read. All numbered files still need
only the standard library; the optional API file declares its dependencies.
-->

---

# SQLite stores rows that a function can read

The supplied illustration creates two container records in a temporary, in-memory database.

```python
connection = sqlite3.connect(":memory:")
connection.execute(
    "CREATE TABLE containers (container_id TEXT PRIMARY KEY, status TEXT)"
)
```

Illustration: [complete create, insert and lookup](../snippets/b0/10_sqlite_read.py)

<!--
sqlite3 ships with Python. This example changes no capstone database and
needs no external database server. The connection exists only for this run.
The next slide explains the value-binding boundary before running the query.
-->

---

# Keep a query's values separate from its SQL

```python
row = connection.execute(
    "SELECT status FROM containers WHERE container_id = ?", (container_id,)
).fetchone()
```

The placeholder receives the lookup value. The trailing comma makes a one-element tuple.

`fetchone` returns a row or `None`. A missing row is not a known status.

<!--
Predict delayed for C1 and unknown for C9 in the complete script. Do not
replace the placeholder with an f-string. This is an introduction to value
binding; B4 develops query meaning, grain, access and generated-SQL validation.
-->

---

# A decorator transforms or registers a callable

```python
@announce
def get_status(container_id: str) -> str:
    ...
```

Here, `@announce` applies `announce` to the defined function. The returned wrapper prints when the function is called.

Illustration: [a small wrapper with an actual read](../snippets/b0/11_decorators.py)

<!--
Explain this as get_status = announce(get_status). The complete file shows
the wrapper and actual body; the excerpt is abbreviated. Decorating a
function does not itself call the business function. B2's @function_tool and
FastAPI's @app.get have their own library-defined behavior; @ is not inherently
an AI or web feature. The small wrapper omits production metadata preservation.
-->

---

# An API route connects a URL to a function

```python
app = FastAPI()

@app.get("/containers/{container_id}")
def get_container(container_id: str) -> dict[str, str]:
    records = {"C1": "delayed", "C2": "on_time"}
    return {"container_id": container_id,
            "status": records.get(container_id, "unknown")}
```

Illustration: [optional local server](../snippets/b0/extensions/server.py)

<!--
The full file imports FastAPI and also supplies /health. The path provides
container_id, the function reads its supplied fixture, and FastAPI encodes the
returned dictionary as a response. This is a separate teaching service, not
the PortOps backend and not a model-backed feature.
-->

---

# Run the optional service in another terminal

From `track-b`:

```bash
uv run --with fastapi --with uvicorn uvicorn server:app \
  --app-dir snippets/b0/extensions --port 8003
```

Open `http://127.0.0.1:8003/docs` and request C1, then C9.

`--with` supplies this example's additional packages without editing the course dependency declaration. Stop the server with Ctrl+C.

<!--
Port 8003 avoids the normal PortOps backend at 8002. The first command can
need package-download access. The unknown result is an ordinary fixture result,
not a real record. Learners should distinguish a running server from a correct
business answer. Use the snippet README if another application occupies 8003.
-->

---

# Async code separates defining work from awaiting it

`async def` defines an async function. Calling it creates a coroutine; `await` obtains its result while allowing supported waiting work to yield control.

```python
async def main():
    status = await get_status("C1")
    print("Awaited observation:", status)
```

Illustration: [complete async script](../snippets/b0/12_async_calls.py)

<!--
The example uses asyncio.sleep(0) to demonstrate yielding, not to simulate a
successful network call or claim a speedup. Merely writing async does not make
blocking work parallel. Read main's result flow before introducing the script
entry point on the following slide.
-->

---

# The execution environment owns the event loop

A standalone script can start its event loop:

```python
if __name__ == "__main__":
    asyncio.run(main())
```

A Jupyter kernel already runs an event loop. In a notebook cell, use `await main()` instead of starting a nested loop.

<!--
Explain __name__ as the script's entry-point guard: importing the file does
not run main. This prepares learners for SDK Runner.run_sync in files and
await Runner.run in the exploration notebooks. Do not use nested event-loop
patches as the default teaching solution.
-->

---

# Logs retain the operation's context

```python
logger.info("Read %s status=%s", container_id, status)
logger.warning("No recorded status for %s", container_id)
```

The complete illustration logs a known read and an expected missing record. The identifier helps explain which case produced the message.

Illustration: [configured logging](../snippets/b0/13_logging.py)

<!--
Open the basicConfig setup before running. Python logging uses stderr by
default; an empty stdout does not mean the example produced no output. Avoid
logging credentials. B5 later traces model/tool steps and operating resources.
-->

---

# A test compares behavior with an independent expectation

```python
self.assertEqual(quote_transport(3, 120.0), 360.0)

with self.assertRaises(ValueError):
    quote_transport(0, 120.0)
```

One test checks the quoted total. The other checks that an invalid booking is rejected.

Illustration: [complete runnable tests](../snippets/b0/14_testing_and_debugging.py)

<!--
Run the file directly; unittest reports two passing tests. Expected 360 is
derived from the supplied case, not by calling the calculation again. This
small example checks only these two behaviors; passing it does not establish
every possible input or a complete production pricing contract.
-->

---

# Debug from a concrete failure

Remove the quote function's input check in the test illustration and rerun it.

The zero-count test should fail. Read its test name, expected exception and actual behavior, then restore the missing decision.

For unexpected errors, read the traceback's final exception and locate the failing source line. Use `breakpoint()` when inspecting values would answer the next question.

<!--
Make the deliberate change only in this tiny teaching file. The distributed
version passes; do not ship a silently broken baseline. No debugger needs to
be running in the initial path. An error message is evidence, not a request
to weaken the expectation until the test passes.
-->

---

# Readable code makes later changes inspectable

Use names that expose the business meaning, such as `container_count` and `quote_transport`.

Keep functions small enough to explain their inputs, result and failure path. Use comments for assumptions that are not evident from the code.

When a learner or coding assistant changes the file, rerun the relevant example and inspect what changed.

<!--
Return to the first quote and ask learners to explain it without narrating
every punctuation mark. Explicit names, interfaces and small examples help
both participants and instructors reason about generated code. Avoid
introducing clever compression merely to reduce the line count.
-->

---

# B0 · Ready to read the first model call

B1 uses imports, named arguments, message lists and dictionaries, object attributes and printed results.

You can now follow those Python operations and distinguish the application code from the model service it calls.

**Practice:** run a core snippet, change one input and explain the output before moving to B1.

<!--
Use the B0 snippet map as the readiness check. Participants should recognize
the structure of B1's first call without having to learn every optional bridge
first. B1 will explain model access, instructions, history, tokens, cost and
latency; do not teach those topics twice here.
-->
