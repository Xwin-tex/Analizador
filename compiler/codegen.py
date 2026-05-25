from .intermediate import IRInstruction


class CodeGenerator:
    def __init__(self, instructions):
        self.instructions = instructions
        self.output = []
        self.indent_level = 0
        self.indent_str = "  "

    def generate(self):
        for instr in self.instructions:
            if instr.opcode == "OPEN_TAG":
                self._emit_open_tag(instr.args[0], instr.args[1])
            elif instr.opcode == "CLOSE_TAG":
                self._emit_close_tag(instr.args[0])
            elif instr.opcode == "TEXT":
                self._emit_text(instr.args[0])
        return "\n".join(self.output)

    def _emit(self, line):
        self.output.append(self.indent_str * self.indent_level + line)

    def _escape_html(self, text):
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&#39;",
            ">": "&gt;",
            "<": "&lt;",
        }
        return "".join(html_escape_table.get(c, c) for c in text)

    def _format_attributes(self, attrs):
        if not attrs:
            return ""
        parts = []
        for key, value in attrs.items():
            escaped = value.replace("&", "&amp;").replace('"', "&quot;")
            parts.append(f'{key}="{escaped}"')
        return " " + " ".join(parts) if parts else ""

    def _emit_open_tag(self, tag_name, attributes):
        attrs_str = self._format_attributes(attributes)
        void_tags = {
            "area", "base", "br", "col", "embed", "hr", "img",
            "input", "link", "meta", "param", "source", "track", "wbr",
        }
        if tag_name in void_tags:
            self._emit(f"<{tag_name}{attrs_str} />")
        else:
            self._emit(f"<{tag_name}{attrs_str}>")
            self.indent_level += 1

    def _emit_close_tag(self, tag_name):
        void_tags = {
            "area", "base", "br", "col", "embed", "hr", "img",
            "input", "link", "meta", "param", "source", "track", "wbr",
        }
        if tag_name in void_tags:
            return
        self.indent_level -= 1
        if self.indent_level < 0:
            self.indent_level = 0
        self._emit(f"</{tag_name}>")

    def _emit_text(self, text):
        escaped = self._escape_html(text)
        self._emit(escaped)
