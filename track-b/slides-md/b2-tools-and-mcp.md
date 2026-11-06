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

# B2 · Tools, agents and MCP

An operations assistant that obtains a recorded fact

Application functions · Agent runtimes · Shared capabilities

<!--
Lecture: 60 minutes, then a separate 60-minute lab. Suggested pacing: slides 2–10, 15 minutes; 11–15, 15 minutes; 16–17, 10 minutes; 18–27, 15 minutes; 28–31, 5 minutes. Explain each new requirement and mechanism before its code illustration. Begin with 01, the ordinary function; use 02 and 03 to illustrate the same agent loop. Explain MCP ownership and discovery before 04/05. The no-tool B1 bridge is in reference/agent_without_tools.py; the optional second MCP client is in extensions/01_llamaindex_mcp_agent.py. All records are synthetic fixtures, not live Maersk data.
-->

---

# The chatbot's missing capability

B1's chatbot can explain general shipping terminology.

It cannot establish C1's current recorded status because it has no connection to that record.

The new requirement is to obtain a fact from an application-owned source, then explain the result to the user.

<!--
Begin at the exact boundary of B1. The limitation concerns data access, not whether a model can write a plausible sentence about a container. A larger model alone does not create that connection. We will add one narrow read capability while retaining the same application/model relationship.
-->

---

# The source of the recorded status

> What is C1's recorded status?

For the classroom example, the application owns:

```text
C1 → delayed
C2 → on_time
```

These synthetic records live in a Python dictionary. Their contents must come from executing a read, not from model knowledge.

<!--
Label the fixture explicitly. A dictionary keeps the source and execution visible without database or enterprise authentication setup. Later, the function could read a service or database without changing why the application needs a capability. Avoid calling these classroom values live Maersk statuses.
-->

---

# An application function obtains the fact

The operation has a clear contract:

```text
Input:  a container identifier
Work:   read the matching classroom record
Output: its status, or an unknown-container result
```

Ordinary Python can perform this read. A model adds value by interpreting the user's request and deciding whether this operation is useful.

<!--
Participants already know functions. Establish the operation in words before showing syntax. Not every lookup needs an agent; direct application logic remains appropriate for fixed workflows. Here the learning objective is how a model-selected information need can reach a defined capability.
-->

---

# The read already works in Python

The application can execute the operation directly, before any model is involved.

```python
def get_container_status(container_id: str) -> str:
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")

print(get_container_status("C1"))
```

Illustration: [ordinary function and invocation](../snippets/b2/01_status_function.py)

<!--
Run this tiny example after explaining its input, work and output. It reads the classroom fixture and prints delayed. There is no model, agent runtime or tool decorator yet. The function's docstring is omitted from the slide to isolate the operation. Ask what is still missing if we want a language model to request this function from a user's question. The next slide supplies that missing description.
-->

---

# A model-facing description of the function

To make the function selectable, the application describes its contract:

| Contract field | Our status operation |
| --- | --- |
| Name | `get_container_status` |
| Purpose | Read a recorded container status |
| Argument schema | `container_id`, a required string |
| Result | A status or an unknown-container result |

**Predict:** after advertising this contract, how many status reads have occurred? What must happen before a record is obtained?

<!--
This is the added layer above the ordinary callable, not a second implementation of the lookup. A decorator can derive the description and schema from a docstring and type hints; show that syntax only after the tool interaction and agent loop are understood. The function body and source dictionary are not part of the advertised schema. A valid string also does not prove record existence or permission.

Reasoning check: Advertising the contract executes zero status reads. The model can request the named operation; only runtime invocation executes its body and obtains the record. Ask learners to identify the execution print they would expect after invocation.
-->

---

# A requested operation and an observed result

**Tool request:** read the status of C1.

```text
name: get_container_status
arguments: {"container_id": "C1"}
```

**Observation after execution:** `delayed`.

