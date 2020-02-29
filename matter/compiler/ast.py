"""Antlr4 AST"""
import copy
import random
from typing import (
    List,
    Optional,
)

from .expressions import Literal, AbcExpression, Choice


class Ast:
    """Antlr4 Ast"""

    tree: List[AbcExpression]
    _multiplication_scale: int
    _random_scale: int
    _default_min_zero: int
    _default_min_one: int
    _default_min_or: int
    _default_max_or: int

    def __new__(
            cls,
            tree_: Optional[List[AbcExpression]] = None,
            multiplication_scale: int = 1,
            random_scale: int = 1,
    ):
        self = super().__new__(cls)

        self.tree = tree_ or []
        self._multiplication_scale = multiplication_scale
        self._random_scale = random_scale
        self._default_min_zero = 0
        self._default_min_one = 1
        self._default_min_or = 0
        self._default_max_or = 4

        return self._create_ast()

    def visit_star_multiplication_grouping(
            self, expr: AbcExpression) -> List[AbcExpression]:
        return self._unpacking_multiplication_grouping(
            expr=expr,
            min_=self._default_min_zero,
            max_=self._multiplication_scale,
        )

    def visit_random_grouping(self, expr: AbcExpression) -> List[AbcExpression]:
        return self._unpacking_random(expr=expr)

    def visit_grouping(self, expr: AbcExpression) -> List[AbcExpression]:
        return self._unpacking_multiplication_grouping(
            expr=expr,
            min_=self._default_min_one,
            max_=self._default_min_one,
        )

    def visit_plus_multiplication_grouping(
            self, expr: AbcExpression) -> List[AbcExpression]:
        return self._unpacking_multiplication_grouping(
            expr=expr,
            min_=self._default_min_one,
            max_=self._multiplication_scale,
        )

    def visit_equal(self, expr: AbcExpression):
        return expr.value.accept(self)

    def visit_choice(self, expr: Choice):
        return self._do_choice(expr.left, expr.right)

    def visit_random_literal(self, expr: AbcExpression):
        return self._unpacking_random(expr)

    def visit_star_multiplication(self, expr: AbcExpression):
        return self._unpacking_multiplication(
            expr,
            min_=self._default_min_zero,
            max_=self._multiplication_scale,
        )

    def visit_plus_multiplication(self, expr: AbcExpression):
        return self._unpacking_multiplication(
            expr,
            min_=self._default_min_one,
            max_=self._multiplication_scale,
        )

    @staticmethod
    def visit_tilde(_: AbcExpression) -> AbcExpression:
        return Literal(value='\x33')  # type: ignore

    @staticmethod
    def visit_literal(expr) -> AbcExpression:
        return expr

    def _create_ast(self):
        new_tree: List[AbcExpression] = copy.copy(self.tree)

        while True:
            for expr in self.tree:
                value = expr.accept(self)

                if expr.type != 'Literal' and not isinstance(value, list):
                    value = [value]

                if isinstance(value, list):
                    index = new_tree.index(expr)
                    new_tree.pop(index)
                    new_tree = new_tree[:index] + value + new_tree[index:]
                    break
            else:
                break

            self.tree = copy.copy(new_tree)

        return [expr.value for expr in self.tree]

    def _unpacking_random(self, expr: AbcExpression) -> List[AbcExpression]:
        if self._repeat(min_=self._default_min_zero, max_=self._random_scale):
            return expr.value
        return []

    def _unpacking_multiplication_grouping(
            self,
            expr: AbcExpression,
            min_: int = 1,
            max_: int = 1,
    ) -> List[AbcExpression]:
        return [
            exp
            for _ in range(self._repeat(min_=min_, max_=max_))
            for exp in expr.value
        ]

    def _unpacking_multiplication(
            self,
            expr: AbcExpression,
            min_: int = 1,
            max_: int = 2,
    ) -> List[AbcExpression]:
        return [expr.value for _ in range(self._repeat(min_=min_, max_=max_))]

    def _do_choice(
            self, left: AbcExpression, right: AbcExpression) -> AbcExpression:
        if self._repeat(min_=self._default_min_or, max_=self._default_max_or):
            return left.accept(self)
        return right.accept(self)

    @staticmethod
    def _repeat(min_: int = 1, max_: int = 1) -> int:
        random.seed()
        return random.randint(min_, max_)
