# AI for SDLC — PDF Markdown extractions

14 source PDFs converted into 14 Markdown documents: 13 Claude Academy playbook lessons and one 19-slide Claude Code presentation. The lesson documents follow the course order.

[Read all extracted documents in one file](all-pdf-content.md)

| Lesson / document | Markdown | Source pages |
| --- | --- | --- |
| 1 | [What changes and where to start](01-introduction.md) | 2 |
| 2 | [Capture as intent.md](02-capture-intent.md) | 2 |
| 3 | [Requirements and design](03-requirements-and-design.md) | 2 |
| 4 | [Claude Code plan mode as the default starting point](04-plan-mode.md) | 2 |
| 5 | [The CLAUDE.md](05-claude-md.md) | 1 |
| 6 | [Skills as institutional knowledge](06-skills-as-institutional-knowledge.md) | 2 |
| 7 | [Parallel sessions and subagents](07-parallel-sessions-and-subagents.md) | 1 |
| 8 | [Give Claude a feedback loop](08-give-claude-a-feedback-loop.md) | 2 |
| 9 | [Continuous evals in CI](09-continuous-evals-in-ci.md) | 2 |
| 10 | [AI in the PR review loop](10-ai-in-the-pr-review-loop.md) | 2 |
| 11 | [Hooks as approval gates](11-hooks-as-approval-gates.md) | 2 |
| 12 | [CI/CD integration and deployment](12-ci-cd-integration-and-deployment.md) | 2 |
| 13 | [Closing the loop on metrics](13-closing-the-loop-on-metrics.md) | 2 |
| Presentation | [Claude Code — Presentation](14-claude-code-presentation.md) | 19 |

## Extraction approach and limits

- These are content extractions, not curriculum summaries. Article headings, paragraphs, lists, comparison tables and visible code examples are preserved and formatted as Markdown.
- The 13 playbook PDFs contain page images. Their text was extracted with local Tesseract OCR; tables and code were checked against the captures and obvious OCR errors corrected. Minor transcription errors may remain.
- The presentation uses its embedded text layer, with slide images retained for diagrams and screenshots. Visible principal screenshot text is also transcribed for slides 8–10; clipped or tiny UI details remain available in the images.
- Website navigation, lesson selectors, pop-up instructions, feedback buttons and footers are omitted from article text. Redundant OCR page images and text-only slide images have been deleted. The source PDFs remain available; `assets/` retains only five visuals: the dependency graph, the presentation chart and three screenshots. All page images whose article text and code were extracted have been deleted.
- Some long code lines were clipped horizontally in the PDFs. All 18 previously marked lines have now been restored from the original online lessons for plan mode, continuous evals, hooks, CI/CD and metrics. The five documents link to their recovery sources and record the check date (2026-10-27). No missing code was inferred.
- The continuous-evals lesson has collapsed “The checker script” and “The log check” sections. The metrics lesson has a collapsed “The detection script” section. Their bodies are absent from the supplied PDFs and are explicitly marked as unavailable.
- The playbook introduction's dependency graph is retained as an image. Original source PDF links are included in every document. Redundant page-image references have been removed.
- Source claims, product names and configuration examples are preserved as supplied. Recovered code blocks were compared with the original lesson HTML; this is transcription verification, not current-product compatibility testing.
- The Academy interface references 14 lessons, but the directory supplies captures of lessons 1–13 only. No lesson 14 content has been added.
