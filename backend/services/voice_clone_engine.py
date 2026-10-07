# -*- coding: utf-8 -*-
"""
Voice Clone & Neural Speech Engine for Pahadi AI Assistant
Powered by edge-tts (hi-IN-SwaraNeural & hi-IN-MadhurNeural) with Gemini Neural TTS and browser fallbacks.
Zero cloud costs and no API key required for natural Hindi-Pahadi voice output.
"""

import os
import sys
import json
import time
import uuid
import base64
import wave
import hashlib
import asyncio
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import edge_tts
except ImportError:
    edge_tts = None

# Locate project directories
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

CUSTOM_VOICE_DIR = PROJECT_ROOT / "custom_voice"
OUTPUTS_DIR = CUSTOM_VOICE_DIR / "outputs"
STATIC_AUDIO_DIR = PROJECT_ROOT / "static_audio"
REFERENCE_VOICE = CUSTOM_VOICE_DIR / "my_voice.wav"
PROFILE_PATH = CUSTOM_VOICE_DIR / "profile.json"

CUSTOM_VOICE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
STATIC_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Pre-calibrated Neural Voices
NEURAL_VOICES = {
    "swara": {
        "voice_id": "hi-IN-SwaraNeural",
        "name": "Swara",
        "displayName": "स्वरा - सौम्य व मधुर स्त्री स्वर (Swara Neural)",
        "gender": "female",
        "default_rate": "-6%",
        "default_pitch": "+0Hz"
    },
    "madhur": {
        "voice_id": "hi-IN-MadhurNeural",
        "name": "Madhur",
        "displayName": "मधुर - शांत व स्पष्ट पुरुष स्वर (Madhur Neural)",
        "gender": "male",
        "default_rate": "-4%",
        "default_pitch": "+0Hz"
    }
}

PLACEHOLDER_KEYS = {"MY_GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE", "<YOUR_KEY>", ""}


def load_gemini_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key and key not in PLACEHOLDER_KEYS:
        return key

    for env_path in [PROJECT_ROOT / ".env", CURRENT_DIR.parent / ".env", Path(".env")]:
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            clean_k = k.strip()
                            clean_v = v.strip().strip('"').strip("'")
                            if clean_k == "GEMINI_API_KEY" and clean_v not in PLACEHOLDER_KEYS:
                                os.environ["GEMINI_API_KEY"] = clean_v
                                return clean_v
            except Exception:
                pass
    return ""


def is_reference_voice_ready() -> bool:
    """Return True if user recorded audio sample exists and has valid size."""
    return REFERENCE_VOICE.exists() and REFERENCE_VOICE.stat().st_size > 1000


def get_voice_profile() -> Dict[str, Any]:
    """Load or initialize user voice profile metadata."""
    if PROFILE_PATH.exists():
        try:
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "voiceName": "hi-IN-SwaraNeural",
        "pitchHz": 220,
        "rate": "-6%",
        "pitch": "+0Hz",
        "calibratedAt": int(time.time()),
        "mode": "edge_tts_neural"
    }


def save_voice_profile(data: Dict[str, Any]) -> Dict[str, Any]:
    """Save updated voice profile preferences."""
    current = get_voice_profile()
    current.update(data)
    current["updatedAt"] = int(time.time())
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)
    return current


def get_voice_status() -> Dict[str, Any]:
    """Return voice clone status and metadata for the web dashboard."""
    ready = is_reference_voice_ready()
    profile = get_voice_profile()
    api_key = load_gemini_api_key()

    return {
        "hasVoice": ready,
        "voicePath": str(REFERENCE_VOICE) if ready else None,
        "voiceSizeBytes": REFERENCE_VOICE.stat().st_size if ready else 0,
        "engineLoaded": True,
        "hasEdgeTts": edge_tts is not None,
        "primaryVoice": "hi-IN-SwaraNeural",
        "hasApiKey": bool(api_key),
        "profile": profile,
        "availableVoices": [
            {"code": k, "voiceId": v["voice_id"], "displayName": v["displayName"], "gender": v["gender"]}
            for k, v in NEURAL_VOICES.items()
        ],
        "engineError": None
    }


async def _generate_edge_tts_async(text: str, voice: str, rate: str, pitch: str, out_path: str) -> None:
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    await communicate.save(out_path)


