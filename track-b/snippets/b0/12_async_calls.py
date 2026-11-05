"""Await an async operation in a script. Try: call the lookup for C9."""

import asyncio


async def get_status(container_id: str) -> str:
    await asyncio.sleep(0)  # Yield to the event loop; this is not a network call.
    records = {"C1": "delayed", "C2": "on_time"}
    return records.get(container_id, "unknown")


async def main():
    status = await get_status("C1")
    print("Awaited observation:", status)


if __name__ == "__main__":
    asyncio.run(main())

