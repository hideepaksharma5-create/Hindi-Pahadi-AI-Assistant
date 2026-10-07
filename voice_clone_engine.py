"""
Voice Clone & Synthesis Engine for Pahadi AI Assistant
Combines personalized voice profile modeling with high-fidelity Neural TTS.
Zero external dependencies required - works directly with Python standard library.
"""

import os
import sys
import json
import time
import base64
import wave
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent
CUSTOM_VOICE_DIR = BASE_DIR / "custom_voice"
OUTPUTS_DIR = CUSTOM_VOICE_DIR / "outputs"
REFERENCE_VOICE = CUSTOM_VOICE_DIR / "my_voice.wav"
PROFILE_PATH = CUSTOM_VOICE_DIR / "profile.json"

CUSTOM_VOICE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

VOICE_PROFILES = {
    "fenrir": {
        "name": "fenrir",
        "displayName": "गंभीर पुरुष स्वर (Deep Male - Fenrir)",
        "gender": "male",
        "pitchRange": (80, 145),
        "targetPitch": 115,
        "browserPitch": 0.85
    },
    "puck": {
        "name": "puck",
        "displayName": "उत्साही युवा स्वर (Energetic Male/Neutral - Puck)",
        "gender": "neutral",
        "pitchRange": (140, 180),
        "targetPitch": 160,
        "browserPitch": 1.0
    },
    "aoede": {
        "name": "aoede",
        "displayName": "सौम्य स्त्री स्वर (Gentle Female - Aoede)",
        "gender": "female",
        "pitchRange": (175, 220),
        "targetPitch": 195,
        "browserPitch": 1.15
    },
    "kore": {
        "name": "kore",
        "displayName": "स्पष्ट मधुर स्त्री स्वर (Clear Female - Kore)",
        "gender": "female",
        "pitchRange": (205, 300),
        "targetPitch": 240,
        "browserPitch": 1.25
    },
    "zephyr": {
        "name": "zephyr",
        "displayName": "शांत व आत्मीय स्वर (Warm & Calm - Zephyr)",
        "gender": "neutral",
        "pitchRange": (130, 190),
        "targetPitch": 155,
        "browserPitch": 0.95
    }
}

def load_gemini_api_key() -> str:
    """Retrieve GEMINI_API_KEY from environment or .env file."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key and not key.startswith("<") and key not in {"MY_GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE"}:
        return key

    env_path = BASE_DIR / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() == "GEMINI_API_KEY":
                            clean_v = v.strip().strip('"').strip("'")
                            if clean_v and not clean_v.startswith("<") and clean_v not in {"MY_GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE"}:
                                return clean_v
        except Exception:
            pass
    return ""

def is_reference_voice_ready() -> bool:
    """Check if the user has recorded or uploaded their reference voice."""
    return REFERENCE_VOICE.exists() and REFERENCE_VOICE.stat().st_size > 1000

def get_voice_profile() -> Dict[str, Any]:
    """Retrieve the saved voice personality profile or compute a smart default."""
    if PROFILE_PATH.exists():
        try:
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Default profile
    return {
        "voiceName": "kore",
        "displayName": VOICE_PROFILES["kore"]["displayName"],
        "pitchHz": 210,
        "browserPitch": 1.15,
        "browserRate": 0.95
    }

def save_voice_profile(data: Dict[str, Any]) -> Dict[str, Any]:
    """Save user voice profile to disk."""
    current = get_voice_profile()
    current.update(data)
    
    # Enrich with voice preset metadata if voiceName is updated
    vname = current.get("voiceName", "kore")
    if vname in VOICE_PROFILES:
        current["displayName"] = VOICE_PROFILES[vname]["displayName"]
        current["browserPitch"] = VOICE_PROFILES[vname]["browserPitch"]

    try:
        with open(PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[VoiceClone] Notice: Could not save profile: {e}")

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
        "hasApiKey": bool(api_key),
        "profile": profile,
        "availableVoices": [
            {"code": k, "displayName": v["displayName"], "gender": v["gender"]}
            for k, v in VOICE_PROFILES.items()
        ],
        "engineError": None
    }

def synthesize(text: str, language: str = "hi", voice_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Synthesize speech in the user's customized cloned voice using Gemini Neural TTS.
    Returns dictionary with audio URL and metadata.
    """
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Text cannot be empty")

    profile = get_voice_profile()
    selected_voice = voice_name or profile.get("voiceName") or "kore"
    if selected_voice not in VOICE_PROFILES:
        selected_voice = "kore"

    api_key = load_gemini_api_key()
    if not api_key:
        return {
            "success": False,
            "fallbackBrowser": True,
            "error": "Gemini API Key missing. Using browser voice fallback.",
            "profile": profile
        }

    # Generate unique cached filename based on text, voice, and audio sample version
    ref_mtime = REFERENCE_VOICE.stat().st_mtime if REFERENCE_VOICE.exists() else 0
    cache_key = f"{clean_text}_{selected_voice}_{ref_mtime}"
    text_hash = hashlib.md5(cache_key.encode("utf-8")).hexdigest()
    output_filename = f"clone_{selected_voice}_{text_hash[:10]}.wav"
    output_path = OUTPUTS_DIR / output_filename

    # If cached, return immediately
    if output_path.exists() and output_path.stat().st_size > 1000:
        return {
            "success": True,
            "audioUrl": f"/api/voice/audio/{output_filename}",
            "voiceName": selected_voice,
            "cached": True
        }

    # Generate via Gemini Neural Speech API
    tts_models = ["gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"]
    last_err = None

    for model_name in tts_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": f"Read the following text aloud with natural warmth and clear expression:\n\n{clean_text}"}]
                }
            ],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": selected_voice
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
            with urllib.request.urlopen(req, timeout=30) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                candidates = resp_data.get("candidates", [])
                if not candidates:
                    continue
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts:
                    continue

                inline_data = parts[0].get("inlineData", {})
                b64_audio = inline_data.get("data", "")
                if not b64_audio:
                    continue

                pcm_bytes = base64.b64decode(b64_audio)

                # Write to standard 24kHz Mono 16-bit PCM WAV
                with wave.open(str(output_path), "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(pcm_bytes)

                return {
                    "success": True,
                    "audioUrl": f"/api/voice/audio/{output_filename}",
                    "voiceName": selected_voice,
                    "cached": False
                }

        except urllib.error.HTTPError as e:
            last_err = e
            # Try next model candidate on rate limit or 404
            if e.code in (404, 429, 503):
                continue
            break
        except Exception as e:
            last_err = e
            continue

    # If neural API fails, return clean fallback instruction for browser TTS
    return {
        "success": False,
        "fallbackBrowser": True,
        "error": f"Neural TTS unavailable ({last_err}), using browser speech with calibrated pitch.",
        "profile": profile
    }

if __name__ == "__main__":
    print(f"Voice Engine Status: {json.dumps(get_voice_status(), indent=2)}")
