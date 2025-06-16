import os
import requests

# Obtiene las API Keys y el ID de voz desde variables de entorno
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'  # Cambia por tu voice_id real de ElevenLabs

def obtener_respuesta_groq(mensaje_usuario):
#Envía el mensaje del usuario a la API de Groq y devuelve la respuesta generada por el modelo.
    if not GROQ_API_KEY:
        raise ValueError("La variable de entorno GROQ_API_KEY no está definida.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Define el modelo a utilizar
    modelo = "llama3-8b-8192"

    # Prepara el mensaje del usuario en el formato requerido por la API
    mensajes = [
        {
            "role": "user",
            "content": mensaje_usuario
        }
    ]

    # Construye el diccionario de datos para la petición
    data = {
        "model": modelo,
        "messages": mensajes
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    respuesta_json = response.json()
    # Extrae el texto de la respuesta del modelo
    return respuesta_json["choices"][0]["message"]["content"]

def guardar_texto_como_audio(texto, nombre_archivo="respuesta.wav"):
#Convierte el texto recibido en un archivo de audio (.wav) usando ElevenLabs.
    if not ELEVENLABS_API_KEY:
        raise ValueError("La variable de entorno ELEVENLABS_API_KEY no está definida.")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    data = {
        "text": texto
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    with open(nombre_archivo, "wb") as f:
        f.write(response.content)
    print(f"Audio guardado como {nombre_archivo}")

def main():
    print("Escribe tu mensaje para el agente (o 'salir' para terminar):")
    contador = 1
    while True:
        mensaje = input("> ")
        if mensaje.lower() == "salir":
            break
        respuesta_agente = obtener_respuesta_groq(mensaje)
        print(f"Agente: {respuesta_agente}")
        nombre_archivo = f"respuesta_{contador}.wav"
        guardar_texto_como_audio(respuesta_agente, nombre_archivo)
        contador += 1

if __name__ == "__main__":
    main()