The request describes work to do. Only the executed function supplies its result.

<!--
This is a schematic representation, not a literal provider response object. Explain the difference between naming an operation and carrying it out. The runtime parses arguments, invokes an admitted function and returns the result associated with the request. Frameworks handle message/correlation details. The full interaction is shown next so these objects have a place in the application.
-->

---

# The tool interaction

```text
User asks about C1
        ↓
Model requests get_container_status("C1")
        ↓
Application runtime executes the function
        ↓
Tool returns the recorded status
        ↓
Model receives the result and answers the user
```

<!--
Teach the whole flow now, before code or protocol fields. Ask learners to point at who generates language and who reads data. This diagram is a schematic, not captured model output. Tool calling is a multi-step model/application exchange. Source: https://developers.openai.com/api/docs/guides/function-calling
-->

---

# The agent's decision and feedback loop

```text
Question + available tools
           |
           v
      Model decides <-------------------+
       |         |                      |
    answer   tool request                |
       |         v                      |
    finish   Runtime executes            |
                 |                      |
                 +---- observation -----+
```

After an observation, the model decides again. The runtime bounds the loop.

<!--
Trace both branches and then the return arrow. For a general terminology question the answer branch may be sufficient. For a recorded status, a tool request obtains the missing observation before the next model decision. The result is not merely shown to the user: it returns to the model. A single successful lookup is the simplest traversal of this loop; it does not establish complex planning. More involved state and workflows remain later material.
-->

---

# The question determines whether a tool is needed

| User question | Evidence needed | Suitable path |
| --- | --- | --- |
| What is container dwell time? | General shipping knowledge | The model may answer directly |
| What is C1's recorded status? | The application's current record | Request the status tool, then answer |

The same agent can take either path. Providing a tool makes an operation available; it does not require every question to use it.

<!--
Ask learners to predict the two paths before opening an SDK example. These are desired behaviors to inspect, not guarantees of model selection. Later, run the tool example with the general terminology question as well as the status question and observe whether execution occurred. This makes model-directed tool use visible without adding a second function or a larger workflow.
-->

---

# Agent definition and runtime

An agent definition specifies instructions, a model and the tools it may request.

The runtime sends requests, executes selected tools, returns observations and continues until the run finishes or reaches a limit.

The OpenAI Agents SDK expresses these responsibilities through `Agent`, tool definitions and `Runner`.

<!--
Only now name SDK objects. A no-tool Agent behaves like the B1 chatbot; reference/agent_without_tools.py is an optional reference, not a core teaching stop. The runner manages mechanics but does not establish that the selected tool or final answer is correct. Distinguish the ordinary OpenAI Python client from the higher-level OpenAI Agents SDK used here. Source: https://developers.openai.com/api/docs/guides/agents/quickstart
-->

---

# A Python function exposed as a tool

The decorator derives the model-facing contract from a typed function and its description.

```python
@function_tool
def get_container_status(container_id: str) -> str:
    """Read a status from the synthetic classroom records."""
    print("TOOL get_container_status:", container_id)
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")
```

Illustration: [complete tool-using agent](../snippets/b2/02_openai_agent_with_tool.py)

<!--
The docstring is shortened for this illustration; the function behavior matches the full file. Connect the name, description and typed argument to the earlier contract. The TOOL print happens when the function executes, not when it is defined. The model is not receiving the dictionary as part of the decorator-generated schema.
-->

---

# The runtime manages the round trip

```python
agent = Agent(
    name="Port operations assistant",
    instructions="Use the tool for recorded statuses.",
    model="gpt-4.1-mini",
    tools=[get_container_status],
)
result = Runner.run_sync(agent, "What is C1's recorded status?",
                         max_turns=4)
print(result.final_output)
```

Illustration: [complete SDK example](../snippets/b2/02_openai_agent_with_tool.py)

