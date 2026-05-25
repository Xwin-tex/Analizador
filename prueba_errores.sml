// ============================================
//  Prueba de DETECCION DE ERRORES
//  Cada seccion prueba un error distinto
//  COMENTA las secciones para probar una por una
// ============================================

html {
  head {
    title { "Prueba de errores" }
  }
  body {

    // --- ERROR 1: Atributo duplicado ---
    // Descomenta la siguiente linea para probar:
    // div[class="a" class="b"] { p { "error" } }

    // --- ERROR 2: Tag void con hijos ---
    // Descomenta:
    // br { p { "no puede tener hijos" } }

    // --- ERROR 3: Falta llave de cierre ---
    // Descomenta:
    // div { p { "falta llave" }

    // --- ERROR 4: Caracter invalido ---
    // Descomenta:
    // p { "texto normal" @ }

    // --- ERROR 5: Tag sin nombre ---
    // Descomenta:
    // { "tag sin nombre" }

    // --- CASO CORRECTO para comparar ---
    h1 { "Prueba de errores del compilador" }
    p { "Si ves este mensaje sin errores, el compilador funciona bien" }
    p { "Para probar errores, descomenta las lineas marcadas arriba" }

  }
}
