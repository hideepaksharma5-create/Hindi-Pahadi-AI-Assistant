# -*- coding: utf-8 -*-
"""
Pahadi AI Assistant - AI Inference & Prompt Engine
Handles Gemini API integration, prompt orchestration, dialect translation,
conversational intelligence with multiple persona modes, and fallback handling.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any, List, Optional

# Optional imports with graceful fallbacks
try:
    import requests  # type: ignore
except ImportError:
    requests = None

try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    load_dotenv = None

# Local data imports
from backend.data.pahadi_dict import (
    DIALECTS,
    get_dialect_meta,
    offline_translate,
)

# Voice engine import
try:
    from backend.services import voice_clone_engine
except ImportError:
    try:
        import voice_clone_engine
    except ImportError:
        voice_clone_engine = None

PLACEHOLDER_KEYS = {"MY_GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE", "<YOUR_KEY>", ""}

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_env_file():
    """Load GEMINI_API_KEY from environment or .env file."""
    if load_dotenv:
        load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
        load_dotenv(dotenv_path=Path(".env"))

    candidate_paths = [
        PROJECT_ROOT / ".env",
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env"
    ]
    for p in candidate_paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            clean_k = k.strip()
                            clean_v = v.strip().strip('"').strip("'")
                            if clean_v and clean_v not in PLACEHOLDER_KEYS:
                                os.environ[clean_k] = clean_v
            except Exception:
                pass


def get_gemini_api_key() -> str:
    """Retrieve verified Gemini API key or empty string."""
    load_env_file()
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    return "" if key in PLACEHOLDER_KEYS else key


def save_gemini_api_key(new_key: str) -> bool:
    """Persist new API key to runtime environment and .env file."""
    clean_key = new_key.strip()
    if not clean_key or clean_key in PLACEHOLDER_KEYS:
        return False

    os.environ["GEMINI_API_KEY"] = clean_key
    env_paths = [PROJECT_ROOT / ".env", Path(".env")]
    for env_path in env_paths:
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"# Pahadi AI Assistant Configuration\nGEMINI_API_KEY={clean_key}\n")
            return True
        except Exception:
            continue
    return True


load_env_file()

# Active Gemini models in preference order
CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-1.5-flash"
]


def extract_json(raw_text: str) -> Dict[str, Any]:
    """Robustly extracts JSON from LLM response, stripping markdown code blocks if present."""
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        raise


def call_gemini_api(prompt: str, system_prompt: str, json_mode: bool = False) -> str:
    """
    Call Gemini Generative Language API with multiple model fallbacks.
    Works seamlessly with requests or standard library urllib.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured")

    last_err = None

    for model in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload: Dict[str, Any] = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ],
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "temperature": 0.35
            }
        }
        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"

        # 1. Try requests library
        if requests:
            try:
                resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
                if resp.status_code in (404, 429, 503):
                    last_err = Exception(f"HTTP {resp.status_code}: {resp.text}")
                    continue
                resp.raise_for_status()
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return ""
            except Exception as e:
                last_err = e
                continue

        # 2. Standard library urllib fallback
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if not candidates:
                    return ""
                parts = candidates[0].get("content", {}).get("parts", [])
                if not parts:
                    return ""
                return parts[0].get("text", "")
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (404, 503, 429):
                continue
            raise
        except Exception as e:
            last_err = e
            continue

    if last_err:
        raise last_err
    return ""