<!--
The illustration shortens the full file's instructions. Run the full script with dotenv and OPEN_AI_KEY configuration. Follow the actual TOOL print before reading the final output. Explain tools as the available capability list, model as the decision/generation dependency, and max_turns as a runtime bound. Do not walk through every SDK field as a separate concept.
-->

---

# Evidence in a tool-assisted answer

Inspect the execution print and returned answer together.

For C1, did the function execute with the intended identifier? Does the answer preserve the returned status?

**Predict:** C9 is a valid string. Does passing the argument schema establish that the container exists? What observation should the function return?

<!--
Run one variation after learners predict the expected evidence. Do not show a prepared final sentence as actual model output. The model may paraphrase on_time or delayed; judge meaning against the result. Knowing a container's name does not itself grant access to a production record. Production permissions are a later data-boundary concern.

Reasoning check: A required string can satisfy the argument schema while naming no record. The actual fixture returns Unknown container for C9; it supplies no evidence of a delayed or on-time status. Run C9 after the prediction and inspect the tool print and final answer.
-->

---

# Limits and unsuccessful runs

An agent may choose the wrong tool, supply an unsuitable argument or repeat an unhelpful request.

Use bounded runs and inspect errors and observations. A limit being reached does not mean the task succeeded.

The executing application remains responsible for argument checks, permitted access and actual side effects.

<!--
Keep the first limit discussion tied to the loop learners have seen. max_turns and max_iterations are framework-specific bounds, not a universal count of Python function calls. Our fixture only reads a dictionary and returns unknown membership explicitly. Do not imply the demonstration implements enterprise identity or production authorisation. Later workflow material develops state, retries and review.
-->

---

# The same runtime responsibilities

| Responsibility | OpenAI Agents SDK | LlamaIndex |
| --- | --- | --- |
| Describe a callable | `@function_tool` | `FunctionTool` |
| Configure the agent | `Agent` | `FunctionAgent` |
| Run decisions and tool feedback | `Runner.run_sync(...)` | `await agent.run(...)` |

Keep the model, function and question fixed. The next example changes how the application packages the same loop.

<!--
This is a concept-to-object map, not a new agent architecture. Learners have already seen the SDK objects; introduce the LlamaIndex names as equivalents for familiar jobs before showing their code. Both projects are open source. That is separate from the selected proprietary GPT-4.1-mini model. Model choice and framework choice are independent decisions. Sources: https://developers.llamaindex.ai/python/framework/understanding/agent/ ; https://github.com/openai/openai-agents-python ; https://github.com/run-llama/llama_index
-->

---

# The same capability in LlamaIndex

```python
agent = FunctionAgent(
    llm=OpenAI(model="gpt-4.1-mini",
               api_key=os.environ["OPEN_AI_KEY"]),
    tools=[FunctionTool.from_defaults(fn=get_container_status)],
    system_prompt="Use the tool for recorded statuses.",
    streaming=False,
)
result = await agent.run(user_msg="What is C1's recorded status?",
                         max_iterations=4)
```

Illustration: [complete LlamaIndex example](../snippets/b2/03_llamaindex_agent.py)

<!--
The full file includes the same function, asyncio entry point, complete instruction and output printing. system_prompt is shortened here. Point out which object supplies the model, which wraps the function and which runs the loop. Ask learners to trace the tool evidence, not just compare line counts.
-->

---

# A second application needs the capability

An operations assistant and a support assistant both need recorded container statuses.

Copying the function and records gives each application a separate implementation to maintain.

We want the capability's owner to publish one implementation that several applications can use.

<!--
Introduce the reuse need before the protocol name. Shared Python packages and ordinary APIs can also share code or services; MCP is not the only way to separate a capability. Its specific contribution is a standard interaction for discovering and invoking exposed capabilities across compatible applications.
-->

---

# One shared implementation

```text
Operations assistant ──┐
                      ├── status capability ── records
Support assistant ────┘
```

The capability's owner maintains its implementation and source data.

