# THE MODERN AI DEVELOPER — v4

**AI-Assisted Engineering for Production Teams** — 3-day intensive for Maersk engineering teams.

|  |  |
| :---- | :---- |
| **Audience** | Software developers (70%) \+ infrastructure engineers (30%) |
| **Format** | Lecture \+ demos \+ hands-on labs (\~60% lab time) |
| **Duration** | 3 full days — 10 modules \+ capstone |
| **Core tools** | Claude Code · Copilot Pro · Copilot CLI · MCP · Langfuse · DuckDB |

## At a Glance

| Day | Theme | Modules |
| :---- | :---- | :---- |
| 1 | **Talk to agents well** | M1 Foundations · M2 Context Engineering · M3 Model Selection |
| 2 | **Ship through the pipeline** | M4 AI Coding · M5 Team Dev on GitHub · M6 Agents & MCP |
| 3 | **Harness, build, iterate** | M7 Team Delivery Flow · M8 Security & Harness · M9 AI for Database Work ·**Capstone build** · M10 Eval & Iteration |

**Themes running end-to-end:**

* Context engineering tied to engineering artefacts (design docs, acceptance criteria, PR templates, test plans)  
* Model harnessing — validation, contracts, guardrails, policy, traceability  
* Team-first delivery — branches, PRs, reviewers, CI, security gates  
* Cost and latency discipline — model selection and phase switching

---

# DAY 1 — Talk to Agents Well

## M1 — Foundations of GenAI

**Goal:** Mental models every developer needs before picking up a coding agent.

**Theory — A developer's view of GenAI**

* Output types: text, code, images, audio, video  
* Key model families:  
  * Closed Source: GPT-5.5 (mini, thinking & pro), Claude(haiku, sonnet & opus) , Gemini ( flash, thinking & pro)   
  * Open-source: Qwen, Deepseek, Kimi, Gemma 4, Gpt-oss  
* Core concepts: tokens, embeddings, context windows, temperature, fine-tuning  
* Non-determinism and what it implies for engineering practice  
* How agents differ from plain LLMs \- the next paradigm

**Theory \+ Demo — Strengths, weaknesses, responsible use**

* Hallucinations, bias, reasoning limits — live demo  
* Why AI-generated code still needs developer oversight  
* Privacy, compliance, copyright considerations  
* Ethics and responsible use — real-world case studies

## M2 — Context Engineering with Github Copilot

**Goal:** Move beyond prompts to systematic context tied to engineering artefacts.

**Theory — Prompt engineering fundamentals**

* Instruction clarity, structure, and constraints  
* Advanced patterns: chain-of-thought, few-shot, role-based  
* Multi-turn conversations: maintaining context and handling drift  
* Treat prompts as software — test, version, regression-check

**Lab — Prompt engineering playground**

1. Build and test the same prompt across Claude and OpenAI Playground  
2. Compare output quality across models on identical tasks  
3. Iterate: form a hypothesis, test, measure, refine  
4. Score prompts for quality against a rubric \- manual eval (learning to quantify the prompt quality)  
5. Document one prompt-pattern that worked and one that didn't

**Theory — Context engineering**

* Why prompt optimisation hits a ceiling and what replaces it  
* Engineering artefacts *as* AI context: design docs, acceptance criteria, CLAUDE.md / AGENTS.md, PR templates, test plans  
* Personal vs team vs `.local.md` separation  
* Context failure modes: poisoning, distraction, confusion, conflict  
* Managing AI context in large, real-world codebases

**Lab — Spec-first design doc**

1. Draft a CLAUDE.md / AGENTS.md and design doc for a real project  
2. Feed the spec into Claude Code and run an implementation task  
3. Run the same task with prompt-only — no spec  
4. Compare outputs side by side and capture the diff  
5. Identify a context failure mode in a provided sample project  
6. Fix it by restructuring the context, not the prompt

## M3 — Model Selection (Cost × Latency × Quality)

**Goal:** Pick the right model for the task. Switch models by phase. Control spend.

**Theory — The three-tier decision tree**

* **Fast \+ cheap** — summaries, extraction, formatting, simple Q\&A (Haiku / Flash / small general-purpose)  
* **Default** — day-to-day coding, multi-step changes, refactors with tests (Sonnet / Pro / general-purpose)  
* **Deep reasoning** — architecture trade-offs, complex debugging, high-stakes reviews (Opus / Thinking / reasoning models)  
* Understanding usage limits and working around them with cheaper model selection  
  * Claude Code and Github Copilot

