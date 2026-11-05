"""Ask the chat model to rewrite a query, then compare actual retrieval.

Try: change the question and check that subject and intent survive rewriting.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from llama_index.llms.openai_like import OpenAILike

load_dotenv()
Settings.tokenizer = str.split
embed = OpenAILikeEmbedding(
    model_name="text-embedding-3-small",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
llm = OpenAILike(
    model="gpt-4.1-mini",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    is_chat_model=True,
)
nodes = [
    TextNode(id_="gate-a", text="Terminal A gate opens at 06:00."),
    TextNode(id_="gate-b", text="Terminal B gate opens at 08:00."),
    TextNode(id_="reefer-a", text="Terminal A reefer desk is beside gate 2."),
]
retriever = VectorStoreIndex(nodes, embed_model=embed).as_retriever(similarity_top_k=1)
question = "For Terminal A, when can I get in through the gate?"
rewrite = llm.complete(
    "Return only a search query; preserve terminal and intent: " + question
).text
print("Original:", question, "Rewrite:", rewrite)
for query in [question, rewrite]:
    print(query, [(hit.node.node_id, hit.score) for hit in retriever.retrieve(query)])
