> **Content update:** Track B now includes B6, “RAG, patterns and agentic RAG with LlamaIndex,” by user request. Teach in order B1 → B2 → B3 → B4 → B6 → B5. Historical day/hour allocations below have not been recalculated and are not the allocation for this expanded content. Allocation will be decided separately. Shared model interface: [MODEL_SETUP.md](../MODEL_SETUP.md).

# The Modern AI Developer

## *Maersk Train the Trainer curriculum for Track A and Track B*

Delivered by Ajinkya Kolhe in collaboration with Imarticus Learning

# **Program overview**

This three-day hands-on program prepares Maersk engineering teams to use AI throughout software delivery and to build controlled agentic applications. The curriculum synthesizes the original Modern AI Developer v4 into 10 technical modules across two complementary content tracks.

All participants complete both tracks together in one combined three-day training. Track A focuses on AI as an engineering collaborator. Track B focuses on AI and agents as components of application runtime behaviour. Trainer enablement and assessed teachbacks are additional stages of the Train the Trainer journey.

**Format:** Concept explanation, demonstrations and hands-on labs, with approximately 60 percent lab time.

**Audience:** Software developers and infrastructure engineers, including Maersk trainer nominees.

**Tools:** Claude Code, GitHub Copilot, Git and worktrees, CI and CodeQL or equivalent scanning, MCP, DuckDB or PostgreSQL, and Langfuse, subject to approved access.

# **Content tracks**

| Track A (1 Day) AI Augmented Software Development | Track B (2 Days) Agentic AI Application Building |
| :---- | :---- |
| A1  Foundations and context engineering (AI Assistant) | B1  From LLMs to AI applications |
| A2  Coding testing debugging and refactoring (Spec Driven Development) | B2  Tools function calling and MCP |
| A3  Team development best practices with coding agents (Skills) | B3  Agentic workflow design |
| A4  Harness security and quality (Hooks & Harness) | B4  Enterprise data knowledge and actions |
| A5  Brief to a validated PR  | B5  Safety observability and evaluation |
| — | B6  RAG, patterns and agentic RAG with LlamaIndex (teach before B5) |

# **Common learning principles**

Structure context before prompting. Keep humans accountable for architecture, scope, high-impact decisions and merge approval. Apply deterministic tests, contracts, permissions and policy checks before model-based evaluation. Measure quality, latency and cost throughout the workflow.

# **Three day technical delivery plan**

Both tracks are delivered to the same cohort. The following allocation is a proposed planning baseline of six teaching hours per day, excluding breaks. Confirm daily contact hours and lab readiness before fixing the agenda.

**Day 1** A1 120 minutes, A2 150 minutes and A3 90 minutes. Establish context, make validated changes and complete the guided team workflow.

**Day 2** A4, A5, B1 and B2 at 90 minutes each. Strengthen coding-agent controls, complete the Track A milestone and begin application and tool integration.

**Day 3** B3, B4 and B5 at 120 minutes each. Build bounded workflows, add governed data, trace failures and demonstrate improvement.

Total: 18 teaching hours. Target approximately 11 hours of guided and independent lab work, including capstone milestones, and seven hours of explanation, demonstrations and debriefs. Capstone time is included within A5 and B5.

# **Scope and readiness**

**Core practice** All 10 modules, one primary coding-agent workflow, one prepared reference application, one tool integration path, one governed dataset and one evaluation loop.

**Demonstration** Alternative coding-tool workflow, model-tier comparison, worktree parallelism and sandbox architecture. Use demonstrations where repeated setup would displace practice.

**Optional extensions** Multiple parallel agents, complex merge conflicts, custom sandbox deployment, advanced model routing and additional integrations. These do not gate completion.

Before training, verify approved tools, model and API access, repository and CI permissions, a tested environment, prepared sandbox, synthetic data and tracing access. Before the first agent lab, establish branch isolation, scoped credentials, allowed actions, diff review and a recovery path.

# **One project with two milestones**

Maersk SMEs and the trainer select the business problem. Participants receive a working starter application, synthetic data, baseline tests, a provided CI pipeline, prepared tool stubs and recovery checkpoints. Each module changes this same application or its engineering controls.

Track A ends with a validated software change and review evidence. Track B extends that application with a bounded, governed and evaluated agentic workflow. These are two milestones in one capstone progression. A Logistics Exception Resolution Agent remains an illustrative option until selected with Maersk.

# **Track A**

AI Augmented Software Development

## **A1 AI Development Foundations and Context Engineering**

**Objective** Establish the mental models and engineering context needed to work effectively with coding assistants and agents.

* LLMs and coding agents; tokens, context windows, non-determinism, limitations and developer responsibility.  
* Prompt engineering to context engineering: design documents, acceptance criteria, test plans and CLAUDE.md or AGENTS.md.  
* Repository context, shared and personal instructions, and context poisoning, distraction, confusion and conflict.  
* Model choice by quality, latency, cost and task complexity; fast, default and deep reasoning tiers and phase-based switching.

