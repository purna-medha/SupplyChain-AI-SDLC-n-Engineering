"""Inspect the chunks and source metadata created by SentenceSplitter.

Try: change chunk_size from 40 to 14 and inspect the Sunday exception.
"""

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

document = Document(
    text="Terminal A gate opens at 06:00. On Sunday it opens at 09:00. Bring ID.",
    metadata={"source": "gate-a", "terminal": "A"},
)
splitter = SentenceSplitter(chunk_size=40, chunk_overlap=0, tokenizer=str.split)
nodes = splitter.get_nodes_from_documents([document])
for node in nodes:
    print("Chunk:", node.text)
    print("Metadata:", node.metadata)