**Theory — Phase-based switching**

* Plan strong, execute cheap: use a deep model for architecture and a default model for the execution loop  
* Worked example: Opus plan → Sonnet execution, measure token cost and quality delta  
* Routing as an advanced pattern (optional): choose per request based on complexity and budget

**Lab — Pick the right model**

1. Given 6 tasks of varying complexity, justify a tier for each  
2. Run the same task on fast / default / deep  
3. Measure latency, token cost, and quality for each run  
4. Apply phase-based switching to one multi-step task and measure the delta  
5. Build a personal cheat-sheet mapping task types to tiers

---

# DAY 2 — Ship Through the Pipeline with AI

## M4 — AI-Powered Coding & Agentic Workflows

**Goal:** Use coding agents productively at the right autonomy level.

**Theory — The coding-tools landscape**

* Copilot Pro, Copilot CLI, and Claude Code — positioning and trade-offs  
* Autonomy spectrum: suggestion → completion → chat → supervised agent run  
* Tool setup, configuration, and codebase integration  
* Honest expectations: where coding agents help and where they don't  
* CLAUDE.md / AGENTS.md for team context; `.local.md` for personal overrides

**Lab — Claude Code / Copilot CLI deep dive in a shared repo**

1. Set up the agent and a working repo with CLAUDE.md / AGENTS.md  
2. Generate a new feature from a one-paragraph brief  
3. Refactor an existing module with the agent as collaborator  
4. Reproduce and fix a real bug using AI assistance  
5. Auto-generate unit and integration tests  
6. Set autonomy checkpoints and let the agent run a multi-step task  
7. Review and validate every diff before committing

**Lab — GitHub Copilot Pro workflow in a shared repo**

1. Use inline completions on an unfamiliar codebase  
2. Ask Copilot Chat questions about your own code  
3. Refactor a small module via Copilot features  
4. Run the same task in Claude Code and Copilot — compare outputs and review effort  
5. Decide which tool fits which task type and write it down

## M5 — Team Development with Coding Agents (continuation of M4)

**Goal:** Make coding agents work in shared repos — branches, PRs, reviews, CI, security gates.

**Theory — Worktrees, parallelism, context offloading**

* Worktree concept: multiple branches checked out simultaneously, sharing one repo  
* Multi-session workflow: run divergent tasks in parallel terminals  
* Context offloading: keep the main thread clean, push messy iteration into isolated worktrees  
* Why this matters: less context bloat, fewer merge collisions, safe parallel exploration

**Theory — Branch and PR discipline**

* One task, one branch, one PR  
* Agents propose changes; humans own merge decisions — non-negotiable  
* PR template for agent-assisted changes: Intent / Scope / Tests / Risk / Rollback  
* Avoid "agent mega-PRs" — keep diffs reviewable

**Theory — CI and security gates as harness**

* CI gates: tests, lint, code scanning  
* CodeQL PR enforcement — PRs must publish CodeQL results with no critical/error alerts before merge  
* Run the agent in a way that *still* passes lint, tests, and code-scanning gates

**Theory — Skills and hooks for team consistency**

* Skills are instruction files; hooks are commands fired at lifecycle points  
* Core idea: hooks guarantee behaviour, instructions only suggest it  
* Examples: auto-lint/format on edit, block destructive commands, enforce repo conventions  
* Reduces token waste from repetitive exploration and hallucinated APIs

**Lab — Simple AI-assisted PR end-to-end on your team Repo (Bring your own Repository)**

1. **Git checkout a test branch, so as to not affect the repository**  
2. Create a feature branch via worktree  
3. Spawn 2 parallel agent sessions exploring different approaches  
4. Implement using Claude Code / Copilot CLI with the repo CLAUDE.md as context  
5. Auto-generate tests alongside the implementation  
6. Open a PR using the AI-assisted change template (Intent/Scope/Tests/Risk/Rollback)  
7. Run agent-assisted first-pass review on your own PR  
8. Watch CI run tests, lint, security scan, CodeQL — fix any failures with AI help  
9. Make the human merge call — discuss as a group what would block merge

## M6 — AI Agents & Model Context Protocol (MCP)

**Goal:** Understand agents and connect them to real tools safely.

**Theory — Anatomy of an agent**

