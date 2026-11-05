"""Inspect embeddings, ranked nodes and metadata before any answer generation.

Try: change top-k or trusted_terminal and inspect the actual returned evidence.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
from llama_index.embeddings.openai_like import OpenAILikeEmbedding

load_dotenv()
Settings.tokenizer = str.split
embed = OpenAILikeEmbedding(
    model_name="text-embedding-3-small",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
nodes = [
    TextNode(
        id_="gate-a", text="Terminal A opens at 06:00.", metadata={"terminal": "A"}
    ),
    TextNode(
        id_="gate-b", text="Terminal B opens at 08:00.", metadata={"terminal": "B"}
    ),
    TextNode(
        id_="reefer-a",
        text="Terminal A reefer desk is beside gate 2.",
        metadata={"terminal": "A"},
    ),
]
question = "When does the gate open?"
print("Query vector dimensions:", len(embed.get_query_embedding(question)))
index = VectorStoreIndex(nodes, embed_model=embed)
trusted_terminal = "A"  # Application scope fixture, not a model decision.
filters = MetadataFilters(
    filters=[MetadataFilter(key="terminal", value=trusted_terminal)]
)
retriever = index.as_retriever(similarity_top_k=2, filters=filters)
for hit in retriever.retrieve(question):
    print(hit.node.node_id, hit.score, hit.node.metadata, hit.node.text)