def gemini_translate(source_text: str, dialect_code: str, is_reverse: bool = False) -> Dict[str, Any]:
    """
    Perform authentic dialect translation via Gemini with strict structured JSON output.
    """
    dialect = get_dialect_meta(dialect_code)
    system_instruction = """
    You are a master linguistic expert in Himalayan Pahadi languages:
    - Himachal varieties: Shimla/Mahasuvi (शिमला पहाड़ी), Mandeali (मंडीयाली), Kangri (कांगड़ी), Kullui (कुल्लवी), Chambeali (चम्बियाली), Sirmauri (सिरमौरी).
    - Uttarakhand varieties: Garhwali (गढ़वाली), Kumaoni (कुमाऊँनी), Jaunsari (जौनसारी).
    - Dogri (डोगरी).
    
    You distinguish each distinct dialect accurately instead of treating all Pahadi as one.
    Translate accurately with authentic vocabulary, Devanagari script, Roman transliteration, and cultural context.
    
    Respond ONLY with a valid JSON object strictly formatted as:
    {
        "translatedText": "Translated sentence in Devanagari (Clean Hindi if translating from Pahadi, or authentic Dialect if translating to Pahadi)",
        "phoneticText": "Accurate Roman English phonetic transliteration",
        "culturalContext": "Why locals phrase it this way, explanation of dialect words, grammar, and cultural nuance",
        "etiquetteTip": "Social etiquette and respectful advice for conversation",
        "regionalVariation": "Specific valley or district nuance (e.g. Kangra, Mandi, Kullu, Shimla)",
        "exampleUsage": "Natural example sentence in the dialect"
    }
    """

    if is_reverse:
        prompt = f"""
        The following text is in the Pahadi dialect: {dialect['displayNameHindi']} ({dialect['displayNameEnglish']} - {dialect['region']}).
        Translate this authentic Pahadi dialect text accurately into natural, clean standard Hindi (मानक हिंदी).
        In culturalContext, explain the meaning of any unique Pahadi words, dialect grammar patterns, or idioms used.
        Pahadi Text: "{source_text}"
        """
    else:
        prompt = f"""
        Translate the following text from Hindi to {dialect['displayNameHindi']} ({dialect['displayNameEnglish']}):
        "{source_text}"
        """

    raw_json = call_gemini_api(prompt, system_instruction, json_mode=True)
    try:
        parsed = extract_json(raw_json)
    except Exception:
        parsed = {}

    return {
        "sourceText": source_text,
        "sourceLanguage": f"{dialect['displayNameHindi']} (पहाड़ी)" if is_reverse else "Hindi",
        "targetDialect": dialect_code,
        "translatedText": parsed.get("translatedText", source_text),
        "phoneticText": parsed.get("phoneticText", ""),
        "culturalContext": parsed.get("culturalContext", "पहाड़ी भाषा और संस्कृति का सुंदर स्वरूप।"),
        "etiquetteTip": parsed.get("etiquetteTip", "बातचीत में आदर और 'जी' का प्रयोग करें।"),
        "regionalVariation": parsed.get("regionalVariation", dialect["region"]),
        "exampleUsage": parsed.get("exampleUsage", ""),
        "isAiPowered": True
    }


def gemini_chat(history: List[Dict[str, Any]], user_msg: str, mode: str, dialect_code: str) -> str:
    """
    Conversational engine with persona-tailored prompts (Elder, Student, Farmer, Standard)
    and voice/TTS cadence optimizations.
    """
    dialect = get_dialect_meta(dialect_code)
    mode_instructions = {
        "elder": "MODE: ELDER FRIENDLY (बुजुर्ग मित्र मोड)\n- Speak with deep warmth, respect, and reassuring simplicity using traditional greetings like 'पैलाग जी', 'नमस्कार जी', 'जय देव जी'. Keep sentences concise, gentle, and easily spoken aloud.",
        "student": "MODE: STUDENT HELPER (छात्र सहायक मोड)\n- Explain concepts clearly with structured points, bilingual English ↔ Hindi/Pahadi terminology, and easy-to-understand examples.",
        "farmer": "MODE: FARMER & ORCHARD HELPER (किसान व बागवान मित्र)\n- Provide expert horticultural advice on apple orchards (winter pruning, Royal Delicious/Gala varieties, Scab and Canker control, chilling hours, anti-hail net subsidy, Himcare, and SPNF natural farming).",
        "standard": "MODE: ALL-ROUND HIMALAYAN AI ASSISTANT\n- Guide with general inquiries, HRTC bus routes, weather and travel safety, cultural folklore, and living traditions across Himachal and Uttarakhand."
    }
    mode_inst = mode_instructions.get(mode, mode_instructions["standard"])

    system_prompt = f"""
    You are 'हिमाचली व हिन्दी AI सहायक' (Pahadi-Hindi AI Assistant) — a culturally attuned, intelligent companion designed for native Hindi speakers and the communities of Himachal Pradesh and Uttarakhand.
    Active Regional Context: {dialect['displayNameHindi']} ({dialect['region']}, {dialect['state']}).

    Core Behavioral Guidelines:
    1. Tone & Persona:
       - Calm, respectful, and articulate, reminiscent of an authentic Himalayan storyteller.
       - Grounded, polite, and hospitable ('मिठास' और 'सत्कार').
       - Avoid robotic jargon or unnatural machine translations.

    2. Language & Dialect Adaptability:
       - When addressed in Hindi: Respond in refined, natural Standard Hindi (खड़ी बोली/मानक हिन्दी).
       - When a specific Pahadi dialect is active ({dialect['code']}):
         * Mahasuvi / Shimla: Reflect Upper/Middle Himachal phrasing ('आपु', 'स्युब', 'के हाल च').
         * Mandyali: Use authentic Mandi valley lexicon ('तुसां', 'किहां', 'आसां', 'भल-भलाई').
         * Kangri: Use Kangra / Lower Himachal nuances ('मिंजो-तिंजो', 'कुथी चले', 'तुहाड़ा').
         * Kulvi: Incorporate Kullu valley expressions ('जय देव जी', 'हौ', 'राजी-खुशी').
         * Garhwali / Kumaoni: Use Uttarakhand expressions ('पैलाग', 'दगड़्या', 'भल छौ').
       - When mixed (Hinglish or colloquial): Understand smoothly and reply in clear Devanagari script.

    3. Optimization for Voice & Text-to-Speech (TTS):
       - Keep sentences fluid, rhythmic, and natural to read aloud.
       - Punctuate carefully with commas and full stops (।) for natural breath pauses.
       - Avoid long nested bullet points when conversational prose sounds better spoken.
       - Avoid placing emojis inside spoken sentences so neural voice engines pronounce speech smoothly.

    4. Cultural Nuance:
       - Honor local geography, agriculture, apple orchard cycles, festivals (Kullu Dussehra, Minjar, Mandi Shivratri, Phooldei), and dev-sanskriti.
       - {mode_inst}
    """

    history_text = ""
    for msg in history[-6:]:
        role = "User" if msg.get("isUser") or msg.get("role") == "user" else "Assistant"
        history_text += f"{role}: {msg.get('text', '')}\n"

    full_prompt = f"{history_text}User: {user_msg}\nAssistant:"
    return call_gemini_api(full_prompt, system_prompt)