Each application retains its own user interaction, model and agent loop.

<!--
Establish ownership before adding transport objects. Ask what a new application needs to know: available operations, their contracts and how to request execution. The two applications do not need to share model memory or become a multi-agent system to reuse a service.
-->

---

# MCP standardises the capability exchange

Model Context Protocol provides an interface through which an application can discover capabilities and invoke offered tools.

For our tool path, the client learns a name, description and input schema, then sends arguments and receives a result.

MCP does not supply the agent's reasoning loop or automatically grant access to records.

<!--
MCP also defines resources and prompts; acknowledge them briefly without adding required implementations. Teach the tool path through the need already established. A custom REST API could perform a status read too; MCP's purpose is the common discovery and interaction contract. Source: https://modelcontextprotocol.io/docs/learn/architecture
-->

---

# Host, client and server

```text
Agent application (host)
    ├── model and agent runtime
    └── MCP client → MCP server → status function → records
```

The **host** uses the model and coordinates the work.

The **client** connects to the server. The **server** exposes and executes the capability.

<!--
Point at each component. The model produces a tool request; it is not itself the network client. In our classroom HTTP examples, the client-side application contacts the local server. This differs from provider-hosted remote MCP paths, where network reachability and execution arrangements differ. Source: https://openai.github.io/openai-agents-python/mcp/
-->

---

# Discovery and invocation

| Exchange | What it establishes |
| --- | --- |
| Discover tools | The server offers a status-reading operation |
| Read its contract | The operation accepts a container identifier |
| Invoke it with C1 | The server executes the requested read |
| Receive the result | The application obtains the observation |

Discovering a tool does not execute it or obtain the record.

<!--
Use the ordinary-language exchange before client method names. The runtimes translate discovered tool definitions into model-facing tools. The returned value becomes an observation in the agent's loop. A direct MCP client can also discover/call without using a language model.
-->

---

# What moved to the server

| Responsibility | Before MCP | Shared-server version |
| --- | --- | --- |
| Model and agent loop | Agent application | Agent application |
| Status function | Agent application | MCP server |
| Classroom records | Agent application | MCP server |
| Tool connection | In-process callable | Discovered MCP interface |

The tool's purpose is unchanged. Ownership and the invocation path have changed.

<!--
Use the ownership diagram and discovery explanation from the preceding slides to interpret this table before opening implementation code. Ask learners which file should own the status function and records, and which should own model instructions. The coming examples should confirm those predictions. A server could later read a database while preserving the same tool contract; clients still need to handle unavailable services and errors.
-->

---

# Local processes and shared HTTP servers

| Transport arrangement | Typical classroom shape |
| --- | --- |
| stdio | A client launches and communicates with a child process |
| Streamable HTTP | Clients connect to an independently running server |

We use one local HTTP server so two agent applications can reuse the same running capability.

Endpoint: `http://127.0.0.1:8765/mcp`

<!--
Choose the transport for the demonstration's intended architecture. A stdio server is not inherently a remote network service, and two independently spawned copies would not demonstrate one shared running server. The classroom HTTP server is bound to the loopback interface. Production hosting and identity are separate work.
-->

---

# The familiar function on the server

The implementation remains ordinary Python. The decorator publishes its tool contract.

```python
@server.tool()
def get_container_status(container_id: str) -> str:
    """Read a status from the synthetic classroom records."""
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "Unknown container")

server.run(transport="streamable-http", host="127.0.0.1", port=8765)
```

Illustration: [complete MCP server](../snippets/b2/04_shared_mcp_server.py)

<!--
The full file imports MCPServer, creates server, logs actual execution and uses a main guard. The docstring is shortened. Run it in a separate terminal after explaining the contract and transport. It remains running while clients connect; it contains no OpenAI model call and needs no OpenAI key.
-->

---

# An agent connected to the shared capability

The runtime discovers the server's tools and routes selected calls through the MCP client.

