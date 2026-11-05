"""B2 starter: answer a container enquiry using actual application reads."""

import argparse
import asyncio

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStreamableHttp

from records import DEFAULT_CONTAINER, MCP_PORT, SOURCE, get_container, get_demurrage
from support import configure_sdk, run_cli

INSTRUCTION = (
    "You are a container help desk assistant. Use tools for recorded status and "
    "fees. Unknown means unavailable in this source, not a known status or zero fee. "
    "Preserve the identifier, status, amount, currency and source. General shipping "
    "definitions need no operational lookup. Do not invent facts or take actions."
)


def read_status(container_id: str) -> dict:
    """Read a recorded container status; unknown identifiers have no status."""
    # TODO B2.1: get_container(container_id); return its status or "unknown".
    # Return {"container_id": ..., "status": ..., "source": SOURCE}.
    raise NotImplementedError("TODO B2.1: implement read_status")


def read_fee(container_id: str) -> dict:
    """Read net payable demurrage in USD; absence is not a zero fee."""
    # TODO B2.2: get_demurrage(container_id); use net_payable_demurrage_fee_usd.
    # Return {"container_id": ..., "net_usd": amount or None, "source": SOURCE}.
    raise NotImplementedError("TODO B2.2: implement read_fee")


def make_agent() -> Agent:
    """B2.3: register both reads as tools on one help desk agent."""
    # TODO: Agent(name=..., model="gpt-4.1-mini", instructions=INSTRUCTION, tools=...).
    # Wrap each read with function_tool(..., failure_error_function=None).
    # That setting keeps unfinished TODOs visible instead of turning them into model observations.
    raise NotImplementedError("TODO B2.3: implement make_agent")


def make_mcp_agent(server) -> Agent:
    """B2.4: use the same instructions, but discover tools from this MCP server."""
    # TODO: construct Agent with mcp_servers=[server], without local tools.
    raise NotImplementedError("TODO B2.4: implement make_mcp_agent")


# Supplied runners: the learner selects local tools or the remote capability.
async def run_mcp(question, url):
    errors = []

    def observe_result(context):
        # MCP tool failures are results; retain them so they cannot look like a completed lab.
        if context.is_error:
            errors.append(context.tool_name)

    async with MCPServerStreamableHttp(
        name="Container help desk", params={"url": url},
        custom_data_extractor=observe_result, failure_error_function=None,
    ) as server:
        print("DISCOVERED:", [tool.name for tool in await server.list_tools()])
        agent = make_mcp_agent(server)
        configure_sdk()
        result = await Runner.run(agent, question, max_turns=6)
        if errors:
            raise RuntimeError(f"MCP reads failed: {errors}. Inspect the server's TODO/error output and rerun.")
        print("ANSWER:", result.final_output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", choices=["direct", "agent", "mcp"])
    parser.add_argument("--container", default=DEFAULT_CONTAINER)
    parser.add_argument("--question")
    parser.add_argument("--mcp-url", default=f"http://127.0.0.1:{MCP_PORT}/mcp")
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    if args.checkpoint == "direct":
        print("STATUS:", read_status(args.container))
        print("FEE:", read_fee(args.container))
        return
    question = args.question or f"What are {args.container}'s recorded status and net demurrage in USD?"
    if args.checkpoint == "mcp":
        asyncio.run(run_mcp(question, args.mcp_url))
    else:
        agent = make_agent()
        configure_sdk()
        result = Runner.run_sync(agent, question, max_turns=6)
        print("ANSWER:", result.final_output)


if __name__ == "__main__":
    run_cli(main)