* Agents vs chatbots — the difference between responding and acting  
* The agent loop: perception → planning → tool execution → feedback  
* Tool use and function calling give agents real-world capabilities  
* Agent types: simple task runners, multi-step planners, multi-agent systems  
* Agent memory patterns: in-context, external retrieval, persistent state  
* Basic telemetry: How to capture and log raw JSON tool calls, system prompts, and model responses to a local file for immediate debugging (a precursor to advanced cloud tracing in M10).

**Theory \+ Demo — MCP as the connectivity layer**

* What MCP is and why it matters — the universal connector for AI tools  
* Architecture: host, client, server components  
* Pre-built MCP servers: filesystem, browser, GitHub, APIs  
* **Connecting agents to databases via MCP** — SQL endpoints, schema discovery, query as a tool call *(expanded in M9 — AI-Assisted Database Work)*  
* How Claude Code uses MCP internally  
* Tool allowlists and denylists — constraining what an agent can call  
* Logging every tool call and MCP call for audit  
* Security and authentication for MCP servers

**Lab — Agents and MCP in practice**

1. Configure and connect a pre-built MCP server (filesystem or GitHub) to Claude Code  
2. Build a simple multi-step agentic workflow with at least two tool calls  
3. Trace the agent loop and identify each phase (perceive / plan / execute / feedback)  
4. Add a tool allowlist and observe the agent fail safely when it tries to overreach  
5. Capture the tool-call log and verify the audit trail is usable

**Theory — Autonomy management and sub-agent patterns**

* Autonomy spectrum: fully supervised → fully autonomous  
* Classify tasks by risk and pick an appropriate autonomy level  
* Design human checkpoints — when to pause and ask vs proceed  
* Reusable sub-agent patterns: orchestrator, shared sub-agents (auth, search, formatter)  
* Broad-search: spawn 2–5 parallel sub-agents, then converge on the best  
* When to split into sub-agents vs keep as one agent with more tools

**End of Day 2:** parallel worktree workflows · tight agent PRs that pass CodeQL · skills/hooks for team consistency · MCP with allowlists and database access.

---

# DAY 3 — Harness, Build, Iterate

## M7 — Team Delivery Flow with Agentic LLMs (Brief → Merge)

**Goal:** Run the full team delivery loop with agents — brief to merge. AI does the work in between; humans own the merge call.

**Theory — The delivery loop**

* The full loop: brief → stories → acceptance criteria → tests → implementation → review → CI → merge  
* Each step has an AI default and an explicit human checkpoint  
* Humans gate architecture, scope, merge approval, and security exceptions  
* AI runs stories, test scaffolding, first-pass review, CI failure triage  
* Agents propose, humans dispose — non-negotiable

**Theory — Testing & QA automation**

* Tests written alongside code, driven from acceptance criteria  
* AI generates unit, integration, and edge-case tests  
* Coverage is a gate, not a vanity metric  
* Regression suites maintained by AI as the codebase evolves

**Theory — CI as the silent reviewer**

* The CI pipeline is the M8 harness expressed in code  
* Standard gates: lint, type-check, unit tests, integration tests, security scan, CodeQL  
* Agent triages failures: reads the trace, proposes a fix, re-runs  
* Every check passes before human review — reduces reviewer fatigue, keeps the merge queue healthy

**Lab — Intermediate AI-assisted PR end-to-end in team repo (Bring your own Repository)**

1. **Git checkout a test branch, so as to not affect the repository**  
2. Start from a one-paragraph brief — use AI to draft user stories and acceptance criteria  
3. Generate the test suite *first* from the acceptance criteria — unit \+ integration \+ at least one edge case  
4. Implement against the failing tests using Claude Code / Copilot CLI on a worktree branch  
5. Run the agent through lint/format hooks before staging — the harness shapes the diff  
6. Open a PR using the AI-assisted change template (Intent / Scope / Tests / Risk / Rollback)  
7. Run an agent-assisted first-pass review on your own PR  
8. Watch CI run lint, tests, security scan, CodeQL — let the agent triage failures and propose fixes  
9. Trade PRs with a teammate — perform a human review focused only on what the harness can't catch  
10. Make the merge call — discuss as a group what blocks merge in real life and why

## M8 — Security, Quality & Model Harnessing

**Goal:** Agents are not trusted collaborators by default. Build the harness that makes them safe to use against real systems.

**Theory — Why a harness, why now**

