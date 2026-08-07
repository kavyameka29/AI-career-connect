"""
Speech Routes — Speech-to-Text (STT) and Text-to-Speech (TTS) endpoints.
"""

from flask import Blueprint, request, jsonify, send_file
from app.services.speech_service import transcribe_audio, synthesize_speech

speech_bp = Blueprint("speech", __name__)


@speech_bp.route("/to-text", methods=["POST"])
def speech_to_text():
    """
    Accept an audio file upload and return its transcription.
    Uses the SpeechRecognition library under the hood.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    transcript = transcribe_audio(audio_file)

    if transcript is None:
        return jsonify({"error": "Could not transcribe audio"}), 500

    return jsonify({"transcript": transcript})


@speech_bp.route("/to-speech", methods=["POST"])
def text_to_speech():
    """
    Accept text and return a synthesized audio file.
    """
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Text cannot be empty"}), 400

    audio_path = synthesize_speech(text)

    if audio_path is None:
        return jsonify({"error": "Speech synthesis failed"}), 500

    return send_file(audio_path, mimetype="audio/wav", as_attachment=False)
