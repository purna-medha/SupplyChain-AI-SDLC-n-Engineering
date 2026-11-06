# Gamma-ready copies · B0–B5

Open one of these UTF-8 text files in a text editor and copy its complete contents. The text uses Markdown headings, tables and code fences, with one slide per standalone `---` block.

| File to paste | Expected slides | Original teaching deck |
| --- | ---: | --- |
| [b0-python-foundations.txt](b0-python-foundations.txt) | 38 | [B0 Markdown](../slides-md/b0-python-foundations.md) |
| [b1-llm-applications.txt](b1-llm-applications.txt) | 33 | [B1 Markdown](../slides-md/b1-llm-applications.md) |
| [b2-tools-and-mcp.txt](b2-tools-and-mcp.txt) | 31 | [B2 Markdown](../slides-md/b2-tools-and-mcp.md) |
| [b3-agentic-workflows.txt](b3-agentic-workflows.txt) | 36 | [B3 Markdown](../slides-md/b3-agentic-workflows.md) |
| [b4-enterprise-data.txt](b4-enterprise-data.txt) | 34 | [B4 Markdown](../slides-md/b4-enterprise-data.md) |
| [b5-safety-observability-evaluation.txt](b5-safety-observability-evaluation.txt) | 36 | [B5 Markdown](../slides-md/b5-safety-observability-evaluation.md) |

## Paste into Gamma

1. Create a presentation in Gamma and paste one file's raw text. Keep each module as a separate presentation. For B4 expect **34 cards**; for B5 expect **36 cards**.
2. Ask Gamma to preserve the supplied text. In the classic generator, choose **Preserve**. In Gamma 5, include that instruction with your pasted content or send it before generating. See [Gamma's import and text-handling guidance](https://help.gamma.app/en/articles/11047840-how-can-i-import-slides-or-content-into-gamma).
3. Use the instruction below in the available prompt/instructions area. Check that the outline has the expected number of cards before generating.
4. After generation, check Python indentation, table columns and diagram arrow directions. If needed, place Python text in a code block and select Python as its language. See [Gamma's code-block guidance](https://ideas.gamma.app/changelog/syntax-highlighting-for-code-blocks).

## Suggested instruction

```text
Create a technical training presentation from the supplied content.

Treat each block separated by a standalone --- line as one slide/card.
The content already includes its cover and closing slides. Keep the existing
slide count, order, titles, explanations and teaching progression.

Preserve the supplied text. Do not summarize, merge slides, add new concepts,
invent operational facts or expand the abbreviated code examples.

Keep Python code exactly as supplied, including indentation, model names,
environment variables and argument values. Present it as readable code.
Preserve every table's rows, columns and wording.

Text blocks containing arrows describe workflows. You may turn them into
simple editable diagrams while preserving labels, branches and directions.

Use a clean 16:9 training layout with a light background, teal headings and
readable body text. Improve the visual layout while preserving the content.
```

## Conversion details

The six copies contain 208 slides and 105 code/diagram blocks. B4/B5's 70 slides and 32 fenced blocks match their refined Markdown sources in order and content, including every table. Marp configuration, CSS, presenter notes and presentation directives were removed. Local illustration-link lines were removed, and remaining local links became plain descriptive text. No machine-local file paths are required by the pasted material.

The original Markdown decks retain their presenter notes and runnable-example links. These text files are separate copies; regenerate them after changing the originals.
