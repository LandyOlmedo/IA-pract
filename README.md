# IA-pract
#
GROQ_API_KEY=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
ELEVENLABS_API_KEY=sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72
ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9




curl -X POST "https://api.groq.com/openai/v1/audio/speech" \
  -H "Content-Type: application/json" \
    -H "Authorization         "text": "Here are three famous Mexican horror legends, each summarized in about 10 seconds:\n\n---\n\n*1. La Llorona (The Weeping Woman)*  \nA vengeful spirit of a mother who drowned her children in a river after her lover betrayed her. Now, she wanders at night, wailing \"¡Ay, mis hijos!\" Her ghost lures people to the water to drown them. Ignoring her cries or approaching her means certain doom.  \n\n---\n\n*2. La Siguanaba (The Deceptive Hag)*  \nAn old woman with long hair who lures men into the forest. If you glimpse her face, it’s hideously distorted. Linked to the Apeninos (forest spirits), she’s often seen near rivers, warning that curiosity about her appearance brings terror.  \n\n---\n\n*3. El Sombrerón (The Wide-Hat Stranger)*  \nA towering, shadowy figure in a wide-brimmed hat who stalks lonely roads. He demands travelers tell a story; if they fail, he steals their soul. Some say he’s a demon testing faith, others a guardian of secrets. Avoid his gaze and keep your stories sharp!  \n\n--- \n\nEach legend blends tragedy, mystery, and a haunting moral lesson. ¡Cuidado!",
: Bearer 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" \
      -d '{
               "model": "playai-tts",
                        "voice": "Arista-PlayAI",
                                 "input": "Here are three famous Mexican horror legends, each summarized in about 10 seconds:\n\n---\n\n*1. La Llorona (The Weeping Woman)*  \nA vengeful spirit of a mother who drowned her children in a river after her lover betrayed her. Now, she wanders at night, wailing \"¡Ay, mis hijos!\" Her ghost lures people to the water to drown them. Ignoring her cries or approaching her means certain doom.  \n\n---\n\n*2. La Siguanaba (The Deceptive Hag)*  \nAn old woman with long hair who lures men into the forest. If you glimpse her face, it’s hideously distorted. Linked to the Apeninos (forest spirits), she’s often seen near rivers, warning that curiosity about her appearance brings terror.  \n\n---\n\n*3. El Sombrerón (The Wide-Hat Stranger)*  \nA towering, shadowy figure in a wide-brimmed hat who stalks lonely roads. He demands travelers tell a story; if they fail, he steals their soul. Some say he’s a demon testing faith, others a guardian of secrets. Avoid his gaze and keep your stories sharp!  \n\n--- \n\nEach legend blends tragedy, mystery, and a haunting moral lesson. ¡Cuidado!",
                                          "response_format": "wav"
                                                 }' \
                                                   --output out.wav









curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/onwK4e9ZLuTAKqWW03F9"  \
  -H "Content-Type: application/json" \
  -H "xi-api-key: sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72" \
  -d '{
         "model_id": "eleven_monolingual_v1",
         "voice_settings": {
           "stability": 0.5,
           "similarity_boost": 0.75
         }
       }' \
  --output out.wav









  curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/gbTn1bmCvNgk0QEAVyfM"  \
  -H "Content-Type: application/json" \
  -H "xi-api-key: sk_707095e9ab968862b09b6edfc4c65c100d65d06ad75dae72" \
  -d '{
         "text": "Aquí tienes tres leyendas horripilantes de México, cada una resumida en unos 10 segundos:\n\n---\n\n*1. La Llorona (La Mujer Llorando)*\nUn espíritu vengativo de una madre que ahogó a sus hijos en un río tras ser abandonada por su amante. Ahora vaga de noche gritando \"¡Ay, mis hijos!\" y atrae a las personas al agua para arrastrarlas. Ignorarla o acercársete puede significar tu perdición.\n\n---\n\n*2. La Siguanaba (La Vieja Engañosa)*\nUna anciana con cabello largo que engaña a los hombres para llevarlos al bosque. Si ves su rostro, es horriblemente deformado. Asociada a los Apeninos, suele aparecer cerca de ríos advirtiendo que mirarla trae terror.\n\n---\n\n*3. El Sombrerón (El Hombre del Sombrero Ancho)*\nUna figura alta y sombría con un sombrero de ala ancha que acecha caminos solitarios. Te exige contar una historia; si fallas, se lleva tu alma. Algunos dicen que es un demonio probando tu fe, otros, un guardián de secretos. Evita su mirada y ten listo un buen cuento.\n\n---\n\nCada leyenda mezcla tragedia, misterio y una moral escalofriante. ¡Cuidado!",
         "model_id": "eleven_multilingual_v1",
         "voice_settings": {
           "stability": 0.5,
           "similarity_boost": 0.75
         }
       }' \
  --output out_spanish.wav





####
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