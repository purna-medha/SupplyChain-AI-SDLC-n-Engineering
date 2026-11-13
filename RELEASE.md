# Client freeze · 13 November 2026

Release tag: `maersk-client-freeze-2026-11-13-r2`. The [repository guide](README.md) and [content summary](MAERSK_AI_ENGINEERING_SUMMARY.md) define the delivered assets. This is the preserved source snapshot for the completed November teaching assignment.

## Changes made for handoff

- Restored the B2 SDK example to its slide-aligned single read tool, GPT-4.1-mini and four-turn bound. The experimental script is preserved locally outside the release.
- Reconciled the inventory, model setup, curriculum, course maps and Track A navigation with actual files.
- Revision 2 excludes intermediate B4/B5 authoring outlines and local Gamma authoring copies, removing their active client links and presenter-note references. Earlier recorded hashes remain historical evidence; final slide content and supplied PowerPoints are unchanged.
- Kept B5's five main examples and two tracing references. Retained unfinished lab functions as intentional learner work.
- Excluded next-delivery planning, bank experiments, local authoring archives, credentials, bytecode, virtual environments and generated databases. PortOps recreates its database from the supplied CSV seeds using the documented reset command.
- Preserved historical live-verification evidence. Documentation-only changes and current offline checks are recorded separately; old evidence hashes were not silently replaced.

## Freeze verification

The source checks below passed on 13 November 2026 and are repeated against the staged client archive before the local freeze commit/tag:

| Check | Result |
| --- | --- |
| PortOps pytest suite | 32 passed; one existing Starlette/httpx deprecation warning |
| Container Help Desk scaffold/control suite | 20 passed; no live model calls |
| Offline snippets | 19 passed: all 14 B0 core examples, four offline B4 examples and B6 chunking/metadata |
| B2 restored SDK example | Actual SDK-wrapped reads returned the expected C1/C2/C9 results under controlled model IO; unfinished-tool variant failed before restoration |
| Python and notebooks | Delivered Python parses; three notebooks have parseable code, empty outputs and no execution counts |
| Markdown teaching sources | Source links and slide-linked snippet set verified; Gamma authoring copies excluded |
| Supplied PowerPoints | Five files, 170 slides; original hashes unchanged; ZIP integrity and XML parts parsed |
| Local navigation | All client Markdown file links resolve within the package |
| Static names and credential patterns | No undefined Python names in the delivered teaching/application paths; no obvious key/private-key patterns in deliverable text |
| Packaging | Verified against a staged Git archive, with source/runtime checks run from its extracted copy |

PowerPoint files are included as supplied. Their layout was not rendered for inspection and their text was not certified identical to Markdown. No paid model calls, dependency upgrades or fresh package installations are part of this freeze.

## Delivery boundaries

The package contains 12 decks and 408 slides including optional B0. B6 has worked examples and a deck, but no learner lab. Formal assessments, completed learner solutions, a separate Track A checkpoint repository, an implemented AI capstone and trainer-readiness assessment are excluded. Estimated lab timings remain unvalidated by an instructor dry run.

Historical source hashes and model observations describe the dates in their own records. Notebook/live-model/MCP/provider behavior was not freshly exercised for every example. Offline success cannot establish generated-answer quality. PortOps tests use a fixed calculation date; its live UI/API use today's date.

## Reproduce the package

From this repository, after selecting the frozen tag:

```bash
git archive --format=zip --prefix=maersk-client-freeze-2026-11-13-r2/ \
  --output=/tmp/maersk-client-freeze-2026-11-13-r2.zip maersk-client-freeze-2026-11-13-r2
```

Use the reviewed Git snapshot for client handoff rather than zipping the local working directory. Local ignored planning material and credentials are not backed up by this archive. No remote push or publication is performed by creating this local release.
