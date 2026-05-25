import sys
import os

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .validator import Validator, ValidationError
from .intermediate import IntermediateGenerator
from .codegen import CodeGenerator


class SimpleMLCompiler:
    def __init__(self, filename):
        self.filename = filename
        self.source = None
        self.tokens = None
        self.ast = None
        self.instructions = None
        self.html = None

    def read_source(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            self.source = f.read()
        return self

    def phase_lexer(self):
        print(f"[Lexer] Tokenizing {self.filename}...")
        lexer = Lexer(self.source, self.filename)
        self.tokens = lexer.tokenize()
        print(f"  -> {len(self.tokens)} tokens generated")
        return self

    def phase_parser(self):
        print("[Parser] Building AST...")
        parser = Parser(self.tokens, self.filename)
        self.ast = parser.parse()
        print(f"  -> AST built successfully")
        return self

    def phase_validator(self):
        print("[Validator] Validating AST...")
        validator = Validator(self.ast, self.filename)
        self.ast = validator.validate()
        print("  -> Validation passed")
        return self

    def phase_intermediate(self):
        print("[Intermediate] Generating intermediate code...")
        gen = IntermediateGenerator(self.ast)
        self.instructions = gen.generate()
        print(f"  -> {len(self.instructions)} IR instructions generated")
        return self

    def phase_codegen(self):
        print("[CodeGen] Generating HTML...")
        gen = CodeGenerator(self.instructions)
        self.html = gen.generate()
        print("  -> HTML generated")
        return self

    def compile(self):
        self.read_source()
        self.phase_lexer()
        self.phase_parser()
        self.phase_validator()
        self.phase_intermediate()
        self.phase_codegen()
        return self.html

    def trace_tokens(self):
        print("\n=== TOKENS ===")
        for t in self.tokens:
            print(f"  {t}")

    def trace_ast(self, node=None, indent=0):
        if node is None:
            node = self.ast
        prefix = "  " * indent
        if hasattr(node, "tag_name"):
            attrs = node.attributes or {}
            attr_str = f" [{', '.join(f'{k}={v!r}' for k, v in attrs.items())}]" if attrs else ""
            print(f"{prefix}<{node.tag_name}>{attr_str}")
            for child in node.children or []:
                self.trace_ast(child, indent + 1)
            print(f"{prefix}</{node.tag_name}>")
        elif hasattr(node, "text"):
            print(f'{prefix}"{node.text}"')
        elif hasattr(node, "children"):
            for child in node.children:
                self.trace_ast(child, indent)

    def trace_ir(self):
        print("\n=== INTERMEDIATE CODE ===")
        for instr in self.instructions:
            print(instr)

    def trace_html(self):
        print("\n=== GENERATED HTML ===")
        print(self.html)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m compiler.main <file.sml> [--trace]")
        print("  --trace   Show detailed compilation trace")
        sys.exit(1)

    filename = sys.argv[1]
    trace = "--trace" in sys.argv

    if not os.path.exists(filename):
        print(f"Error: file not found: {filename}")
        sys.exit(1)

    try:
        compiler = SimpleMLCompiler(filename)

        if trace:
            compiler.read_source().phase_lexer()
            compiler.trace_tokens()
            compiler.phase_parser()
            compiler.trace_ast()
            compiler.phase_validator()
            compiler.phase_intermediate()
            compiler.trace_ir()
            compiler.phase_codegen()
            compiler.trace_html()
        else:
            html = compiler.compile()
            print(html)

    except (LexerError, ParseError, ValidationError) as e:
        print(f"Compilation error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
