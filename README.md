# 🏔️ Pahadi AI Assistant (पहाड़ी संगम)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Android](https://img.shields.io/badge/Android-API%2024%2B%20(Compose)-green.svg)](https://developer.android.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/Powered%20By-Google%20Gemini-orange.svg)](https://ai.google.dev/)

> **पहाड़ी संगम** — A production-ready, authentic AI assistant and dialect translator connecting standard Hindi with the rich linguistic heritage of the Himalayas (**Himachal Pradesh**, **Uttarakhand**, and the **Dogra Belt**).

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Supported Himalayan Dialects](#-supported-himalayan-dialects)
- [Key Features](#-key-features)
- [Architecture & Repository Structure](#-architecture--repository-structure)
- [Prerequisites](#-prerequisites)
- [Quickstart Guide](#-quickstart-guide)
  - [1. Backend / Web Application](#1-backend--web-application)
  - [2. Streamlit Dashboard Mode](#2-streamlit-dashboard-mode)
  - [3. Android Mobile Application](#3-android-mobile-application)
- [Environment Configuration](#-environment-configuration)
- [Offline Fallback System](#-offline-fallback-system)
- [Voice Cloning Engine](#-voice-cloning-engine)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Project Overview

Across the Western and Central Himalayas, millions of people speak diverse Pahadi languages and dialects. Standard translation tools often overlook dialectal nuances, treating diverse speech communities as identical.

**Pahadi AI Assistant** solves this by combining:
1. **Gemini Generative AI**: Fine-tuned prompt engineering with authentic vocabulary, Devanagari script, Roman phonetic transliteration, and cultural etiquette advice.
2. **Offline Linguistic Knowledge Base**: A curated dictionary of phrases, idioms, phonetic heuristics, and emergency services that works even without internet connectivity.
3. **Personalized Voice Cloning & Neural TTS**: Calibrated pitch profiling and Google Neural TTS synthesis.
4. **Himalayan Heritage Repository**: Authentic local folklore, agricultural advisory for apple orchards, HRTC bus routes, and disaster helpline contacts.
5. **Multiplatform Delivery**: High-performance Python backend with embedded glassmorphic Web UI, optional Streamlit interface, and native Android Studio integration.

---

## 🗣️ Supported Himalayan Dialects

| Dialect Code | Local Name (देवनागरी) | English Name | Region / Districts | State |
| :--- | :--- | :--- | :--- | :--- |
| `kangri` | **कांगड़ी** | Kangri | कांगड़ा घाटी, हमीरपुर, ऊना | हिमाचल प्रदेश |
| `mandeali` | **मंडीयाली** | Mandeali | मंडी, सुंदरनगर, छोटी काशी | हिमाचल प्रदेश |
| `kullui` | **कुल्लवी** | Kullui | कुल्लू घाटी, मनाली, बंजार | हिमाचल प्रदेश |
| `shimla_pahari` | **शिमला / महासूवी** | Shimla Pahari / Mahasuvi | शिमला, ठियोग, कोटखाई, रोहड़ू, सोलन | हिमाचल प्रदेश |
| `chambeali` | **चम्बियाली** | Chambeali | चंबा, रावी घाटी, भरमौर | हिमाचल प्रदेश |
| `sirmauri` | **सिरमौरी** | Sirmauri / Giripar | नाहन, रेणुका जी, गिरि-पार (हाटी क्षेत्र) | हिमाचल प्रदेश |
| `garhwali` | **गढ़वाली** | Garhwali | श्रीनगर, पौड़ी, टिहरी, चमोली, उत्तरकाशी | उत्तराखंड |
| `kumaoni` | **कुमाऊँनी** | Kumaoni | अल्मोड़ा, नैनीताल, पिथौरागढ़, बागेश्वर | उत्तराखंड |
| `dogri` | **डोगरी** | Dogri | जम्मू, उधमपुर, कांगड़ा शिवालिक बेल्ट | जम्मू / हिमाचल |
| `jaunsari` | **जौनसारी** | Jaunsari | जौनसार-बावर, चकराता, देहरादून पहाड़ियां | उत्तराखंड |

---

## 🚀 Key Features

- **🌐 Bidirectional Translation**: Hindi ➔ Pahadi and Pahadi ➔ Hindi with Devanagari script, Romanized pronunciation, and valley-specific cultural notes.
- **🎙️ Personalized Voice Cloning**: Record a short audio snippet to calibrate pitch; synthesize replies in a personalized cloned voice via Gemini Neural TTS.
- **🎭 4 Persona Chat Modes**:
  - 👵 **Elder Friendly (बुजुर्ग मित्र)**: Warm, short, respectful traditional phrasing (`पैलाग जी`, `जय देव जी`).
  - 📚 **Student Helper (छात्र सहायक)**: Bilingual revision guides, exam points, and concept explainers.
  - 🍎 **Farmer & Orchard Helper (बागवान मित्र)**: Scientific apple pruning guide, scab disease control, chilling hours, and government subsidies (Himcare, SPNF).
  - 🏔️ **All-Round Himalayan AI**: HRTC bus timings, road travel alerts, and weather advisories.
- **🚨 Instant Disaster & Emergency Hub**: Quick access to National Emergency (`112`), HP Disaster Authority (`1077`), Ambulance (`108`), Women Helpline (`1091`), and HRTC Control Room (`01772803017`).
- **🏛️ Living Folk Heritage**: Curated stories of Golu Devta, Kullu Dussehra, Mahasu Devta, Nanda Devi Raj Jat, and Phooldei.

---

## 🏗️ Architecture & Repository Structure

```text
Hindi-Pahadi-AI-Assistant/
├── android/                         # Android Mobile Application (Native & Gradle)
│   ├── app/                         # Jetpack Compose / Material 3 Application
│   │   ├── src/main/java/           # Kotlin architecture (MVVM, Room, Gemini Client)
│   │   └── build.gradle.kts         # App module configuration
│   ├── webview_companion/           # Lightweight WebView companion APK project
│   ├── gradle/                      # Gradle wrapper & version catalogs
│   ├── gradlew                      # Unix gradle wrapper script
│   ├── gradlew.bat                  # Windows gradle wrapper script
│   ├── build.gradle.kts             # Top-level build script
│   ├── settings.gradle.kts          # Top-level project settings
│   └── gradle.properties            # JVM & Android build properties
│
├── backend/                         # Python AI Engine & Server Core
│   ├── app.py                       # HTTP server, routing, and PWA endpoints
│   ├── data/                        # Regional linguistics & knowledge
│   │   ├── pahadi_dict.py           # Dictionaries, phrases, folklore, and offline translation
│   │   └── pahadi_dict.json         # Serialized standalone JSON dictionary
│   ├── services/                    # AI Inference & Voice Cloning
│   │   ├── engine.py                # Gemini LLM orchestration, model fallback, chat
│   │   └── voice_clone_engine.py    # Voice modeling & Neural TTS synthesis
│   ├── ui/                          # Front-end templates
│   │   └── index_html.py            # Glassmorphic Himalayan web interface
│   └── requirements.txt             # Backend dependencies
│
├── custom_voice/                    # Local voice samples and calibrated profiles
│   ├── my_voice.wav                 # Reference audio sample
│   └── profile.json                 # Pitch and voice profile configuration
│
├── .env.example                     # Environment template for API keys
├── .gitignore                       # Clean Git tracking (pycache & build artifacts excluded)
├── requirements.txt                 # Project-wide Python dependencies
├── app.py                           # Convenient root runner (points to backend.app)
└── README.md                        # Project documentation
```

---

## 📋 Prerequisites

- **Python**: Python 3.10 or higher
- **Android Studio** (for mobile builds): Android Studio Hedgehog / Koala / Ladybug with JDK 17
- **Google Gemini API Key**: Free tier or paid key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## ⚡ Quickstart Guide

### 1. Backend / Web Application

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hideepaksharma5-create/Hindi-Pahadi-AI-Assistant.git
   cd Hindi-Pahadi-AI-Assistant
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   Open `.env` in an editor and insert your Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSy...YourKeyHere
   ```

4. **Launch the Application**:
   ```bash
   python app.py
   # Or directly from the backend folder:
   python backend/app.py
   ```
   The browser will automatically open to `http://localhost:8080`.

---

### 2. Streamlit Dashboard Mode

If you prefer using Streamlit for an interactive multi-tab dashboard:
```bash
streamlit run app.py
# Or:
streamlit run backend/app.py
```

---

### 3. Android Mobile Application

The repository contains a fully native Android client built with **Jetpack Compose**, **Material 3**, and **Kotlin Coroutines**:

1. Open **Android Studio**.
2. Click **File ➔ Open...** and select the `android/` directory:
   ```text
   C:\path\to\Hindi-Pahadi-AI-Assistant\android
   ```
3. Allow Gradle to sync.
4. Run the project on an Android device or emulator, or build an APK:
   ```bash
   cd android
   ./gradlew assembleDebug
   ```
   The generated APK will be located at:
   `android/app/build/outputs/apk/debug/app-debug.apk`

---

## ⚙️ Environment Configuration

| Variable | Description | Default | Required? |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google Gemini API Key for online chat & translation | Empty | Recommended (runs offline if omitted) |
| `PORT` | Local HTTP server port | `8080` | Optional |

> **Note**: Even if no API key is provided, the application runs automatically in **Offline Mode** using the embedded regional linguistic database.

---

## 📴 Offline Fallback System

When no internet connection or API key is available, `backend/data/pahadi_dict.py` provides:
- Exact phrase matching across 10 dialects.
- Heuristic recognition of common Pahadi inquiry particles (`कुथी चले` ➔ *कहाँ जा रहे हैं*, `किद्दां आ` ➔ *कैसे हैं*, `पैलाग` ➔ *प्रणाम*).
- Full access to emergency numbers and cultural heritage stories.

---

## 🎙️ Voice Cloning Engine

The voice engine operates through:
1. **Audio Recording**: User records a 3-5 second audio sample in the browser or app.
2. **Pitch Profiling**: Analyzes fundamental frequency ($F_0$) to map gender and pitch characteristics.
3. **Neural Synthesis**: Directs requests to Gemini Neural TTS (`gemini-2.5-flash-preview-tts`) with matching acoustic attributes (`fenrir`, `puck`, `aoede`, `kore`, `charon`).
4. **Browser Fallback**: If offline, synthesizes speech using the browser Web Speech API calibrated to the user's recorded pitch.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewDialectPhrases`).
3. Commit your changes (`git commit -m "feat: add Kangri idioms"`).
4. Push to the branch (`git push origin feature/NewDialectPhrases`).
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
