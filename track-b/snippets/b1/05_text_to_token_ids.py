"""Inspect real tokenizer output: text -> token IDs -> decoded text.

Try: change container to reefer or add punctuation. Compare the token counts.
This calls a tokenizer locally; it does not generate an LLM reply.
"""

import tiktoken

# Use the hosted model's tokenizer; these IDs are not SmolLM2's vocabulary.
encoder = tiktoken.encoding_for_model("gpt-4.1-mini")

for text in ["container", "Container dwell time at a port.", "MSKU1234567"]:
    token_ids = encoder.encode(text)
    print("\nText:", text)
    print("Characters:", len(text), "Tokens:", len(token_ids))
    print("Token IDs:", token_ids)
    print("Decoded text:", encoder.decode(token_ids))

# IDs index a vocabulary. They are not vectors or semantic similarity scores.
# Inside the model: IDs -> embeddings -> transformer -> vocabulary scores
# -> next token ID. Generation repeats; decoding converts the IDs back to text.
