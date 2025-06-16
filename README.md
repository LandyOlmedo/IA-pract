# IA-pract
#
Primero, buscamos más que nada un proyecto interesante, en el cual queremos que nuestra IA pueda contarnos historias de terror, especificamente sobre México, la que sea, aunque sabemos perfectamente que no nos gustaría que simplemente le escribamos y esta nos platique lo que le decimos, sino que queremos que nuestra IA nos escuche y esta nos pueda platicar leyendas de terror mexicanas

Para ello, hicimos algo arriesgado pero que podría salir satisfactorio, asi que nos movimos de la interfaz de IA "*Groq" y buscamos una adecuada para nuestro proyecto, es así que al investigar, nos movimos a "EvenLabs*".
Esta plataforma nos podrá ayudar a hablarle a la *IA* y que está nos pueda contestar el "*prompt*".

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