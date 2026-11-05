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

# B1 · LLMs in a simple application

A shipping-terminology chatbot

Hosted and local models · Conversations · Tokens, cost and latency

<!--
Lecture: 60 minutes, followed by a separate 60-minute lab. Suggested lecture pacing: slides 2–5, 7 minutes; 6–12, 15 minutes; 13–18, 12 minutes; 19–30, 21 minutes; 31–33, 5 minutes. Explain concepts before opening their code illustrations. Run selected examples; leave variations for the lab. No internal documents, live container records, retrieval or tools are connected in B1. Source links lead to complete standalone scripts.
-->

---

# A language feature in an application

An operations trainee asks:

> What is container dwell time?

A useful feature accepts the question and returns a readable explanation.

The language model supplies the generated explanation. Ordinary application code connects it to the user.

<!--
Begin with the user's need. Ask what makes an explanation useful: it should describe the shipping term, remain concise, and avoid confusing cargo containers with software containers. We can judge these properties before choosing an SDK. An optional opening demonstration can show an actual answer without opening code yet.
-->

---

# The model's role

```text
User question → application → language model
                    ↑              ↓
               display reply ← generated text
```

The application collects input, sends a request and handles the response.

The model generates language. It has no connection to the organisation's systems unless the application provides one.

<!--
Trace the arrows. The model is a dependency used for a small slice of functionality. An API key does not connect it to company records. Error handling is an application responsibility even though small teaching scripts let failures surface directly. A terminal already provides enough interface to demonstrate this feature.
-->

---

# Learned capability and inference

**Pretraining:** learning patterns from training data by adjusting model weights.

**Inference:** using learned weights to generate an output for a new input.

A question can use learned knowledge. It does not automatically trigger a search or a read of current company data.

<!--
Distinguish preparing a model from calling it. Do not imply all training is pretraining; instruction tuning and other adaptation may follow. Our examples perform inference. Supplying a conversation also does not retrain the model. This explains why model access and operational-data access are separate capabilities.
-->

---

# Useful language, imperfect answers

Models can explain terms, rewrite text and answer general questions.

They can also misunderstand a term, invent a detail or vary their wording across repeated calls.

Check the explanation against the intended shipping meaning. A successful API call establishes access; answer quality needs a separate check.

<!--
Separate transport success from task success. In an earlier run, the small local model interpreted dwell time as a software-container concept; adding shipping context did not guarantee correctness either. Use actual output if demonstrating this, rather than promising a particular failure. We introduce the need to inspect answers without building an evaluation framework yet.
-->

---

# Proprietary and open-weight models

| Model access | What the developer receives |
| --- | --- |
| Proprietary model | Inference access through a provider's service |
| Open-weight model | Downloadable parameters under the model's licence |

Open weights can run locally or be hosted by another provider.

Available weights do not establish that training data, training code or every use is unrestricted.

<!--
This distinction concerns access and control, not a ranking of intelligence. Our examples use hosted OpenAI and a local SmolLM2 GGUF. Use open-weight precisely and inspect the applicable licence. Avoid equating downloadable weights with an entirely open training process.
-->

---

# Where inference runs

```text
Hosted: Python → provider API → model on provider hardware

Local:  Python → Ollama API   → model on this machine
```

Both paths send a request and receive generated text.

They differ in where computation happens, who operates the model and how that computation is paid for.

<!--
Keep model licensing separate from deployment location. Hosted APIs can serve open weights. Local deployment needs a suitable runtime and hardware. The OpenAI path requires network access and a configured key. The local model is downloaded first; subsequent inference uses the local Ollama service.
-->

---

# Choosing an access path

| Consideration | Hosted API | Local open weights |
| --- | --- | --- |
| Initial access | Account, key and model access | Runtime, download and hardware |
| Inference operation | Provider operates the service | You operate the runtime |
| Cost | Applicable API usage charges | Hardware and operating effort |
| Request processing | Provider service boundary | Local runtime boundary |

Choose a model and deployment that meet the task's quality and operating requirements.

<!--
Do not conclude that local inference is costless or that all local models are weaker. The 135M model is a small-download teaching choice, not the capability ceiling of open weights. Provider data handling depends on the agreement; local execution alone does not establish the security of an entire application.
-->

---

# A hosted model in Python

The request implements the application/model boundary we have described.

```python
load_dotenv()
question = "Briefly explain container dwell time in shipping."
response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPEN_AI_KEY"],
    messages=[{"role": "user", "content": question}],
)
print(response.choices[0].message.content)
```

Illustration: [complete hosted example](../snippets/b1/01_openai_call.py)

