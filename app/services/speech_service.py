"""
Speech Service
================
Provides speech-to-text (STT) and text-to-speech (TTS) capabilities.
Uses the `SpeechRecognition` library for STT and `pyttsx3` for TTS.
Can be swapped for cloud-based providers (Google, Azure, Whisper) later.
"""

import os
import uuid
import tempfile
import speech_recognition as sr
import pyttsx3
from flask import current_app


class SpeechService:
    """Handles audio transcription and synthesis."""

    @staticmethod
    def speech_to_text(audio_file) -> str:
        """
        Transcribe an uploaded audio file to text.
        Accepts WAV files. For other formats, convert first.
        """
        recognizer = sr.Recognizer()

        # Save the uploaded file temporarily
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
        tmp_path = os.path.join(upload_dir, f"{uuid.uuid4().hex}.wav")
        audio_file.save(tmp_path)

        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "[Could not understand the audio]"
        except sr.RequestError as e:
            text = f"[Speech recognition error: {e}]"
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        return text

    @staticmethod
    def text_to_speech(text: str) -> str:
        """
        Synthesize text into a WAV audio file.
        Returns the path to the generated file.
        """
        output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}.wav")

        try:
            engine = pyttsx3.init()
            engine.save_to_file(text, output_path)
            engine.runAndWait()
        except Exception as e:
            # Fallback/Log the error when running on headless servers without voice engines
            current_app.logger.error(f"TTS synthesis failed (likely missing system speech drivers): {e}")
            # Create an empty or dummy wav file to prevent file-not-found crashes
            with open(output_path, "wb") as f:
                # Minimal 44-byte WAV header for an empty audio file
                f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')
        
        return output_path

