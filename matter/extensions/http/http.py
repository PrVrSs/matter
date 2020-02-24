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


target = Path(__file__).parent / 'http.g4'


@final
class HTTP(BaseExtension):

    __implements__ = Network
    __mutations_alg__ = HTTPAlgorithm
    __mutations_scheme__ = HTTPMutation
    __files__ = str(target.resolve()),

    def __init__(self, config):
        super().__init__()
        self._config = config


def matte_extension():
    return HTTP
