import abc
from enum import Enum
from typing import Any, Iterator, Dict, List


class AbcExpression(metaclass=abc.ABCMeta):
    """Abstract Expression"""
    type: str = ''
    value: Any = None

    @abc.abstractmethod
    def accept(self, visitor):
        ...


class ParserType(Enum):
    ANTLR4 = 'antlr4'
    BISON = 'bison'

    @classmethod
    def _missing_(cls, _: Any) -> 'ParserType':
        return ParserType.ANTLR4


class AbcParser(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add_rule_from_file(
            self,
            files: str,
    ) -> Dict[str, List[AbcExpression]]:
        """"""

    def get_sub_rule_list(
            self,
            rule_name: str,
            multiplication_scale: int,
            random_scale: int,
    ) -> Iterator[AbcExpression]:
        """"""""
