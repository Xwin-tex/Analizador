import re
from .token import Token, TokenType


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, source, filename="<unknown>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def error(self, message):
        raise LexerError(f"{self.filename}:{self.line}:{self.column}: {message}")

    def peek(self, offset=0):
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else None

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace(self):
        while self.pos < len(self.source) and self.peek() in " \t\r":
            self.advance()

    def skip_comment(self):
        while self.pos < len(self.source) and self.peek() != "\n":
            self.advance()

    def read_string(self):
        start_col = self.column
        self.advance()
        value = []
        while self.pos < len(self.source):
            ch = self.peek()
            if ch == '"':
                self.advance()
                return "".join(value)
            elif ch == "\\":
                self.advance()
                esc = self.advance() if self.pos < len(self.source) else None
                escapes = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}
                value.append(escapes.get(esc, esc or "\\"))
            else:
                value.append(self.advance())
        self.error("Unterminated string")

    def read_identifier(self):
        start = self.pos
        while self.pos < len(self.source) and (self.peek().isalnum() or self.peek() in "_-"):
            self.advance()
        return self.source[start:self.pos]

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            ch = self.peek()

            if ch in " \t\r":
                self.skip_whitespace()
                continue

            if ch == "\n":
                self.advance()
                continue

            if ch == "/" and self.pos + 1 < len(self.source) and self.source[self.pos + 1] == "/":
                self.skip_comment()
                continue

            if ch == "{":
                tokens.append(Token(TokenType.LBRACE, "{", self.line, self.column))
                self.advance()
                continue

            if ch == "}":
                tokens.append(Token(TokenType.RBRACE, "}", self.line, self.column))
                self.advance()
                continue

            if ch == "[":
                tokens.append(Token(TokenType.LBRACKET, "[", self.line, self.column))
                self.advance()
                continue

            if ch == "]":
                tokens.append(Token(TokenType.RBRACKET, "]", self.line, self.column))
                self.advance()
                continue

            if ch == "=":
                tokens.append(Token(TokenType.EQUALS, "=", self.line, self.column))
                self.advance()
                continue

            if ch == '"':
                t = Token(TokenType.STRING, None, self.line, self.column)
                t.value = self.read_string()
                tokens.append(t)
                continue

            if ch.isalpha() or ch == "_":
                t = Token(TokenType.IDENTIFIER, None, self.line, self.column)
                t.value = self.read_identifier()
                tokens.append(t)
                continue

            self.error(f"Unexpected character: {ch!r}")

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        self.tokens = tokens
        return tokens
