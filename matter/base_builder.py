from .compiler import AbcParser, setup_parser
from .tree_builder import build_sentence


async def create_builder(files):
    return await BaseBuilder().setup_parser(files)


class BaseBuilder:
    def __init__(self):
        self._parser: AbcParser = setup_parser('antlr4')

    async def setup_parser(self, files):
        await self._parser.add_rule_from_file(files=files)

        return self

    def build_sentence(self, start_rule: str = 'root'):
        return build_sentence(self._parser, start_rule)
