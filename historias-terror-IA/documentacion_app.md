
# Explicación básica del código (línea por línea)

---

## 1. Importar las librerías necesarias

```python
import os
import requests
```
- **`import os`**  
  Permite usar funciones del sistema operativo, como leer claves secretas (API keys) que guardas en tu computadora.
- **`import requests`**  
  Permite enviar y recibir información de servicios de internet (APIs), como la IA o la voz.

---

## 2. Configuración de claves y voz

```python
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'  # Cambia este por el tuyo si tienes otro
```
- **`GROQ_API_KEY = os.environ.get('GROQ_API_KEY')`**  
  Busca la clave secreta de Groq (para la IA) en tu sistema.
- **`ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')`**  
  Busca la clave secreta de ElevenLabs (para la voz) en tu sistema.
- **`VOICE_ID = ...`**  
  Es el código de la voz que quieres usar para convertir texto en audio.

---

## 3. Función para pedir respuesta a la IA

```python
def pedir_respuesta(mensaje):
    # Si no tenemos la llave, mostramos un error
    if not GROQ_API_KEY:
        print("No se encontró la clave GROQ_API_KEY.")
        return ""
    # Esta es la dirección a donde vamos a mandar el mensaje
    url = "https://api.groq.com/openai/v1/chat/completions"
    # Esto dice quiénes somos y qué tipo de datos enviamos
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    # Preparamos el mensaje para la IA
    datos = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "user",
                "content": mensaje
            }
        ]
    }
    # Enviamos el mensaje y recibimos la respuesta
    respuesta = requests.post(url, headers=headers, json=datos)
    respuesta.raise_for_status()
    respuesta_json = respuesta.json()
    # Sacamos el texto que nos dio la IA
    return respuesta_json["choices"][0]["message"]["content"]
```
- **`def pedir_respuesta(mensaje):`**  
  Define una función que le manda un mensaje a la IA y regresa la respuesta.
- **`if not GROQ_API_KEY:`**  
  Si no hay clave, muestra un mensaje de error y sale de la función.
- **`url = ...`**  
  Es la dirección de internet a la que se manda el mensaje para hablar con la IA.
- **`headers = {...}`**  
  Indica quién eres (con tu clave) y el tipo de datos que mandas (JSON).
- **`datos = {...}`**  
  Prepara el mensaje para la IA, diciendo qué modelo usar y el contenido del mensaje.
- **`respuesta = requests.post(...)`**  
  Manda los datos a la IA y guarda la respuesta.
- **`respuesta.raise_for_status()`**  
  Si hubo un error al enviar/recibir, detiene el programa y avisa.
- **`respuesta_json = respuesta.json()`**  
  Convierte la respuesta que da la IA a un formato que Python entiende.
- **`return ...`**  
  Saca el texto de la respuesta de la IA y lo devuelve.

---

## 4. Función para convertir texto en audio

```python
def texto_a_audio(texto, nombre_archivo="respuesta.wav"):
    # Si no tenemos la llave, mostramos un error
    if not ELEVENLABS_API_KEY:
        print("No se encontró la clave ELEVENLABS_API_KEY.")
        return
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    datos = {"text": texto}
    respuesta = requests.post(url, headers=headers, json=datos)
    respuesta.raise_for_status()
    # Guardamos el audio en la computadora
    with open(nombre_archivo, "wb") as archivo:
        archivo.write(respuesta.content)
    print(f"Se guardó el audio como '{nombre_archivo}'")
```
- **`def texto_a_audio(texto, nombre_archivo="respuesta.wav"):`**  
  Define una función que convierte un texto en audio y lo guarda en un archivo.
- **`if not ELEVENLABS_API_KEY:`**  
  Si no hay clave, muestra un mensaje de error y sale de la función.
- **`url = ...`**  
  Es la dirección de internet a la que se manda el texto para convertirlo en audio.
- **`headers = {...}`**  
  Indica tu clave secreta y el formato de datos y audio que quieres.
- **`datos = {"text": texto}`**  
  Prepara el texto que quieres convertir en voz.
- **`respuesta = requests.post(...)`**  
  Manda el texto a ElevenLabs y recibe el audio.
- **`respuesta.raise_for_status()`**  
  Si hubo un error, detiene el programa y avisa.
- **`with open(nombre_archivo, "wb") as archivo:`**  
  Abre (o crea) un archivo para guardar el audio.
- **`archivo.write(respuesta.content)`**  
  Escribe el audio recibido en el archivo.
- **`print(f"...")`**  
  Muestra un mensaje avisando que el archivo de audio fue guardado.

---

## 5. Programa principal (lo que interactúa con el usuario)

