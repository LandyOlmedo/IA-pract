from flask import Flask, render_template, request, send_from_directory, flash, session
import os
import requests

app = Flask(__name__)
app.secret_key = 'historia-terror-ia'

# Aquí guardamos nuestras llaves secretas para usar las APIs
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = 'gbTn1bmCvNgk0QEAVyfM'  # Cambia este por el tuyo si tienes otro

# Función para pedir respuesta a la IA

def pedir_respuesta(mensaje):
    # Si no tenemos la llave, mostramos un error
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
            {
                "role": "user",
                "content": mensaje
            }
        ]
    }
    try:
        # Enviamos el mensaje y recibimos la respuesta
        respuesta = requests.post(url, headers=headers, json=datos, timeout=20)
        respuesta.raise_for_status()
        respuesta_json = respuesta.json()
        # Sacamos el texto que nos dio la IA
        return respuesta_json["choices"][0]["message"]["content"], None
    except Exception as e:
        return None, f"Error al conectar con la API de Groq: {e}"

# Función para convertir texto en audio

def texto_a_audio(texto, nombre_archivo="respuesta.wav"):
    # Si no tenemos la llave, mostramos un error
    if not ELEVENLABS_API_KEY:
        return None, "No se encontró la clave ELEVENLABS_API_KEY."
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
        # Guardamos el audio en la computadora
        with open(os.path.join("static", nombre_archivo), "wb") as archivo:
            archivo.write(respuesta.content)
        return nombre_archivo, None
    except Exception as e:
        return None, f"Error al generar el audio: {e}"

# Rutas de la aplicación web

@app.route('/', methods=['GET', 'POST'])
def index():
    respuesta = None
    if 'audio_files' not in session:
        session['audio_files'] = []
    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        if mensaje:
            respuesta, error_ia = pedir_respuesta(mensaje)
            if error_ia:
                flash(error_ia, 'error')
            elif respuesta:
                audio_file, error_audio = texto_a_audio(respuesta, f"respuesta_{len(session['audio_files'])+1}.wav")
                if error_audio:
                    flash(error_audio, 'error')
                else:
                    session['audio_files'].append(audio_file)
                    session.modified = True
    return render_template('index.html', respuesta=respuesta, audio_files=session.get('audio_files', []))

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Este es el punto de inicio del programa
if __name__ == '__main__':
    app.run(debug=True)