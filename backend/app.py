from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from deep_translator import GoogleTranslator
import urllib.request
import urllib.parse

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
    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "en")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Google TTS uses locale codes, not plain language codes
    TTS_LANG_MAP = {
        "en": "en-US", "fa": "fa-IR", "ar": "ar-SA", "fr": "fr-FR",
        "es": "es-ES", "de": "de-DE", "zh-CN": "zh-CN", "ru": "ru-RU",
        "tr": "tr-TR", "ur": "ur-PK", "hi": "hi-IN",
    }
    tts_lang = TTS_LANG_MAP.get(lang, lang)

    encoded = urllib.parse.quote(text)
    url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&q={encoded}&tl={tts_lang}&client=gtx&ttsspeed=0.9"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://translate.google.com"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            audio = resp.read()
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
