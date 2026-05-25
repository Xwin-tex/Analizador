// ============================================
//  Prueba completa del compilador SimpleML
//  Incluye todos los casos posibles
// ============================================

// --- 1. ELEMENTOS BASICOS ---
html[lang="es"] {
  head {
    title { "Prueba completa del compilador SimpleML" }
    meta[charset="utf-8"]
    meta[name="viewport" content="width=device-width"]
  }
  body {

    // --- 2. TEXTO PLANO ---
    h1 { "Prueba exhaustiva del compilador" }
    p { "Este archivo prueba todas las caracteristicas del lenguaje SimpleML" }

    // --- 3. LISTAS ---
    h2 { "Lista de compras" }
    ul {
      li { "Manzanas" }
      li { "Pan" }
      li { "Leche" }
      li { "Huevos" }
    }

    // --- 4. LISTA ORDENADA ---
    h2 { "Top 3 lenguajes" }
    ol {
      li { "Python" }
      li { "JavaScript" }
      li { "Rust" }
    }

    // --- 5. TABLA ---
    h2 { "Tabla de ejemplo" }
    table[border="1"] {
      tr {
        th { "Nombre" }
        th { "Edad" }
        th { "Ciudad" }
      }
      tr {
        td { "Ana" }
        td { "25" }
        td { "Madrid" }
      }
      tr {
        td { "Luis" }
        td { "30" }
        td[class="destacado"] { "Bogota" }
      }
    }

    // --- 6. FORMULARIO ---
    h2 { "Formulario de contacto" }
    form[action="/enviar" method="POST"] {
      div[class="campo"] {
        label[for="nombre"] { "Nombre:" }
        input[type="text" id="nombre" name="nombre"]
      }
      div[class="campo"] {
        label[for="email"] { "Email:" }
        input[type="email" id="email" name="email" required="true"]
      }
      div[class="campo"] {
        label[for="mensaje"] { "Mensaje:" }
        textarea[id="mensaje" name="mensaje"] { "Escribe tu mensaje aqui..." }
      }
      button[type="submit"] { "Enviar formulario" }
    }

    // --- 7. IMAGEN Y ENLACES ---
    h2 { "Multimedia" }
    img[src="imagen.jpg" alt="Descripcion de la imagen"]
    br
    a[href="https://ejemplo.com"] { "Visitar ejemplo.com" }

    // --- 8. CONTENEDORES ANIDADOS ---
    h2 { "Contenedores anidados" }
    div[class="nivel1"] {
      p { "Nivel 1" }
      div[class="nivel2"] {
        p { "Nivel 2" }
        div[class="nivel3"] {
          p { "Nivel 3 - maxima profundidad" }
        }
      }
    }

    // --- 9. MULTIPLES ATRIBUTOS ---
    h2 { "Elemento con multiples atributos" }
    div[id="principal" class="contenedor" style="color: blue" data-info="ejemplo"] {
      p { "Este div tiene 4 atributos" }
    }

    // --- 10. ELEMENTOS SIN ATRIBUTOS NI HIJOS ---
    hr
    br

    // --- 11. TEXTO CON CARACTERES ESPECIALES ---
    h2 { "Caracteres especiales" }
    p { "Texto con <> & "" '' y acentos: á é í ó ú ñ" }

    // --- 12. TEXTO CON ESCAPES ---
    h2 { "Secuencias de escape" }
    p { "Salto de linea:\nNueva linea\nTabulador:\tTab" }

    // --- 13. FOOTER ---
    footer {
      p { "Fin de la prueba - Compilador SimpleML 2026" }
    }
  }
}
