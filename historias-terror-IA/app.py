from flask import Flask, render_template, request, send_from_directory, flash
import os
import requests

app = Flask(__name__)
app.secret_key = 'historia-terror-ia'


# Configuración de llaves desde variables de entorno
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'  # Cambia por tu VOICE_ID real

# Función para pedir respuesta a la IA

def pedir_respuesta(mensaje):
    if not GROQ_API_KEY:
        return None, "No se encontró la clave GROQ_API_KEY."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    datos = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", 
            "content": mensaje}
        ]
    }
    try:
        respuesta = requests.post(url, headers=headers, json=datos, timeout=20)
        respuesta.raise_for_status()
        respuesta_json = respuesta.json()
        return respuesta_json["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error al conectar con la API de Groq: {e}"

# Función para convertir texto en audio

def texto_a_audio(texto, nombre_archivo="respuesta_1.wav"):
    if not ELEVENLABS_API_KEY or not VOICE_ID:
        return None, "No se encontró la clave ELEVENLABS_API_KEY o VOICE_ID."
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/wav"
    }
    datos = {"text": texto}
    try:
        respuesta = requests.post(url, headers=headers, json=datos, timeout=20)
        respuesta.raise_for_status()
        ruta_audio = os.path.join("static", nombre_archivo)
        with open(ruta_audio, "wb") as archivo:
            archivo.write(respuesta.content)
        return nombre_archivo, None
    except Exception as e:
        return None, f"Error al generar el audio: {e}"

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    audio_file = None
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
    return render_template('index.html', respuesta=respuesta, audio_file=audio_file)

# Servir archivos estáticos (audio)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Solo ejecuta el servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