<!--
Run the complete file, which includes imports, matching generation settings and cost reporting. The excerpt isolates the request. The hosted and local examples use the same question, temperature and output limit; different model/runtime behavior can still produce different answers. Identify the model, input message and returned text after learners can name their roles. OPEN_AI_KEY is the configured variable. Model-reference comments are below the main operation in the complete file.
-->

---

# The response and the application

Generated text is one part of the response. Usage metadata can describe the tokens consumed.

The application extracts the reply and displays it in a terminal, page or chat interface.

A chatbot screen wraps this boundary. It does not add company knowledge to the model.

<!--
Return to the application diagram. A terminal establishes the feature; a UI can wrap the same call. Missing credentials, unavailable services and empty replies are application failures to handle, not evidence to replace with a canned success. Do not devote a separate slide to the response object's attribute path.
-->

---

# The local model and its runtime

**SmolLM2-135M-Instruct:** the selected open-weight model.

**GGUF:** the file format used by the selected distribution.

**Ollama:** loads and runs the model locally, exposing an API.

**LiteLLM:** provides our Python code with a common request/response interface across hosted and local examples.

<!--
Explain each layer before showing the local call. Download unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M through Ollama before class; the file is about 105 MB. Ollama must be running. No llama-cpp-python or Transformers installation is required by this script. Sources: https://huggingface.co/unsloth/SmolLM2-135M-Instruct-GGUF/tree/main ; https://docs.litellm.ai/docs/providers/ollama
-->

---

# A local model through the same interface

The selected `model` runs on this machine's Ollama service.

```python
response = completion(
    model=model,
    api_base="http://localhost:11434",
    messages=[{"role": "user", "content": question}],
    max_tokens=100,
    temperature=0,
)
```

Illustration: [complete local example](../snippets/b1/02_ollama_call.py)

<!--
The full file defines question as the same shipping question used in the hosted example. model is its full ollama_chat/hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M identifier. LiteLLM uses the native Ollama chat route; no separate LiteLLM proxy is needed. Ask what changed from the hosted path and what retained the same role. Generation settings are explained after instructions and messages.
-->

---

# Instructions shape requested behavior

The user asks about dwell time. The application wants a concise explanation suitable for a trainee.

An instruction such as “Answer in one short sentence” describes that desired behavior.

Changing it can change the presentation of an answer. It does not supply new operational facts or guarantee correctness.

<!--
Introduce instructions through a user-experience requirement, before showing role dictionaries. Ask learners to predict the effect of requesting three numbered points for the same question. Distinguish changing presentation from connecting data. Hold the question fixed during the demonstration.
-->

---

# Conversation roles

| Role in these examples | Meaning |
| --- | --- |
| `system` | Application-supplied behavioral instruction |
| `user` | A question or message from the user |
| `assistant` | An earlier generated model reply |

The provider or runtime formats the messages for its model.

<!--
Use these three roles rather than surveying every provider-specific role. Some APIs expose developer instructions and other item types. The chat UI and model transcript need not contain identical material. Messages ultimately become a formatted token sequence. Source: https://huggingface.co/docs/transformers/main/chat_templating
-->

---

# Instructions and question in one request

The roles express the distinction already established in words.

```python
messages=[
    {"role": "system", "content": "Answer in one short sentence."},
    {"role": "user", "content": question},
],
```

Illustration: [instruction example](../snippets/b1/03_system_instruction.py)

Keep the question fixed. Compare one sentence with three numbered points.

<!--
This is the messages argument inside the complete call. question is the same shipping question as the first call, so adding the system instruction is the change being illustrated. Ask for a prediction before running a variation. If the model ignores the form, inspect that limit. An instruction influences generation; it does not execute a validation rule or establish a private fact.
-->

---

# A follow-up depends on the conversation

First question:

> What is container dwell time?

Follow-up:

> How does that differ from detention?

“That” refers to the earlier topic. A fresh request containing only the follow-up does not establish that reference.

<!--
Ask what information makes the follow-up understandable. A model without history might guess the topic; do not promise failure. Guessing is different from receiving the earlier exchange. Both questions concern general terminology, not an internal record.
-->

---

# The application maintains history

In this stateless call pattern, each request contains the conversation the model should use now.

The application retains earlier user messages and actual assistant replies, then adds the new question.

This is conversation state supplied as input. It does not update the model's learned weights.

<!--
Distinguish displayed chat history, input history and training. Some APIs manage conversation state on the application's behalf; we use explicit message lists to expose the mechanism. Using the same model name does not independently restore an earlier conversation.
-->

---

# History in the next request

