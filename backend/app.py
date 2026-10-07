#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pahadi AI Assistant (पहाड़ी संगम) - Main Application Server & UI
Connects data repositories, the AI inference engine, and the client UI.
Runs directly on the Python standard library or with optional Streamlit/FastAPI integration.
"""

import os
import sys
import json
import http.server
import socketserver
import webbrowser
from pathlib import Path
from typing import Dict, Any, List

# Reconfigure stdout/stderr encodings for Windows CMD / PowerShell
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure parent and project root are in sys.path
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Regional data imports
from backend.data.pahadi_dict import (
    DIALECTS,
    EMERGENCY_CONTACTS,
    KNOWLEDGE_TOPICS,
    CURATED_PHRASES,
    CULTURAL_STORIES,
    get_dialect_meta,
    offline_translate,
)

# AI Engine imports
from backend.services.engine import (
    get_gemini_api_key,
    save_gemini_api_key,
    gemini_translate,
    gemini_chat,
    translate,
    chat,
)

# Voice Clone Engine
try:
    from backend.services import voice_clone_engine
except ImportError:
    try:
        import voice_clone_engine
    except ImportError:
        voice_clone_engine = None

# UI Template
from backend.ui.index_html import INDEX_HTML

PORT = 8080


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Multi-threaded TCP Server allowing concurrent client requests."""
    daemon_threads = True
    allow_reuse_address = True


class PahadiServerHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler for Pahadi AI Web Application and REST API."""

    def _send_data(self, data: bytes, content_type: str = "application/json", status: int = 200):
        self.send_response(status)
        self.send_header(
            "Content-Type",
            f"{content_type}; charset=utf-8" if "text" in content_type or "json" in content_type else content_type,
        )
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Connection", "close")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_json(self, data: Any, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self._send_data(body, "application/json", status)

    def _send_html(self, html_text: str, status: int = 200):
        body = html_text.encode("utf-8")
        self._send_data(body, "text/html", status)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        try:
            path = self.path.split("?")[0]
            if path in ["/", "/index.html"]:
                self._send_html(INDEX_HTML)
            elif path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
            elif path == "/api/dialects":
                self._send_json(DIALECTS)
            elif path == "/api/phrases":
                self._send_json(CURATED_PHRASES)
            elif path == "/api/stories":
                self._send_json(CULTURAL_STORIES)
            elif path == "/api/knowledge":
                self._send_json(KNOWLEDGE_TOPICS)
            elif path == "/api/emergency":
                self._send_json(EMERGENCY_CONTACTS)
            elif path == "/api/status":
                key = get_gemini_api_key()
                has_key = bool(key)
                self._send_json({"hasKey": has_key, "online": has_key})
            elif path == "/api/voice/status":
                st = voice_clone_engine.get_voice_status() if voice_clone_engine else {"hasVoice": False, "engineLoaded": False}
                self._send_json(st)
            elif path.startswith("/api/voice/audio/"):
                fname = os.path.basename(path)
                fpath = PROJECT_ROOT / "custom_voice" / "outputs" / fname
                if fpath.exists():
                    with open(fpath, "rb") as f:
                        self._send_data(f.read(), "audio/wav")
                else:
                    self._send_data(b"Audio Not Found", "text/plain", 404)
            elif path == "/api/voice/sample":
                fpath = PROJECT_ROOT / "custom_voice" / "my_voice.wav"
                if fpath.exists():
                    with open(fpath, "rb") as f:
                        self._send_data(f.read(), "audio/wav")
                else:
                    self._send_data(b"Sample Not Found", "text/plain", 404)
            elif path.startswith("/audio/"):
                fname = os.path.basename(path)
                fpath = PROJECT_ROOT / "static_audio" / fname
                if not fpath.exists():
                    fpath = PROJECT_ROOT / "custom_voice" / "outputs" / fname
                if fpath.exists():
                    mime = "audio/mpeg" if fname.endswith(".mp3") else "audio/wav"
                    with open(fpath, "rb") as f:
                        self._send_data(f.read(), mime)
                else:
                    self._send_data(b"Audio Not Found", "text/plain", 404)
            elif path == "/manifest.json":
                manifest = {
                    "name": "पहाड़ी संगम AI - Pahadi AI Assistant",
                    "short_name": "Pahadi AI",
                    "start_url": "/",
                    "display": "standalone",
                    "background_color": "#0f172a",
                    "theme_color": "#0f172a",
                    "description": "हिमाचली और गढ़वाली-कुमाऊँनी AI सहायक व अनुवादक",
                }
                self._send_json(manifest)
            elif path == "/sw.js":
                sw = "self.addEventListener('fetch', function(e) { e.respondWith(fetch(e.request)); });"
                self._send_data(sw.encode("utf-8"), "application/javascript")
            else:
                self._send_data(b"Not Found", "text/plain", 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def do_POST(self):
        try:
            path = self.path.split("?")[0]
            content_len = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
            body = json.loads(post_data) if post_data else {}

            if path in ["/api/tts", "/api/voice/synthesize"]:
                text = body.get("text", "").strip()
                voice_name = body.get("voice") or body.get("voiceName") or "hi-IN-SwaraNeural"
                rate = body.get("rate", "-6%")
                pitch = body.get("pitch", "+0Hz")

                if not text:
                    self._send_json({"success": False, "status": "error", "error": "No text provided"}, 400)
                else:
                    try:
                        if voice_clone_engine:
                            res = voice_clone_engine.synthesize(text, voice_name=voice_name, rate=rate, pitch=pitch)
                            self._send_json(res)
                        else:
                            self._send_json({
                                "success": False,
                                "status": "fallback",
                                "fallbackBrowser": True,
                                "error": "Voice engine unavailable, using browser speech."
                            }, 200)
                    except Exception as e:
                        self._send_json({"success": False, "status": "error", "error": str(e)}, 500)


            if path == "/api/translate":
                query = body.get("query", "")
                dialect_code = body.get("dialect", "kangri")
                is_reverse = body.get("isReverse", False)

                result = translate(query, dialect_code, is_reverse)
                self._send_json(result)

            elif path == "/api/chat":
                msg = body.get("message", "")
                mode = body.get("mode", "standard")
                dialect_code = body.get("dialect", "kangri")
                history = body.get("history", [])

                reply = chat(history, msg, mode, dialect_code)
                self._send_json({"reply": reply})

            elif path == "/api/set-key":
                new_key = body.get("key", "").strip()
                success = save_gemini_api_key(new_key)
                if success:
                    self._send_json({"success": True})
                else:
                    self._send_json({"success": False, "error": "अमान्य API Key"}, 400)

            elif path == "/api/voice/upload":
                import base64
                audio_b64 = body.get("audioData", "")
                voice_name = body.get("voiceName", "kore")
                pitch_hz = body.get("pitchHz", 200)

                if audio_b64:
                    if "," in audio_b64:
                        audio_b64 = audio_b64.split(",", 1)[1]
                    audio_bytes = base64.b64decode(audio_b64)
                    out_path = PROJECT_ROOT / "custom_voice" / "my_voice.wav"
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(out_path, "wb") as f:
                        f.write(audio_bytes)

                    if voice_clone_engine:
                        voice_clone_engine.save_voice_profile({
                            "voiceName": voice_name,
                            "pitchHz": pitch_hz
                        })

                    self._send_json({"success": True, "size": len(audio_bytes), "voiceName": voice_name})
                else:
                    self._send_json({"success": False, "error": "No audio received"}, 400)

            elif path == "/api/voice/synthesize":
                text = body.get("text", "")
                voice_name = body.get("voiceName")
                if not text:
                    self._send_json({"success": False, "error": "No text provided"}, 400)
                else:
                    try:
                        if voice_clone_engine and voice_clone_engine.is_reference_voice_ready():
                            res = voice_clone_engine.synthesize(text, voice_name=voice_name)
                            self._send_json(res)
                        else:
                            self._send_json({
                                "success": False,
                                "error": "कृपया पहले अपनी आवाज़ रिकॉर्ड करें!"
                            }, 400)
                    except Exception as e:
                        self._send_json({"success": False, "error": str(e)}, 500)

            else:
                self._send_data(b"Not Found", "text/plain", 404)
        except Exception as e:
            self._send_json({"error": str(e)}, 500)


def render_streamlit_app():
    """Streamlit interface if invoked via 'streamlit run app.py'."""
    import streamlit as st  # type: ignore

    st.set_page_config(
        page_title="Pahadi AI - पहाड़ी संगम",
        page_icon="🏔️",
        layout="wide"
    )

    st.title("🏔️ Pahadi AI Assistant (पहाड़ी संगम)")
    st.markdown("### Himalayan AI Assistant & Dialect Translator")

    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ सेटिंग्स (Settings)")
        dialect_options = {d["code"]: f"{d['displayNameHindi']} ({d['displayNameEnglish']})" for d in DIALECTS}
        selected_code = st.selectbox(
            "पहाड़ी बोली चुनें (Select Dialect):",
            options=list(dialect_options.keys()),
            format_func=lambda k: dialect_options[k]
        )
        selected_meta = get_dialect_meta(selected_code)
        st.info(f"📍 **क्षेत्र:** {selected_meta['region']}\n\n🏛️ **राज्य:** {selected_meta['state']}")

        mode = st.selectbox(
            "संवाद मोड (Persona Mode):",
            options=["standard", "elder", "student", "farmer"],
            format_func=lambda m: {
                "standard": "🏔️ All-Round Assistant",
                "elder": "👵 Elder Friendly (बुजुर्ग मित्र)",
                "student": "📚 Student Helper (छात्र सहायक)",
                "farmer": "🍎 Farmer & Orchard Helper (बागवान मित्र)"
            }[m]
        )

        curr_key = get_gemini_api_key()
        api_input = st.text_input("Gemini API Key:", value=curr_key, type="password")
        if st.button("Save API Key"):
            if save_gemini_api_key(api_input):
                st.success("API Key saved!")
            else:
                st.error("Invalid API Key.")

    # Tabs for main features
    tab_trans, tab_chat, tab_phrases, tab_lore = st.tabs(["🔤 अनुवादक (Translator)", "💬 संवाद (AI Chat)", "📖 वाक्यांश (Phrases)", "🏛️ लोक धरोहर (Lore)"])

    with tab_trans:
        col1, col2 = st.columns(2)
        with col1:
            reverse = st.checkbox("पहाड़ी ➔ हिंदी (Pahadi to Hindi)", value=False)
            input_label = "पहाड़ी वाक्य लिखें:" if reverse else "हिंदी वाक्य लिखें:"
            user_input = st.text_area(input_label, height=120, placeholder="उदा: आप कैसे हैं? / आपु किद्दां आ?")
            if st.button("अनुवाद करें (Translate)", type="primary"):
                if user_input.strip():
                    with st.spinner("अनुवाद हो रहा है..."):
                        result = translate(user_input, selected_code, reverse)
                    with col2:
                        st.success(f"**अनुवाद:** {result.get('translatedText')}")
                        st.caption(f"**उच्चारण (Phonetic):** {result.get('phoneticText')}")
                        st.info(f"**सांस्कृतिक संदर्भ:** {result.get('culturalContext')}")
                        st.markdown(f"💡 **शिष्टाचार सुझाव:** {result.get('etiquetteTip')}")
                else:
                    st.warning("कृपया कुछ टेक्स्ट लिखें।")

    with tab_chat:
        st.subheader("हिमालयी मित्र से संवाद")
        user_msg = st.text_input("अपना प्रश्न या संदेश लिखें:", placeholder="उदा: रोहतांग का मौसम कैसा है? / सेब में प्रूनिंग कब करें?")
        if st.button("भेजें (Send)"):
            if user_msg.strip():
                with st.spinner("उत्तर तैयार हो रहा है..."):
                    reply = chat([], user_msg, mode, selected_code)
                st.markdown(f"**उत्तर:**\n\n{reply}")

    with tab_phrases:
        st.subheader(f"प्रामाणिक {selected_meta['displayNameHindi']} वाक्यांश")
        dialect_phrases = [p for p in CURATED_PHRASES if p.get("dialect") == selected_code]
        if dialect_phrases:
            for p in dialect_phrases:
                with st.expander(f"{p['hindi']} ➔ {p['translation']}"):
                    st.write(f"**उच्चारण:** {p['phonetic']}")
                    st.write(f"**अंग्रेज़ी:** {p['english']}")
                    st.caption(f"**सांस्कृतिक टिप्पणी:** {p['culturalNote']}")
        else:
            for p in CURATED_PHRASES[:6]:
                with st.expander(f"{p['hindi']} ➔ {p['translation']}"):
                    st.write(f"**उच्चारण:** {p['phonetic']}")
                    st.caption(f"**बोली:** {p['dialect']} | {p['culturalNote']}")

    with tab_lore:
        st.subheader("हिमालयी लोककथाएं एवं धरोहर")
        for story in CULTURAL_STORIES:
            with st.expander(f"{story['titleHindi']} ({story['region']})"):
                st.write(story['summary'])
                st.markdown(f"**कथा:**\n{story['fullStory']}")
                st.info(f"**सांस्कृतिक महत्व:** {story['culturalSignificance']}")


def run(port: int = PORT):
    """Start Pahadi AI Web Application Server."""
    # Check if executed inside Streamlit runtime
    if "streamlit" in sys.modules and any("streamlit" in arg for arg in sys.argv):
        render_streamlit_app()
        return

    httpd = None
    for p in [port, 8080, 8081, 8082, 8085, 8090]:
        try:
            server_address = ("", p)
            httpd = ThreadedTCPServer(server_address, PahadiServerHandler)
            port = p
            break
        except OSError:
            continue

    if not httpd:
        print("Error: Could not bind to an available port.")
        return

    url = f"http://localhost:{port}"
    print("=" * 64)
    print("  🏔️  Pahadi AI Assistant (पहाड़ी संगम) is Running!")
    print(f"  👉 Web App URL: {url}")
    print("  ⭐ Press Ctrl+C in this terminal to stop the server.")
    print("=" * 64)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Pahadi AI server...")
        httpd.server_close()


if __name__ == "__main__":
    # If streamlit was invoked via command line
    if len(sys.argv) > 1 and sys.argv[1] == "streamlit":
        render_streamlit_app()
    else:
        run()
