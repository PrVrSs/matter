import asyncio
from functools import wraps
from itertools import chain


def flatmap(function, iterable):
    return chain.from_iterable(map(function, iterable))


async def anext(__obj__):
    return await __obj__.anext()


def async_click(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import uvloop  # pylint: disable=import-outside-toplevel
        uvloop.install()
        return asyncio.run(func(*args, **kwargs), debug=True)

    return wrapper
