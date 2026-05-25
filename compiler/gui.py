import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import sys

from .lexer import Lexer, LexerError
from .parser import Parser, ParseError
from .validator import Validator, ValidationError
from .intermediate import IntermediateGenerator
from .codegen import CodeGenerator


class SimpleML_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SimpleML Compiler")
        self.root.geometry("1100x700")
        self.root.minsize(900, 600)

        try:
            self.root.iconbitmap(default="")
        except Exception:
            pass

        self.current_file = None
        self.trace_mode = tk.BooleanVar(value=False)

        self._build_ui()

    def _build_ui(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Abrir (.sml)", command=self._open_file)
        file_menu.add_command(label="Guardar (.sml)", command=self._save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exportar HTML...", command=self._export_html)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        examples_menu = tk.Menu(menubar, tearoff=0)
        examples_menu.add_command(label="Página simple", command=lambda: self._load_example("simple_page.sml"))
        examples_menu.add_command(label="Formulario", command=lambda: self._load_example("form.sml"))
        examples_menu.add_command(label="Prueba completa", command=lambda: self._load_example("prueba_completa.sml"))
        menubar.add_cascade(label="Ejemplos", menu=examples_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self._show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(toolbar, text="▶ Compilar", command=self._compile).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Checkbutton(toolbar, text="Traza completa", variable=self.trace_mode).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Label(toolbar, text="Estado:").pack(side=tk.LEFT, padx=(10, 5))
        self.status_bar = ttk.Label(toolbar, text="Listo", relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Paned window for source/output split
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left: Source editor
        left_frame = ttk.LabelFrame(paned, text="Código SimpleML", padding="3")
        self.source_text = scrolledtext.ScrolledText(
            left_frame, wrap=tk.WORD, font=("Consolas", 11),
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
            tabs=("4c",)
        )
        self.source_text.pack(fill=tk.BOTH, expand=True)
        paned.add(left_frame, weight=1)

        # Right: Output tabs
        right_frame = ttk.LabelFrame(paned, text="Resultados", padding="3")
        self.output_tabs = ttk.Notebook(right_frame)
        self.output_tabs.pack(fill=tk.BOTH, expand=True)

        # HTML tab
        self.html_text = scrolledtext.ScrolledText(
            self.output_tabs, wrap=tk.NONE, font=("Consolas", 10),
            bg="#1e1e1e", fg="#d4d4d4", state=tk.DISABLED
        )
        self.output_tabs.add(self.html_text, text="  HTML  ")

        # Tokens tab
        self.tokens_text = scrolledtext.ScrolledText(
            self.output_tabs, wrap=tk.NONE, font=("Consolas", 10),
            bg="#1e1e1e", fg="#d4d4d4", state=tk.DISABLED
        )
        self.output_tabs.add(self.tokens_text, text="  Tokens  ")

        # AST tab
        self.ast_text = scrolledtext.ScrolledText(
            self.output_tabs, wrap=tk.NONE, font=("Consolas", 10),
            bg="#1e1e1e", fg="#d4d4d4", state=tk.DISABLED
        )
        self.output_tabs.add(self.ast_text, text="  AST  ")

        # IR tab
        self.ir_text = scrolledtext.ScrolledText(
            self.output_tabs, wrap=tk.NONE, font=("Consolas", 10),
            bg="#1e1e1e", fg="#d4d4d4", state=tk.DISABLED
        )
        self.output_tabs.add(self.ir_text, text="  Código Intermedio  ")

        # Errors tab
        self.errors_text = scrolledtext.ScrolledText(
            self.output_tabs, wrap=tk.WORD, font=("Consolas", 10),
            bg="#2d1b1b", fg="#ff6b6b", state=tk.DISABLED
        )
        self.output_tabs.add(self.errors_text, text="  Errores  ")

        paned.add(right_frame, weight=1)

        self._set_status("Listo. Carga o escribe código SimpleML y presiona Compilar.")

    def _set_status(self, text):
        self.status_bar.config(text=text)
        self.root.update_idletasks()

    def _set_output(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete("1.0", tk.END)
        widget.insert("1.0", text)
        widget.config(state=tk.DISABLED)

    def _clear_outputs(self):
        for w in [self.html_text, self.tokens_text, self.ast_text, self.ir_text, self.errors_text]:
            w.config(state=tk.NORMAL)
            w.delete("1.0", tk.END)
            w.config(state=tk.DISABLED)

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Abrir archivo SimpleML",
            filetypes=[("SimpleML files", "*.sml"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.source_text.delete("1.0", tk.END)
                self.source_text.insert("1.0", content)
                self.current_file = path
                self._set_status(f"Abierto: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def _save_file(self):
        path = filedialog.asksaveasfilename(
            title="Guardar archivo SimpleML",
            defaultextension=".sml",
            filetypes=[("SimpleML files", "*.sml"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            try:
                content = self.source_text.get("1.0", tk.END).rstrip("\n")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                self.current_file = path
                self._set_status(f"Guardado: {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    def _export_html(self):
        html = self.html_text.get("1.0", tk.END).strip()
        if not html:
            messagebox.showwarning("Sin datos", "Compila primero antes de exportar.")
            return
        path = filedialog.asksaveasfilename(
            title="Exportar HTML",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                self._set_status(f"HTML exportado: {os.path.basename(path)}")
                if messagebox.askyesno("Abrir", "¿Abrir el HTML en el navegador?"):
                    os.startfile(path)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    def _load_example(self, name):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(base_dir, "examples", name),
            os.path.join(base_dir, name),
            os.path.join(base_dir, "..", name),
        ]
        for path in candidates:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.source_text.delete("1.0", tk.END)
                self.source_text.insert("1.0", content)
                self.current_file = path
                self._set_status(f"Ejemplo cargado: {name}")
                return
        messagebox.showerror("Error", f"No se encontró el ejemplo: {name}")

    def _show_about(self):
        messagebox.showinfo(
            "Acerca de SimpleML Compiler",
            "SimpleML Compiler v1.0\n\n"
            "Un compilador didáctico que transforma\n"
            "el lenguaje SimpleML a HTML.\n\n"
            "Fases del compilador:\n"
            "  1. Análisis Léxico (Lexer)\n"
            "  2. Análisis Sintáctico (Parser)\n"
            "  3. Validación Semántica\n"
            "  4. Código Intermedio\n"
            "  5. Generación de HTML\n"
        )

    def _compile(self):
        self._clear_outputs()
        source = self.source_text.get("1.0", tk.END).strip()
        if not source:
            self._set_output(self.errors_text, "Error: No hay código para compilar.\nEscribe o carga un archivo .sml")
            self.output_tabs.select(self.errors_text)
            self._set_status("Error: código vacío")
            return

        trace = self.trace_mode.get()
        filename = self.current_file or "editor.sml"
        errors = []

        # Phase 1: Lexer
        try:
            self._set_status("Fase 1/5: Analizando léxicamente...")
            lexer = Lexer(source, filename)
            tokens = lexer.tokenize()
            token_str = "\n".join(f"  {t}" for t in tokens)
            self._set_output(self.tokens_text, token_str)

            if trace:
                self._set_output(self.tokens_text,
                    f"=== {len(tokens)} tokens generados ===\n{token_str}")
        except LexerError as e:
            self._set_status("Error en análisis léxico")
            self._set_output(self.errors_text, f"ERROR LÉXICO:\n{e}")
            self.output_tabs.select(self.errors_text)
            return

        # Phase 2: Parser
        try:
            self._set_status("Fase 2/5: Construyendo AST...")
            parser = Parser(tokens, filename)
            ast = parser.parse()
            ast_str = self._ast_to_str(ast)
            self._set_output(self.ast_text, ast_str)
        except ParseError as e:
            self._set_status("Error en análisis sintáctico")
            self._set_output(self.errors_text, f"ERROR DE SINTAXIS:\n{e}")
            self.output_tabs.select(self.errors_text)
            return

        # Phase 3: Validator
        try:
            self._set_status("Fase 3/5: Validando semántica...")
            validator = Validator(ast, filename)
            validator.validate()
        except ValidationError as e:
            self._set_status("Error de validación")
            self._set_output(self.errors_text, f"ERROR SEMÁNTICO:\n{e}")
            self.output_tabs.select(self.errors_text)
            return

        # Phase 4: Intermediate
        self._set_status("Fase 4/5: Generando código intermedio...")
        ir_gen = IntermediateGenerator(ast)
        instructions = ir_gen.generate()
        ir_str = "\n".join(repr(instr) for instr in instructions)
        self._set_output(self.ir_text, ir_str)

        # Phase 5: Codegen
        self._set_status("Fase 5/5: Generando HTML...")
        codegen = CodeGenerator(instructions)
        html = codegen.generate()
        self._set_output(self.html_text, html)

        self._set_status(f"✓ Compilación exitosa — {len(instructions)} instrucciones IR")
        self.output_tabs.select(self.html_text)

        if errors:
            self._set_output(self.errors_text, "\n".join(errors))

    def _ast_to_str(self, node, indent=0):
        prefix = "  " * indent
        parts = []
        if hasattr(node, "tag_name"):
            attrs = node.attributes or {}
            attr_str = ""
            if attrs:
                attr_str = " [" + ", ".join(f"{k}={v!r}" for k, v in attrs.items()) + "]"
            parts.append(f"{prefix}<{node.tag_name}>{attr_str}")
            for child in node.children or []:
                parts.append(self._ast_to_str(child, indent + 1))
            parts.append(f"{prefix}</{node.tag_name}>")
        elif hasattr(node, "text"):
            parts.append(f'{prefix}"{node.text}"')
        elif hasattr(node, "children"):
            for child in node.children:
                parts.append(self._ast_to_str(child, indent))
        return "\n".join(parts)


def main():
    root = tk.Tk()
    app = SimpleML_GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
