# -*- coding: utf-8 -*-
"""
Himalayan Pine & Saffron Themed Web Application UI
Integrated with Gemini AI Backend, Dialect Translation, Voice Synthesis,
Living Heritage Glossary, and Emergency Services.
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>हिमाचली व हिन्दी AI सहायक | Pahadi-Hindi AI Assistant</title>
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#0a130e" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-capable" content="yes" />

  <!-- Fonts: Inter & Noto Sans Devanagari -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --pine-900: #072213;
      --pine-800: #0b391f;
      --pine-700: #134e2c;
      --pine-500: #228b53;
      --saffron-500: #e58e26;
      --saffron-400: #f39c12;
      --bg-dark: #0a130e;
      --surface-glass: rgba(16, 37, 26, 0.82);
      --surface-border: rgba(255, 255, 255, 0.12);
      --text-main: #f5f6fa;
      --text-muted: #a4b0be;
      --user-bubble: #174229;
      --bot-bubble: rgba(22, 45, 33, 0.9);
      --radius-lg: 16px;
      --radius-sm: 8px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Noto Sans Devanagari', 'Inter', -apple-system, sans-serif;
    }

    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(19, 78, 44, 0.4) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(229, 142, 38, 0.18) 0%, transparent 45%),
        radial-gradient(circle at 50% 50%, rgba(7, 34, 19, 0.6) 0%, transparent 80%);
      color: var(--text-main);
      height: 100vh;
      display: flex;
      overflow: hidden;
    }

    /* Layout Sidebar */
    .sidebar {
      width: 320px;
      background: var(--surface-glass);
      backdrop-filter: blur(16px);
      border-right: 1px solid var(--surface-border);
      display: flex;
      flex-direction: column;
      padding: 20px;
      gap: 16px;
      z-index: 20;
      transition: transform 0.3s ease;
      overflow-y: auto;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .brand-icon {
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--saffron-500), var(--pine-500));
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: #fff;
      box-shadow: 0 4px 14px rgba(229, 142, 38, 0.3);
      flex-shrink: 0;
    }

    .brand-title h1 {
      font-size: 1.05rem;
      font-weight: 700;
      color: #fff;
      line-height: 1.2;
    }

    .brand-title p {
      font-size: 0.75rem;
      color: var(--saffron-400);
      font-weight: 500;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.72rem;
      padding: 3px 8px;
      border-radius: 100px;
      background: rgba(34, 139, 83, 0.2);
      border: 1px solid rgba(34, 139, 83, 0.4);
      color: #4ade80;
    }
    .status-pill.offline {
      background: rgba(245, 158, 11, 0.15);
      border-color: rgba(245, 158, 11, 0.3);
      color: #fcd34d;
    }
    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: currentColor;
    }

    .section-label {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .persona-select {
      width: 100%;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 8px 10px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      outline: none;
      cursor: pointer;
    }
    .persona-select option {
      background: #0f241a;
      color: #fff;
    }

    .dialect-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      max-height: 38vh;
      overflow-y: auto;
      padding-right: 2px;
    }
    .dialect-list::-webkit-scrollbar {
      width: 4px;
    }
    .dialect-list::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
    }

    .dialect-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 9px 12px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s ease;
      font-size: 0.86rem;
      text-align: left;
    }

    .dialect-btn:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: var(--pine-500);
      transform: translateX(2px);
    }

    .dialect-btn.active {
      background: linear-gradient(90deg, rgba(19, 78, 44, 0.9), rgba(11, 57, 31, 0.95));
      border-color: var(--saffron-500);
      color: #fff;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }

    .dialect-badge {
      font-size: 0.68rem;
      padding: 2px 6px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 4px;
      color: var(--text-muted);
      white-space: nowrap;
    }

    .dialect-btn.active .dialect-badge {
      background: var(--saffron-500);
      color: #111;
      font-weight: bold;
    }

    .sidebar-actions {
      margin-top: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.84rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
    }

    /* Main Chat Area */
    .main-chat {
      flex: 1;
      display: flex;
      flex-direction: column;
      position: relative;
      background: transparent;
    }

    .chat-header {
      padding: 14px 22px;
      background: var(--surface-glass);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .mobile-menu-btn {
      display: none;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--surface-border);
      color: #fff;
      font-size: 1.1rem;
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      cursor: pointer;
    }

    .current-dialect-info h2 {
      font-size: 1.05rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .current-dialect-info p {
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .btn-icon-top {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: 0.2s;
    }
    .btn-icon-top:hover {
      background: rgba(255, 255, 255, 0.12);
    }
    .btn-icon-top.active-toggle {
      background: rgba(229, 142, 38, 0.25);
      border-color: var(--saffron-500);
      color: var(--saffron-400);
    }

    /* Translation Banner / Direct Switcher */
    .view-switcher-bar {
      padding: 8px 22px;
      background: rgba(11, 57, 31, 0.35);
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 0.82rem;
    }

    .view-tabs {
      display: flex;
      gap: 6px;
    }
    .view-tab {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 4px 10px;
      border-radius: 100px;
      cursor: pointer;
      font-size: 0.78rem;
      transition: all 0.2s;
    }
    .view-tab.active {
      background: var(--pine-700);
      color: #fff;
      border-color: rgba(34, 139, 83, 0.6);
    }

    /* Chat Messages */
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 20px 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .message {
      max-width: 78%;
      display: flex;
      flex-direction: column;
      gap: 5px;
      animation: fadeIn 0.25s ease-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .message.user {
      align-self: flex-end;
    }

    .message.bot {
      align-self: flex-start;
    }

    .bubble {
      padding: 13px 18px;
      border-radius: var(--radius-lg);
      font-size: 0.94rem;
      line-height: 1.55;
      border: 1px solid var(--surface-border);
      position: relative;
      word-break: break-word;
      white-space: pre-wrap;
    }

    .message.user .bubble {
      background: var(--user-bubble);
      border-bottom-right-radius: 4px;
      border-color: rgba(34, 139, 83, 0.5);
      color: #fff;
    }

    .message.bot .bubble {
      background: var(--bot-bubble);
      border-bottom-left-radius: 4px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }

    .pronunciation {
      font-size: 0.8rem;
      color: var(--saffron-400);
      font-style: italic;
      margin-top: 8px;
      border-top: 1px dashed rgba(255, 255, 255, 0.12);
      padding-top: 6px;
    }

    .cultural-context-box {
      font-size: 0.78rem;
      color: #94a3b8;
      margin-top: 6px;
      background: rgba(0, 0, 0, 0.25);
      padding: 6px 10px;
      border-radius: 6px;
      border-left: 2px solid var(--saffron-500);
    }

    .message-meta {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 0.72rem;
      color: var(--text-muted);
      padding: 0 4px;
    }

    .action-icon-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.78rem;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: color 0.2s;
    }

    .action-icon-btn:hover {
      color: #fff;
    }

    .typing-indicator {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
    }
    .typing-dot {
      width: 6px;
      height: 6px;
      background: var(--saffron-400);
      border-radius: 50%;
      animation: bounce 1.2s infinite ease-in-out;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
      0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
      40% { transform: scale(1); opacity: 1; }
    }

    /* Translator Tab View (Dedicated Mode) */
    .translator-view {
      display: none;
      flex: 1;
      padding: 24px;
      overflow-y: auto;
      flex-direction: column;
      gap: 16px;
    }
    .translator-view.active {
      display: flex;
    }

    .trans-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 18px;
    }
    @media (max-width: 768px) {
      .trans-grid { grid-template-columns: 1fr; }
    }

    .trans-card {
      background: var(--bot-bubble);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .trans-card textarea {
      width: 100%;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-sm);
      color: #fff;
      padding: 12px;
      font-size: 0.95rem;
      min-height: 140px;
      outline: none;
      resize: vertical;
    }
    .trans-card textarea:focus {
      border-color: var(--saffron-500);
    }

    /* Chat Input Bar */
    .chat-input-bar {
      padding: 14px 22px;
      background: var(--surface-glass);
      backdrop-filter: blur(12px);
      border-top: 1px solid var(--surface-border);
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }

    .input-wrapper {
      flex: 1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      display: flex;
      align-items: center;
      padding: 6px 12px;
      gap: 8px;
      transition: border-color 0.2s;
    }

    .input-wrapper:focus-within {
      border-color: var(--saffron-500);
      background: rgba(255, 255, 255, 0.08);
    }

    .chat-textarea {
      flex: 1;
      background: transparent;
      border: none;
      color: var(--text-main);
      font-size: 0.94rem;
      outline: none;
      resize: none;
      max-height: 120px;
      min-height: 24px;
      line-height: 1.45;
    }

    .mic-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 1.1rem;
      padding: 4px;
      border-radius: 50%;
      transition: all 0.2s;
    }
    .mic-btn:hover {
      color: #fff;
    }
    .mic-btn.recording {
      color: #ef4444;
      animation: pulse 1s infinite alternate;
    }

    @keyframes pulse {
      from { transform: scale(1); }
      to { transform: scale(1.2); }
    }

    .send-btn {
      background: linear-gradient(135deg, var(--saffron-500), var(--pine-500));
      border: none;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.1rem;
      transition: transform 0.1s, opacity 0.2s;
      flex-shrink: 0;
      box-shadow: 0 4px 12px rgba(229, 142, 38, 0.3);
    }

    .send-btn:active {
      transform: scale(0.94);
    }

    /* Modal Overlay & Dialogs */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 99;
      padding: 16px;
    }

    .modal-card {
      background: #0d2217;
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      width: 100%;
      max-width: 580px;
      max-height: 82vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
      animation: modalIn 0.25s ease-out;
    }

    @keyframes modalIn {
      from { transform: scale(0.95); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .modal-header {
      padding: 14px 20px;
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(0, 0, 0, 0.2);
    }

    .modal-body {
      padding: 16px 20px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .dict-entry {
      background: rgba(255, 255, 255, 0.03);
      padding: 12px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    .dict-word {
      font-weight: 600;
      color: var(--saffron-400);
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }

    .dict-meaning {
      font-size: 0.88rem;
      color: #e2e8f0;
      margin-top: 4px;
    }
    .dict-note {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .key-input {
      width: 100%;
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--surface-border);
      color: #fff;
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      font-size: 0.9rem;
      outline: none;
    }
    .key-input:focus {
      border-color: var(--saffron-500);
    }

    .btn-primary-action {
      background: linear-gradient(135deg, var(--saffron-500), var(--pine-500));
      border: none;
      color: #fff;
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      font-weight: 600;
      cursor: pointer;
      font-size: 0.9rem;
      transition: all 0.2s;
    }

    /* Voice Recording Modal */
    .audio-visualizer {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      height: 60px;
      background: rgba(0, 0, 0, 0.3);
      border-radius: var(--radius-sm);
      margin: 10px 0;
    }
    .visualizer-bar {
      width: 6px;
      height: 20px;
      background: var(--saffron-400);
      border-radius: 3px;
      transition: height 0.1s ease;
    }

    @media (max-width: 768px) {
      .sidebar {
        position: absolute;
        left: -330px;
        height: 100%;
        box-shadow: 10px 0 30px rgba(0,0,0,0.5);
      }
      .sidebar.open {
        transform: translateX(330px);
      }
      .mobile-menu-btn {
        display: block;
      }
      .message {
        max-width: 90%;
      }
      .header-actions {
        display: none;
      }
    }
  </style>
</head>
<body>

  <!-- Sidebar / Dialect Switcher -->
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="brand-icon">🏔️</div>
      <div class="brand-title">
        <h1>पहाड़ी-हिन्दी AI</h1>
        <p>Himalayan Dialects Assistant</p>
      </div>
    </div>

    <div>
      <div class="section-label">
        <span>सिस्टम स्थिति</span>
        <span class="status-pill offline" id="statusPill">
          <span class="status-dot"></span>
          <span id="statusText">ऑफ़लाइन</span>
        </span>
      </div>
      <select id="personaModeSelect" class="persona-select" onchange="changePersonaMode(this.value)">
        <option value="standard">🏔️ सर्व-सहायक मोड (Standard)</option>
        <option value="elder">👵 बुजुर्ग मित्र मोड (Elder Friendly)</option>
        <option value="student">📚 छात्र सहायक मोड (Student Helper)</option>
        <option value="farmer">🍎 बागवान व किसान मित्र (Apple Farmer)</option>
      </select>
    </div>

    <div>
      <div class="section-label">
        <span>बोली चुनें (Select Dialect)</span>
        <span id="dialectCount" style="font-size:0.68rem; color:var(--saffron-400);">10 बोलियां</span>
      </div>
      <div class="dialect-list" id="dialectList">
        <button class="dialect-btn active" onclick="setDialect('hindi', 'मानक हिन्दी', 'राजभाषा / Standard Hindi', this)">
          <span>मानक हिन्दी</span>
          <span class="dialect-badge">Hindi</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('kangri', 'कांगड़ी (Kangri)', 'कांगड़ा घाटी, हमीरपुर, ऊना', this)">
          <span>कांगड़ी (Kangri)</span>
          <span class="dialect-badge">Kangra</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('mandeali', 'मंडीयाली (Mandeali)', 'मंडी, सुंदरनगर, छोटी काशी', this)">
          <span>मंडीयाली (Mandeali)</span>
          <span class="dialect-badge">Mandi</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('kullui', 'कुल्लवी (Kullui)', 'कुल्लू घाटी, मनाली, बंजार', this)">
          <span>कुल्लवी (Kullui)</span>
          <span class="dialect-badge">Kullu</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('shimla_pahari', 'शिमला / महासूवी', 'शिमला, ठियोग, कोटखाई, रोहड़ू', this)">
          <span>महासूवी (Mahasuvi)</span>
          <span class="dialect-badge">Shimla</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('chambeali', 'चम्बियाली (Chambeali)', 'चंबा, रावी घाटी, भरमौर', this)">
          <span>चम्बियाली (Chambeali)</span>
          <span class="dialect-badge">Chamba</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('sirmauri', 'सिरमौरी (Sirmauri)', 'नाहन, रेणुका जी, गिरि-पार (हाटी)', this)">
          <span>सिरमौरी (Sirmauri)</span>
          <span class="dialect-badge">Sirmaur</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('garhwali', 'गढ़वाली (Garhwali)', 'श्रीनगर, पौड़ी, टिहरी, चमोली', this)">
          <span>गढ़वाली (Garhwali)</span>
          <span class="dialect-badge">Garhwal</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('kumaoni', 'कुमाऊँनी (Kumaoni)', 'अल्मोड़ा, नैनीताल, पिथौरागढ़', this)">
          <span>कुमाऊँनी (Kumaoni)</span>
          <span class="dialect-badge">Kumaon</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('dogri', 'डोगरी (Dogri)', 'जम्मू व शिवालिक क्षेत्र', this)">
          <span>डोगरी (Dogri)</span>
          <span class="dialect-badge">Dogri</span>
        </button>
        <button class="dialect-btn" onclick="setDialect('jaunsari', 'जौनसारी (Jaunsari)', 'जौनसार-बावर, चकराता', this)">
          <span>जौनसारी (Jaunsari)</span>
          <span class="dialect-badge">Jaunsar</span>
        </button>
      </div>
    </div>

    <div class="sidebar-actions">
      <button class="btn-secondary" onclick="openGlossaryModal()">
        📖 शब्दकोश व वाक्यांश (Glossary)
      </button>
      <button class="btn-secondary" onclick="openHeritageModal()">
        🏛️ लोक धरोहर व कहानियां (Lore)
      </button>
      <button class="btn-secondary" onclick="openEmergencyModal()">
        🚨 आपातकालीन नंबर (Helplines)
      </button>
      <button class="btn-secondary" onclick="openVoiceModal()">
        🎙️ आवाज़ क्लोनिंग (Custom Voice)
      </button>
      <button class="btn-secondary" style="border-color:rgba(229, 142, 38, 0.4);" onclick="openKeyModal()">
        🔑 API Key सेट करें
      </button>
    </div>
  </aside>

  <!-- Main Chat & Workspace Area -->
  <main class="main-chat">
    <header class="chat-header">
      <div class="header-left">
        <button class="mobile-menu-btn" onclick="toggleSidebar()">☰</button>
        <div class="current-dialect-info">
          <h2 id="currentDialectTitle">मानक हिन्दी <span>•</span> <small style="font-size:0.8rem; color:var(--saffron-400);">सक्रिय</small></h2>
          <p id="currentDialectSub">राजभाषा / Standard Hindi</p>
        </div>
      </div>
      <div class="header-actions">
        <button class="btn-icon-top" id="phoneticsToggleBtn" onclick="togglePronunciation()">🔤 उच्चारण (Phonetics)</button>
        <button class="btn-icon-top" onclick="switchView('translator')">🔄 सीधा अनुवादक</button>
        <button class="btn-icon-top" onclick="clearChat()">🗑️ साफ़ करें</button>
      </div>
    </header>

    <!-- Mode Banner -->
    <div class="view-switcher-bar">
      <div class="view-tabs">
        <button class="view-tab active" id="tabChat" onclick="switchView('chat')">💬 संवाद (AI Chat)</button>
        <button class="view-tab" id="tabTrans" onclick="switchView('translator')">🔤 अनुवादक (Translator)</button>
      </div>
      <div style="color:var(--saffron-400); font-size:0.75rem;" id="activePersonaBadge">
        मोड: सर्व-सहायक
      </div>
    </div>

    <!-- Chat Messages Stream -->
    <div class="chat-messages" id="chatMessages">
      <div class="message bot">
        <div class="bubble">
          नमस्कार जी! 🙏 पहाड़ी संगम AI में आपका स्वागत है।
          
आप अपनी पसंदीदा पहाड़ी बोली (कांगड़ी, मण्डीयाली, कुल्लवी, शिमला/महासूवी, गढ़वाली, कुमाऊँनी, आदि) या मानक हिन्दी में सवाल पूछ सकते हैं, अनुवाद कर सकते हैं, या सेब बागवानी और पर्यटन की जानकारी प्राप्त कर सकते हैं।
          <div class="pronunciation" style="display:none;">
            Namaskar ji! Pahadi Sangam AI mein aapka swagat hai.
          </div>
        </div>
        <div class="message-meta">
          <span>AI सहायक</span>
          <button class="action-icon-btn" onclick="speakText(this)">🔊 बोलें</button>
          <button class="action-icon-btn" onclick="copyText(this)">📋 कॉपी</button>
        </div>
      </div>
    </div>

    <!-- Dedicated Direct Translator View -->
    <div class="translator-view" id="translatorView">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3 style="color:#fff;">द्वि-दिशा पहाड़ी अनुवादक (Bidirectional Translator)</h3>
        <label style="font-size:0.85rem; color:var(--saffron-400); cursor:pointer;">
          <input type="checkbox" id="reverseTranslateCheck" onchange="toggleTranslateDirection()"> पहाड़ी ➔ हिन्दी (Reverse)
        </label>
      </div>
      <div class="trans-grid">
        <div class="trans-card">
          <label style="font-weight:600; color:var(--text-muted);" id="transSourceLabel">स्रोत पाठ (हिंदी):</label>
          <textarea id="transInput" placeholder="यहाँ टेक्स्ट लिखें (उदा: आप कैसे हैं? / मौसम कैसा है?)"></textarea>
          <button class="btn-primary-action" onclick="handleDirectTranslate()">अनुवाद करें (Translate)</button>
        </div>
        <div class="trans-card">
          <label style="font-weight:600; color:var(--text-muted);" id="transTargetLabel">अनुवाद परिणाम (पहाड़ी):</label>
          <div id="transOutput" style="background:rgba(0,0,0,0.3); border:1px solid var(--surface-border); border-radius:var(--radius-sm); padding:14px; min-height:140px; color:#fff; font-size:1.05rem; white-space:pre-wrap;">
            परिणाम यहाँ दिखाई देगा...
          </div>
          <div id="transPhonetic" style="font-size:0.85rem; color:var(--saffron-400); font-style:italic;"></div>
          <div id="transContext" class="cultural-context-box" style="display:none;"></div>
        </div>
      </div>
    </div>

    <!-- Chat Input Bar -->
    <div class="chat-input-bar" id="chatInputBar">
      <div class="input-wrapper">
        <button class="mic-btn" id="micBtn" onclick="toggleSpeechRecognition()" title="आवाज़ से बोलें (Voice Input)">🎙️</button>
        <textarea 
          id="userInput" 
          class="chat-textarea" 
          rows="1" 
          placeholder="यहाँ सन्देश लिखें या प्रश्न पूछें... (उदा: सेब की प्रूनिंग कब करें? / तुसीं किद्दां हो?)" 
          onkeydown="handleKey(event)"
          oninput="autoResize(this)"></textarea>
      </div>
      <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
    </div>
  </main>

  <!-- Glossary Modal -->
  <div class="modal-overlay" id="glossaryModal" onclick="closeAllModals(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 style="color:#fff;">📖 पहाड़ी-हिन्दी शब्दकोश व प्रामाणिक वाक्यांश</h3>
        <button class="btn-secondary" style="padding:4px 10px;" onclick="closeModal('glossaryModal')">✕</button>
      </div>
      <div style="padding:10px 20px 0; display:flex; gap:8px;">
        <input type="text" id="glossarySearch" class="key-input" placeholder="वाक्यांश या शब्द खोजें..." oninput="filterGlossary()" />
      </div>
      <div class="modal-body" id="glossaryBody">
        <div style="color:var(--text-muted); text-align:center; padding:20px;">लोड हो रहा है...</div>
      </div>
    </div>
  </div>

  <!-- Heritage Lore Modal -->
  <div class="modal-overlay" id="heritageModal" onclick="closeAllModals(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 style="color:#fff;">🏛️ हिमालयी लोक धरोहर एवं कथाएं</h3>
        <button class="btn-secondary" style="padding:4px 10px;" onclick="closeModal('heritageModal')">✕</button>
      </div>
      <div class="modal-body" id="heritageBody">
        <div style="color:var(--text-muted); text-align:center; padding:20px;">लोड हो रहा है...</div>
      </div>
    </div>
  </div>

  <!-- Emergency Contacts Modal -->
  <div class="modal-overlay" id="emergencyModal" onclick="closeAllModals(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 style="color:#fff;">🚨 आपातकालीन व आपदा प्रबंधन हेल्पलाइन</h3>
        <button class="btn-secondary" style="padding:4px 10px;" onclick="closeModal('emergencyModal')">✕</button>
      </div>
      <div class="modal-body" id="emergencyBody">
        <div style="color:var(--text-muted); text-align:center; padding:20px;">लोड हो रहा है...</div>
      </div>
    </div>
  </div>

  <!-- API Key Modal -->
  <div class="modal-overlay" id="keyModal" onclick="closeAllModals(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 style="color:#fff;">🔑 Google Gemini API Key</h3>
        <button class="btn-secondary" style="padding:4px 10px;" onclick="closeModal('keyModal')">✕</button>
      </div>
      <div class="modal-body">
        <p style="font-size:0.85rem; color:var(--text-muted);">
          Google AI Studio से प्राप्त मुफ़्त API Key दर्ज करें। Key आपके स्थानीय सिस्टम में सुरक्षित रूप से संरक्षित रहेगी।
        </p>
        <input type="password" id="apiKeyInput" class="key-input" placeholder="AIzaSy..." />
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
          <a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:var(--saffron-400); font-size:0.82rem; text-decoration:none;">
            + मुफ़्त Key प्राप्त करें ↗
          </a>
          <button class="btn-primary-action" onclick="saveApiKey()">सुरक्षित करें (Save)</button>
        </div>
        <div id="keyFeedback" style="font-size:0.82rem; margin-top:6px;"></div>
      </div>
    </div>
  </div>

  <!-- Voice Cloning Modal -->
  <div class="modal-overlay" id="voiceModal" onclick="closeAllModals(event)">
    <div class="modal-card" onclick="event.stopPropagation()">
      <div class="modal-header">
        <h3 style="color:#fff;">🎙️ निजी आवाज़ क्लोनिंग (Voice Clone)</h3>
        <button class="btn-secondary" style="padding:4px 10px;" onclick="closeModal('voiceModal')">✕</button>
      </div>
      <div class="modal-body">
        <p style="font-size:0.85rem; color:var(--text-muted);">
          3 से 5 सेकंड तक अपनी आवाज़ में कोई भी वाक्य बोलकर रिकॉर्ड करें। सिस्टम आपके पिच को कैलिब्रेट करके AI उत्तर आपके निजी स्वर में सुनाएगा।
        </p>
        <div class="audio-visualizer" id="audioVisualizer">
          <div class="visualizer-bar" style="height:15px;"></div>
          <div class="visualizer-bar" style="height:35px;"></div>
          <div class="visualizer-bar" style="height:22px;"></div>
          <div class="visualizer-bar" style="height:45px;"></div>
          <div class="visualizer-bar" style="height:18px;"></div>
        </div>
        <div style="display:flex; gap:10px; justify-content:center; align-items:center;">
          <button class="btn-primary-action" id="recordVoiceBtn" onclick="toggleVoiceRecord()">🔴 रिकॉर्ड शुरू करें</button>
          <button class="btn-secondary" id="playSampleBtn" onclick="playVoiceSample()" style="display:none;">▶️ नमूना सुनें</button>
        </div>
        <div id="voiceStatusMsg" style="font-size:0.82rem; text-align:center; color:var(--text-muted); margin-top:6px;"></div>
      </div>
    </div>
  </div>

  <script>
    let activeDialect = 'hindi';
    let activeDialectName = 'मानक हिन्दी';
    let showPhonetics = false;
    let personaMode = 'standard';
    let chatHistory = [];
    let isOnline = false;
    let phrasesData = [];
    let storiesData = [];
    let emergencyData = [];
    let recognition = null;
    let isRecognizing = false;
    let mediaRecorder = null;
    let audioChunks = [];
    let isRecordingVoice = false;

    // Initialize on page load
    async function init() {
      await checkStatus();
      await loadPhrases();
      await loadStories();
      await loadEmergency();
      setupSpeechRecognition();
    }

    async function checkStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        isOnline = data.hasKey;
        const pill = document.getElementById('statusPill');
        const text = document.getElementById('statusText');
        if (isOnline) {
          pill.className = 'status-pill';
          text.textContent = 'ऑनलाइन (Gemini AI)';
        } else {
          pill.className = 'status-pill offline';
          text.textContent = 'ऑफ़लाइन मोड (ऑफलाइन शब्दकोश)';
        }
      } catch (e) {
        console.warn('Status fetch failed', e);
      }
    }

    function setDialect(id, name, desc, btnEl) {
      activeDialect = id;
      activeDialectName = name;
      document.querySelectorAll('.dialect-btn').forEach(btn => btn.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      document.getElementById('currentDialectTitle').innerHTML = `${name} <span>•</span> <small style="font-size:0.8rem; color:var(--saffron-400);">सक्रिय</small>`;
      document.getElementById('currentDialectSub').textContent = desc;

      if (window.innerWidth <= 768) {
        document.getElementById('sidebar').classList.remove('open');
      }
    }

    function toggleSidebar() {
      document.getElementById('sidebar').classList.toggle('open');
    }

    function changePersonaMode(val) {
      personaMode = val;
      const labels = {
        standard: 'मोड: सर्व-सहायक',
        elder: 'मोड: बुजुर्ग मित्र (आदरणीय व संक्षिप्त संवाद)',
        student: 'मोड: छात्र सहायक (द्विभाषी नोट्स व स्पष्टीकरण)',
        farmer: 'मोड: किसान व बागवान मित्र (सेब व कृषि सलाह)'
      };
      document.getElementById('activePersonaBadge').textContent = labels[val] || 'मोड: सर्व-सहायक';
    }

    function togglePronunciation() {
      showPhonetics = !showPhonetics;
      const btn = document.getElementById('phoneticsToggleBtn');
      if (btn) btn.classList.toggle('active-toggle', showPhonetics);
      document.querySelectorAll('.pronunciation').forEach(el => {
        el.style.display = showPhonetics ? 'block' : 'none';
      });
    }

    function switchView(viewName) {
      const chatContainer = document.getElementById('chatMessages');
      const chatInput = document.getElementById('chatInputBar');
      const transView = document.getElementById('translatorView');
      const tabChat = document.getElementById('tabChat');
      const tabTrans = document.getElementById('tabTrans');

      if (viewName === 'translator') {
        chatContainer.style.display = 'none';
        chatInput.style.display = 'none';
        transView.classList.add('active');
        tabTrans.classList.add('active');
        tabChat.classList.remove('active');
      } else {
        chatContainer.style.display = 'flex';
        chatInput.style.display = 'flex';
        transView.classList.remove('active');
        tabChat.classList.add('active');
        tabTrans.classList.remove('active');
      }
    }

    function autoResize(textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    function handleKey(e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    }

    function clearChat() {
      const container = document.getElementById('chatMessages');
      container.innerHTML = `
        <div class="message bot">
          <div class="bubble">
            संवाद साफ़ कर दिया गया है। आप नया प्रश्न पूछ सकते हैं!
          </div>
        </div>
      `;
      chatHistory = [];
    }

    function copyText(btn) {
      const bubble = btn.closest('.message').querySelector('.bubble');
      // Extract only clean text without pronunciation snippet
      let text = '';
      for (let node of bubble.childNodes) {
        if (node.nodeType === Node.TEXT_NODE) text += node.textContent;
      }
      text = text.trim() || bubble.innerText.trim();
      navigator.clipboard.writeText(text);
      const originalText = btn.innerHTML;
      btn.innerHTML = '✓ कॉपीड';
      setTimeout(() => btn.innerHTML = originalText, 1500);
    }

    async function speakText(btn) {
      const bubble = btn.closest('.message').querySelector('.bubble');
      let text = '';
      for (let node of bubble.childNodes) {
        if (node.nodeType === Node.TEXT_NODE) text += node.textContent;
      }
      text = text.trim() || bubble.innerText.trim();
      if (!text) return;

      btn.style.color = 'var(--saffron-400)';
      
      // Try Neural TTS from backend
      try {
        const res = await fetch('/api/voice/synthesize', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        if (data.success && data.audioUrl) {
          const audio = new Audio(data.audioUrl);
          audio.play();
          audio.onended = () => btn.style.color = '';
          return;
        }
      } catch (err) {
        console.warn('Backend TTS failed, using browser speech:', err);
      }

      // Browser Web Speech API Fallback
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'hi-IN';
        utterance.rate = 0.95;
        utterance.pitch = 1.0;
        utterance.onend = () => btn.style.color = '';
        window.speechSynthesis.speak(utterance);
      } else {
        btn.style.color = '';
      }
    }

    // Speech-to-text Web Speech API
    function setupSpeechRecognition() {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'hi-IN';

        recognition.onstart = () => {
          isRecognizing = true;
          document.getElementById('micBtn').classList.add('recording');
        };
        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          const input = document.getElementById('userInput');
          input.value = transcript;
          autoResize(input);
        };
        recognition.onerror = () => {
          isRecognizing = false;
          document.getElementById('micBtn').classList.remove('recording');
        };
        recognition.onend = () => {
          isRecognizing = false;
          document.getElementById('micBtn').classList.remove('recording');
        };
      }
    }

    function toggleSpeechRecognition() {
      if (!recognition) {
        alert('आपके ब्राउज़र में आवाज़ पहचान (Web Speech API) उपलब्ध नहीं है। कृपया Chrome या Edge का उपयोग करें।');
        return;
      }
      if (isRecognizing) {
        recognition.stop();
      } else {
        recognition.start();
      }
    }

    // Send chat message to backend
    async function sendMessage() {
      const input = document.getElementById('userInput');
      const text = input.value.trim();
      if (!text) return;

      const container = document.getElementById('chatMessages');

      // Append User message
      const userMsg = document.createElement('div');
      userMsg.className = 'message user';
      userMsg.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
      container.appendChild(userMsg);

      input.value = '';
      input.style.height = 'auto';
      container.scrollTop = container.scrollHeight;

      // Append typing indicator
      const typingMsg = document.createElement('div');
      typingMsg.className = 'message bot';
      typingMsg.id = 'typingIndicator';
      typingMsg.innerHTML = `
        <div class="bubble">
          <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
          </div>
        </div>
      `;
      container.appendChild(typingMsg);
      container.scrollTop = container.scrollHeight;

      chatHistory.push({ role: 'user', isUser: true, text });

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            message: text,
            dialect: activeDialect,
            mode: personaMode,
            history: chatHistory
          })
        });

        const data = await response.json();
        const replyText = data.reply || "उत्तर प्राप्त नहीं हो सका। कृपया पुनः प्रयास करें।";
        chatHistory.push({ role: 'assistant', isUser: false, text: replyText });

        // Remove typing indicator
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) typingEl.remove();

        // Bot message bubble
        const botMsg = document.createElement('div');
        botMsg.className = 'message bot';
        botMsg.innerHTML = `
          <div class="bubble">
            ${escapeHtml(replyText)}
            <div class="pronunciation" style="display:${showPhonetics ? 'block' : 'none'};">
              Phonetic guidance active
            </div>
          </div>
          <div class="message-meta">
            <span>AI सहायक (${activeDialectName})</span>
            <button class="action-icon-btn" onclick="speakText(this)">🔊 बोलें</button>
            <button class="action-icon-btn" onclick="copyText(this)">📋 कॉपी</button>
          </div>
        `;
        container.appendChild(botMsg);
        container.scrollTop = container.scrollHeight;

      } catch (err) {
        console.error('Chat error:', err);
        const typingEl = document.getElementById('typingIndicator');
        if (typingEl) typingEl.remove();

        const errorMsg = document.createElement('div');
        errorMsg.className = 'message bot';
        errorMsg.innerHTML = `
          <div class="bubble" style="border-color:#ef4444;">
            सर्वर से संपर्क करने में समस्या हुई। ऑफ़लाइन शब्दकोश उपलब्ध है।
          </div>
        `;
        container.appendChild(errorMsg);
        container.scrollTop = container.scrollHeight;
      }
    }

    // Direct Bidirectional Translation
    async function handleDirectTranslate() {
      const input = document.getElementById('transInput').value.trim();
      const isReverse = document.getElementById('reverseTranslateCheck').checked;
      const outBox = document.getElementById('transOutput');
      const phonBox = document.getElementById('transPhonetic');
      const ctxBox = document.getElementById('transContext');

      if (!input) {
        outBox.textContent = 'कृपया अनुवाद के लिए कुछ टेक्स्ट लिखें।';
        return;
      }

      outBox.textContent = 'अनुवाद हो रहा है...';
      phonBox.textContent = '';
      ctxBox.style.display = 'none';

      try {
        const res = await fetch('/api/translate', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            query: input,
            dialect: activeDialect,
            isReverse: isReverse
          })
        });
        const data = await res.json();
        outBox.textContent = data.translatedText || input;
        if (data.phoneticText) {
          phonBox.textContent = `उच्चारण (Phonetics): ${data.phoneticText}`;
        }
        if (data.culturalContext) {
          ctxBox.textContent = `💡 सांस्कृतिक संदर्भ: ${data.culturalContext}`;
          ctxBox.style.display = 'block';
        }
      } catch (err) {
        outBox.textContent = 'अनुवाद में त्रुटि हुई।';
      }
    }

    function toggleTranslateDirection() {
      const isReverse = document.getElementById('reverseTranslateCheck').checked;
      document.getElementById('transSourceLabel').textContent = isReverse ? `स्रोत पाठ (${activeDialectName}):` : 'स्रोत पाठ (हिंदी):';
      document.getElementById('transTargetLabel').textContent = isReverse ? 'अनुवाद परिणाम (हिंदी):' : `अनुवाद परिणाम (${activeDialectName}):`;
    }

    // Modal Handlers
    function openGlossaryModal() {
      renderGlossary(phrasesData);
      document.getElementById('glossaryModal').style.display = 'flex';
    }

    function openHeritageModal() {
      renderHeritage(storiesData);
      document.getElementById('heritageModal').style.display = 'flex';
    }

    function openEmergencyModal() {
      renderEmergency(emergencyData);
      document.getElementById('emergencyModal').style.display = 'flex';
    }

    function openKeyModal() {
      document.getElementById('keyModal').style.display = 'flex';
    }

    function openVoiceModal() {
      document.getElementById('voiceModal').style.display = 'flex';
    }

    function closeModal(id) {
      document.getElementById(id).style.display = 'none';
    }

    function closeAllModals(e) {
      if (e.target.classList.contains('modal-overlay')) {
        e.target.style.display = 'none';
      }
    }

    async function loadPhrases() {
      try {
        const res = await fetch('/api/phrases');
        phrasesData = await res.json();
      } catch (e) {
        console.warn('Phrases load failed', e);
      }
    }

    async function loadStories() {
      try {
        const res = await fetch('/api/stories');
        storiesData = await res.json();
      } catch (e) {
        console.warn('Stories load failed', e);
      }
    }

    async function loadEmergency() {
      try {
        const res = await fetch('/api/emergency');
        emergencyData = await res.json();
      } catch (e) {
        console.warn('Emergency load failed', e);
      }
    }

    function renderGlossary(list) {
      const body = document.getElementById('glossaryBody');
      if (!list || list.length === 0) {
        body.innerHTML = '<div style="text-align:center; color:var(--text-muted);">कोई वाक्यांश नहीं मिला।</div>';
        return;
      }
      body.innerHTML = list.map(item => `
        <div class="dict-entry">
          <div class="dict-word">
            <span>${escapeHtml(item.hindi)} ➔ ${escapeHtml(item.translation)}</span>
            <span style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(item.dialect || '')}</span>
          </div>
          <div class="dict-meaning">🗣️ <em>${escapeHtml(item.phonetic || '')}</em> | 🇬🇧 ${escapeHtml(item.english || '')}</div>
          ${item.culturalNote ? `<div class="dict-note">💡 ${escapeHtml(item.culturalNote)}</div>` : ''}
        </div>
      `).join('');
    }

    function filterGlossary() {
      const q = document.getElementById('glossarySearch').value.toLowerCase().trim();
      const filtered = phrasesData.filter(p => 
        (p.hindi && p.hindi.toLowerCase().includes(q)) ||
        (p.translation && p.translation.toLowerCase().includes(q)) ||
        (p.phonetic && p.phonetic.toLowerCase().includes(q)) ||
        (p.english && p.english.toLowerCase().includes(q))
      );
      renderGlossary(filtered);
    }

    function renderHeritage(stories) {
      const body = document.getElementById('heritageBody');
      if (!stories || stories.length === 0) {
        body.innerHTML = '<div style="text-align:center; color:var(--text-muted);">कहानियां लोड नहीं हो सकीं।</div>';
        return;
      }
      body.innerHTML = stories.map(s => `
        <div class="dict-entry">
          <div class="dict-word" style="color:var(--saffron-400); font-size:1rem;">
            ${escapeHtml(s.titleHindi)}
          </div>
          <div style="font-size:0.8rem; color:var(--saffron-500); margin:2px 0;">📍 ${escapeHtml(s.region || '')}</div>
          <p style="font-size:0.88rem; line-height:1.5; color:#e2e8f0; margin-top:6px;">${escapeHtml(s.fullStory || s.summary || '')}</p>
          ${s.culturalSignificance ? `<div class="dict-note" style="margin-top:6px;">🌟 <strong>सांस्कृतिक महत्व:</strong> ${escapeHtml(s.culturalSignificance)}</div>` : ''}
        </div>
      `).join('');
    }

    function renderEmergency(contacts) {
      const body = document.getElementById('emergencyBody');
      if (!contacts || contacts.length === 0) {
        body.innerHTML = '<div style="text-align:center; color:var(--text-muted);">हेल्पलाइन नंबर लोड नहीं हो सके।</div>';
        return;
      }
      body.innerHTML = contacts.map(c => `
        <div class="dict-entry" style="display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div class="dict-word" style="font-size:0.95rem;">${c.icon || '🚨'} ${escapeHtml(c.titleHindi)}</div>
            <div class="dict-note">${escapeHtml(c.description || '')}</div>
          </div>
          <a href="tel:${c.number}" style="background:var(--pine-700); color:#fff; text-decoration:none; padding:6px 14px; border-radius:100px; font-weight:bold; font-size:0.9rem;">
            📞 ${escapeHtml(c.number)}
          </a>
        </div>
      `).join('');
    }

    async function saveApiKey() {
      const key = document.getElementById('apiKeyInput').value.trim();
      const feedback = document.getElementById('keyFeedback');
      if (!key) {
        feedback.style.color = '#ef4444';
        feedback.textContent = 'कृपया एक मान्य Key दर्ज करें।';
        return;
      }

      feedback.style.color = '#e2e8f0';
      feedback.textContent = 'सत्यापित किया जा रहा है...';

      try {
        const res = await fetch('/api/set-key', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ key })
        });
        const data = await res.json();
        if (data.success) {
          feedback.style.color = '#4ade80';
          feedback.textContent = '✓ API Key सफलतापूर्वक सुरक्षित हो गई!';
          setTimeout(() => {
            closeModal('keyModal');
            checkStatus();
          }, 1000);
        } else {
          feedback.style.color = '#ef4444';
          feedback.textContent = data.error || 'अमान्य Key';
        }
      } catch (err) {
        feedback.style.color = '#ef4444';
        feedback.textContent = 'सर्वर से संपर्क करने में त्रुटि।';
      }
    }

    // Voice sample recording
    async function toggleVoiceRecord() {
      const btn = document.getElementById('recordVoiceBtn');
      const statusMsg = document.getElementById('voiceStatusMsg');

      if (isRecordingVoice) {
        // Stop recording
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
          mediaRecorder.stop();
        }
        isRecordingVoice = false;
        btn.textContent = '🔴 रिकॉर्ड शुरू करें';
        btn.style.background = '';
      } else {
        // Start recording
        try {
          const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
          mediaRecorder = new MediaRecorder(stream);
          audioChunks = [];

          mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) audioChunks.push(e.data);
          };

          mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            statusMsg.textContent = 'आवाज़ विश्लेषण एवं अपलोड हो रहा है...';
            
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = async () => {
              const base64Audio = reader.result;
              try {
                const res = await fetch('/api/voice/upload', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({ audioData: base64Audio, voiceName: 'kore', pitchHz: 220 })
                });
                const data = await res.json();
                if (data.success) {
                  statusMsg.style.color = '#4ade80';
                  statusMsg.textContent = '✓ आपकी आवाज़ कैलिब्रेट हो गई!';
                  document.getElementById('playSampleBtn').style.display = 'inline-flex';
                } else {
                  statusMsg.style.color = '#ef4444';
                  statusMsg.textContent = 'अपलोड विफल रहा।';
                }
              } catch (e) {
                statusMsg.style.color = '#ef4444';
                statusMsg.textContent = 'सर्वर त्रुटि।';
              }
            };
          };

          mediaRecorder.start();
          isRecordingVoice = true;
          btn.textContent = '⏹️ रिकॉर्डिंग रोकें';
          btn.style.background = '#ef4444';
          statusMsg.textContent = 'बोलिए... (3 से 5 सेकंड)';
        } catch (err) {
          alert('माइक्रोफ़ोन एक्सेस नहीं मिल सका: ' + err.message);
        }
      }
    }

    function playVoiceSample() {
      const audio = new Audio('/api/voice/sample?t=' + Date.now());
      audio.play();
    }

    function escapeHtml(str) {
      if (!str) return '';
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    window.onload = init;
  </script>
</body>
</html>
"""
