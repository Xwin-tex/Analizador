from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER = auto()
    STRING = auto()
    LBRACE = auto()       # {
    RBRACE = auto()       # }
    LBRACKET = auto()     # [
    RBRACKET = auto()     # ]
    EQUALS = auto()       # =
    EOF = auto()

class Token:
    def __init__(self, token_type, value=None, line=1, column=1):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, Ln {self.line}:{self.column})"
