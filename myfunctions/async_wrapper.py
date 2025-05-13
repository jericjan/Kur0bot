import asyncio
from functools import partial, wraps
from typing import Any, Callable, Coroutine, Optional, ParamSpec, TypeVar

# To represent the parameters of the wrapped function
P = ParamSpec("P")
# To represent the return type of the wrapped function
R = TypeVar("R")


def async_wrap(func: Callable[P, R]) -> Callable[P, Coroutine[Any, Any, R]]:
    @wraps(func)
    async def run(*args: Any, loop: Optional[asyncio.events.AbstractEventLoop] = None, executor: Optional[Any] =None, **kwargs: Any):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run
