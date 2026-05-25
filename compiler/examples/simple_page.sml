html[lang="en"] {
  head {
    title { "My SimpleML Page" }
    meta[charset="utf-8"]
    link[rel="stylesheet" href="style.css"]
  }
  body {
    header {
      h1[class="main-title"] { "Welcome to SimpleML" }
      p { "A lightweight markup language that compiles to HTML" }
    }
    main {
      section[class="content"] {
        h2 { "Features" }
        ul {
          li { "Clean syntax" }
          li { "Custom attributes" }
          li { "Nested elements" }
          li { "Compiles to valid HTML" }
        }
      }
      section[class="about"] {
        h2 { "About" }
        p { "SimpleML is a custom markup language designed for educational purposes." }
        p { "It demonstrates all phases of a compiler: lexer, parser, validator, intermediate code generation, and code generation." }
      }
    }
    footer {
      p { "Created with SimpleML Compiler" }
    }
  }
}
