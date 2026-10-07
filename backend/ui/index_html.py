# -*- coding: utf-8 -*-
"""Himalayan Glassmorphism Web App UI"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pahadi AI - पहाड़ी संगम (AI Assistant & Translator)</title>
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#0f172a" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Yantramanav:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border: rgba(255, 255, 255, 0.08);
      --accent-primary: #38bdf8;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --input-bg: rgba(15, 23, 42, 0.6);
      --radius: 16px;
      --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.2);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Outfit', 'Yantramanav', sans-serif;
      background: radial-gradient(circle at top right, #1e1b4b, #0f172a 60%, #020617);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      padding: 1rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      font-size: 2rem;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      border-radius: 12px;
      padding: 4px 8px;
    }
    .brand h1 {
      font-size: 1.4rem;
      font-weight: 700;
      background: linear-gradient(to right, #38bdf8, #a5b4fc, #f472b6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand p { font-size: 0.8rem; color: var(--text-muted); }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .nav-tabs {
      display: flex;
      background: rgba(30, 41, 59, 0.8);
      border-radius: 100px;
      padding: 4px;
      border: 1px solid var(--card-border);
    }
    .nav-tab {
      padding: 8px 16px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      border-radius: 100px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.2s ease;
      font-size: 0.9rem;
    }
    .nav-tab.active {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #fff;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    .btn-key {
      background: rgba(245, 158, 11, 0.15);
      color: #fcd34d;
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 8px 14px;
      border-radius: 100px;
      font-size: 0.85rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-key:hover { background: rgba(245, 158, 11, 0.25); }

    main {
      flex: 1;
      max-width: 1200px;
      width: 100%;
      margin: 0 auto;
      padding: 1.5rem 1rem;
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; animation: fadeIn 0.3s ease; }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Common Card */
    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: var(--shadow);
      margin-bottom: 1.5rem;
    }

    /* Translator Tab */
    .translator-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 768px) {
      .translator-grid { grid-template-columns: 1fr; }
      header { flex-direction: column; gap: 12px; }
      .nav-tabs { flex-wrap: wrap; justify-content: center; }
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
    }
    .dialect-select {
      background: var(--input-bg);
      color: var(--text);
      border: 1px solid var(--card-border);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.9rem;
      outline: none;
      cursor: pointer;
    }
    .dialect-select option { background: #1e293b; color: #fff; }

    textarea {
      width: 100%;
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      border-radius: 12px;
      padding: 1rem;
      font-size: 1rem;
      font-family: inherit;
      resize: vertical;
      min-height: 120px;
      outline: none;
      transition: border-color 0.2s;
    }
    textarea:focus { border-color: var(--accent-primary); }

    .action-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
    }
    .btn-primary {
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: white;
      border: none;
      padding: 10px 24px;
      border-radius: 10px;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
      transition: all 0.2s;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }
    .btn-primary:hover { transform: translateY(-1px); filter: brightness(1.1); }

    .btn-icon {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text);
      width: 40px;
      height: 40px;
      border-radius: 10px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 1.1rem;
      transition: all 0.2s;
    }
    .btn-icon:hover { background: rgba(255, 255, 255, 0.15); }
    .btn-icon.recording { background: var(--accent-rose); animation: pulse 1.5s infinite; }

    @keyframes pulse {
      0% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.6); }
      70% { box-shadow: 0 0 0 10px rgba(244, 63, 94, 0); }
      100% { box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }
    }

    .result-box {
      background: rgba(15, 23, 42, 0.5);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.25rem;
      min-height: 120px;
    }
    .result-text { font-size: 1.3rem; font-weight: 600; color: #38bdf8; margin-bottom: 0.5rem; }
    .phonetic-text { font-size: 0.95rem; color: #a5b4fc; font-style: italic; margin-bottom: 1rem; }

    .badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 100px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }
    .badge-ai { background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-offline { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }

    .context-card {
      margin-top: 1rem;
      background: rgba(30, 41, 59, 0.4);
      border-left: 4px solid var(--accent-amber);
      padding: 0.75rem 1rem;
      border-radius: 0 8px 8px 0;
      font-size: 0.85rem;
      line-height: 1.5;
    }
    .context-card h5 { color: #fcd34d; margin-bottom: 4px; }

    /* Chat Tab */
    .chat-container {
      display: flex;
      flex-direction: column;
      height: 72vh;
    }
    .mode-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 1rem;
      overflow-x: auto;
      padding-bottom: 6px;
    }
    .mode-chip {
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 100px;
      font-size: 0.85rem;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .mode-chip.active {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-primary);
      color: #38bdf8;
      font-weight: 600;
    }

    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      background: rgba(15, 23, 42, 0.4);
      border-radius: 12px;
      border: 1px solid var(--card-border);
    }
    .message {
      max-width: 80%;
      padding: 0.9rem 1.2rem;
      border-radius: 16px;
      font-size: 0.95rem;
      line-height: 1.5;
      animation: fadeIn 0.2s ease;
    }
    .message.user {
      align-self: flex-end;
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: white;
      border-bottom-right-radius: 4px;
    }
    .message.assistant {
      align-self: flex-start;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid var(--card-border);
      border-bottom-left-radius: 4px;
      transition: border-color 0.3s, box-shadow 0.3s;
    }
    .message.assistant.speaking-bubble {
      border-color: rgba(56, 189, 248, 0.6);
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
    }
    .msg-content {
      line-height: 1.6;
      word-break: break-word;
    }
    .msg-content strong {
      color: #fcd34d;
    }
    .msg-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-tts {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      margin-top: 8px;
      padding: 5px 12px;
      font-size: 0.8rem;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.16);
      color: #93c5fd;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }
    .btn-tts:hover {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      color: #ffffff;
      transform: translateY(-1px);
    }
    .btn-tts.speaking {
      background: rgba(239, 68, 68, 0.25);
      border-color: #ef4444;
      color: #fca5a5;
      animation: pulseSpeaking 1.5s infinite ease-in-out;
    }
    @keyframes pulseSpeaking {
      0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
      50% { box-shadow: 0 0 10px 2px rgba(239, 68, 68, 0.6); }
    }

    .chat-input-bar {
      display: flex;
      gap: 10px;
      margin-top: 1rem;
    }
    .chat-input-bar input {
      flex: 1;
      background: var(--input-bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      padding: 12px 16px;
      border-radius: 12px;
      font-size: 1rem;
      outline: none;
    }
    .chat-input-bar input:focus { border-color: var(--accent-primary); }

    /* Grid cards for Phrasebook & Lore */
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.25rem;
    }
    .phrase-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 1.25rem;
      transition: transform 0.2s;
    }
    .phrase-card:hover { transform: translateY(-2px); border-color: rgba(56, 189, 248, 0.4); }
    .phrase-target { font-size: 1.15rem; font-weight: 600; color: #38bdf8; margin: 6px 0; }
    .phrase-phonetic { font-size: 0.85rem; color: #a5b4fc; font-style: italic; margin-bottom: 8px; }
    .phrase-meta { font-size: 0.8rem; color: var(--text-muted); }

    /* Emergency Contacts */
    .emergency-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    .emergency-card {
      background: rgba(244, 63, 94, 0.08);
      border: 1px solid rgba(244, 63, 94, 0.2);
      border-radius: 12px;
      padding: 1rem;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .emergency-card .num { font-size: 1.4rem; font-weight: 700; color: #fda4af; }

    /* Modal */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }
    .modal-overlay.active { display: flex; }
    .modal-box {
      background: #1e293b;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 1.5rem;
      max-width: 540px;
      width: 100%;
      max-height: 88vh;
      overflow-y: auto;
      box-shadow: var(--shadow);
      position: relative;
    }
    .modal-box h3 { margin-bottom: 0.8rem; color: #fcd34d; }
    .modal-box input {
      width: 100%;
      background: #0f172a;
      border: 1px solid var(--card-border);
      color: white;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 1.25rem;
      outline: none;
    }
    .modal-actions { display: flex; justify-content: flex-end; gap: 10px; }
    .btn-secondary {
      background: transparent;
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="brand-icon">🏔️</div>
      <div>
        <h1>Pahadi AI (पहाड़ी संगम)</h1>
        <p>Himalayan Dialect Assistant & Cultural Translator</p>
      </div>
    </div>

    <div class="header-actions">
      <nav class="nav-tabs">
        <button class="nav-tab active" onclick="switchTab('translator')">🔄 अनुवादक (Translator)</button>
        <button class="nav-tab" onclick="switchTab('chat')">💬 पहाड़ी मित्र (Chat)</button>
        <button class="nav-tab" onclick="switchTab('phrasebook')">📖 वाक्यांश (Phrasebook)</button>
        <button class="nav-tab" onclick="switchTab('heritage')">🏛️ धरोहर व ज्ञान</button>
      </nav>

      <button class="btn-key" id="voiceCloneNavBtn" onclick="openVoiceCloneModal()" style="background: rgba(139, 92, 246, 0.15); border-color: #8b5cf6; color: #c4b5fd;">
        <span id="voiceCloneStatusIcon">🎙️</span> <span id="voiceCloneStatusText">मेरी आवाज़ (Voice)</span>
      </button>

      <button class="btn-key" onclick="openKeyModal()">
        <span>🔑</span> <span id="keyStatusText">Gemini Key</span>
      </button>
    </div>
  </header>

  <main>
    <!-- TAB 1: TRANSLATOR -->
    <div id="tab-translator" class="tab-content active">
      <div class="translator-grid">
        <!-- Input Side -->
        <div class="card">
          <div class="panel-header">
            <h3 id="inputTitle">मानक हिंदी (Hindi)</h3>
            <button class="btn-icon" onclick="swapDirection()" title="दिशा बदलें (Swap Direction)">⇄</button>
          </div>
          <textarea id="sourceInput" placeholder="यहाँ वाक्य लिखें या माइक दबाकर बोलें... (e.g. आप कैसे हैं? / आज बर्फ पड़ रही है)"></textarea>
          <div class="action-row">
            <div style="display: flex; gap: 8px;">
              <button id="micBtn" class="btn-icon" onclick="toggleSpeech()" title="बोलें (Speak)">🎙️</button>
              <button class="btn-icon" onclick="clearInput()" title="साफ करें">🧹</button>
            </div>
            <button class="btn-primary" onclick="doTranslate()">अनुवाद करें (Translate) ✨</button>
          </div>
        </div>

        <!-- Output Side -->
        <div class="card">
          <div class="panel-header">
            <h3 id="outputTitle">पहाड़ी बोली (Pahadi Dialect)</h3>
            <select id="dialectSelect" class="dialect-select" onchange="onDialectChange()">
              <!-- Options populated by JS -->
            </select>
          </div>
          <div class="result-box">
            <div id="badgeContainer"><span class="badge badge-offline">Offline Engine Active</span></div>
            <div id="translatedOutput" class="result-text">अनुवाद यहाँ दिखाई देगा...</div>
            <div id="phoneticOutput" class="phonetic-text"></div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px; flex-wrap:wrap; gap:8px;">
              <button id="speakResultBtn" class="btn-tts" onclick="speakTranslation()" title="उच्चारण सुनें (Listen)" style="display:none;">
                <span class="tts-icon">🔊</span> <span class="tts-label">सुनें (Read Aloud)</span>
              </button>
              <button class="mode-chip voiceModeToggleBtn" onclick="toggleVoiceMode()" title="आवाज़ बदलें">
                🎙️ आवाज़: <span class="voiceModeLabel" style="color:#c084fc; font-weight:600;">मेरी आवाज़ (Cloned) ✨</span>
              </button>
            </div>
          </div>

          <div id="contextCard" class="context-card" style="display:none;">
            <h5>सांस्कृतिक संदर्भ (Cultural Context):</h5>
            <p id="contextText"></p>
            <div id="etiquetteBox" style="margin-top: 6px; color: #a5b4fc;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: CHAT (PAHADI MITRA) -->
    <div id="tab-chat" class="tab-content">
      <div class="card chat-container">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom: 0.8rem;">
          <div class="mode-bar" style="margin-bottom:0; flex:1;">
            <button class="mode-chip active" onclick="setChatMode('standard', this)">🌟 सर्वज्ञ मित्र (Standard)</button>
            <button class="mode-chip" onclick="setChatMode('elder', this)">👴 बुजुर्ग मित्र (Elder Friendly)</button>
            <button class="mode-chip" onclick="setChatMode('farmer', this)">🍎 किसान व बागवान (Apple/Farm)</button>
            <button class="mode-chip" onclick="setChatMode('student', this)">📚 छात्र सहायक (Student)</button>
          </div>
          <div style="display:flex; align-items:center; gap:8px;">
            <button class="mode-chip voiceModeToggleBtn" onclick="toggleVoiceMode()" title="आवाज़ चुनें (डिफ़ॉल्ट या आपकी क्लोन आवाज़)">
              🎙️ आवाज़: <span class="voiceModeLabel" style="color:#c084fc; font-weight:600;">मेरी आवाज़ (Cloned) ✨</span>
            </button>
            <button id="autoReadToggle" class="mode-chip" onclick="toggleAutoRead()" title="उत्तर मिलते ही अपने-आप आवाज़ में बोलकर सुनाएं">
              🔊 ऑटो-रीड: <span id="autoReadStatus" style="color:#f87171; font-weight:600;">बंद</span>
            </button>
            <button id="globalStopTtsBtn" class="mode-chip" onclick="stopAllSpeech()" style="display:none; background: rgba(239, 68, 68, 0.2); border-color: #ef4444; color: #fca5a5;" title="आवाज़ तुरंत बंद करें">
              ⏹️ बोलना रोकें
            </button>
          </div>
        </div>

        <div id="chatMessages" class="chat-messages">
          <div class="message assistant">
            <div class="msg-content">नमस्कार जी! पैलाग! मैं <strong>'पहाड़ी मित्र'</strong> हूँ। आप मुझसे हिमाचली व गढ़वाली-कुमाऊंनी बोलियों, सेब के बगीचों, पारंपरिक धाम, लोककथाओं या सामान्य सहायता के बारे में पूछ सकते हैं।</div>
            <div class="msg-actions">
              <button class="btn-tts" onclick="speakChatMessage(this)" title="बोलकर सुनाएं (Read Aloud)">
                <span class="tts-icon">🔊</span> <span class="tts-label">सुनें (Read Aloud)</span>
              </button>
            </div>
          </div>
        </div>

        <div class="chat-input-bar">
          <input type="text" id="chatInput" placeholder="पहाड़ी मित्र से कुछ भी पूछें... (Enter दबाएं)" onkeydown="if(event.key==='Enter') sendChatMessage()" />
          <button class="btn-icon" onclick="toggleChatMic()" title="बोलें">🎙️</button>
          <button class="btn-primary" onclick="sendChatMessage()">भेजें</button>
        </div>
      </div>
    </div>

    <!-- TAB 3: PHRASEBOOK -->
    <div id="tab-phrasebook" class="tab-content">
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 10px;">
          <h2>📖 प्रामाणिक पहाड़ी वाक्यांश (Curated Phrasebook)</h2>
          <select id="phraseDialectFilter" class="dialect-select" onchange="renderPhrases()">
            <option value="all">सभी बोलियाँ (All Dialects)</option>
          </select>
        </div>
        <div id="phraseGrid" class="grid-2">
          <!-- Filled by JS -->
        </div>
      </div>
    </div>

    <!-- TAB 4: HERITAGE & KNOWLEDGE -->
    <div id="tab-heritage" class="tab-content">
      <div class="card">
        <h2>🚨 महत्वपूर्ण आपातकालीन संपर्क (Emergency Services)</h2>
        <div id="emergencyGrid" class="emergency-grid"></div>
      </div>

      <div class="card">
        <h2>🏔️ स्थानीय ज्ञान व सरकारी योजनाएं (Knowledge & Schemes)</h2>
        <div id="knowledgeGrid" class="grid-2" style="margin-top: 1rem;"></div>
      </div>

      <div class="card">
        <h2>📜 लोककथाएं व सांस्कृतिक धरोहर (Folk Lore & Legends)</h2>
        <div id="storiesGrid" class="grid-2" style="margin-top: 1rem;"></div>
      </div>
    </div>
  </main>

  <!-- KEY MODAL -->
  <div id="keyModal" class="modal-overlay">
    <div class="modal-box" style="max-width: 520px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.8rem;">
        <h3 style="margin:0;">🔑 ऑनलाइन मोड सक्रिय करें (Activate Online Mode)</h3>
        <button class="btn-icon" onclick="closeKeyModal()" style="font-size:1.1rem; line-height:1;">✕</button>
      </div>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.75rem;">
        ऑनलाइन मोड चालू करने के लिए Google Gemini API Key की आवश्यकता होती है। यह पूरी तरह <strong>मुफ्त (Free)</strong> है।
      </p>
      <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 10px; padding: 12px; margin-bottom: 1rem; font-size: 0.85rem; line-height: 1.5; color: #bae6fd;">
        <strong style="color: #38bdf8;">🌐 3 सरल चरणों में मुफ्त API Key प्राप्त करें:</strong><br>
        1. <strong><a href="https://aistudio.google.com/app/apikey" target="_blank" style="color: #67e8f9; text-decoration: underline; font-weight: 600;">Google AI Studio (aistudio.google.com) ↗</a></strong> खोलें।<br>
        2. अपने Google अकाउंट से लॉगिन करें और <strong>"Create API key"</strong> पर क्लिक करें।<br>
        3. प्राप्त की गई की (उदा. <code>AIzaSy...</code>) को कॉपी करके नीचे पेस्ट करें।
      </div>
      <input type="password" id="geminiKeyInput" placeholder="यहाँ API Key पेस्ट करें (e.g. AIzaSy...)" style="width: 100%; box-sizing: border-box; margin-bottom: 0.5rem; padding: 10px 14px; border-radius: 8px; border: 1px solid var(--card-border); background: var(--input-bg); color: var(--text);" />
      <div id="keyFeedback" style="font-size: 0.85rem; margin-bottom: 0.75rem; display: none;"></div>
      <div class="modal-actions" style="margin-top: 1rem;">
        <button class="btn-secondary" onclick="closeKeyModal()">रद्द करें (Cancel)</button>
        <button class="btn-primary" onclick="saveGeminiKey()">सुरक्षित करें और ऑनलाइन मोड चालू करें 🚀</button>
      </div>
    </div>
  </div>

  <!-- VOICE CLONE MODAL -->
  <div id="voiceCloneModal" class="modal-overlay" onclick="if(event.target===this) closeVoiceCloneModal()">
    <div class="modal-box" style="max-width: 540px; position: relative;">
      <!-- Pinned Floating Close Button - Never scrolls out of view -->
      <button type="button" class="btn-cut-modal" onclick="closeVoiceCloneModal()" title="विंडो बंद करें (Cut / Close)" style="position: absolute; top: 12px; right: 14px; z-index: 99; background: #ef4444; color: white; border: none; border-radius: 8px; padding: 6px 14px; font-weight: 700; font-size: 0.88rem; cursor: pointer; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4); display: flex; align-items: center; gap: 4px;">
        ✕ कट करें (Cut)
      </button>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 0.8rem; padding-right: 120px;">
        <h3 style="margin:0; color: #c084fc; font-size: 1.15rem;">🎙️ आवाज़ क्लोन स्टूडियो (Voice Studio)</h3>
      </div>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.8rem; line-height: 1.5;">
        AI को अपनी आवाज़ में बोलने के लिए सिखाएं। नीचे माइक बटन दबाकर 8-10 सेकंड का अपना वॉइस सैंपल रिकॉर्ड करें, या अपनी मनपसंद न्यूरल आवाज़ शैली चुनें।
      </p>

      <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 12px; margin-bottom: 0.85rem; font-size: 0.88rem; color: #fde68a;">
        <strong>📖 रिकॉर्ड करते समय इस वाक्य को बोलें:</strong><br>
        <em>"नमस्कार जी! मैं पहाड़ी संगम AI सहायक का उपयोग कर रहा हूँ। यह मेरी अपनी आवाज़ का नमूना है।"</em>
      </div>

      <!-- Neural Preset Selector -->
      <div style="margin-bottom: 0.85rem; text-align: left;">
        <label style="font-size: 0.85rem; font-weight: 600; color: #c084fc; display: block; margin-bottom: 0.4rem;">
          🎭 आवाज़ की शैली (AI Neural Voice Preset):
        </label>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;" id="voicePresetsContainer">
          <label style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:8px; cursor:pointer; font-size:0.82rem;">
            <input type="radio" name="voicePreset" value="fenrir" onchange="onVoicePresetChange('fenrir')">
            <span>🦁 गंभीर पुरुष (Fenrir)</span>
          </label>
          <label style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:8px; cursor:pointer; font-size:0.82rem;">
            <input type="radio" name="voicePreset" value="puck" onchange="onVoicePresetChange('puck')">
            <span>⚡ उत्साही युवा (Puck)</span>
          </label>
          <label style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:8px; cursor:pointer; font-size:0.82rem;">
            <input type="radio" name="voicePreset" value="aoede" onchange="onVoicePresetChange('aoede')">
            <span>🌸 सौम्य स्त्री (Aoede)</span>
          </label>
          <label style="display:flex; align-items:center; gap:8px; padding:8px 10px; background:rgba(30,41,59,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:8px; cursor:pointer; font-size:0.82rem;">
            <input type="radio" name="voicePreset" value="kore" checked onchange="onVoicePresetChange('kore')">
            <span>🌺 स्पष्ट मधुर (Kore)</span>
          </label>
        </div>
        <div id="detectedPitchInfo" style="display:none; font-size:0.82rem; color:#38bdf8; margin-top:6px; font-weight:500;"></div>
      </div>

      <!-- Live Recorder Panel -->
      <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid var(--card-border); border-radius: 12px; padding: 1.25rem; text-align: center; margin-bottom: 1rem;">
        <div id="recordTimer" style="font-size: 1.8rem; font-weight: 700; color: #38bdf8; margin-bottom: 0.4rem;">00:00</div>
        <div id="recordStatus" style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">नीचे लाल बटन दबाकर बोलना शुरू करें</div>

        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
          <button id="startRecordBtn" class="btn-primary" onclick="startVoiceRecording()" style="background: linear-gradient(135deg, #ef4444, #dc2626);">
            🎙️ रिकॉर्ड शुरू करें (Start)
          </button>
          <button id="stopRecordBtn" class="btn-primary" onclick="stopVoiceRecording()" style="display: none; background: #475569;">
            ⏹️ रिकॉर्डिंग रोकें (Stop)
          </button>
        </div>

        <!-- Preview player -->
        <div id="recordedPreviewSection" style="display: none; margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem;">
          <div style="font-size: 0.85rem; margin-bottom: 0.5rem; color: #34d399;">✅ रिकॉर्डिंग पूरी हुई! प्ले करके सुनें:</div>
          <audio id="recordedAudioPlayer" controls style="width: 100%; height: 36px; margin-bottom: 0.75rem;"></audio>
          <div style="display: flex; gap: 8px; flex-wrap: wrap;">
            <button id="saveVoiceBtn" class="btn-primary" onclick="uploadRecordedVoice()" style="background: linear-gradient(135deg, #10b981, #059669); flex: 1; font-weight: 600;">
              💾 यह आवाज़ AI में सुरक्षित करें (Save Voice)
            </button>
            <button type="button" class="btn-secondary" onclick="closeVoiceCloneModal()" style="border-color: #ef4444; color: #fca5a5; font-weight: 600; padding: 8px 16px; border-radius: 12px; background: rgba(239, 68, 68, 0.15);">
              ✕ कट करें (Cut)
            </button>
          </div>
        </div>
      </div>

      <!-- File upload fallback -->
      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem; flex-wrap: wrap; gap: 6px;">
        <span>या WAV/MP3 ऑडियो फाइल अपलोड करें:</span>
        <input type="file" id="voiceFileInput" accept="audio/*" onchange="handleVoiceFileUpload(event)" style="font-size: 0.8rem; max-width: 190px;" />
      </div>

      <div id="voiceFeedback" style="font-size: 0.88rem; margin-top: 0.75rem; display: none; padding: 12px; border-radius: 8px; background: rgba(16, 185, 129, 0.1);"></div>
      <div class="modal-actions" style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 0.8rem;">
        <span style="font-size: 0.8rem; color: var(--text-muted);">बाहर क्लिक करें, Esc दबाएं या लाल 'कट करें' दबाएं</span>
        <button class="btn-primary" onclick="closeVoiceCloneModal()" style="background: linear-gradient(135deg, #ef4444, #dc2626); font-weight: 600; padding: 8px 18px;">
          ✕ कट / विंडो बंद करें (Cut / Close)
        </button>
      </div>
    </div>
  </div>

  <script>
    let dialects = [];
    let phrases = [];
    let isPahadiToHindi = false;
    let currentChatMode = "standard";
    let chatHistory = [];
    let recognition = null;

    async function init() {
      // 1. Fetch Dialects
      const dResp = await fetch('/api/dialects');
      dialects = await dResp.json();
      
      const sel = document.getElementById('dialectSelect');
      const filterSel = document.getElementById('phraseDialectFilter');
      sel.innerHTML = '';
      dialects.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.code;
        opt.textContent = `${d.displayNameHindi} - ${d.region}`;
        sel.appendChild(opt);

        const fOpt = document.createElement('option');
        fOpt.value = d.code;
        fOpt.textContent = d.displayNameHindi;
        filterSel.appendChild(fOpt);
      });

      // 2. Fetch Knowledge & Lore
      loadEmergency();
      loadKnowledge();
      loadStories();
      loadPhrases();

      // Check key & voice clone status
      checkKeyStatus();
      checkVoiceCloneStatus();
    }

    function switchTab(name) {
      document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      document.querySelector(`[onclick="switchTab('${name}')"]`).classList.add('active');
      document.getElementById(`tab-${name}`).classList.add('active');
    }

    function swapDirection() {
      isPahadiToHindi = !isPahadiToHindi;
      const inTitle = document.getElementById('inputTitle');
      const outTitle = document.getElementById('outputTitle');
      const dialectName = document.getElementById('dialectSelect').selectedOptions[0]?.text || "पहाड़ी बोली";

      if (isPahadiToHindi) {
        inTitle.textContent = `${dialectName} (Input)`;
        outTitle.textContent = "मानक हिंदी (Hindi Output)";
        document.getElementById('sourceInput').placeholder = "पहाड़ी में लिखें (e.g. आपु किद्दां आ? / तुसीं कुथी चले?)";
      } else {
        inTitle.textContent = "मानक हिंदी (Hindi Input)";
        outTitle.textContent = "पहाड़ी बोली (Pahadi Output)";
        document.getElementById('sourceInput').placeholder = "यहाँ वाक्य लिखें या माइक दबाकर बोलें...";
      }
    }

    function onDialectChange() {
      if (isPahadiToHindi) {
        const dialectName = document.getElementById('dialectSelect').selectedOptions[0]?.text || "पहाड़ी बोली";
        document.getElementById('inputTitle').textContent = `${dialectName} (Input)`;
      }
    }

    function clearInput() {
      document.getElementById('sourceInput').value = '';
    }

    async function doTranslate() {
      const text = document.getElementById('sourceInput').value.trim();
      if (!text) return;

      const dialectCode = document.getElementById('dialectSelect').value;
      const outBox = document.getElementById('translatedOutput');
      const phoneticBox = document.getElementById('phoneticOutput');
      const badgeBox = document.getElementById('badgeContainer');
      const contextCard = document.getElementById('contextCard');

      outBox.textContent = "अनुवाद हो रहा है...";
      phoneticBox.textContent = "";

      try {
        const resp = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: text,
            dialect: dialectCode,
            isReverse: isPahadiToHindi
          })
        });

        const data = await resp.json();
        outBox.textContent = data.translatedText;
        phoneticBox.textContent = data.phoneticText || "";
        document.getElementById('speakResultBtn').style.display = 'inline-flex';

        badgeBox.innerHTML = data.isAiPowered ? 
          '<span class="badge badge-ai">✨ Gemini AI Powered</span>' : 
          '<span class="badge badge-offline">⚡ Built-in Offline Engine</span>';

        if (data.culturalContext) {
          contextCard.style.display = 'block';
          document.getElementById('contextText').textContent = data.culturalContext;
          document.getElementById('etiquetteBox').textContent = data.etiquetteTip ? `💡 शिष्टाचार: ${data.etiquetteTip}` : "";
        } else {
          contextCard.style.display = 'none';
        }

      } catch (err) {
        outBox.textContent = "अनुवाद में त्रुटि आई। कृपया पुनः प्रयास करें।";
      }
    }

    function speakTranslation() {
      const text = document.getElementById('translatedOutput').textContent;
      if (!text || text.includes("...")) return;
      const btn = document.getElementById('speakResultBtn');
      speakText(text, btn);
    }

    // Speech Recognition
    function toggleSpeech() {
      const micBtn = document.getElementById('micBtn');
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("आपका ब्राउज़र वॉइस इनपुट का समर्थन नहीं करता है। Google Chrome का उपयोग करें।");
        return;
      }

      if (recognition) {
        recognition.stop();
        recognition = null;
        micBtn.classList.remove('recording');
        return;
      }

      recognition = new SpeechRecognition();
      recognition.lang = 'hi-IN';
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => micBtn.classList.add('recording');
      recognition.onresult = (e) => {
        const transcript = e.results[0][0].transcript;
        document.getElementById('sourceInput').value = transcript;
        doTranslate();
      };
      recognition.onend = () => {
        micBtn.classList.remove('recording');
        recognition = null;
      };
      recognition.onerror = () => {
        micBtn.classList.remove('recording');
        recognition = null;
      };
      recognition.start();
    }

    // TTS & Speech Synthesis Controls
    let currentSpeakingUtterance = null;
    let currentSpeakingBtn = null;
    let isAutoReadEnabled = false;

    function cleanTextForSpeech(text) {
      if (!text) return "";
      return text
        .replace(/\\*\\*(.*?)\\*\\*/g, '$1')     // remove bold **
        .replace(/\\*(.*?)\\*/g, '$1')         // remove italic *
        .replace(/#{1,6}\\s+/g, '')           // remove headings
        .replace(/`{1,3}.*?`{1,3}/gs, '')    // remove code blocks
        .replace(/\\[(.*?)\\]\\(.*?\\)/g, '$1')  // remove markdown links
        .replace(/^\\s*[\\*\\-\\+•]\\s+/gm, '')   // remove bullet symbols
        .replace(/^\\s*\\d+\\.\\s+/gm, '')       // remove numbered list prefixes
        .replace(/\\n+/g, ' ')                // replace newlines with space
        .trim();
    }

    function formatMarkdown(text) {
      if (!text) return "";
      let escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
      
      // bold **text**
      escaped = escaped.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      // italic *text*
      escaped = escaped.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
      // bullet lines
      escaped = escaped.replace(/^[\\*\\-\\•]\\s+(.*)$/gm, '<div style="margin-left: 12px; margin-bottom: 3px;">• $1</div>');
      // newlines to paragraphs / breaks
      escaped = escaped.replace(/\\n\\n+/g, '<div style="margin-bottom: 0.6rem;"></div>');
      escaped = escaped.replace(/\\n/g, '<br>');
      return escaped;
    }

    function getHindiVoice() {
      if (!window.speechSynthesis) return null;
      const voices = window.speechSynthesis.getVoices();
      if (!voices || voices.length === 0) return null;
      
      return voices.find(v => v.lang === 'hi-IN' || v.lang === 'hi_IN') ||
             voices.find(v => v.lang.toLowerCase().startsWith('hi')) ||
             voices.find(v => v.name.toLowerCase().includes('hindi')) ||
             voices.find(v => v.lang.includes('IN')) ||
             voices[0];
    }

    if (window.speechSynthesis) {
      window.speechSynthesis.onvoiceschanged = () => {
        // Cache voices in background
        getHindiVoice();
      };
    }

    // Voice Clone & Audio State
    let selectedVoiceMode = 'default'; // 'default' or 'cloned'
    let selectedVoicePreset = 'aoede';
    let detectedPitchHz = 200;
    let currentAudioPlayer = null;
    let mediaRecorder = null;
    let recordedChunks = [];
    let recordTimerInterval = null;
    let recordSeconds = 0;
    let recordedBlob = null;
    let hasClonedVoice = false;

    function setVoiceMode(mode) {
      selectedVoiceMode = mode;
      localStorage.setItem('pahadiVoiceMode', mode);
      
      const labels = document.querySelectorAll('.voiceModeLabel');
      const btns = document.querySelectorAll('.voiceModeToggleBtn, #voiceModeToggle');
      
      if (mode === 'cloned') {
        labels.forEach(lbl => {
          lbl.textContent = 'मेरी आवाज़ (Cloned) ✨';
          lbl.style.color = '#c084fc';
        });
        btns.forEach(btn => {
          btn.style.borderColor = '#c084fc';
          btn.style.background = 'rgba(192, 132, 252, 0.2)';
        });
      } else {
        labels.forEach(lbl => {
          lbl.textContent = 'डिफ़ॉल्ट आवाज़ (Default)';
          lbl.style.color = '#38bdf8';
        });
        btns.forEach(btn => {
          btn.style.borderColor = '';
          btn.style.background = '';
        });
      }
    }

    function onVoicePresetChange(val) {
      selectedVoicePreset = val;
    }

    function openVoiceCloneModal() {
      document.getElementById('voiceCloneModal').classList.add('active');
      checkVoiceCloneStatus();
    }

    function closeVoiceCloneModal() {
      document.getElementById('voiceCloneModal').classList.remove('active');
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        stopVoiceRecording();
      }
    }

    // Keyboard Escape key listener to cut/close modal
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeVoiceCloneModal();
        if (typeof closeKeyModal === 'function') closeKeyModal();
      }
    });

    async function checkVoiceCloneStatus() {
      try {
        const resp = await fetch('/api/voice/status');
        const data = await resp.json();
        hasClonedVoice = data.hasVoice;
        const icon = document.getElementById('voiceCloneStatusIcon');
        const text = document.getElementById('voiceCloneStatusText');
        const feedback = document.getElementById('voiceFeedback');
        
        if (data.profile && data.profile.voiceName) {
          selectedVoicePreset = data.profile.voiceName;
          const radio = document.querySelector(`input[name="voicePreset"][value="${selectedVoicePreset}"]`);
          if (radio) radio.checked = true;
        }

        if (data.hasVoice) {
          if (icon) icon.textContent = '🟢';
          if (text) text.textContent = 'मेरी आवाज़ (Active)';

          // If voice exists and user hasn't explicitly chosen 'default', activate cloned mode!
          const userSavedPref = localStorage.getItem('pahadiVoiceMode');
          if (userSavedPref !== 'default') {
            setVoiceMode('cloned');
          } else {
            setVoiceMode('default');
          }

          if (feedback) {
            feedback.style.display = 'block';
            feedback.style.color = '#34d399';
            feedback.style.background = 'rgba(16, 185, 129, 0.15)';
            feedback.style.border = '1px solid #10b981';
            feedback.innerHTML = `✅ <strong>आपकी आवाज़ सुरक्षित है</strong> (${(data.voiceSizeBytes / 1024).toFixed(1)} KB, Preset: ${selectedVoicePreset.toUpperCase()})। चैट व अनुवाद में 'मेरी आवाज़' सक्रिय है।`;
          }
        } else {
          setVoiceMode('default');
          if (icon) icon.textContent = '🎙️';
          if (text) text.textContent = 'मेरी आवाज़ (Voice)';
        }
      } catch (e) {
        console.error("Voice status error", e);
      }
    }

    function toggleVoiceMode() {
      if (selectedVoiceMode === 'default') {
        if (!hasClonedVoice) {
          openVoiceCloneModal();
          const feedback = document.getElementById('voiceFeedback');
          if (feedback) {
            feedback.style.display = 'block';
            feedback.style.color = '#f59e0b';
            feedback.textContent = '⚠️ कृपया पहले नीचे अपना 8-10 सेकंड का वॉइस सैंपल रिकॉर्ड या अपलोड करें!';
          }
          return;
        }
        setVoiceMode('cloned');
      } else {
        setVoiceMode('default');
      }
    }

    async function analyzeRecordedAudioPitch(blob) {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const arrayBuf = await blob.arrayBuffer();
        const audioBuf = await ctx.decodeAudioData(arrayBuf);
        const chanData = audioBuf.getChannelData(0);
        const rate = audioBuf.sampleRate;

        // Autocorrelation pitch detector
        const start = Math.floor(chanData.length * 0.25);
        const len = Math.min(2048, Math.floor(chanData.length * 0.5));
        let bestCorrelation = 0;
        let bestOffset = -1;
        const minOffset = Math.floor(rate / 350); // ~350 Hz
        const maxOffset = Math.floor(rate / 85);  // ~85 Hz

        for (let offset = minOffset; offset <= maxOffset; offset++) {
          let diffSum = 0;
          for (let i = 0; i < len; i++) {
            diffSum += Math.abs(chanData[start + i] - chanData[start + i + offset]);
          }
          const correlation = 1 - (diffSum / len);
          if (correlation > bestCorrelation) {
            bestCorrelation = correlation;
            bestOffset = offset;
          }
        }

        if (bestOffset > 0) {
          detectedPitchHz = Math.round(rate / bestOffset);
        }
        ctx.close();

        // Intelligent tone mapping
        if (detectedPitchHz < 145) {
          selectedVoicePreset = 'fenrir';
        } else if (detectedPitchHz < 175) {
          selectedVoicePreset = 'puck';
        } else if (detectedPitchHz < 215) {
          selectedVoicePreset = 'aoede';
        } else {
          selectedVoicePreset = 'kore';
        }

        const radio = document.querySelector(`input[name="voicePreset"][value="${selectedVoicePreset}"]`);
        if (radio) radio.checked = true;

        const info = document.getElementById('detectedPitchInfo');
        if (info) {
          info.style.display = 'block';
          info.textContent = `🎯 स्वर विश्लेषण: अनुमानित पिच ~${detectedPitchHz} Hz (सुझाया गया न्यूरल टोन: ${selectedVoicePreset.toUpperCase()})`;
        }
      } catch (err) {
        console.warn("Pitch analysis notice:", err);
      }
    }

    async function startVoiceRecording() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recordedChunks = [];
        mediaRecorder = new MediaRecorder(stream);
        
        mediaRecorder.ondataavailable = (e) => {
          if (e.data && e.data.size > 0) {
            recordedChunks.push(e.data);
          }
        };

        mediaRecorder.onstop = async () => {
          recordedBlob = new Blob(recordedChunks, { type: 'audio/wav' });
          const audioUrl = URL.createObjectURL(recordedBlob);
          const player = document.getElementById('recordedAudioPlayer');
          player.src = audioUrl;
          document.getElementById('recordedPreviewSection').style.display = 'block';
          document.getElementById('recordStatus').textContent = '✅ रिकॉर्डिंग पूरी हुई! विश्लेषण किया जा रहा है...';
          await analyzeRecordedAudioPitch(recordedBlob);
          document.getElementById('recordStatus').textContent = '✅ रिकॉर्डिंग पूरी हुई! नीचे प्ले करके देखें या सेव करें।';
        };

        mediaRecorder.start();
        document.getElementById('startRecordBtn').style.display = 'none';
        document.getElementById('stopRecordBtn').style.display = 'inline-block';
        document.getElementById('recordedPreviewSection').style.display = 'none';
        document.getElementById('recordStatus').textContent = '🔴 रिकॉर्ड हो रहा है... कृपया दिया गया वाक्य स्पष्ट बोलें!';

        recordSeconds = 0;
        document.getElementById('recordTimer').textContent = '00:00';
        clearInterval(recordTimerInterval);
        recordTimerInterval = setInterval(() => {
          recordSeconds++;
          const sec = recordSeconds < 10 ? '0' + recordSeconds : recordSeconds;
          document.getElementById('recordTimer').textContent = `00:${sec}`;
          if (recordSeconds >= 12) {
            stopVoiceRecording();
          }
        }, 1000);

      } catch (err) {
        alert("माइक्रोफोन का एक्सेस नहीं मिल सका। कृपया ब्राउज़र में माइक की अनुमति दें।");
      }
    }

    function stopVoiceRecording() {
      clearInterval(recordTimerInterval);
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
      }
      document.getElementById('startRecordBtn').style.display = 'inline-block';
      document.getElementById('stopRecordBtn').style.display = 'none';
    }

    async function uploadRecordedVoice() {
      if (!recordedBlob) return;
      const feedback = document.getElementById('voiceFeedback');
      const saveBtn = document.getElementById('saveVoiceBtn');
      if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.textContent = '⏳ सुरक्षित हो रहा है...';
      }

      feedback.style.display = 'block';
      feedback.style.color = '#38bdf8';
      feedback.style.background = 'rgba(56, 189, 248, 0.15)';
      feedback.style.border = '1px solid #38bdf8';
      feedback.textContent = 'आपकी आवाज़ और न्यूरल प्रोफाइल सुरक्षित की जा रही है...';

      const reader = new FileReader();
      reader.onloadend = async () => {
        const base64Audio = reader.result;
        try {
          const resp = await fetch('/api/voice/upload', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              audioData: base64Audio,
              voiceName: selectedVoicePreset,
              pitchHz: detectedPitchHz
            })
          });
          const data = await resp.json();
          if (data.success) {
            hasClonedVoice = true;
            setVoiceMode('cloned');
            checkVoiceCloneStatus();

            feedback.style.color = '#34d399';
            feedback.style.background = 'rgba(16, 185, 129, 0.2)';
            feedback.style.border = '1px solid #10b981';
            feedback.innerHTML = `
              <div style="font-weight: 700; font-size: 1rem; margin-bottom: 4px;">🎉 बधाई! आपकी आवाज़ AI में सुरक्षित हो गई है।</div>
              <div>अब चैट और अनुवाद दोनों में AI आपकी न्यूरल आवाज़ में बोलेगा।</div>
              <div style="margin-top: 8px; font-size: 0.85rem; color: #a7f3d0; font-weight: 600;">
                ⏱️ यह विंडो <strong>1.5 सेकंड में स्वतः बंद हो जाएगी</strong> (या ऊपर लाल 'कट करें' दबाएं)।
              </div>
            `;

            if (saveBtn) {
              saveBtn.textContent = '✅ आवाज़ सुरक्षित हो गई!';
              saveBtn.style.background = '#10b981';
            }

            // Auto-close modal after 1.8 seconds so user is never stuck
            setTimeout(() => {
              closeVoiceCloneModal();
              if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.textContent = '💾 यह आवाज़ AI में सुरक्षित करें (Save Voice)';
                saveBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
              }
            }, 1800);

          } else {
            feedback.style.color = '#f87171';
            feedback.style.background = 'rgba(239, 68, 68, 0.15)';
            feedback.style.border = '1px solid #ef4444';
            feedback.textContent = data.error || 'आवाज़ सुरक्षित करने में त्रुटि आई।';
            if (saveBtn) {
              saveBtn.disabled = false;
              saveBtn.textContent = '💾 पुनः प्रयास करें (Try Again)';
            }
          }
        } catch (e) {
          feedback.style.color = '#f87171';
          feedback.textContent = 'सर्वर से संपर्क करने में असमर्थ।';
          if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.textContent = '💾 पुनः प्रयास करें (Try Again)';
          }
        }
      };
      reader.readAsDataURL(recordedBlob);
    }

    async function handleVoiceFileUpload(e) {
      const file = e.target.files[0];
      if (!file) return;
      recordedBlob = file;
      const player = document.getElementById('recordedAudioPlayer');
      player.src = URL.createObjectURL(file);
      document.getElementById('recordedPreviewSection').style.display = 'block';
      await analyzeRecordedAudioPitch(file);
      uploadRecordedVoice();
    }

    function stopAllSpeech() {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      if (currentAudioPlayer) {
        currentAudioPlayer.pause();
        currentAudioPlayer.currentTime = 0;
        currentAudioPlayer = null;
      }
      if (currentSpeakingBtn) {
        currentSpeakingBtn.classList.remove('speaking');
        const label = currentSpeakingBtn.querySelector('.tts-label');
        const icon = currentSpeakingBtn.querySelector('.tts-icon');
        if (label) label.textContent = 'सुनें (Read Aloud)';
        if (icon) icon.textContent = '🔊';
        const parentMsg = currentSpeakingBtn.closest('.message');
        if (parentMsg) parentMsg.classList.remove('speaking-bubble');
        currentSpeakingBtn = null;
      }
      const stopBtn = document.getElementById('globalStopTtsBtn');
      if (stopBtn) stopBtn.style.display = 'none';
      currentSpeakingUtterance = null;
    }

    async function speakText(rawText, btnElement = null) {
      // If user clicks the currently active speaking button, stop it
      if (btnElement && btnElement === currentSpeakingBtn) {
        stopAllSpeech();
        return;
      }

      stopAllSpeech();

      const spokenText = cleanTextForSpeech(rawText);
      if (!spokenText) return;

      if (btnElement) {
        currentSpeakingBtn = btnElement;
        btnElement.classList.add('speaking');
        const label = btnElement.querySelector('.tts-label');
        const icon = btnElement.querySelector('.tts-icon');
        if (label) label.textContent = selectedVoiceMode === 'cloned' ? '⏳ आवाज़ बन रही है...' : 'रोकें (Stop)';
        if (icon) icon.textContent = selectedVoiceMode === 'cloned' ? '✨' : '⏹️';
        const parentMsg = btnElement.closest('.message');
        if (parentMsg) parentMsg.classList.add('speaking-bubble');
      }

      const stopBtn = document.getElementById('globalStopTtsBtn');
      if (stopBtn) stopBtn.style.display = 'inline-flex';

      // 1. Cloned Voice Mode (Neural TTS)
      if (selectedVoiceMode === 'cloned') {
        try {
          const resp = await fetch('/api/voice/synthesize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              text: spokenText,
              voiceName: selectedVoicePreset
            })
          });
          const data = await resp.json();
          if (data.success && data.audioUrl) {
            if (btnElement) {
              const label = btnElement.querySelector('.tts-label');
              const icon = btnElement.querySelector('.tts-icon');
              if (label) label.textContent = 'रोकें (Stop)';
              if (icon) icon.textContent = '⏹️';
            }
            if (currentAudioPlayer) {
              currentAudioPlayer.pause();
              currentAudioPlayer = null;
            }
            // Add cache-busting timestamp to audio URL so browser plays the fresh audio
            const cacheBuster = data.audioUrl + (data.audioUrl.includes('?') ? '&' : '?') + 't=' + Date.now();
            currentAudioPlayer = new Audio(cacheBuster);
            currentAudioPlayer.onended = () => stopAllSpeech();
            currentAudioPlayer.onerror = (err) => {
              console.error("Audio playback error:", err);
              stopAllSpeech();
            };
            await currentAudioPlayer.play();
            return;
          } else {
            console.warn("Cloned synthesis notice, falling back to browser voice:", data.error);
          }
        } catch (e) {
          console.warn("Cloned synthesis error, falling back to browser voice:", e);
        }
      }

      // 2. Browser Voice (Default Mode or Fallback)
      if (!window.speechSynthesis) {
        alert("आपका ब्राउज़र टेक्स्ट-टू-स्पीच का समर्थन नहीं करता है।");
        stopAllSpeech();
        return;
      }

      if (btnElement) {
        const label = btnElement.querySelector('.tts-label');
        const icon = btnElement.querySelector('.tts-icon');
        if (label) label.textContent = 'रोकें (Stop)';
        if (icon) icon.textContent = '⏹️';
      }

      const utterance = new SpeechSynthesisUtterance(spokenText);
      const voice = getHindiVoice();
      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      } else {
        utterance.lang = 'hi-IN';
      }

      if (selectedVoiceMode === 'cloned') {
        if (selectedVoicePreset === 'fenrir') utterance.pitch = 0.8;
        else if (selectedVoicePreset === 'puck') utterance.pitch = 1.0;
        else if (selectedVoicePreset === 'aoede') utterance.pitch = 1.15;
        else if (selectedVoicePreset === 'kore') utterance.pitch = 1.25;
      } else {
        utterance.pitch = 1.0;
      }

      utterance.rate = 0.95;
      utterance.onend = () => stopAllSpeech();
      utterance.onerror = () => stopAllSpeech();

      currentSpeakingUtterance = utterance;
      window.speechSynthesis.speak(utterance);
    }

    function speakChatMessage(btn) {
      const rawText = btn.dataset.rawText ? decodeURIComponent(btn.dataset.rawText) : "";
      if (rawText) {
        speakText(rawText, btn);
      } else {
        const parent = btn.closest('.message');
        const content = parent.querySelector('.msg-content') || parent;
        speakText(content.innerText, btn);
      }
    }

    function toggleAutoRead() {
      isAutoReadEnabled = !isAutoReadEnabled;
      const statusSpan = document.getElementById('autoReadStatus');
      const btn = document.getElementById('autoReadToggle');
      if (isAutoReadEnabled) {
        statusSpan.textContent = 'चालू 🔊';
        statusSpan.style.color = '#34d399';
        btn.style.borderColor = '#10b981';
        btn.style.background = 'rgba(16, 185, 129, 0.15)';
      } else {
        statusSpan.textContent = 'बंद';
        statusSpan.style.color = '#f87171';
        btn.style.borderColor = '';
        btn.style.background = '';
        stopAllSpeech();
      }
    }

    // Chat functionality
    function setChatMode(mode, btn) {
      currentChatMode = mode;
      document.querySelectorAll('.mode-chip').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
    }

    async function sendChatMessage() {
      const input = document.getElementById('chatInput');
      const msg = input.value.trim();
      if (!msg) return;
      input.value = '';

      const container = document.getElementById('chatMessages');
      const uDiv = document.createElement('div');
      uDiv.className = 'message user';
      uDiv.textContent = msg;
      container.appendChild(uDiv);

      chatHistory.push({ isUser: true, text: msg });

      const aDiv = document.createElement('div');
      aDiv.className = 'message assistant';
      aDiv.innerHTML = '<div class="msg-content" style="color: #93c5fd;">विचार कर रहा हूँ... 🏔️</div>';
      container.appendChild(aDiv);
      container.scrollTop = container.scrollHeight;

      try {
        const resp = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            mode: currentChatMode,
            dialect: document.getElementById('dialectSelect').value,
            history: chatHistory
          })
        });
        const data = await resp.json();
        const formattedHtml = formatMarkdown(data.reply);
        aDiv.innerHTML = `
          <div class="msg-content">${formattedHtml}</div>
          <div class="msg-actions">
            <button class="btn-tts" onclick="speakChatMessage(this)" title="बोलकर सुनाएं (Read Aloud)">
              <span class="tts-icon">🔊</span> <span class="tts-label">सुनें (Read Aloud)</span>
            </button>
          </div>
        `;
        const ttsBtn = aDiv.querySelector('.btn-tts');
        ttsBtn.dataset.rawText = encodeURIComponent(data.reply);
        chatHistory.push({ isUser: false, text: data.reply });

        // Auto-read aloud if enabled
        if (isAutoReadEnabled) {
          speakText(data.reply, ttsBtn);
        }
      } catch (e) {
        aDiv.innerHTML = '<div class="msg-content" style="color:#f87171;">क्षमा करें, प्रतिक्रिया प्राप्त करने में समस्या हुई। कृपया पुनः प्रयास करें।</div>';
      }
      container.scrollTop = container.scrollHeight;
    }

    function toggleChatMic() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) return alert("ब्राउज़र स्पीच का समर्थन नहीं करता");
      const rec = new SpeechRecognition();
      rec.lang = 'hi-IN';
      rec.onresult = (e) => {
        document.getElementById('chatInput').value = e.results[0][0].transcript;
        sendChatMessage();
      };
      rec.start();
    }

    // Phrases
    async function loadPhrases() {
      const r = await fetch('/api/phrases');
      phrases = await r.json();
      renderPhrases();
    }

    function renderPhrases() {
      const filter = document.getElementById('phraseDialectFilter').value;
      const grid = document.getElementById('phraseGrid');
      grid.innerHTML = '';

      const filtered = filter === 'all' ? phrases : phrases.filter(p => p.dialect === filter);
      filtered.forEach(p => {
        const card = document.createElement('div');
        card.className = 'phrase-card';
        card.innerHTML = `
          <span class="badge" style="background: rgba(245, 158, 11, 0.2); color: #fcd34d;">${p.categoryHindi || p.category}</span>
          <div class="phrase-target">${p.translation}</div>
          <div class="phrase-phonetic">${p.phonetic}</div>
          <p style="font-size: 0.95rem; margin-bottom: 6px;"><strong>हिंदी:</strong> ${p.hindi}</p>
          <p class="phrase-meta">💡 ${p.culturalNote}</p>
        `;
        grid.appendChild(card);
      });
    }

    // Knowledge & Emergency
    async function loadEmergency() {
      const r = await fetch('/api/emergency');
      const list = await r.json();
      const grid = document.getElementById('emergencyGrid');
      grid.innerHTML = '';
      list.forEach(item => {
        const el = document.createElement('div');
        el.className = 'emergency-card';
        el.innerHTML = `
          <div style="font-size: 1.8rem;">${item.icon}</div>
          <div>
            <div class="num">${item.number}</div>
            <strong style="font-size: 0.85rem; display: block;">${item.titleHindi}</strong>
            <span style="font-size: 0.75rem; color: var(--text-muted);">${item.description}</span>
          </div>
        `;
        grid.appendChild(el);
      });
    }

    async function loadKnowledge() {
      const r = await fetch('/api/knowledge');
      const list = await r.json();
      const grid = document.getElementById('knowledgeGrid');
      grid.innerHTML = '';
      list.forEach(k => {
        const el = document.createElement('div');
        el.className = 'phrase-card';
        el.innerHTML = `
          <span class="badge" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8;">${k.category}</span>
          <h4 style="margin: 8px 0; color: #f8fafc;">${k.title}</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">${k.summary}</p>
          <div style="font-size: 0.8rem; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 8px; white-space: pre-line;">${k.details}</div>
        `;
        grid.appendChild(el);
      });
    }

    async function loadStories() {
      const r = await fetch('/api/stories');
      const list = await r.json();
      const grid = document.getElementById('storiesGrid');
      grid.innerHTML = '';
      list.forEach(s => {
        const el = document.createElement('div');
        el.className = 'phrase-card';
        el.innerHTML = `
          <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">${s.region}</span>
          <h4 style="margin: 8px 0; color: #f8fafc;">${s.titleHindi}</h4>
          <p style="font-size: 0.85rem; color: #a5b4fc; font-style: italic; margin-bottom: 6px;">${s.titleEnglish}</p>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 8px;">${s.summary}</p>
          <div style="font-size: 0.8rem; background: rgba(0,0,0,0.2); padding: 8px; border-radius: 8px; white-space: pre-line;">${s.fullStory}</div>
        `;
        grid.appendChild(el);
      });
    }

    // Modal & API Key
    function openKeyModal() { document.getElementById('keyModal').classList.add('active'); }
    function closeKeyModal() { document.getElementById('keyModal').classList.remove('active'); }

    async function checkKeyStatus() {
      try {
        const r = await fetch('/api/status');
        const st = await r.json();
        const text = document.getElementById('keyStatusText');
        const badgeBox = document.getElementById('badgeContainer');
        if (st.hasKey) {
          text.textContent = "🟢 Online AI Active";
          text.style.color = "#34d399";
          if (badgeBox && !badgeBox.dataset.hasResult) {
            badgeBox.innerHTML = '<span class="badge badge-ai">🟢 Online AI Engine Ready</span>';
          }
        } else {
          text.textContent = "🟠 Go Online (API Key)";
          text.style.color = "#fcd34d";
          if (badgeBox && !badgeBox.dataset.hasResult) {
            badgeBox.innerHTML = '<span class="badge badge-offline">Offline Engine (Tap "Go Online" above)</span>';
          }
        }
      } catch (e) {
        console.error("Status check failed", e);
      }
    }

    async function saveGeminiKey() {
      const key = document.getElementById('geminiKeyInput').value.trim();
      const feedback = document.getElementById('keyFeedback');
      if (!key) {
        feedback.style.display = 'block';
        feedback.style.color = '#f87171';
        feedback.textContent = '⚠️ कृपया अपनी Gemini API Key पेस्ट करें!';
        return;
      }
      
      feedback.style.display = 'block';
      feedback.style.color = '#38bdf8';
      feedback.textContent = 'सत्यापित और सुरक्षित किया जा रहा है...';

      try {
        const resp = await fetch('/api/set-key', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ key: key })
        });
        const data = await resp.json();
        if (data.success) {
          feedback.style.color = '#34d399';
          feedback.textContent = '✅ शानदार! API Key सुरक्षित हो गई और ऑनलाइन मोड सक्रिय हो गया है!';
          setTimeout(() => {
            closeKeyModal();
            checkKeyStatus();
            feedback.style.display = 'none';
          }, 1200);
        } else {
          feedback.style.color = '#f87171';
          feedback.textContent = data.error || 'त्रुटि: की सुरक्षित नहीं हो सकी।';
        }
      } catch (err) {
        feedback.style.color = '#f87171';
        feedback.textContent = 'सर्वर से संपर्क करने में असमर्थ।';
      }
    }

    window.onload = init;
  </script>
</body>
</html>
"""

