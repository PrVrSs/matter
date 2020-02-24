import re
from typing import List, Dict, AsyncIterator, Tuple, Iterator

import aiofiles

from .ast import Ast
from .parser import Parser
from .scanner import Scanner
from .token import Token
from .interfaces import AbcParser, ParserType, AbcExpression


class Antlr4ParserFacade(AbcParser):

    __slots__ = '_rule_dictionary', '_file_structure'

    _rule_pattern = re.compile(r'(?P<rule>\w*\n?\s*):(?P<body>[^\n][^;]*)')

    def __init__(self):
        self._rule_dictionary:  Dict[str, List[AbcExpression]] = {}
        # need fix for support:  "SEMI: ';'; "

    async def add_rule_from_file(
            self, files: str) -> Dict[str, List[AbcExpression]]:
        for file in files:
            async for rule in self._read_grammar(file):
                self._rule_dictionary[self._sanitize_rule(rule[0])] = (
                    self._parse_rule(rule[1]))

        return self._rule_dictionary

    def get_sub_rule_list(
            self,
            rule_name: str,
            multiplication_scale: int = 1,
            random_scale: int = 2,
    ) -> Iterator[AbcExpression]:
        return Ast(
            self._rule_dictionary[rule_name],
            multiplication_scale,
            random_scale,
        )

    async def _read_grammar(self, file: str) -> AsyncIterator[Tuple[str, str]]:
        async with aiofiles.open(file, mode='r') as grammar_file:
            data = await grammar_file.read()

            for rule in self._rule_pattern.findall(data):
                yield rule

    @staticmethod
    def _parse_rule(rule) -> List[AbcExpression]:
        tokens: List[Token] = Scanner(rule).scan_tokens()

        return Parser(tokens).parse()

    @staticmethod
    def _sanitize_rule(rule: str) -> str:
        return (
            rule
            .replace('\n', '')
            .replace('  ', '')
            .rstrip()
        )


def setup_parser(parser_type: str) -> AbcParser:
    parser_factory = {
        ParserType.ANTLR4: lambda: Antlr4ParserFacade()
    }

    return parser_factory[ParserType(parser_type)]()

