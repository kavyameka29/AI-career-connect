"""
Speech Service — STT & TTS
---------------------------
Speech-to-Text  : Uses the SpeechRecognition library (Google Web Speech API).
Text-to-Speech  : Uses pyttsx3 (offline) or gTTS (Google, requires internet).
"""

import os
import tempfile
import uuid

import speech_recognition as sr
from flask import current_app


# ── Speech-to-Text ──────────────────────────────────────────────────

def transcribe_audio(audio_file) -> str | None:
    """
    Transcribe an uploaded audio file to text.

    Args:
        audio_file: A FileStorage object from Flask's request.files.

    Returns:
        The transcribed text, or None on failure.
    """
    recognizer = sr.Recognizer()

    # Save uploaded file temporarily
    upload_dir = current_app.config.get("UPLOAD_FOLDER", "instance/uploads")
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, f"{uuid.uuid4()}.wav")

    try:
        audio_file.save(temp_path)

        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

        transcript = recognizer.recognize_google(audio_data)
        return transcript

    except sr.UnknownValueError:
        return None  # Could not understand audio
    except sr.RequestError as e:
        current_app.logger.error(f"STT service error: {e}")
        return None
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


# ── Text-to-Speech ──────────────────────────────────────────────────

def synthesize_speech(text: str) -> str | None:
    """
    Convert text to a WAV audio file.

    Returns:
        Path to the generated audio file, or None on failure.
    """
    engine = current_app.config.get("TTS_ENGINE", "pyttsx3")
    upload_dir = current_app.config.get("UPLOAD_FOLDER", "instance/uploads")
    os.makedirs(upload_dir, exist_ok=True)
    output_path = os.path.join(upload_dir, f"tts_{uuid.uuid4()}.wav")

    try:
        if engine == "gtts":
            from gtts import gTTS

            tts = gTTS(text=text, lang="en")
            mp3_path = output_path.replace(".wav", ".mp3")
            tts.save(mp3_path)
            return mp3_path
        else:
            import pyttsx3

            tts_engine = pyttsx3.init()
            tts_engine.save_to_file(text, output_path)
            tts_engine.runAndWait()
            return output_path

    except Exception as e:
        current_app.logger.error(f"TTS error: {e}")
        return None
