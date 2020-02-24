import abc
from enum import Enum
from typing import Any, Iterator, Dict, List


class AbcExpression(metaclass=abc.ABCMeta):
    """Abstract Expression"""
    type: str = None
    value: Any = None

    @abc.abstractmethod
    def accept(self, visitor): ...


class ParserType(Enum):
    ANTLR4 = 'antlr4'
    BISON = 'bison'

    @classmethod
    def _missing_(cls, _: str) -> 'ParserType':
        return ParserType.ANTLR4


class AbcParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add_rule_from_file(
            self, *args: Any, **kwargs: Any) -> Dict[str, List[AbcExpression]]:
        """"""

    def get_sub_rule_list(
            self, *args: Any, **kwargs: Any) -> Iterator[AbcExpression]:
        """"""""
