# B1 · Preserved examples for later topics

These standalone examples are retained outside the [six core B1 snippets](../README.md).

Their filenames describe the topic; they are not additional numbered B1 lessons.

| File | Later teaching purpose |
| --- | --- |
| [supply_context.py](supply_context.py) | Supply a synthetic operational record as evidence |
| [json_output.py](json_output.py) | Request JSON mode and decode the actual model reply |
| [validate_schema.py](validate_schema.py) | Validate a prepared JSON value with Pydantic |

The first two call OpenAI and read `OPEN_AI_KEY` using dotenv. Schema validation uses a clearly labelled prepared value and needs no model access. Nothing here claims access to actual Maersk records.

The JSON example requests a JSON object through `response_format`; an instruction alone can still produce Markdown fences. JSON mode does not enforce the fields or allowed status values. See [OpenAI's structured-output and JSON-mode guide](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=chat).
