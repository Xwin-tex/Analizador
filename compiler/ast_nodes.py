class ASTNode:
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"

class DocumentNode(ASTNode):
    def __init__(self, children=None):
        self.children = children or []

class ElementNode(ASTNode):
    def __init__(self, tag_name, attributes=None, children=None):
        self.tag_name = tag_name
        self.attributes = attributes or {}
        self.children = children or []

class TextNode(ASTNode):
    def __init__(self, text):
        self.text = text

class CommentNode(ASTNode):
    def __init__(self, text):
        self.text = text
