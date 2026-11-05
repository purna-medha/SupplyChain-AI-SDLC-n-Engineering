"""Retrieve a candidate pool, then rerank it with LlamaIndex's LLMRerank.

Try: remove gate-a from the pool and explain the limit of reranking.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.postprocessor import LLMRerank
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
question = "When does Terminal A gate open?"
retriever = VectorStoreIndex(nodes, embed_model=embed).as_retriever(similarity_top_k=3)
candidates = retriever.retrieve(question)
print("Before:", [hit.node.node_id for hit in candidates])
reranker = LLMRerank(llm=llm, top_n=1)
reranked = reranker.postprocess_nodes(candidates, query_str=question)
for hit in reranked:
    print("After:", hit.node.node_id, hit.score, hit.node.text)
