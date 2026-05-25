html[lang="es"] {
  head {
    title { "Formulario de contacto" }
    meta[charset="utf-8"]
  }
  body {
    h1 { "Contacto" }
    form[action="/submit" method="POST"] {
      div[class="field"] {
        label[for="name"] { "Nombre:" }
        input[type="text" id="name" name="name"]
      }
      div[class="field"] {
        label[for="email"] { "Email:" }
        input[type="email" id="email" name="email"]
      }
      div[class="field"] {
        label[for="message"] { "Mensaje:" }
        textarea[id="message" name="message"] { "Escribe aquí..." }
      }
      button[type="submit"] { "Enviar" }
    }
  }
}