Retain the first call's actual reply before asking the follow-up.

```python
messages.append({
    "role": "assistant",
    "content": first.choices[0].message.content,
})
messages.append({
    "role": "user", "content": "How does that differ from detention?",
})
```

Illustration: [two-turn conversation](../snippets/b1/04_conversation_history.py)

<!--
Run the full file and inspect the printed second request. The original user message remains in messages; these appends add the actual assistant text and latest question. In the lab, keep only the final question and identify what context disappeared. Never replace an actual reply with a prepared successful one.
-->

---

# Tokens represent text

A tokenizer divides text into model-specific units and assigns vocabulary IDs.

A token may represent a word, part of a word, punctuation or other bytes. Character and word counts are not reliable token counts.

The model's request contains tokens for the formatted messages as well as their text.

<!--
Ask learners to predict counts for container, a shipping phrase and MSKU1234567 before encoding. Avoid a universal tokens-per-word rule. IDs belong to a particular vocabulary. The following illustration uses the hosted model's tokenizer, not SmolLM2's.
-->

---

# Text and token IDs

Encoding exposes the tokenizer's units; decoding reconstructs the text.

```python
encoder = tiktoken.encoding_for_model("gpt-4.1-mini")
text = "Container dwell time at a port."
token_ids = encoder.encode(text)
print(token_ids)
print(encoder.decode(token_ids))
```

Illustration: [tokenizer example](../snippets/b1/05_text_to_token_ids.py)

<!--
The full file compares text, counts, IDs and decoded text for three samples; this frame selects one phrase. This executes a tokenizer, not a generation call. Run once online before class to cache vocabulary data. Token-byte inspection is an optional exploration in the snippet guide. Actual response usage is preferable to visible word counts for measuring requests.
-->

---

# The generation pipeline

```text
Formatted input → token IDs → token embedding vectors
                                     ↓
                          transformer layers
                                     ↓
                    scores over vocabulary tokens
                                     ↓
                           next token selection
```

Token IDs index the vocabulary. Embedding vectors are numerical representations used inside the model.

<!--
Keep this to a short conceptual bridge, not a tensor exercise. There is no separate vector-ID stage. An embedding lookup maps IDs to learned vectors; model layers produce context-dependent representations, and an output head produces vocabulary scores. Internal token embeddings differ from document/query embeddings used later for retrieval.
-->

---

# Generation continues one token at a time

The selected token joins the sequence. The model predicts another token using the extended context.

Generation stops at a stopping condition or the configured limit.

The tokenizer decodes generated IDs into readable text. Longer answers generally require more generation work.

<!--
Connect the mechanism to an observable consequence. The next unit is a token, not necessarily a word. Implementations may cache intermediate computation; do not imply every token recomputes the entire prompt from scratch. Source: https://huggingface.co/docs/transformers/v4.48.2/llm_tutorial
-->

---

# Variability and output length

Repeated requests can produce different wording.

Where supported, **temperature** changes how randomly the next token is selected. Lower temperature guarantees neither correctness nor identical results.

An **output-token limit** bounds generation length. Reaching the limit can leave an answer unfinished.

<!--
Now that token selection is understood, return to temperature=0 and max_tokens=100 in the local call. These settings solve different problems. A fluent short answer can be false. Parameter support and names vary across providers/models. Reasoning-model output budgets may include tokens the user never sees; return to this when discussing cost.
-->

---

# The context window is a bounded budget

Instructions, retained history and the current question consume input capacity.

Generation also needs room within the model's supported limits. Input, output and reasoning limits depend on the model/API.

A conversation cannot grow indefinitely. The application must eventually choose what context to retain.

<!--
Do not equate maximum output length with full context-window size. Explain the constraint before introducing trimming. Later work can implement trimming and summarisation; neither creates unlimited memory or changes trained weights.
-->

---

# History grows the input to later calls

```text
Turn 1: instruction + question 1
Turn 2: instruction + question 1 + reply 1 + question 2
Turn 3: instruction + earlier exchanges + question 3
```

Keeping more history usually increases later input counts.

Total session input is the sum across requests, not just the final request's size.

<!--
This is a schematic, not measured tokenizer output. Distinguish one request's context budget from the accumulated processing across a session. Prompt caching can change billing for repeated prefixes; history still remains in the logical request. Next inspect actual reported usage.
-->

---

# Lab extension · Usage across a conversation

The loop retains actual replies and reports each request separately.

```python
messages.append({"role": "user", "content": question})
response = completion(model=model, messages=messages,
                      api_base="http://localhost:11434", max_tokens=64)
reply = response.choices[0].message.content
messages.append({"role": "assistant", "content": reply})
print("Input tokens:", response.usage.prompt_tokens)
```

