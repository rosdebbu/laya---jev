"""
Sarvam AI (India's Sovereign Indic AI) Integration Module for KisanZess.
Provides high-fidelity Indic Speech-to-Text (Saaras:v1), Text-to-Speech (Bulbul:v1),
and Vernacular Translation (Mayura:v1) across 10+ Indian languages:
Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia.
"""

from __future__ import annotations
import os
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("reflex_agent.sarvam")

# Official Sarvam AI Language Codes & Display Names
SUPPORTED_INDIC_LANGUAGES: Dict[str, Dict[str, str]] = {
    "hi-IN": {"name": "Hindi", "native": "हिन्दी", "script": "Devanagari", "default_speaker": "meera"},
    "bn-IN": {"name": "Bengali", "native": "বাংলা", "script": "Bengali", "default_speaker": "ananya"},
    "ta-IN": {"name": "Tamil", "native": "தமிழ்", "script": "Tamil", "default_speaker": "meera"},
    "te-IN": {"name": "Telugu", "native": "తెలుగు", "script": "Telugu", "default_speaker": "meera"},
    "mr-IN": {"name": "Marathi", "native": "मराठी", "script": "Devanagari", "default_speaker": "meera"},
    "gu-IN": {"name": "Gujarati", "native": "ગુજરાતી", "script": "Gujarati", "default_speaker": "meera"},
    "pa-IN": {"name": "Punjabi", "native": "ਪੰਜਾਬੀ", "script": "Gurmukhi", "default_speaker": "arvind"},
    "kn-IN": {"name": "Kannada", "native": "ಕನ್ನಡ", "script": "Kannada", "default_speaker": "meera"},
    "ml-IN": {"name": "Malayalam", "native": "മലയാളം", "script": "Malayalam", "default_speaker": "meera"},
    "od-IN": {"name": "Odia", "native": "ଓଡ଼ିଆ", "script": "Odia", "default_speaker": "meera"},
    "en-IN": {"name": "Indian English", "native": "English", "script": "Latin", "default_speaker": "arvind"},
}


class SarvamSpeechEngine:
    """
    Client for Sarvam AI Sovereign Indic Voice and Translation APIs.
    Gracefully falls back to browser/local speech synthesis when API key is not supplied.
    """

    API_BASE = "https://api.sarvam.ai"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SARVAM_API_KEY", "")
        self.has_key = bool(self.api_key.strip())

    def text_to_speech(
        self,
        text: str,
        language_code: str = "hi-IN",
        speaker: Optional[str] = None,
        pace: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Synthesize speech using Sarvam Bulbul:v1 Indic TTS model.
        Returns base64 WAV audio bytes.
        """
        start = time.perf_counter()
        lang_info = SUPPORTED_INDIC_LANGUAGES.get(language_code, SUPPORTED_INDIC_LANGUAGES["hi-IN"])
        chosen_speaker = speaker or lang_info["default_speaker"]

        if not self.has_key:
            return {
                "success": False,
                "provider": "client_fallback",
                "message": "SARVAM_API_KEY not set. Using native Indic browser Web Speech synthesis.",
                "language_code": language_code,
                "speaker": chosen_speaker,
                "text": text,
                "elapsed_ms": 0.0,
            }

        try:
            import httpx
            # Truncate to maximum permissible character length for single utterance if needed
            truncated_text = text[:500]

            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "inputs": [truncated_text],
                "target_language_code": language_code,
                "speaker": chosen_speaker,
                "pitch": 0,
                "pace": pace,
                "loudness": 1.5,
                "speech_sample_rate": 8000,
                "enable_preprocessing": True,
                "model": "bulbul:v1",
            }

            with httpx.Client(timeout=8.0) as client:
                res = client.post(f"{self.API_BASE}/text-to-speech", json=payload, headers=headers)
                elapsed = (time.perf_counter() - start) * 1000.0

                if res.status_code == 200:
                    data = res.json()
                    audios = data.get("audios", [])
                    audio_b64 = audios[0] if audios else None
                    return {
                        "success": True,
                        "provider": "sarvam_ai",
                        "model": "bulbul:v1",
                        "audio_base64": audio_b64,
                        "language_code": language_code,
                        "speaker": chosen_speaker,
                        "elapsed_ms": round(elapsed, 1),
                    }
                else:
                    logger.warning(f"Sarvam TTS failed with status {res.status_code}: {res.text}")
                    return {
                        "success": False,
                        "provider": "client_fallback",
                        "error": f"Sarvam API error: {res.status_code}",
                        "language_code": language_code,
                    }

        except Exception as e:
            logger.error(f"Sarvam TTS exception: {e}")
            return {
                "success": False,
                "provider": "client_fallback",
                "error": str(e),
                "language_code": language_code,
            }

    def speech_to_text(
        self,
        audio_file_path_or_bytes: Any,
        language_code: str = "hi-IN",
    ) -> Dict[str, Any]:
        """
        Transcribe audio using Sarvam Saaras:v1 Indic Speech-to-Text model.
        """
        start = time.perf_counter()
        if not self.has_key:
            return {
                "success": False,
                "provider": "client_fallback",
                "message": "SARVAM_API_KEY not configured. Use browser Web Speech Recognition.",
            }

        try:
            import httpx
            headers = {"api-subscription-key": self.api_key}
            files = {"file": audio_file_path_or_bytes}
            data = {"model": "saaras:v1", "language_code": language_code}

            with httpx.Client(timeout=10.0) as client:
                res = client.post(
                    f"{self.API_BASE}/speech-to-text",
                    files=files,
                    data=data,
                    headers=headers,
                )
                elapsed = (time.perf_counter() - start) * 1000.0
                if res.status_code == 200:
                    transcription = res.json().get("transcript", "")
                    return {
                        "success": True,
                        "provider": "sarvam_ai",
                        "model": "saaras:v1",
                        "transcript": transcription,
                        "language_code": language_code,
                        "elapsed_ms": round(elapsed, 1),
                    }
                return {"success": False, "error": res.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def translate(
        self,
        text: str,
        source_language_code: str = "en-IN",
        target_language_code: str = "hi-IN",
    ) -> Dict[str, Any]:
        """
        Translate vernacular text using Sarvam Mayura:v1.
        """
        start = time.perf_counter()
        if not self.has_key:
            return {
                "success": False,
                "provider": "client_fallback",
                "translated_text": text,
                "message": "SARVAM_API_KEY not set",
            }

        try:
            import httpx
            headers = {
                "api-subscription-key": self.api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "input": text,
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
                "model": "mayura:v1",
                "speaker_gender": "Female",
                "mode": "formal",
            }
            with httpx.Client(timeout=6.0) as client:
                res = client.post(f"{self.API_BASE}/translate", json=payload, headers=headers)
                elapsed = (time.perf_counter() - start) * 1000.0
                if res.status_code == 200:
                    out = res.json().get("translated_text", text)
                    return {
                        "success": True,
                        "translated_text": out,
                        "elapsed_ms": round(elapsed, 1),
                    }
                return {"success": False, "translated_text": text, "error": res.text}
        except Exception as e:
            return {"success": False, "translated_text": text, "error": str(e)}
