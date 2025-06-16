import os
import requests

# Configuración:
# Aquí guardamos nuestras llaves secretas para usar las APIs
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'  # Cambia este por el tuyo si tienes otro

# Función para pedir respuesta a la IA

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


# Función para convertir texto en audio

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


# Programa principal:
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

# Este es el punto de inicio del programa
if __name__ == "__main__":
    main()