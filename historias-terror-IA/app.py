from flask import Flask, render_template, request, jsonify
import requests
import os

ELEVENLABS_API_KEY = ("sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72")
VOICE_ID = ("gbTn1bmCvNgk0QEAVyfM", "gbTn1bmCvNgk0QEAVyfM")

app = Flask(__name__)

# Tus claves (guarda esto en variables de entorno en producción)
ELEVENLABS_API_KEY = "sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72"
VOICE_ID = "gbTn1bmCvNgk0QEAVyfM"  # Puedes elegir alguna voz de ElevenLabs

# Lista de historias de terror predefinidas
stories = [
    "Una noche fría, escuchaste pasos detrás de ti... pero no había nadie.",
    "Alguien llamó a tu puerta a las 3 AM. Al abrir, solo viste tus propias huellas de sangre regresando hacia adentro.",
    "Despertaste y notaste que alguien te observaba desde el espejo. No era tu reflejo.",
    "Recibiste un mensaje de texto de tu yo futuro advirtiéndote que no salgas de tu casa nunca más."
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate-story", methods=["POST"])
def generate_story():
    story = stories[random.randint(0, len(stories) - 1)]
    return jsonify({"story": story})

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    text = data["text"]

    url = f"https://api.elevenlabs.io/v1/text-to-speech/gbTn1bmCvNgk0QEAVyfM" 
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72
    }
    body = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": "Error generando audio"}), 500

    return response.content, response.headers['Content-Type']

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)