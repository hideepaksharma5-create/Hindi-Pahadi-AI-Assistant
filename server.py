# -*- coding: utf-8 -*-
"""
Pahadi AI Assistant - FastAPI & Edge-TTS Neural Audio Server
Serves high-fidelity neural speech (hi-IN-SwaraNeural) and all assistant APIs.
"""

import os
import sys
import uuid
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List

# Add workspace directory to path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    import edge_tts
except ImportError:
    edge_tts = None

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Internal engine & data imports
from backend.data.pahadi_dict import (
    DIALECTS,
    EMERGENCY_CONTACTS,
    KNOWLEDGE_TOPICS,
    CURATED_PHRASES,
    CULTURAL_STORIES,
    get_dialect_meta,
)
from backend.services.engine import (
    get_gemini_api_key,
    save_gemini_api_key,
    translate,
    chat,
)
from backend.ui.index_html import INDEX_HTML

app = FastAPI(title="Hindi-Pahadi AI Audio Engine & Assistant")

# Allow Web requests & CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = BASE_DIR / "static_audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/audio", StaticFiles(directory=str(AUDIO_DIR)), name="audio")


class TTSRequest(BaseModel):
    text: str
    rate: str = "-6%"   # Slightly slower pace matches gentle storytelling cadence
    pitch: str = "+0Hz"
    voice: Optional[str] = "hi-IN-SwaraNeural"


class ChatRequest(BaseModel):
    message: str
    dialect: Optional[str] = "kangri"
    mode: Optional[str] = "standard"
    history: Optional[List[Dict[str, Any]]] = []


class TranslateRequest(BaseModel):
    query: str
    dialect: Optional[str] = "kangri"
    isReverse: Optional[bool] = False


class SetKeyRequest(BaseModel):
    key: str


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return HTMLResponse(content=INDEX_HTML)


@app.get("/manifest.json")
async def get_manifest():
    return {
        "name": "हिमाचल AI - Pahadi AI Assistant",
        "short_name": "Pahadi AI",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#090d16",
        "theme_color": "#090d16",
        "description": "हिमाचली और हिन्दी AI सहायक व अनुवादक"
    }


@app.get("/api/status")
async def get_status():
    key = get_gemini_api_key()
    return {
        "hasKey": bool(key),
        "online": bool(key),
        "ttsEngine": "edge-tts (hi-IN-SwaraNeural)" if edge_tts else "browser-fallback"
    }


@app.get("/api/dialects")
async def get_dialects():
    return DIALECTS


@app.get("/api/phrases")
async def get_phrases():
    return CURATED_PHRASES


@app.get("/api/stories")
async def get_stories():
    return CULTURAL_STORIES


@app.get("/api/emergency")
async def get_emergency():
    return EMERGENCY_CONTACTS


@app.get("/api/knowledge")
async def get_knowledge():
    return KNOWLEDGE_TOPICS


@app.post("/api/tts")
async def generate_speech(req: TTSRequest):
    clean_text = req.text.strip()
    if not clean_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    if not edge_tts:
        raise HTTPException(
            status_code=500,
            detail="edge-tts package is not installed. Run: pip install edge-tts"
        )

    # Voice selection: default hi-IN-SwaraNeural (female), option for hi-IN-MadhurNeural (male)
    voice = req.voice or "hi-IN-SwaraNeural"
    file_name = f"voice_{uuid.uuid4().hex[:8]}.mp3"
    file_path = str(AUDIO_DIR / file_name)

    try:
        communicate = edge_tts.Communicate(
            text=clean_text,
            voice=voice,
            rate=req.rate,
            pitch=req.pitch
        )
        await communicate.save(file_path)

        return {
            "status": "success",
            "audio_url": f"/audio/{file_name}",
            "voice": voice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation error: {str(e)}")


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    reply = chat(req.history or [], req.message, req.mode or "standard", req.dialect or "kangri")
    return {"reply": reply}


@app.post("/api/translate")
async def api_translate(req: TranslateRequest):
    res = translate(req.query, req.dialect or "kangri", req.isReverse or False)
    return res


@app.post("/api/set-key")
async def api_set_key(req: SetKeyRequest):
    success = save_gemini_api_key(req.key)
    if success:
        return {"success": True}
    return JSONResponse(status_code=400, content={"success": False, "error": "अमान्य API Key"})


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print("=" * 64)
    print("  🏔️  Himachal AI Assistant & Neural Voice Server Running!")
    print(f"  👉 Web App URL: http://localhost:{port}")
    print("  🎙️  TTS Model: Microsoft hi-IN-SwaraNeural")
    print("=" * 64)
    uvicorn.run(app, host="0.0.0.0", port=port)
