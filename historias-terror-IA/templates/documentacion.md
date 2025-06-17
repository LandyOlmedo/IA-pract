# Documentación de `index.html`

---

**1. Línea de declaración especial (Motor de plantillas Mako o similar):**

```html
$def with ()
```
Esta línea indica que la plantilla puede recibir parámetros, aunque en este caso no se pasan argumentos explícitos.

---

**2. Estructura básica del documento HTML:**

```html
<!DOCTYPE html>
<html lang="es">
```
Define el tipo de documento y el idioma principal como español.

---

**3. Encabezado (`<head>`):**

```html
<head>
    <meta charset="UTF-8">
    <title>Historias de Terror IA</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fff; color: #222; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 30px auto; padding: 16px; }
        h1 { text-align: center; font-size: 1.1em; }
        label { font-size: 1em; }
        textarea { width: 100%; min-height: 50px; margin-bottom: 8px; }
        button { width: 100%; padding: 8px; }
        .respuesta { background: #eee; padding: 8px; margin: 10px 0; }
        .audio-box { margin: 8px 0; text-align: center; }
        .flash { background: #f99; color: #222; padding: 6px; margin-bottom: 8px; text-align: center; }
    </style>
</head>
```
- Define la codificación de caracteres como UTF-8.
- El título de la página es “Historias de Terror IA”.
- Incluye estilos CSS para dar formato y diseño moderno a la página.

---

**4. Cuerpo del documento (`<body>`):**

```html
<body>
    <div class="container">
        <h1>Historias de Terror IA</h1>
        ...
    </div>
</body>
```
- El contenido principal está dentro de un contenedor centrado y estilizado.

---

**5. Mensajes Flash (errores o avisos):**

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="flash">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
```
- Utiliza la sintaxis de Jinja2 para mostrar mensajes temporales (flash) enviados desde Flask, como errores o avisos.

---

**6. Formulario de entrada de mensaje:**

```html
<form method="post">
    <label for="mensaje">Mensaje:</label>
    <textarea id="mensaje" name="mensaje" required></textarea>
    <button type="submit">Enviar</button>
</form>
```
- Permite al usuario escribir un mensaje y enviarlo al servidor.
- El campo `textarea` es obligatorio.

---

**7. Mostrar la respuesta de la IA (si existe):**

```html
{% if respuesta %}
    <div class="respuesta">{{ respuesta }}</div>
{% endif %}
```
- Si el servidor devuelve una respuesta, se muestra en un recuadro destacado.

---

**8. Reproductor de audio (si existe archivo de audio):**

```html
{% if audio_file %}
<div class="audio-box">
    <audio controls>
        <source src="/static/{{ audio_file }}" type="audio/wav">
        Tu navegador no soporta el elemento de audio.
    </audio>
</div>
{% endif %}
```
- Si hay un archivo de audio generado, se muestra un reproductor para escucharlo directamente en la página.

---

**9. Cierre de etiquetas HTML:**

```html
    </div>
</body>
</html>
```
- Finaliza el contenedor principal, el cuerpo y el documento HTML.

---