```python
async with MCPServerStreamableHttp(
    name="Port operations tools",
    params={"url": "http://127.0.0.1:8765/mcp"},
) as server:
    agent = Agent(
        name="Port operations assistant",
        model="gpt-4.1-mini",
        instructions="Use the tool for recorded statuses.",
        mcp_servers=[server],
    )
    result = await Runner.run(agent, "What is C1's recorded status?",
                              max_turns=4)
```

Illustration: [complete MCP agent](../snippets/b2/05_openai_mcp_agent.py)

<!--
The full standalone file supplies imports, key configuration, the complete instruction, an explicit discovery print and final output. Explain the connection as one illustration of the ownership change already taught. This application contains no status implementation or records. Compare mcp_servers=[server] with the earlier tools=[get_container_status], then inspect actual execution in the server terminal. The client connection closes when its context ends; the independently running server remains available.
-->

---

# Another application can reuse the server

The OpenAI agent and a LlamaIndex agent can connect to the same MCP endpoint.

Each retains its own model interaction and agent loop. Both obtain statuses through the server's existing function and records.

**Lab extension:** connect the second client and inspect both applications' requests in the server terminal.

Extension: [LlamaIndex MCP client](../snippets/b2/extensions/01_llamaindex_mcp_agent.py)

<!--
Consolidate the sharing concept without introducing another block of adapter code into the lecture. The supplied second client is an extension, not a prerequisite for understanding the first client/server exchange. It asks about C2 while the OpenAI client asks about C1. Both use the same running server. If time permits, briefly run it to show discovery and server-side execution. The earlier LlamaIndex example has already established that a framework can package the same agent loop.
-->

---

# Results and access remain application concerns

An unknown container is a result to handle, not a reason to invent a status.

The server owns checks on its records and operations. A discoverable tool does not imply that every caller may use every record.

The classroom server demonstrates read-only synthetic data. Production identity and authorisation require additional implementation.

<!--
Keep this limitation proportionate and connected to the observed C9 case. Our dictionary membership check is not a production permission system. The host's selected tool list and the server's data access rules have different responsibilities. A valid argument schema alone establishes neither record existence nor permission.
-->

---

# The complete tool-assisted application

```text
User question → agent runtime <-> model
                    ↓ selected tool request
                MCP client
                    ↓
                MCP server → status function → records
                    ↓ observation
                agent runtime <-> model → user-facing answer
```

The agent decides what to request. The executing capability supplies the observation.

<!--
Ask learners to narrate the full path and identify who calls whom. The diagram is schematic. Execution can return an error or unknown result instead of a usable fact. An agent framework can manage the mechanics while the developer still owns the capabilities, boundaries and acceptance of the final output.
-->

---

# Lab · A tool-using assistant and a shared server

Working draft: [standalone B2 lab](../labs/container_help_desk/B2.md).

| Step | Learner implementation |
| --- | --- |
| Direct reads | Return recorded status and supplied net fee |
| Tool agent | Register the two read functions |
| Shared tools | Connect to the supplied MCP server |
| Observation | Inspect reads, discovery and unknown IDs |

A second framework is optional. Scope and timing remain provisional.

<!--
The lab has four unfinished functions and supplied synthetic adapters. Its MCP port 8871 differs from the lecture server's 8765. No PortOps lab variant is distributed. Use the actual lab README for setup.
-->

---

# B2 · What the application now does

It can obtain a recorded fact through a tool and use the result in an answer.

An agent runtime manages model decisions and observation feedback. MCP lets different applications discover and invoke the shared capability.

**Explain:** how does the application now answer C1's status question, and which component owns that fact?

<!--
Close on the requirement B1 could not meet. Learners should distinguish model choice, agent runtime, tool implementation and protocol connection. Later material can add more involved workflows or document retrieval. Searching an internal document collection requires a retrieval capability; using MCP alone has not provided it.
-->
