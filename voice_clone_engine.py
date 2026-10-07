# -*- coding: utf-8 -*-
"""
Voice Clone Engine Proxy
Forwards calls to backend.services.voice_clone_engine.
"""
from backend.services.voice_clone_engine import *

if __name__ == "__main__":
    import json
    print(f"Voice Engine Status: {json.dumps(get_voice_status(), indent=2)}")