**Hands on lab** Run the same repository task with minimal context and engineered context. Compare the implementation, tests and review effort; repair a supplied context failure.

**Checkpoint** Produce a repository instruction file and specification with acceptance criteria; justify a model choice and show the context comparison.

## **A2 AI Powered Coding Testing Debugging and Refactoring**

**Objective** Use AI to implement and improve code while validating every proposed change.

* Understand repository structure, dependencies and conventions; plan a small change before generating code.  
* Feature implementation, multi-file changes, refactoring and defect diagnosis.  
* Unit and integration tests and edge cases; check tests against acceptance criteria to catch shared code and test misunderstandings.  
* Claude Code and GitHub Copilot: plan, implement, test and inspect; split tasks, refresh context, reject changes and revert mistakes.

**Hands on lab** Implement a feature, reproduce and fix a defect, refactor a module and generate tests in the common reference repository.

**Checkpoint** Demonstrate acceptance criteria with reviewed tests, identify a flawed AI suggestion and show a rejected or reverted change.

## **A3 Team Development with Coding Agents**

**Objective** Integrate coding agents into shared repository and review practices.

* Shared repository context, branches and worktrees; isolated agent sessions and recovery from conflicting changes.  
* One task, one branch, one PR; PR intent, scope, tests, risk and rollback.  
* AI-assisted first-pass review, human review and human merge ownership.  
* CI tests, lint and security gates; CodeQL or equivalent scanning; reusable skills and hooks.

**Hands on lab** Use a provided CI pipeline to complete a guided worktree-to-PR workflow. Implement, test, fix a failed check and exchange the PR for human review.

**Checkpoint** Submit a focused PR with clear validation evidence and explain the remaining human review decisions.

# **Track A continued**

## **A4 Safe AI Engineering Harness Security and Quality**

**Objective** Build the controls that make coding-agent execution and generated changes safe to review.

* Harness pillars: tests, lint, static analysis, schema and contract validation, policy and traceability.  
* AI-generated-code vulnerabilities, prompt injection and poisoned repository instructions. **out of scope**  
* Coding-agent execution controls: use a prepared container sandbox, isolate credentials, scope permissions and gate sensitive commands.  **out of scope** 
* Allowed paths and tools, destructive-command prevention, security checks and deterministic validation before subjective evaluation.

**Hands on lab** Add lint and formatting hooks, destructive-command blocking, structured-output validation and tool or path restrictions. Test attempted overreach in an isolated disposable environment.

**Checkpoint** Show that the controls catch an invalid output or unauthorized action and retain a usable execution log.

## **A5 AI Augmented Delivery from Brief to a Validated PR**

**Objective** Integrate the complete software-delivery lifecycle on the shared reference application.

* Brief to requirements, acceptance criteria, design, repository context and test plan.  
* Implementation with coding agents; automated tests, first-pass review, CI and security validation.  
* Human checkpoints for architecture, scope, security exceptions and merge approval.  
* Reviewable change evidence: intended behaviour, passing checks, known limitations and rollback approach.

**Hands on lab** Complete the Track A capstone as an end-to-end feature or change, using the context and harness established in A1 to A4.

**Checkpoint** Deliver a PR ready for human review against defined criteria, with checks, remaining risks, rollback and a justified merge or hold decision.

# **Track A capstone**

Participants implement or improve a feature in the common Maersk-relevant enterprise application. The business problem will be co-designed with Maersk domain SMEs so it remains realistic and understandable across technical backgrounds. All Track A labs extend, inspect or improve the same reference codebase.

**Evidence** Specification and repository instructions; implementation diff; automated tests; CI and security results; completed PR; review and merge rationale.

# **Human responsibilities**

Developers remain responsible for understanding the code, verifying requirements and tests, reviewing security implications, and deciding whether the change is suitable to merge. Passing automated checks supports this decision without replacing engineering judgment.

# **Track B**

Agentic AI Application Building

Outcome: build a bounded enterprise-style agentic workflow with tools, governed data, human approval boundaries, traces and measurable evaluation.

## **B1 From LLMs to AI Applications**

**Objective** Turn a model call into a structured and validated application feature.

* Model APIs, system instructions, prompts, context and structured outputs.  
* Deterministic and probabilistic components; application architecture and validation boundaries.  
* Model selection based on application quality, latency, cost and risk.  
* Controlled inputs, output schemas, error handling and developer responsibility for application behaviour.

**Hands on lab** Convert a basic LLM call into a structured feature with controlled inputs and validated outputs in the reference application.

**Checkpoint** Demonstrate a valid output and safe handling of an invalid or incomplete response.

## **B2 Tools Function Calling and Model Context Protocol**

**Objective** Connect the application to approved tools with explicit permissions and logging.

* Agents and chatbots; tool use, function calling and the agent execution loop.  
* Tool schemas, external APIs and MCP host, client and server concepts.  
* Authentication, scoped permissions, allowlists and denylists, tool-call logging and safe failure behaviour.  
* Clear tool descriptions and validation of tool arguments and returned results.

**Hands on lab** Connect controlled external tools through function calling or MCP and execute a workflow involving at least two tool calls.

