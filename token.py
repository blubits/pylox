"""Tokens in the Lox language.

:Author:     Maded Batara III
"""

from typing import TypeVar
import tokentype

T = TypeVar('T')

class Token:

    def __init__(self, ttype: tokentype.TokenType, lexeme: str, literal: T, line: int):
        self.ttype = ttype
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal is None:
            return "<[{0}] {1}>".format(self.ttype, self.lexeme if self.lexeme else "N/A")
        else:
            return "<[{0}] {1} {2}>".format(self.ttype, self.lexeme, self.literal)
