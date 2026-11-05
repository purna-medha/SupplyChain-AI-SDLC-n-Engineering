"""Combine dense and keyword retrieval using LlamaIndex's fusion class.

Try: compare the three rankings for a gate question and a reefer question.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings, SimpleKeywordTableIndex, VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever
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
dense = VectorStoreIndex(nodes, embed_model=embed).as_retriever(similarity_top_k=2)
keyword = SimpleKeywordTableIndex(nodes, llm=llm).as_retriever(retriever_mode="simple")
hybrid = QueryFusionRetriever(
    retrievers=[dense, keyword],
    llm=llm,
    mode="reciprocal_rerank",
    num_queries=1,
    similarity_top_k=2,
    use_async=False,
)
for name, retriever in [("dense", dense), ("keyword", keyword), ("hybrid", hybrid)]:
    print(
        name,
        [(hit.node.node_id, hit.score) for hit in retriever.retrieve("reefer desk")],
    )
