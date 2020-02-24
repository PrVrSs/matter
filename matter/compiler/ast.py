"""Antlr4 AST"""
import copy
import random
from typing import (
    List,
    Optional,
    Any,
)

from .expressions import Literal, AbcExpression, Choice


class Ast:
    """Antlr4 Ast"""
    __slots__ = (
        'tree',
        '_multiplication_scale',
        '_random_scale',
        '_default_min_zero',
        '_default_min_one',
        '_default_min_or',
        '_default_max_or'
    )

    def __new__(
            cls,
            tree_: Optional[List[AbcExpression]] = None,
            multiplication_scale: int = 1,
            random_scale: int = 1,
            *args: Any,
            **kwargs: Any,
    ):
        self = super().__new__(cls)

        self.tree: List[AbcExpression] = tree_ or []
        self._multiplication_scale: int = multiplication_scale
        self._random_scale: int = random_scale
        self._default_min_zero: int = 0
        self._default_min_one: int = 1
        self._default_min_or: int = 0
        self._default_max_or: int = 4

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
    def visit_tilde(expr: AbcExpression) -> AbcExpression:
        return Literal(value='\x33')

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
