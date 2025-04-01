import asyncio
from functools import partial, wraps
from typing import Any, Callable, Optional


def async_wrap(func: Callable[..., Any]):
    @wraps(func)
    async def run(*args: Any, loop: Optional[asyncio.events.AbstractEventLoop] = None, executor: Optional[Any] =None, **kwargs: Any):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run
