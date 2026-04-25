from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

SUPPORTED_LANGUAGES = {
    "en": "English", "fa": "Persian", "ar": "Arabic", "fr": "French",
    "es": "Spanish", "de": "German", "zh-CN": "Chinese", "ru": "Russian",
    "tr": "Turkish", "ur": "Urdu", "hi": "Hindi",
}

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    from_lang = data.get("from_lang", "en")
    to_lang = data.get("to_lang", "fa")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long (max 5000 characters)"}), 400
    try:
        translator = GoogleTranslator(source=from_lang, target=to_lang)
        translated = translator.translate(text)
        return jsonify({"translation": translated, "from": from_lang, "to": to_lang})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tts", methods=["GET"])
def tts():
    import asyncio
    import edge_tts
    import io

    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "en")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Microsoft Edge TTS voices — high quality, free, Persian supported
    VOICE_MAP = {
        "en":    "en-US-JennyNeural",
        "fa":    "fa-IR-DilaraNeural",
        "ar":    "ar-SA-ZariyahNeural",
        "fr":    "fr-FR-DeniseNeural",
        "es":    "es-ES-ElviraNeural",
        "de":    "de-DE-KatjaNeural",
        "zh-CN": "zh-CN-XiaoxiaoNeural",
        "ru":    "ru-RU-SvetlanaNeural",
        "tr":    "tr-TR-EmelNeural",
        "ur":    "ur-PK-UzmaNeural",
        "hi":    "hi-IN-SwaraNeural",
    }
    voice = VOICE_MAP.get(lang, "en-US-JennyNeural")

    async def generate():
        buf = io.BytesIO()
        communicate = edge_tts.Communicate(text, voice, rate="-5%")
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])
        return buf.getvalue()

    try:
        audio = asyncio.run(generate())
        return Response(audio, mimetype="audio/mpeg", headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/languages", methods=["GET"])
def languages():
    return jsonify(SUPPORTED_LANGUAGES)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