Lab extension: [context-growth example](../snippets/b1/extensions/01_context_growth.py)

<!--
This is an optional lab illustration, not a seventh core lecture snippet. The shortened excerpt shows one iteration of the full file's actual local conversation. The preceding conceptual slide is sufficient for the lecture's history-growth explanation. Inspect usage separately from answer quality and never present prepared counts as live measurements.
-->

---

# Token usage and API cost

For a simple uncached text request:

```text
Estimated cost = input tokens × input rate
               + output tokens × output rate
```

Use matching units for counts and rates. Cached input and reasoning tokens may have additional billing rules.

Local inference has no provider per-call charge in our setup; hardware and electricity still cost money.

<!--
Explain per-token versus per-million-token rates; divide counts by one million when using the latter. The script uses LiteLLM pricing data to estimate USD cost, not an invoice. Reasoning can be billable output even when absent from displayed text. Avoid dated price tables to memorise. Source: https://docs.litellm.ai/docs/completion/token_usage
-->

---

# Response time has several causes

A measured call can include network time, queueing, input processing and output generation.

A local first call may also include model loading. A later warm call can behave differently.

Compare repeated runs on the same task. Model size or one fast reply does not establish the best application choice.

<!--
Our metric is wall-clock time around a non-streaming completion, not separately time to first token or generation speed. Separate loading and warm inference. Output length, hardware, runtime, caching and service conditions all affect comparisons; model tokenizers and reasoning behavior may differ as well.
-->

---

# Measuring an actual call

Timing and pricing make the operating questions observable.

```python
started = perf_counter()
response = completion(model=model, messages=messages,
                      api_key=os.environ["OPEN_AI_KEY"])
elapsed = perf_counter() - started
cost_usd = completion_cost(completion_response=response, model=model)
print("Seconds:", elapsed, "Usage:", response.usage)
print(f"Estimated cost (USD): ${cost_usd:.8f}")
```

Illustration: [same-task model comparison](../snippets/b1/06_compare_models.py)

<!--
The full file sends the same shipping-definition question to both models and prints actual answers. This is a shortened measurement block. Check explanation quality first. Cheaper token rates can still lead to a more expensive request if a model generates more billable tokens. Repeated measurements are needed for an application decision.
-->

---

# Choosing a model for the feature

Keep the question and expected answer requirements fixed.

Check that each explanation is correct and useful. Then compare elapsed time and estimated total request cost across repeated runs.

Choose a sufficient model for the task. A tiny local model demonstrates deployment mechanics without establishing suitable answer quality.

<!--
Treat the classroom comparison as a small experiment, not a leaderboard. Ask why token price alone cannot decide request cost. Keep model/provider choices separate from SDK/interface choices. Several terminology questions could improve the experiment later; a full evaluation suite belongs elsewhere.
-->

---

# The boundary of this chatbot

The application explains general terminology and maintains a conversation about it.

Now a user asks:

> What is C1's current recorded status?

That answer needs an operational source. Model knowledge and chat history do not establish the current record.

<!--
This opens B2 rather than prompting a record-pasting exercise inside B1. Ask where the answer must come from. B2 adds an application capability to obtain the fact. Internal document retrieval is a separate later extension. A guessed status must not be presented as a recorded value.
-->

---

# Lab · A shipping-terminology chatbot

| Time | Extend the understood application |
| --- | --- |
| 0–5 min | Confirm the prepared environment and local model |
| 5–20 min | Run hosted/local calls; change question and instruction |
| 20–35 min | Add a follow-up; compare with and without history |
| 35–50 min | Record tokens, elapsed time and estimated API cost |
| 50–60 min | Compare answers and explain one quality/cost trade-off |

Use the [B1 snippets and setup](../snippets/b1/README.md).

<!--
This is the separate one-hour lab. Prepare credentials, dependencies, Ollama and downloads beforehand. Deliverable: a working conversation and a small table of actual observations. Record unavailable service access as a failure, never fake success. Record grounding, JSON schemas and permissions are outside the required B1 lab.
-->

---

# B1 · What the application now does

It calls a hosted or local model, provides instructions and retains conversation history.

We can inspect how text becomes tokens and how requests consume time and resources.

**Explain:** why does a useful dwell-time definition give us no evidence about C1's current status?

<!--
Ask for a causal explanation, not a glossary recital. Learners should distinguish learned knowledge, request context and access to current records. B2 starts with the capability the application must add. B1 has connected no tools or internal documents.
-->
