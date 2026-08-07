"""Speech routes — speech-to-text and text-to-speech endpoints."""

from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required
from app.services.speech_service import SpeechService

speech_bp = Blueprint("speech", __name__)


@speech_bp.route("/transcribe", methods=["POST"])
@login_required
def transcribe():
    """Accept an audio file and return its transcription."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files["audio"]
    text = SpeechService.speech_to_text(audio_file)
    return jsonify({"transcription": text})


@speech_bp.route("/synthesize", methods=["POST"])
@login_required
def synthesize():
    """Accept text and return a synthesized audio file."""
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text cannot be empty."}), 400

    audio_path = SpeechService.text_to_speech(text)
    return send_file(audio_path, mimetype="audio/wav")
