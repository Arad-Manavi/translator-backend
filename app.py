from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend PWA

SUPPORTED_LANGUAGES = {
    "en": "English",
    "fa": "Persian",
    "ar": "Arabic",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "zh-CN": "Chinese",
    "ru": "Russian",
    "tr": "Turkish",
    "ur": "Urdu",
    "hi": "Hindi",
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

@app.route("/languages", methods=["GET"])
def languages():
    return jsonify(SUPPORTED_LANGUAGES)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
