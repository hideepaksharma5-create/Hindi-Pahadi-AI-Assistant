#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pahadi AI Assistant (पहाड़ी संगम) - Root Application Runner
Seamlessly forwards to backend.app. Supports both standard standalone
server (`python app.py`) and Streamlit web dashboard (`streamlit run app.py`).
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Check if running via Streamlit
is_streamlit = "streamlit" in sys.modules or any("streamlit" in arg for arg in sys.argv)

if is_streamlit:
    from backend.app import render_streamlit_app
    render_streamlit_app()
else:
    from backend.app import run
    if __name__ == "__main__":
        run()