**Checkpoint** Show the execution trail and verify that an unavailable or disallowed tool fails safely.

## **B3 Agentic Workflow Design**

**Objective** Design a multi-step agent workflow with bounded autonomy and explicit state.

* Perception, planning, action and feedback loops; state and workflow progression.  
* Bounded retries, failure handling and human-in-the-loop checkpoints.  
* Risk-based autonomy; single-agent and multi-agent patterns, orchestrators, reusable sub-agents and parallel execution.  
* When a deterministic workflow is sufficient and when agentic behaviour adds value.

**Hands on lab** Build a bounded multi-step workflow with controlled tools, explicit checkpoints and a deliberately introduced failure.

**Checkpoint** Demonstrate correct progression, a retry or stop condition, and a human approval boundary.

# **Track B continued**

## **B4 Enterprise Data Knowledge and Actions**

**Objective** Ground agent decisions in enterprise-style data while controlling access and actions.

* Enterprise APIs, SQL databases, schema discovery and knowledge access through tools or MCP.  
* Natural-language-to-SQL with schema context; validate joins, filters, generated queries and results.  
* DuckDB over governed local data or approved database access; curated data products and read-only defaults.  
* Least privilege, PII boundaries, row and query-cost limits, bounded retries and approval for high-impact writes.

**Hands on lab** Connect the reference agent to governed synthetic data. Generate and validate queries, then use the results within a controlled decision workflow.

**Checkpoint** Show valid query results and demonstrate that a prohibited query or action is blocked.

## **B6 RAG, Patterns and Agentic RAG with LlamaIndex**

**Objective** Build a document-grounded answer pipeline, diagnose retrieval failures and choose when agent-directed retrieval adds value.

* Documents, chunking, metadata, embeddings and similarity search; inspect retrieval before generation.
* Basic RAG through LlamaIndex; answer synthesis, returned sources, missing evidence and unsupported claims.
* Failure-driven retrieval patterns: metadata scope, hybrid lexical/dense fusion, reranking and query rewriting; discuss sentence-window/parent-context expansion as extensions.
* Query engines as tools; bounded FunctionAgent retrieval, query selection, observations and stop conditions.
* Retrieval hit/recall measures versus answer faithfulness and agent task success; identical-case before/after comparisons.

**Hands on lab** Use tiny synthetic port documents independently of PortOps. Inspect a worked baseline, complete evidence checks, then design an unsupplied changed-case evaluation and compare a fixed RAG pipeline with agent-directed retrieval.

**Checkpoint** Show retrieved evidence, identify a retrieval or generation failure, justify one pattern change, and inspect the actual agent/tool trace where model access is available. Live exercises use the shared OpenAI-compatible chat and embedding endpoints.

**Materials** [B6 module pack](../track-b/modules/b6/README.md). Time allocation remains pending.

## **B5 Safe Observable and Evaluated Agentic Applications**

**Objective** Control agent actions and measure whether the application works reliably.

* Runtime application controls: guardrails, policy gates, output and tool-call validation, and human approval boundaries.  
* Langfuse or equivalent tracing: prompts, responses, tool calls, execution steps, tokens, latency and cost.  
* Representative test cases; schema and task-completion checks; rubric-based LLM-as-judge where appropriate.  
* Failure classification by prompt, tool or context, architecture and knowledge; diagnose, fix and re-evaluate.

**Hands on lab** Instrument the capstone, capture traces from representative runs, define five evaluation cases and diagnose a failure. Apply a fix and compare before and after results.

**Checkpoint** Present a traced workflow, evaluation results and one documented improvement cycle, including a control or evaluation that caught an issue.

# **Track B capstone**

Extend the common application into an enterprise agentic workflow, such as a Logistics Exception Resolution Agent. The agent receives an exception, retrieves permitted operational data or policy, selects approved tools, recommends or performs allowed actions, seeks human approval where required and records the execution trail. The final use case is selected with Maersk SMEs.

**Evidence** Structured AI feature; tool or MCP integration; bounded workflow; governed data access; policy controls; traces; evaluation cases and measured improvement.

# **Reusable teaching assets**

Each technical module is supported by instructor slides and demo cues, a standard lab, a module assessment and a checkpoint in the common capstone. Reference repositories include starting code, completed solutions, module checkpoints, synthetic data, setup instructions and troubleshooting guidance.

The subsequent TTT stages prepare nominees to explain concepts, demonstrate workflows, facilitate labs and handle questions. Two assessed teachbacks provide feedback and validate readiness for internal delivery.

# **Train the Trainer journey**

**Virtual orientation** Set learner and trainer expectations, observation criteria, preparation requirements and teachback assignments.

**Days 1 to 3** Complete both technical tracks as learners while observing explanation, demonstration, lab support and debrief techniques.

**Practice period** Over one to two weeks, rehearse, close technical gaps, improve trainer notes and prepare a second segment.

Readiness outcomes: Ready to Deliver Independently, Ready with Initial Support, or Requires Additional Practice. These assess teaching readiness separately from technical module completion.

