import re
from .ast_nodes import DocumentNode, ElementNode, TextNode


class ValidationError(Exception):
    pass


VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class Validator:
    def __init__(self, ast, filename="<unknown>"):
        self.ast = ast
        self.filename = filename
        self.errors = []

    def error(self, message, node=None):
        raise ValidationError(f"{self.filename}: {message}")

    def validate(self):
        self._validate_node(self.ast, [])
        return self.ast

    def _validate_node(self, node, ancestors):
        if isinstance(node, DocumentNode):
            for child in node.children:
                self._validate_node(child, ancestors)
            return

        if isinstance(node, TextNode):
            return

        if isinstance(node, ElementNode):
            tag = node.tag_name

            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_-]*$", tag):
                self.error(f"Invalid tag name: '{tag}'")

            if len(ancestors) > 0 and ancestors[-1] in VOID_ELEMENTS:
                self.error(f"Void element <{ancestors[-1]}> cannot have children")

            if tag in VOID_ELEMENTS and node.children:
                self.error(f"Void element <{tag}> cannot have children")

            for child in node.children:
                self._validate_node(child, ancestors + [tag])