def synthesize(
    text: str,
    language: str = "hi",
    voice_name: Optional[str] = None,
    rate: str = "-6%",
    pitch: str = "+0Hz"
) -> Dict[str, Any]:
    """
    Synthesize speech using Microsoft hi-IN-SwaraNeural via edge-tts (or Gemini Neural TTS fallback).
    Returns dictionary with audio URL and metadata.
    """
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Text cannot be empty")

    profile = get_voice_profile()
    voice = voice_name or profile.get("voiceName") or "hi-IN-SwaraNeural"
    if voice in NEURAL_VOICES:
        voice = NEURAL_VOICES[voice]["voice_id"]
    if not voice.startswith("hi-IN"):
        voice = "hi-IN-SwaraNeural"

    # Compute cache key from text and voice parameters
    cache_key = f"{clean_text}_{voice}_{rate}_{pitch}"
    text_hash = hashlib.md5(cache_key.encode("utf-8")).hexdigest()
    output_filename = f"voice_{text_hash[:10]}.mp3"

    # Primary destination in static_audio and outputs
    static_file_path = STATIC_AUDIO_DIR / output_filename
    outputs_file_path = OUTPUTS_DIR / output_filename

    # If cached, return immediately
    if static_file_path.exists() and static_file_path.stat().st_size > 1000:
        return {
            "success": True,
            "status": "success",
            "audio_url": f"/audio/{output_filename}",
            "audioUrl": f"/audio/{output_filename}",
            "voice": voice,
            "cached": True
        }

    # 1. Try edge-tts synthesis (Primary High-Fidelity Neural Voice)
    if edge_tts:
        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Running inside an existing event loop (e.g., FastAPI / uvicorn)
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as pool:
                        pool.submit(asyncio.run, _generate_edge_tts_async(clean_text, voice, rate, pitch, str(static_file_path))).result()
                else:
                    loop.run_until_complete(_generate_edge_tts_async(clean_text, voice, rate, pitch, str(static_file_path)))
            except RuntimeError:
                asyncio.run(_generate_edge_tts_async(clean_text, voice, rate, pitch, str(static_file_path)))

            if static_file_path.exists() and static_file_path.stat().st_size > 500:
                # Also copy to outputs dir
                try:
                    import shutil
                    shutil.copy2(static_file_path, outputs_file_path)
                except Exception:
                    pass

                return {
                    "success": True,
                    "status": "success",
                    "audio_url": f"/audio/{output_filename}",
                    "audioUrl": f"/audio/{output_filename}",
                    "voice": voice,
                    "cached": False
                }
        except Exception as e:
            print(f"Notice: edge-tts generation exception: {e}")

    # 2. Fallback: Gemini Neural Speech API if API Key is present
    api_key = load_gemini_api_key()
    if api_key:
        tts_models = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]
        for model_name in tts_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [{"text": f"Read the following text aloud with natural warmth:\n\n{clean_text}"}]
                    }
                ],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": "kore"
                            }
                        }
                    }
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=25) as resp:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    candidates = resp_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            inline_data = parts[0].get("inlineData", {})
                            b64_audio = inline_data.get("data", "")
                            if b64_audio:
                                pcm_bytes = base64.b64decode(b64_audio)
                                wav_file = STATIC_AUDIO_DIR / f"voice_{text_hash[:10]}.wav"
                                with wave.open(str(wav_file), "wb") as wf:
                                    wf.setnchannels(1)
                                    wf.setsampwidth(2)
                                    wf.setframerate(24000)
                                    wf.writeframes(pcm_bytes)
                                return {
                                    "success": True,
                                    "status": "success",
                                    "audio_url": f"/audio/{wav_file.name}",
                                    "audioUrl": f"/audio/{wav_file.name}",
                                    "voice": "gemini-neural",
                                    "cached": False
                                }
            except Exception:
                continue

    # 3. Browser fallback
    return {
        "success": False,
        "status": "fallback",
        "fallbackBrowser": True,
        "error": "Using browser Web Speech API fallback.",
        "profile": profile
    }


if __name__ == "__main__":
    print(f"Voice Engine Status: {json.dumps(get_voice_status(), indent=2)}")
    test_res = synthesize("नमस्ते जी! पहाड़ी संगम AI में आपका स्वागत है।")
    print(f"Test Synthesis Result: {json.dumps(test_res, indent=2)}")