```python
def main():
    print("Escribe un mensaje (o escribe 'salir' para terminar):")
    numero = 1
    while True:
        mensaje = input("> ")
        if mensaje.lower() == "salir":
            print("¡Hasta luego!")
            break
        respuesta = pedir_respuesta(mensaje)
        print("IA:", respuesta)
        archivo_audio = f"respuesta_{numero}.wav"
        texto_a_audio(respuesta, archivo_audio)
        numero += 1
```
- **`def main():`**  
  Define la función principal del programa.
- **`print("...")`**  
  Muestra un mensaje de bienvenida e instrucciones.
- **`numero = 1`**  
  Empieza un contador para los archivos de audio.
- **`while True:`**  
  Empieza un ciclo que se repite hasta que el usuario escriba "salir".
- **`mensaje = input("> ")`**  
  Pide al usuario que escriba un mensaje.
- **`if mensaje.lower() == "salir":`**  
  Si escriben "salir", muestra un mensaje de despedida y termina el ciclo.
- **`respuesta = pedir_respuesta(mensaje)`**  
  Manda el mensaje a la IA y recibe la respuesta.
- **`print("IA:", respuesta)`**  
  Muestra la respuesta de la IA en pantalla.
- **`archivo_audio = f"respuesta_{numero}.wav"`**  
  Prepara el nombre para el archivo de audio.
- **`texto_a_audio(respuesta, archivo_audio)`**  
  Convierte la respuesta en audio y la guarda en el archivo.
- **`numero += 1`**  
  Suma uno al contador para el siguiente archivo.

---

## 6. Punto de inicio del programa

```python
if __name__ == "__main__":
    main()
```
- **`if __name__ == "__main__":`**  
  Hace que el programa empiece aquí cuando ejecutas el archivo.
- **`main()`**  
  Llama a la función principal para que empiece todo el flujo.

---

# Explicación detallada del código de la aplicación web (Flask)

## ¿Qué hace este proyecto?
Esta aplicación permite que un usuario escriba un mensaje en una página web, la IA responde con una historia de terror y, además, la respuesta se convierte en audio para poder escucharla directamente desde el navegador.

---

## Explicación del código principal (`app.py`)

### 1. Importaciones y configuración
```python
from flask import Flask, render_template, request, send_from_directory, flash
import os
import requests
```
- **Flask**: Permite crear la aplicación web.
- **os**: Permite acceder a variables del sistema (para las claves API).
- **requests**: Permite hacer peticiones HTTP a las APIs externas.

### 2. Inicialización de la app y claves
```python
app = Flask(__name__)
app.secret_key = 'historia-terror-ia'
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'
```
- Se crea la app Flask y se define una clave secreta para manejar mensajes temporales.
- Se obtienen las claves de las APIs desde variables de entorno.

### 3. Función para pedir respuesta a la IA
```python
def pedir_respuesta(mensaje):
    # Si no tenemos la clave, mostramos un error
    if not GROQ_API_KEY:
        return None, "No se encontró la clave GROQ_API_KEY."
    # Esta es la dirección a donde vamos a mandar el mensaje
    url = "https://api.groq.com/openai/v1/chat/completions"
    # Esto dice quiénes somos y qué tipo de datos enviamos
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    # Preparamos el mensaje para la IA
    datos = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": mensaje}
        ]
    }
    # Intentamos enviar la solicitud y procesar la respuesta
    try:
        respuesta = requests.post(url, headers=headers, json=datos, timeout=20)
        respuesta.raise_for_status()
        respuesta_json = respuesta.json()
        return respuesta_json["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error al conectar con la API de Groq: {e}"
```
- **`def pedir_respuesta(mensaje):`**  
  Define una función que le manda un mensaje a la IA y regresa la respuesta.
- **`if not GROQ_API_KEY:`**  
  Si no hay clave, muestra un mensaje de error y sale de la función.
- **`url = ...`**  
  Es la dirección de internet a la que se manda el mensaje para hablar con la IA.
- **`headers = {...}`**  
  Indica quién eres (con tu clave) y el tipo de datos que mandas (JSON).
- **`datos = {...}`**  
  Prepara el mensaje para la IA, diciendo qué modelo usar y el contenido del mensaje.
- **`respuesta = requests.post(...)`**  
  Manda los datos a la IA y guarda la respuesta.
- **`respuesta.raise_for_status()`**  
  Si hubo un error al enviar/recibir, detiene el programa y avisa.
- **`respuesta_json = respuesta.json()`**  
  Convierte la respuesta que da la IA a un formato que Python entiende.
- **`return ...`**  
  Saca el texto de la respuesta de la IA y lo devuelve.

---

