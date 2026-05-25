from .token import TokenType
from .ast_nodes import DocumentNode, ElementNode, TextNode


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens, filename="<unknown>"):
        self.tokens = tokens
        self.filename = filename
        self.pos = 0

    def error(self, message):
        tok = self.current()
        raise ParseError(f"{self.filename}:{tok.line}:{tok.column}: {message}")

    def current(self):
        return self.tokens[self.pos]

    def peek(self, offset=0):
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def check(self, *types):
        return self.current().type in types

    def match(self, *types):
        if self.check(*types):
            return self.advance()
        return None

    def expect(self, token_type, message=None):
        if self.check(token_type):
            return self.advance()
        self.error(message or f"Expected {token_type.name}, got {self.current().type.name}")

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse(self):
        children = []
        while not self.check(TokenType.EOF):
            node = self.parse_node()
            if node is not None:
                children.append(node)
        return DocumentNode(children)

    def parse_node(self):
        if self.check(TokenType.IDENTIFIER):
            return self.parse_element()
        if self.check(TokenType.STRING):
            tok = self.advance()
            return TextNode(tok.value)
        self.error(f"Unexpected token: {self.current().type.name} ({self.current().value!r})")

    def parse_element(self):
        tag_tok = self.expect(TokenType.IDENTIFIER, "Expected tag name")
        tag_name = tag_tok.value
        attributes = {}

        if self.match(TokenType.LBRACKET):
            attributes = self.parse_attribute_list()
            self.expect(TokenType.RBRACKET, "Expected ] after attribute list")

        if self.match(TokenType.LBRACE):
            children = self.parse_content()
            self.expect(TokenType.RBRACE, f"Expected }} after content of <{tag_name}>")
            return ElementNode(tag_name, attributes, children)

        return ElementNode(tag_name, attributes)

    def parse_attribute_list(self):
        attrs = {}
        seen = set()
        while self.check(TokenType.IDENTIFIER):
            name_tok = self.advance()
            name = name_tok.value
            if name in seen:
                self.error(f"Duplicate attribute '{name}'")
            seen.add(name)
            self.expect(TokenType.EQUALS, f"Expected = after attribute '{name}'")
            val_tok = self.expect(TokenType.STRING, f"Expected value for attribute '{name}'")
            attrs[name] = val_tok.value
        return attrs

    def parse_content(self):
        children = []
        while not self.check(TokenType.RBRACE, TokenType.EOF):
            node = self.parse_node()
            if node is not None:
                children.append(node)
        return children
