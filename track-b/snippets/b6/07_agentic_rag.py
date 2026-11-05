"""Make a query engine available as a retrieval tool in a bounded agent.

Try: ask about crane capacity and inspect actual tool observations and sources.
"""

import asyncio
import os
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.core.agent.workflow import FunctionAgent, ToolCallResult
from llama_index.core.tools import QueryEngineTool
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
    is_function_calling_model=True,
)
nodes = [
    TextNode(id_="gate-a", text="Terminal A gate opens at 06:00."),
    TextNode(id_="reefer-a", text="Terminal A reefer desk is beside gate 2."),
]
engine = VectorStoreIndex(nodes, embed_model=embed).as_query_engine(llm=llm)
tool = QueryEngineTool.from_defaults(
    query_engine=engine,
    name="terminal_notes",
    description="Search synthetic Terminal A notes.",
)
agent = FunctionAgent(
    tools=[tool],
    llm=llm,
    streaming=False,
    timeout=90,
    system_prompt="Use notes for facts. Report missing evidence.",
)


async def main():
    handler = agent.run(user_msg="When does Terminal A open?", max_iterations=3)
    async for event in handler.stream_events():
        if isinstance(event, ToolCallResult):
            print("Tool:", event.tool_name, event.tool_kwargs)
            print("Observation:", event.tool_output.content)
            for hit in getattr(event.tool_output.raw_output, "source_nodes", []):
                print("Source:", hit.node.node_id, hit.node.text)
    print("Answer:", await handler)


asyncio.run(main())
