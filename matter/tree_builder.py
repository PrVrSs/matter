from collections import deque
from typing import List

from pampy import match, _


__all__ = (
    'RuleNode',
    'build_sentence',
)


class RuleNode:

    __slots__ = ('_name', '_children')

    def __init__(self, name: str):
        self._name: str = name
        self._children: list = []

    @property
    def children(self) -> List['RuleNode']:
        return self._children

    @children.setter
    def children(self, list_child: List['RuleNode']):
        self._children = list_child

    def append_child(self, child: 'RuleNode') -> None:
        self._children.append(child)

    @property
    def name(self) -> str:
        return self._name

    def is_leaf(self) -> bool:
        return not self.children


class Tree:

    def __init__(self, root: RuleNode):
        self.root: RuleNode = root

    def walk(self):
        queue = deque((self.root,))

        while queue:
            node = queue.popleft()

            if node.is_leaf():
                yield node.name

            queue.extendleft(reversed(node.children))


CONST_FOR_REPLACE = {
    '.': '\x39', 'A-Z_$0-9': 'AZ_$9', 'A-Z_$': 'AZ_$',
    '0-9A-F': '9F', '0-9': '99', '01': '01', 'A-Z0-9._$': 'AZ9.', 'SEMI': ';'
}


def build_tree(parser, start_rule) -> Tree:
    tree = Tree(root=RuleNode(start_rule))
    queue = deque((tree.root,))

    while queue:
        node = queue.popleft()

        node.children = [
            RuleNode(rule) for rule in parser.get_sub_rule_list(node.name)
        ]

        queue.extend(pass_node(node.children))

    return tree


def replace_as(expr):
    return match(
        expr,
        'SEMI', ';',
        _, expr
    )


def build_sentence(parser, start_rule):
    tree = build_tree(parser, start_rule)

    for leaf in tree.walk():
        yield replace_as(leaf.strip('\''))


def pass_node(nodes):
    return [
        node for node in nodes
        if (
            node.name != 'EOF' and
            node.name != '0-9' and
            node.name != 'SEMI' and
            node.name != 'A-Za-z' and
            node.name != '0-9A-F' and
            node.name != 'A-Z_$' and
            (node.name[-1] != '\'' and node.name[0] != '\'')
        )
    ]
