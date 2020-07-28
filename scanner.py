"""The lexical scanner of the Lox language.

:Author:     Maded Batara III
"""

from typing import List, Any, Callable
from token import Token
from tokentype import TokenType

ErrorFunc = Callable[[str, str, str], None]

def is_digit(tok: str) -> bool:
    return ord('0') <= ord(tok) <= ord('9')

def is_alpha(tok: str) -> bool:
    return (ord('a') <= ord(tok) <= ord('z')) \
        or (ord('A') <= ord(tok) <= ord('Z')) \
        or tok == '_'

def is_alphanum(tok: str) -> bool:
    return is_alpha(tok) or is_digit(tok)

reserved = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE
}

class Scanner:

    def __init__(self, source: str, error_func: ErrorFunc):
        self.source = source
        self.error_func = ErrorFunc
        self.tokens = []

        # first character in the lexeme
        self.start = 0

        # current character in the lexeme
        self.current = 0

        # current line in the code
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        while not self.at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        tok = self.advance()
        if tok == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif tok == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif tok == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif tok == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif tok == ',':
            self.add_token(TokenType.COMMA)
        elif tok == '.':
            self.add_token(TokenType.DOT)
        elif tok == '-':
            self.add_token(TokenType.MINUS)
        elif tok == '+':
            self.add_token(TokenType.PLUS)
        elif tok == ';':
            self.add_token(TokenType.SEMICOLON)
        elif tok == '*':
            self.add_token(TokenType.STAR)
        elif tok == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match(
                '=') else TokenType.BANG)
        elif tok == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match(
                '=') else TokenType.EQUAL)
        elif tok == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match(
                '=') else TokenType.LESS)
        elif tok == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match(
                '=') else TokenType.GREATER)
        elif tok == '/':
            if self.match('/'):
                # Absorb the comment
                while self.peek() != '\n' and not self.at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif tok == ' ' or tok == '\r' or tok == '\t':
            pass
        elif tok == '\n':
            self.line += 1
        elif tok == '"':
            self.absorb_string()
        elif is_digit(tok):
            self.absorb_number()
        elif is_alpha(tok):
            self.absorb_identifier()
        else:
            self.error_func(
                self.line, "Unexpected character: {0}".format(tok))

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected: str) -> bool:
        if self.at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def absorb_string(self):
        # Find the end of the string
        while self.peek() != '"' and not self.at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.at_end():
            # String wasn't closed, raise an error
            self.error_func(self.line, "Unterminated string")
            return
        # Absorb the closing "
        self.advance()
        self.add_token(TokenType.STRING,
                       self.source[self.start + 1: self.current - 1])

    def absorb_number(self):
        while is_digit(self.peek()):
            self.advance()
        # Find a decimal point
        if self.peek() == '.' and is_digit(self.peek_next()):
            # If decimal point found, consume the period and continue
            # reading the number
            self.advance()
            while is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(
            self.source[self.start:self.current]))

    def absorb_identifier(self):
        while (is_alphanum(self.peek())):
            self.advance()
        identifier = self.source[self.start: self.current]
        self.add_token(reserved.get(identifier, TokenType.IDENTIFIER))

    def add_token(self, ttype: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(ttype, text, literal, self.line))

    def at_end(self):
        return self.current >= len(self.source)
