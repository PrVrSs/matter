import asyncio
import logging
import logging.config
from functools import wraps
from itertools import chain

import uvloop

from .config import LOGGING_CONFIG


def flatmap(function, *iterable):
    return chain.from_iterable(map(function, iterable))


def set_logging(level):
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger('matte.error')


async def anext(__obj__):
    return await __obj__.anext()


def async_click(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uvloop.install()
        return asyncio.run(func(*args, **kwargs), debug=True)

    return wrapper
