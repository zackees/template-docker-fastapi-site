import asyncio
import time
import traceback
import warnings
from typing import Awaitable, TypeVar

from mediabiasscorer.memory_cache import SharedMemoryData, create_shared_memory

SHARED_MEMORY = create_shared_memory(owner=True)

event_loop = asyncio.new_event_loop()
T = TypeVar("T")


def sync_await(coro: Awaitable[T]) -> T:
    return event_loop.run_until_complete(coro)


def store_shared_memory(shared_memory_data: SharedMemoryData) -> None:
    SHARED_MEMORY["shared"] = shared_memory_data


def update() -> None:
    shared_data: SharedMemoryData = SharedMemoryData(initialized=True)
    store_shared_memory(shared_data)


def main() -> None:
    update()
    try:
        while True:
            try:
                update()
            except Exception as e:  # pylint: disable=broad-except
                stack_trace_str = "".join(traceback.format_tb(e.__traceback__))
                warnings.warn(
                    f"Failed to update: {e}.\n Stack Trace:\n{stack_trace_str}"
                )
            time.sleep(60)
    except KeyboardInterrupt:
        time.sleep(5)  # give time for the server to shutdown
        print("Exiting.")


if __name__ == "__main__":
    main()
