# SimpleML Compiler

**Un compilador didáctico que transforma SimpleML (lenguaje de marcado ligero) en HTML válido.**

Demuestra las 5 fases fundamentales de un compilador: análisis léxico, análisis sintáctico, validación semántica, generación de código intermedio y generación de código final.

---

## Tabla de contenidos

- [Características](#características)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
  - [Línea de comandos](#línea-de-comandos)
  - [Interfaz gráfica](#interfaz-gráfica)
- [Lenguaje SimpleML](#lenguaje-simpleml)
  - [Sintaxis](#sintaxis)
  - [Ejemplos](#ejemplos)
- [Arquitectura del compilador](#arquitectura-del-compilador)
  - [Fase 1: Análisis Léxico (Lexer)](#fase-1-análisis-léxico-lexer)
  - [Fase 2: Análisis Sintáctico (Parser)](#fase-2-análisis-sintáctico-parser)
  - [Fase 3: Validación Semántica (Validator)](#fase-3-validación-semántica-validator)
  - [Fase 4: Código Intermedio (Intermediate)](#fase-4-código-intermedio-intermediate)
  - [Fase 5: Generación de Código (CodeGen)](#fase-5-generación-de-código-codegen)
- [Detección de errores](#detección-de-errores)
- [Ejecutar pruebas](#ejecutar-pruebas)
- [Licencia](#licencia)

---

## Características

- Lenguaje **SimpleML** de sintaxis limpia y expresiva
- Compilación completa a **HTML válido e indentado**
- **Interfaz gráfica** (GUI) con editor de código y visualización por fases
- **Traza completa** del proceso de compilación (tokens, AST, IR, HTML)
- **Detección de errores** en cada fase con mensajes detallados
- Escapado automático de caracteres especiales HTML (`<`, `>`, `&`, `"`, `'`)
- Soporte para elementos **void** (`br`, `hr`, `img`, `input`, `meta`, etc.)
- Elementos con **múltiples atributos**
- **Anidación profunda** de contenedores
- **Comentarios** con `//`

---

## Estructura del proyecto

```
simpleml-compiler/
├── compiler/
│   ├── __init__.py
│   ├── token.py              # Definición de tipos de token
│   ├── lexer.py              # Fase 1: Análisis léxico
│   ├── ast_nodes.py          # Definición de nodos del AST
│   ├── parser.py             # Fase 2: Análisis sintáctico
│   ├── validator.py          # Fase 3: Validación semántica
│   ├── intermediate.py       # Fase 4: Código intermedio
│   ├── codegen.py            # Fase 5: Generación de HTML
│   ├── main.py               # CLI del compilador
│   ├── gui.py                # Interfaz gráfica (Tkinter)
│   └── examples/
│       ├── simple_page.sml
│       ├── form.sml
│       └── prueba_completa.sml
├── README.md
└── LICENSE
```

---

## Requisitos

- **Python 3.8+**
- Tkinter (incluido con Python en Windows, en Linux instalar `python3-tk`)

### Verificar instalación

```bash
python --version
python -c "import tkinter; print('Tkinter OK')"
```

---

## Instalación

```bash
git clone https://github.com/tu-usuario/simpleml-compiler.git
cd simpleml-compiler
```

No requiere dependencias externas.

---

## Uso

### Línea de comandos

Compilar un archivo `.sml` y mostrar el HTML generado:

```bash
python -m compiler.main archivo.sml
```

Guardar la salida en un archivo HTML:

```bash
python -m compiler.main archivo.sml > pagina.html
```

Ver la traza completa del compilador (tokens, AST, IR, HTML):

```bash
python -m compiler.main archivo.sml --trace
```

### Interfaz gráfica

```bash
python -m compiler.gui
```

La GUI ofrece:
| Componente | Descripción |
|---|---|
| Editor de código | Panel izquierdo con tema oscuro |
| Pestaña HTML | Código HTML generado |
| Pestaña Tokens | Lista completa de tokens del lexer |
| Pestaña AST | Árbol de sintaxis abstracta |
| Pestaña Código Intermedio | Instrucciones IR |
| Pestaña Errores | Mensajes de error detallados |
| Botón Compilar | Ejecuta las 5 fases |
| Exportar HTML | Guarda el HTML y lo abre en el navegador |

---

## Lenguaje SimpleML

SimpleML es un lenguaje de marcado ligero diseñado para este compilador. Su sintaxis es más compacta que HTML pero genera HTML estándar.

### Sintaxis

```
// Comentarios con doble barra

// Elemento con atributos y contenido
nombre_tag[atributo1="valor1" atributo2="valor2"] {
  "texto"
}

// Elemento sin contenido (self-closing)
nombre_tag[atributo="valor"]

// Elemento sin atributos ni contenido
nombre_tag

// Texto plano
"texto en comillas dobles"

// Secuencias de escape en strings
\n  -> nueva línea
\t  -> tabulación
\"  -> comilla literal
\\  -> barra invertida literal
```

### Elementos void

Estos elementos se renderizan como `<tag />` y **no pueden tener hijos**:

```
area, base, br, col, embed, hr, img, input,
link, meta, param, source, track, wbr
```

### Ejemplos

**Página simple:**

```
html[lang="es"] {
  head {
    title { "Mi página" }
  }
  body {
    h1[class="titulo"] { "Hola Mundo" }
    p { "Esto es un párrafo." }
    img[src="foto.jpg" alt="Descripción"]
  }
}
```

**Formulario:**

```
form[action="/enviar" method="POST"] {
  div[class="campo"] {
    label[for="nombre"] { "Nombre:" }
    input[type="text" id="nombre" name="nombre"]
  }
  button[type="submit"] { "Enviar" }
}
```

**Lista anidada:**

```
ul {
  li { "Elemento 1" }
  li { "Elemento 2" }
  li { "Elemento 3" }
}
```

---

## Arquitectura del compilador

El compilador sigue el modelo clásico de compilación en 5 fases:

```
Código fuente (.sml)
       │
       ▼
┌─────────────────┐
│ 1. LEXER        │  Análisis léxico → tokens
│    lexer.py     │
└────────┬────────┘
         │ tokens
         ▼
┌─────────────────┐
│ 2. PARSER       │  Análisis sintáctico → AST
│    parser.py    │
└────────┬────────┘
         │ AST
         ▼
┌─────────────────┐
│ 3. VALIDATOR    │  Validación semántica
│    validator.py │
└────────┬────────┘
         │ AST validado
         ▼
┌─────────────────┐
│ 4. INTERMEDIATE │  Código intermedio (IR)
│  intermediate.py│
└────────┬────────┘
         │ instrucciones IR
         ▼
┌─────────────────┐
│ 5. CODEGEN      │  Generación de HTML
│    codegen.py   │
└────────┬────────┘
         │ HTML
         ▼
    archivo.html
```

### Fase 1: Análisis Léxico (Lexer)

**Archivo:** `compiler/lexer.py`

Convierte el código fuente en una secuencia de tokens.

| Token | Descripción |
|---|---|
| `IDENTIFIER` | Nombres de etiquetas y atributos |
| `STRING` | Texto entre comillas dobles `"..."` |
| `LBRACE` / `RBRACE` | `{` y `}` |
| `LBRACKET` / `RBRACKET` | `[` y `]` |
| `EQUALS` | `=` |
| `EOF` | Fin del archivo |

Los comentarios (`//`) y espacios en blanco se descartan durante esta fase.

### Fase 2: Análisis Sintáctico (Parser)

**Archivo:** `compiler/parser.py`

Construye el **Árbol de Sintaxis Abstracta (AST)** usando un parser descendente recursivo.

Gramática:
```
document    = { element | text }
element     = IDENTIFIER [ "[" attribute_list "]" ] [ "{" content "}" ]
attribute_list = IDENTIFIER "=" STRING { IDENTIFIER "=" STRING }
content     = { element | text }
text        = STRING
```

**Detección de errores en esta fase:**
- Atributos duplicados
- Llaves o corchetes faltantes
- Nombres de etiqueta esperados

### Fase 3: Validación Semántica (Validator)

**Archivo:** `compiler/validator.py**

Recorre el AST y verifica reglas semánticas:

- **Elementos void** (`<br>`, `<hr>`, `<img>`, etc.) no pueden tener hijos
- **Nombres de etiqueta** deben ser identificadores válidos
- Un elemento void **no puede estar dentro de otro elemento void**

### Fase 4: Código Intermedio (Intermediate)

**Archivo:** `compiler/intermediate.py**

Convierte el AST en una secuencia plana de instrucciones IR:

| Instrucción | Significado |
|---|---|
| `OPEN_TAG nombre {attrs}` | Abre una etiqueta |
| `CLOSE_TAG nombre` | Cierra una etiqueta |
| `TEXT contenido` | Texto plano |

Ejemplo de IR para `p { "Hola" }`:
```
OPEN_TAG 'p', {}
TEXT 'Hola'
CLOSE_TAG 'p'
```

### Fase 5: Generación de Código (CodeGen)

**Archivo:** `compiler/codegen.py`

Convierte las instrucciones IR en HTML con:
- **Indentación** automática (2 espacios por nivel)
- **Elementos void** se renderizan como `<tag />` (self-closing)
- **Escapado HTML** de caracteres especiales (`<` → `&lt;`, `&` → `&amp;`, etc.)
- **Atributos** formateados correctamente

---

## Detección de errores

Cada fase detecta errores específicos:

| Fase | Error detectado | Ejemplo |
|---|---|---|
| **Lexer** | Carácter no reconocido | `p { "texto" @ }` |
| **Parser** | Atributo duplicado | `div[class="a" class="b"]` |
| **Parser** | Llave faltante | `div { p { "texto" }` |
| **Parser** | Corchete faltante | `div[class="a"` |
| **Validator** | Tag void con hijos | `br { p { "texto" } }` |
| **Validator** | Tag void anidado en void | `br` dentro de otro `br` |

---

## Ejecutar pruebas

El proyecto incluye archivos de prueba:

```bash
# Probar caso completo (válido)
python -m compiler.main compiler/examples/prueba_completa.sml --trace

# Probar errores (descomentar líneas en el archivo)
python -m compiler.main prueba_errores.sml

# Probar error de atributo duplicado
python -m compiler.main compiler/examples/error_duplicate_attr.sml

# Probar error de tag void con hijos
python -m compiler.main compiler/examples/error_void_children.sml
```

---

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
