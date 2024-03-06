"""
Event loop that allows us to test async function calls synchronously.
"""

import asyncio
from typing import Awaitable, TypeVar

event_loop = asyncio.new_event_loop()

T = TypeVar("T")


def sync_await(coro: Awaitable[T]) -> T:
    return event_loop.run_until_complete(coro)
