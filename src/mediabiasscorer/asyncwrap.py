"""Async related tools"""

import asyncio
import atexit
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar("T")

DEFAULT_EXECUTOR = ThreadPoolExecutor(max_workers=12)


def asyncwrap(func: Callable[..., T]) -> Callable[..., Awaitable[T]]:
    """Wrap a function to run in an async loop"""

    @wraps(func)
    async def run(
        *args,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        executor: Optional[ThreadPoolExecutor] = None,
        **kwargs,
    ) -> T:  # pylint: disable=unused-argument
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        executor = executor or DEFAULT_EXECUTOR
        return await loop.run_in_executor(executor, pfunc)

    return run


@atexit.register
def close_executor():
    """Waits until the executor is closed"""
    DEFAULT_EXECUTOR.shutdown(wait=True)
