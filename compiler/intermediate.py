from .ast_nodes import DocumentNode, ElementNode, TextNode


class IRInstruction:
    def __init__(self, opcode, *args):
        self.opcode = opcode
        self.args = args

    def __repr__(self):
        args = ", ".join(repr(a) for a in self.args)
        return f"  {self.opcode} {args}"


class IntermediateGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.instructions = []

    def generate(self):
        self._process_node(self.ast)
        return self.instructions

    def _process_node(self, node):
        if isinstance(node, DocumentNode):
            for child in node.children:
                self._process_node(child)
        elif isinstance(node, ElementNode):
            self.instructions.append(
                IRInstruction("OPEN_TAG", node.tag_name, dict(node.attributes))
            )
            for child in node.children:
                self._process_node(child)
            self.instructions.append(
                IRInstruction("CLOSE_TAG", node.tag_name)
            )
        elif isinstance(node, TextNode):
            self.instructions.append(
                IRInstruction("TEXT", node.text)
            )