* Agents and coding models need a harness around them — not blind trust  
* Four root causes of agent failure: prompt, tool/context, architecture, knowledge gap  
* What "harness" means in practice: tests, lint, security scans, schema/contract checks, policy, traceability  
* Layer subjective evaluation on top of objective checks — never the other way around  
* Sandboxing in practice: Using open source docker sandbox \- agent-infra/sandbox to give the agent a workspace that is physically isolated

**Theory — AI security**

* Prompt injection in coding tools — real CVE examples  
* Common vulnerability patterns in AI-generated code  
* Secure-review checklist — critical points before every commit  
* OWASP considerations specific to AI-assisted workflows  
* Prompt poisoning in source code — how attackers exploit AI coding tools  
* LLM & Application Red teaming as proof-of-danger**:** Using promptfoo to sweep codebase to surface concrete security mistakes  
* Execution security practices: Protecting the host system through containerized agent execution, credential scoping at invocation, and implementing network egress allowlists.  
* Sensitive commands gating: Intercepting and blocking sensitive commands (kubectl, vault, aws)

**Theory — The harness pillars**

* Deterministic rules — hooks and skills that check AI output before it lands  
* Linting and static analysis — what AI code must pass before review  
* Tests — auto-generated and pre-existing; both must pass  
* Contract validation — schema, type, and shape checks on structured outputs  
* Policy restrictions for agents acting on real systems: allowed tools, allowed tables, row limits, cost limits, blast-radius classification, approval gates  
* Traceability — every tool call logged, every decision auditable *(deep dive in M10)*  
* Order of operations: deterministic checks first, LLM-as-judge only on what passes

**Lab — Build the harness pillars** *M7 ran the harness end-to-end. Here we build the pillars the harness is made of.*

1. Building harness and sandbox for execution and evaluation  
2. Harness  
   * Add a hook that runs lint and format on every agent edit before staging  
   * Add a hook that blocks destructive commands (rm \-rf, force-push, db drop) from agent execution  
   * Write a JSON schema and contract-validate an AI-generated structured output  
   * Configure an MCP tool allowlist and denylist for a coding agent  
   * Implement a policy gate: agent can only write inside an allowed-paths whitelist  
   * Add traceability — log every tool call with timestamp, agent run ID, and tool arguments  
   *   
3. Sandbox  
   * Build the Sandbox: Establish your sandbox using agent-infra/sandbox (Docker)  
   * The Proof of Danger (Unsandboxed): Run an unsandboxed agent against an overreaching task  
   * Try to make the agent overreach in 3 ways — verify each pillar catches it

**Theory — Post-deployment observability**

* AI-assisted debugging in production environments  
* Logging strategies designed for code built by AI agents  
* Incident response — using AI to triage, diagnose, and resolve faster  
* Observability patterns that work well with AI-generated codebases

## M9 — AI-Assisted Database Work ★ NEW

*Expands the databases-via-MCP point from M6. AI is not just for code; engineers also write queries and connect to operational data.*

**Goal:** Engineers use AI to generate SQL, connect agents to databases, and validate every query and result before trusting any answer.

**Theory — Why AI for database work**

* Engineers spend serious time on queries, schemas, and operational data pulls — not just code  
* The same agent that writes code can write SQL  
* Database work has its own failure modes: wrong join, leaked PII, missed WHERE, deprecated table  
* The same harness discipline applies — validate before you trust