### 4. Función para convertir texto en audio
```python
def texto_a_audio(texto, nombre_archivo="respuesta.wav"):
    # Si no tenemos la llave, mostramos un error
    if not ELEVENLABS_API_KEY:
        return None, "No se encontró la clave ELEVENLABS_API_KEY."
    # Esta es la dirección a donde vamos a mandar el texto
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    # Esto dice quiénes somos y qué tipo de datos enviamos
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    # Preparamos el texto para la conversión a audio
    datos = {"text": texto}
    # Intentamos enviar la solicitud y guardar el archivo de audio recibido
    try:
        respuesta = requests.post(url, headers=headers, json=datos, timeout=20)
        respuesta.raise_for_status()
        with open(os.path.join("static", nombre_archivo), "wb") as archivo:
            archivo.write(respuesta.content)
        return nombre_archivo, None
    except Exception as e:
        return None, f"Error al generar el audio: {e}"
```
- **`def texto_a_audio(texto, nombre_archivo="respuesta.wav"):`**  
  Define una función que convierte un texto en audio y lo guarda en un archivo.
- **`if not ELEVENLABS_API_KEY:`**  
  Si no hay clave, muestra un mensaje de error y sale de la función.
- **`url = ...`**  
  Es la dirección de internet a la que se manda el texto para convertirlo en audio.
- **`headers = {...}`**  
  Indica tu clave secreta y el formato de datos y audio que quieres.
- **`datos = {"text": texto}`**  
  Prepara el texto que quieres convertir en voz.
- **`respuesta = requests.post(...)`**  
  Manda el texto a ElevenLabs y recibe el audio.
- **`respuesta.raise_for_status()`**  
  Si hubo un error, detiene el programa y avisa.
- **`with open(nombre_archivo, "wb") as archivo:`**  
  Abre (o crea) un archivo para guardar el audio.
- **`archivo.write(respuesta.content)`**  
  Escribe el audio recibido en el archivo.
- **`print(f"...")`**  
  Muestra un mensaje avisando que el archivo de audio fue guardado.

---

### 5. Ruta principal de la app web
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    audio_file = None
    # Si el usuario envía un formulario (POST), procesamos el mensaje recibido
    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        if mensaje:
            respuesta, error_ia = pedir_respuesta(mensaje)
            if error_ia:
                flash(error_ia, 'error')
            elif respuesta:
                audio_file, error_audio = texto_a_audio(respuesta, "respuesta_1.wav")
                if error_audio:
                    flash(error_audio, 'error')
    # Renderizamos la plantilla HTML, enviando la respuesta y el archivo de audio (si existen)
    return render_template('index.html', respuesta=respuesta, audio_file=audio_file)
```
- **`@app.route('/', methods=['GET', 'POST'])`**  
  Define la ruta principal de la aplicación web, que acepta métodos GET y POST.
- **`def index():`**  
  Función que maneja la lógica de la ruta principal.
- **`respuesta = None`**  
  Inicializa la variable de respuesta de la IA.
- **`audio_file = None`**  
  Inicializa la variable del archivo de audio.
- **`if request.method == 'POST':`**  
  Verifica si el usuario ha enviado un mensaje.
- **`mensaje = request.form.get('mensaje')`**  
  Obtiene el mensaje del formulario enviado.
- **`if mensaje:`**  
  Si hay un mensaje, pide la respuesta a la IA.
- **`respuesta, error_ia = pedir_respuesta(mensaje)`**  
  Llama a la función que se comunica con la IA.
- **`if error_ia:`**  
  Si hay un error con la IA, muéstralo.
- **`elif respuesta:`**  
  Si hay una respuesta, conviértela a audio.
- **`audio_file, error_audio = texto_a_audio(respuesta, "respuesta_1.wav")`**  
  Llama a la función que convierte texto a audio.
- **`if error_audio:`**  
  Si hay un error al generar el audio, muéstralo.
- **`return render_template('index.html', respuesta=respuesta, audio_file=audio_file)`**  
  Renderiza la plantilla HTML con la respuesta y el archivo de audio.

---

### 6. Ruta para archivos estáticos
```python
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
```
- **`@app.route('/static/<path:filename>')`**  
  Define una ruta para servir archivos estáticos (como el audio generado).
- **`def static_files(filename):`**  
  Función que maneja la solicitud de archivos estáticos.
- **`return send_from_directory('static', filename)`**  
  Envía el archivo solicitado desde la carpeta `static`.

---

### 7. Inicio de la app
```python
if __name__ == '__main__':
    app.run(debug=True)
```
- **`if __name__ == '__main__':`**  
  Este es el punto de inicio del programa. Si este archivo se ejecuta directamente, inicia la aplicación web en modo desarrollo.
- **`app.run(debug=True)`**  
  Inicia el servidor de desarrollo de Flask.

---

## Resumen para cualquier público
- El usuario escribe un mensaje en la web.
- El mensaje se manda a una IA que responde con una historia de terror.
- La respuesta se convierte en audio y se puede escuchar en la misma página.
- Si ocurre algún error (por ejemplo, falta de claves), se muestra un mensaje claro.

---