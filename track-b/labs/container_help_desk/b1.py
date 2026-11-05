"""B1 starter: help a new operations colleague understand shipping terms.

Implement only the three TODO functions. Run with --help for checkpoints.
"""

import argparse
import os
from time import perf_counter

from litellm import completion, completion_cost

from support import run_cli

HOSTED_MODEL = "openai/gpt-4.1-mini"
LOCAL_MODEL = "ollama_chat/hf.co/unsloth/SmolLM2-135M-Instruct-GGUF:Q4_K_M"
INSTRUCTION = (
    "You help a new port operations colleague. Explain shipping terminology in "
    "two short sentences. You have no access to current container records. "
    "If asked for an operational status, explain that a connected source is needed."
)


def ask_model(messages: list[dict], model: str):
    """B1.1: return the full LiteLLM response, not just its generated text."""
    # TODO: call completion with model, messages, max_tokens=160, temperature=0.
    # Hosted: api_key=os.environ["OPEN_AI_KEY"]. Local: api_base="http://localhost:11434".
    raise NotImplementedError("TODO B1.1: implement ask_model")


def make_messages(question: str, instruction: str) -> list[dict]:
    """B1.2: put the supplied instruction and question in their message roles."""
    # TODO: return a system message followed by a user message.
    raise NotImplementedError("TODO B1.2: implement make_messages")


def add_follow_up(messages: list[dict], reply: str, question: str) -> list[dict]:
    """B1.3: retain the actual assistant reply before the new user question."""
    # TODO: return the history plus an assistant message and a user message.
    raise NotImplementedError("TODO B1.3: implement add_follow_up")


# Supplied runner: measurements and presentation, not an implementation answer.
def show_call(messages, model):
    started = perf_counter()
    response = ask_model(messages, model)
    elapsed = perf_counter() - started
    reply = response.choices[0].message.content
    if not reply:
        raise ValueError("The model returned no text; this checkpoint has no usable reply.")
    print("REPLY:", reply)
    print("Seconds:", round(elapsed, 3))
    print("Tokens in/out:", response.usage.prompt_tokens, response.usage.completion_tokens)
    if model.startswith("ollama_chat/"):
        print("Provider API charge: USD 0; hardware and operation still have a cost.")
    else:
        estimate = completion_cost(completion_response=response, model=model)
        print("Estimated USD:", f"{estimate:.8f}" if estimate is not None else "unavailable")
    return reply


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", choices=["call", "instruction", "history", "compare"])
    parser.add_argument("--question", default="What is container dwell time in shipping?")
    parser.add_argument("--follow-up", default="How does that differ from detention?")
    parser.add_argument("--model", default=HOSTED_MODEL)
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    messages = [{"role": "user", "content": args.question}]
    if args.checkpoint in {"instruction", "history"}:
        messages = make_messages(args.question, INSTRUCTION)
    if args.checkpoint == "compare":
        for model in [HOSTED_MODEL, LOCAL_MODEL]:
            print("\nMODEL:", model)
            show_call(messages, model)
        return
    reply = show_call(messages, args.model)
    if args.checkpoint == "history":
        messages = add_follow_up(messages, reply, args.follow_up)
        print("SECOND REQUEST:", messages)
        show_call(messages, args.model)


if __name__ == "__main__":
    run_cli(main)