**Theory — Connecting agents to databases \- Postgres, DuckDB, or others (M6's MCP hook, deep)**

* MCP DB servers expose schema discovery, query execution, and result streaming as tool calls  
* Read replicas only — agents never touch primary by default  
* Least-privilege roles, short-lived tokens, no shared service accounts  
* Cost ceilings on connection pools — agents can issue many queries quickly  
* ~~DuckDB over Parquet for local analytical workloads~~  
* Expose curated data products, not raw warehouse tables

**Theory — AI-assisted query generation (text-to-SQL)**

* Feed the model the schema, sample rows, and column docs — not just the question  
* Few-shot with example questions and queries from your domain  
* Decompose complex questions into intermediate SQL steps  
* Bounded retry — agent reads the DB error, rewrites, retries  
* Query rewriting and optimisation as a separate AI pass

**Lab — AI-assisted query generation over a governed dataset**

1. Connect a coding agent to DuckDB over a governed Parquet dataset via MCP  
2. Ask 3 natural-language analytical questions; have the agent generate SQL for each  
3. Execute through DuckDB and capture results

## CAPSTONE — Build the AI-Assisted Engineering Workflow

**Build only.** Instrumentation, evaluation, and the improvement cycle happen in M10.

Teams build a small AI-assisted engineering workflow — a feature or internal tool — through the full team-delivery pipeline.

**Build**

* AI Features use case discovery for your own repo (Bring your own repository)  
* Spec-first: write CLAUDE.md / AGENTS.md and a design doc before touching code  
* Build with Claude Code / Copilot CLI as primary driver; Copilot Pro for inline support  
* Connect at least one external tool via MCP (database access encouraged — exercises M9 skills)  
* Ship through the team-development pipeline: worktree → branch → PR → CI

**Shared build requirements**

1. Spec first — CLAUDE.md / AGENTS.md and design doc before code  
2. Generate automated tests alongside the build, not as an afterthought  
3. Apply the M8 harness: tests \+ lint \+ at least one policy or contract check  
4. Run agent-assisted first-pass review before share-out  
5. Brief share-out: what you built, what the AI got right, what surprised you

**Phase-1 graduation** — working build, harness in place. *(Tracing, evals, and one full improvement cycle are added in M10.)*

## M10 — Evaluation, Logging & Iterative Improvement

*The closing module. Operates on the capstone you just built.*

**Goal:** Diagnose *why* an AI system fails, trace the root cause, and apply the right fix — prompt, tool description, architecture, or missing skill. Apply this to your own capstone, not just toy examples.

**Theory \+ Demo — Tracing and logging with Langfuse**

* Langfuse: open-source, framework-agnostic, works natively with Claude  
* What to trace: inputs, outputs, tool calls, intermediate steps, tokens, latency  
* Read a trace: healthy run vs failing one — live demo

**Theory — The refinement loop**

* Analyse failures → identify root cause → apply the right fix → re-run evals  
* Decision tree: refine prompt vs fix tool vs restructure agent  
* Why fine-tuning is usually the wrong first move

**Lab — Instrument, evaluate, iterate (programme close)**

1. Add Langfuse instrumentation to the capstone and capture traces from 3–5 representative inputs  
2. Define 5 test cases (happy path \+ edge cases); write objective evals (schema \+ task-completion checks) plus one LLM-as-judge eval with a rubric  
3. From the traces, pick one failure or weakness and diagnose the root cause by class (prompt / tool / architecture / knowledge)  
4. Apply the fix, re-run the evals, and measure the before/after delta  
5. Share out: what changed, what the eval scores say, what you'd monitor in production

**Final graduation criteria (programme close):**

* Capstone working, harnessed, and instrumented with traces  
* One documented improvement cycle with measured before/after numbers  
* At least one example where the harness or eval caught a real issue

**Group close:** what changes on Monday — personal action plan.

---

## Tools Reference

| Tool | Use | Depth |
| :---- | :---- | :---- |
| Claude Code | Primary agentic coding tool — labs, agents, SDLC, capstone | Deep — used throughout |
| Copilot Pro · Copilot CLI | Internal CLI/IDE agent target — team workflows, PR/CI | Deep — M4, M5, capstone |
| MCP | Tool and data connectivity for agents | Conceptual \+ lab in M6 |
| Postgres / Duckdb ★ | Local analytical engine over Parquet — AI-generated SQL execution | Deep — M9 lab (and capstone if DB used) |
| Git worktrees | Parallel agent sessions, context offloading, branch isolation | Practical — M5 lab |
| CodeQL | Security scanning as a CI gate | Practical — M5 / M8 labs |
| Langfuse | Tracing, logging, evaluation for AI agents | Deep — M10 closing module |

---

## What changed vs v2

* **Positioning** shifted from a tools course to an engineering-delivery course  
* **Vibe coding** removed; rapid-prototyping demos moved to an optional appendix  
* **Model selection** added as a first-class module (M3) — fast/default/deep tiers and phase switching  
* **Team development on GitHub** promoted to Day 2 (M5) — worktrees, PR discipline, CI/CodeQL, skills/hooks  
* **Model harnessing** is now a central theme (M8) — security, harness pillars, policy, traceability  
* **RAG/vector** module replaced entirely by **M9 AI-Assisted Database Work** — engineers using AI to generate SQL, connect to databases via MCP, and validate queries against schema and policy. RAG is no longer a topic in this curriculum.  
* **Capstone arc** restructured: build in capstone (with harness from M8 \+ grounded AI from M9), then instrument and iterate in M10 — so evaluation applies to what students actually built

