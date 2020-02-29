"""Antlr4 Expressions"""
from typing import Any

import attr

from .interfaces import AbcExpression


@attr.s(slots=True)
class Choice(AbcExpression):
    """Choice expression"""
    left = attr.ib(type=AbcExpression)
    operator = attr.ib(type=Any)
    right = attr.ib(type=AbcExpression)
    type: str = 'Choice'

    def accept(self, visitor):
        return visitor.visit_choice(self)


@attr.s(slots=True)
class Equal(AbcExpression):
    """Equal expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Equal'

    def accept(self, visitor):
        return visitor.visit_equal(self)


@attr.s(slots=True)
class Literal(AbcExpression):
    """Literal expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Literal'

    def accept(self, visitor):
        return visitor.visit_literal(self)


@attr.s(slots=True)
class RandomLiteral(AbcExpression):
    """RandomLiteral expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'RandomLiteral'

    def accept(self, visitor):
        return visitor.visit_random_literal(self)


@attr.s(slots=True)
class StarMultiplication(AbcExpression):
    """StarMultiplication expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Multiplication'

    def accept(self, visitor):
        return visitor.visit_star_multiplication(self)


@attr.s(slots=True)
class PlusMultiplication(AbcExpression):
    """PlusMultiplication expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Multiplication'

    def accept(self, visitor):
        return visitor.visit_plus_multiplication(self)


@attr.s(slots=True)
class Grouping(AbcExpression):
    """Grouping expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Grouping'

    def accept(self, visitor):
        return visitor.visit_grouping(self)


@attr.s(slots=True)
class StarMultiplicationGrouping(AbcExpression):
    """StarMultiplicationGrouping expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'MultiplicationGrouping'

    def accept(self, visitor):
        return visitor.visit_star_multiplication_grouping(self)


@attr.s(slots=True)
class PlusMultiplicationGrouping(AbcExpression):
    """PlusMultiplicationGrouping expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'PlusMultiplicationGrouping'

    def accept(self, visitor):
        return visitor.visit_plus_multiplication_grouping(self)


@attr.s(slots=True)
class RandomGrouping(AbcExpression):
    """RandomGrouping expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'RandomGrouping'

    def accept(self, visitor):
        return visitor.visit_random_grouping(self)


@attr.s(slots=True)
class Tilde(AbcExpression):
    """Tilde expression"""
    value = attr.ib(type=AbcExpression)
    type: str = 'Tilde'

    def accept(self, visitor):
        return visitor.visit_tilde(self)
