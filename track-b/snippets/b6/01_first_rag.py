"""Build a complete small RAG answer, then inspect its returned sources.

Try: ask about crane capacity, which is absent from the synthetic notes.
"""

import os
from dotenv import load_dotenv
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from llama_index.llms.openai_like import OpenAILike

load_dotenv()
Settings.tokenizer = str.split  # Classroom budget counts words, not model tokens.
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
documents = [
    Document(text="Terminal A gate opens at 06:00.", metadata={"source": "gate-a"}),
    Document(
        text="Terminal A reefer desk is beside gate 2.", metadata={"source": "reefer-a"}
    ),
]
index = VectorStoreIndex.from_documents(documents, embed_model=embed)
engine = index.as_query_engine(llm=llm, similarity_top_k=2)
response = engine.query(
    "When does Terminal A open? Use only notes; report absent evidence."
)
print("Answer:", response)
for hit in response.source_nodes:
    print("Source:", hit.node.metadata, hit.node.text)
