"""Token"""
from .token_type import TokenType


class Token:
    """Token"""
    __slots__ = (
        'token_type',
        'lexeme',
        'literal',
    )

    def __init__(self, token_type: TokenType, lexeme: str, literal):
        self.token_type: TokenType = token_type
        self.lexeme: str = lexeme
        self.literal = literal

    def __str__(self):
        return f'{self.token_type} {self.lexeme} {self.literal}'
