from typing import NamedTuple, final
from pathlib import Path

from matter.extensions.extansion import BaseExtension


class Network:
    pass


class Characteristic(NamedTuple):
    min_len: int = 1
    max_len: int = 2
    regexp: str = ''


class HTTPMutation:
    HEXDIG = Characteristic()


class HTTPAlgorithm:
    pass


HTTP_GRAMMAR = (Path(__file__).parent / 'http.g4').resolve()


@final
class HTTP(BaseExtension):

    __implements__ = Network  # type: ignore
    __mutations_alg__ = HTTPAlgorithm  # type: ignore
    __mutations_scheme__ = HTTPMutation  # type: ignore
    __files__ = (str(HTTP_GRAMMAR),)  # type: ignore

    def __init__(self, config):
        super().__init__()
        self._config = config


def matte_extension():
    return HTTP