def translate(query: str, dialect_code: str = "kangri", is_reverse: bool = False) -> Dict[str, Any]:
    """
    Unified translation interface: attempts online Gemini translation first,
    smoothly falls back to local dictionary heuristics if offline or without API key.
    """
    key = get_gemini_api_key()
    if key:
        try:
            return gemini_translate(query, dialect_code, is_reverse)
        except Exception as e:
            print(f"Gemini translation failed, using offline fallback: {e}")
    return offline_translate(query, dialect_code, is_reverse)


def chat(history: List[Dict[str, Any]], message: str, mode: str = "standard", dialect_code: str = "kangri") -> str:
    """
    Unified chat interface: queries Gemini LLM when online, or produces
    informative contextual guidance in offline mode.
    """
    key = get_gemini_api_key()
    if key:
        try:
            return gemini_chat(history, message, mode, dialect_code)
        except Exception as e:
            print(f"Gemini chat failed, using offline message: {e}")

    dialect = get_dialect_meta(dialect_code)
    
    # Offline contextual responses
    msg_lower = message.lower()
    if any(w in msg_lower for w in ["सेब", "apple", "प्रूनिंग", "pruning", "बागवान", "farming"]):
        return (
            f"नमस्कार जी! ({dialect['displayNameHindi']})\n\n"
            f"हिमाचल में सेब के बगीचों के लिए आवश्यक सलाह:\n"
            f"1. प्रूनिंग (काट-छांट): दिसंबर से फरवरी के बीच जब पेड़ सुप्तावस्था (dormancy) में हों।\n"
            f"2. चिलिंग आवर्स: उच्च गुणवत्ता के लिए 800 से 1200 घंटे 7°C से कम तापमान आवश्यक है।\n"
            f"3. रोग नियंत्रण: स्कैब और कैंकर से बचाव हेतु कॉपर ऑक्सीक्लोराइड व बोर्डो मिश्रण का प्रयोग करें।\n"
            f"4. योजनाएं: उद्यान विभाग द्वारा एंटी-हेल नेट और प्राकृतिक खेती (SPNF) पर अनुदान उपलब्ध है।"
        )
    elif any(w in msg_lower for w in ["hrtc", "बस", "bus", "मार्ग", "रूट"]):
        return (
            f"नमस्कार जी!\n\n"
            f"एचआरटीसी (HRTC) बस सेवा संबंधी जानकारी:\n"
            f"• 24x7 पूछताछ एवं नियंत्रण कक्ष: 0177-2803017\n"
            f"• आईएसबीटी शिमला: 0177-2658322\n"
            f"• ऑनलाइन बुकिंग: hrtchp.com या HRTC मोबाइल ऐप\n"
            f"• विशेष सुविधा: हिमाचल राज्य के भीतर महिलाओं को सामान्य बसों के किराये में 50% की छूट दी जाती है।"
        )

    return (
        f"नमस्कार जी! ({dialect['displayNameHindi']})\n\n"
        f"आपका संदेश प्राप्त हुआ: \"{message}\"।\n\n"
        f"वर्तमान में AI सेवा ऑफ़लाइन मोड में संचालित है। "
        f"ऑनलाइन संवादी AI (Gemini AI) को सक्रिय करने के लिए सेटिंग्स में जाकर अपनी Gemini API Key दर्ज करें। "
        f"तब तक आप अनुवादक, शब्दकोश, आपातकालीन हेल्पलाइन और लोक कथाओं का पूर्ण आनंद ले सकते हैं!"
    )
