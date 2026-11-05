# B3 Teaching Deck Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan in the current session. Preserve unrelated workspace changes and do not stage or commit them.

**Goal:** Build the agreed B3 lecture in the established B1/B2 Marp style, with complete runnable illustrations and no lab design.

**Architecture:** One synthetic shipment investigation motivates increasingly independent decisions, specialist coordination, and retained progress with human review. Explain each concept before its code. Keep the six required examples standalone; preserve the previous four examples as references. Optional parallelism and LlamaIndex comparisons remain outside the required run sequence.

**Tech stack:** Marp Markdown, Python 3.11+, OpenAI Agents SDK 0.20.0, GPT-4.1-mini, LlamaIndex versions already tested in B2, dotenv with OPEN_AI_KEY.

**Spec:** User-approved three-section outline in this conversation: multi-step autonomy; orchestration/delegation; state and human participation. Labs are deferred until tomorrow morning.

## Global constraints

- Match B1/B2's 16:9 theme, typography, colours and embedded presenter notes.
- Plan a 60-minute lecture, approximately 20 minutes per section including illustrations.
- Use synthetic C1/C2 shipment records and clearly identified demonstration policies.
- Preserve actual model replies and tool observations; never present schematic output as a live trace.
- Keep arithmetic deterministic, specialist roles narrow, and decisions bounded.
- Review the exact pending action; test real SDK interruption, serialization and resumption for approval and rejection.
- Keep lab starters, assessments and deferred B4–B6 material unchanged.

## Review focus

- Unknown C9 must not acquire invented operational facts.
- A low turn budget must produce an incomplete outcome rather than false completion.
- Specialist calls and handoffs must show actual execution and final-answer ownership.
- Follow-up history and application task state must be distinguished; saved JSON alone is not a durable agent checkpoint.
- Rejection must execute no outbox action; approval must execute the reviewed payload once in the demonstration.

## Tasks

- [x] Record the B1/B2 teaching pattern and validate the installed SDK interfaces and official source guidance.
- [x] Write a temporary behavioral verifier for the six planned core paths and two optional comparisons; observe the initial missing-file failure.
- [x] Preserve existing B3 scripts in reference/; implement sequentially numbered workflow, investigation, delegation, handoff, state/memory and approval examples plus optional parallel/LlamaIndex comparisons.
- [x] Run actual examples, including unknown input, bounded stopping and approve/reject paths; repair failures at their cause.
- [x] Replace the B3 deck with approximately 36 slides, following the agreed conceptual progression and linking matching complete examples.
- [x] Update B3 guides and module indexes, dependency/run instructions, counts and link references.
- [x] Render the reference and B3 decks, inspect all slides, verify code excerpts/links/pacing and obtain one independent final review.
- [x] Report the deck, source examples and concrete verification results without claiming lab completion.

## Execution rulings

- The user's explicit instruction to build the approved scope authorizes implementation now; no additional plan-approval pause is needed.
- Work in the shared checkout so the user's current teaching files remain the deliverable. Do not change unrelated staged additions, deletions or external project files.
- Use temporary scripts for behavioral verification; keep the learner examples free of test harnesses and project helper imports.

## Verification outcome

The six core scripts and two optional comparisons passed 11 behavioral scenarios. Approval restoration initially required an awaited SDK call; output review tightened two model instructions and the parallel fixture. All changed paths were rerun. An independent reviewer checked conceptual progression and SDK claims; substantive findings were addressed. All 36 B3 slides were visually inspected alongside B1/B2. Lab files remain unchanged.
