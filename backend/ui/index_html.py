# -*- coding: utf-8 -*-
"""
Himachal AI Assistant (हिमाचल संगम AI) - Modern Multi-Feature Web Interface
Crafted with Tailwind CSS, Lucide Icons, Glassmorphism, Deep Himalayan Pine & Saffron Design.
Features:
1. Multi-Tab Navigation (AI Chat, Live Translator, Himalayan Audio Folklore, Living Glossary, Emergency Hub)
2. High-Fidelity Edge-TTS Neural Audio with hi-IN-SwaraNeural & hi-IN-MadhurNeural + Waveform Equalizer
3. Real-time Dialect Chat across 10 Himalayan Dialects + Standard Hindi
4. Direct Live Translator with Cultural Etiquette Notes and Phonetic Guide
5. Interactive Audio Folklore Narration Player
6. Instant Offline / Online Auto-Detection and Gemini Fallbacks
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="hi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>हिमाचल संगम AI | Hindi-Pahadi AI Assistant</title>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#090d16">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">

  <!-- Google Fonts: Inter & Cinzel / Noto Sans Devanagari for regional typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Devanagari:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            pine: {
              50: '#f0fdf4',
              100: '#dcfce7',
              500: '#228b53',
              600: '#16a34a',
              700: '#15803d',
              800: '#166534',
              900: '#0b391f',
              950: '#052213',
            },
            saffron: {
              300: '#fcd34d',
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
            },
            mist: {
              800: '#1e293b',
              900: '#0f172a',
              950: '#090d16',
            }
          },
          fontFamily: {
            sans: ['Inter', 'Noto Sans Devanagari', 'sans-serif'],
            serif: ['Cinzel', 'Noto Sans Devanagari', 'serif'],
          },
          boxShadow: {
            'glow-saffron': '0 0 25px -3px rgba(245, 158, 11, 0.3)',
            'glow-pine': '0 0 30px -4px rgba(21, 128, 61, 0.35)',
          }
        }
      }
    }
  </script>

  <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(15, 23, 42, 0.4);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(100, 116, 139, 0.3);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(245, 158, 11, 0.5);
    }

    .glass-panel {
      background: rgba(15, 23, 42, 0.82);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .glass-card {
      background: rgba(30, 41, 59, 0.55);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.07);
    }

    .glass-card-hover {
      transition: all 0.25s ease;
    }
    .glass-card-hover:hover {
      background: rgba(30, 41, 59, 0.75);
      border-color: rgba(245, 158, 11, 0.35);
      transform: translateY(-2px);
    }

    /* Himalayan Mountain Pattern Accent */
    .himalaya-pattern {
      background-image: 
        radial-gradient(circle at 1px 1px, rgba(255,255,255,0.035) 1px, transparent 0),
        radial-gradient(circle at 10% 20%, rgba(19, 78, 44, 0.38) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(229, 142, 38, 0.18) 0%, transparent 45%);
      background-size: 24px 24px, 100% 100%, 100% 100%;
    }

    /* Equalizer Wave Animation */
    .eq-bar {
      display: inline-block;
      width: 3px;
      height: 12px;
      margin: 0 1px;
      background-color: #fbbf24;
      border-radius: 2px;
      animation: eq-bounce 1s infinite ease-in-out alternate;
    }
    .eq-bar:nth-child(2) { animation-delay: 0.2s; height: 16px; }
    .eq-bar:nth-child(3) { animation-delay: 0.4s; height: 10px; }
    .eq-bar:nth-child(4) { animation-delay: 0.6s; height: 14px; }

    @keyframes eq-bounce {
      0% { transform: scaleY(0.3); }
      100% { transform: scaleY(1.3); }
    }

    /* Tab transitions */
    .tab-view {
      display: none;
    }
    .tab-view.active {
      display: flex;
    }
  </style>
</head>
<body class="bg-mist-950 text-slate-100 font-sans min-h-screen flex flex-col himalaya-pattern selection:bg-saffron-500/30 selection:text-saffron-400">

  <!-- Main Top Header -->
  <header class="sticky top-0 z-40 w-full glass-panel border-b border-white/10 px-4 lg:px-8 py-2.5 transition-colors duration-200">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-3">
      
      <!-- Brand & Status -->
      <div class="flex items-center gap-3">
        <button id="sidebarToggleBtn" class="lg:hidden p-2 rounded-xl hover:bg-slate-800/60 text-slate-300">
          <i data-lucide="menu" class="w-5 h-5"></i>
        </button>
        <div class="relative flex items-center justify-center w-10 h-10 rounded-2xl bg-gradient-to-br from-pine-700 to-pine-900 border border-pine-600/60 shadow-glow-pine shrink-0">
          <i data-lucide="mountain-snow" class="w-5 h-5 text-saffron-400"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
              <span>हिमाचल</span>
              <span class="text-saffron-400 font-serif">संगम AI</span>
            </h1>
            <span id="headerStatusPill" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span id="headerStatusDot" class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              <span id="headerStatusText">ऑनलाइन • 8080</span>
            </span>
          </div>
          <p class="text-xs text-slate-400 hidden sm:block">10 पहाड़ी बोलियों व मानक हिन्दी का संवादात्मक सेतु</p>
        </div>
      </div>

      <!-- Navigation Tabs (Desktop Center) -->
      <nav class="hidden md:flex items-center gap-1 bg-slate-900/70 p-1 rounded-2xl border border-white/10">
        <button class="nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition bg-saffron-500 text-mist-950 shadow-md" data-tab="chat">
          <i data-lucide="message-square" class="w-3.5 h-3.5"></i>
          <span>संवादी AI</span>
        </button>
        <button class="nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 flex items-center gap-1.5 transition" data-tab="translate">
          <i data-lucide="languages" class="w-3.5 h-3.5"></i>
          <span>लाइव अनुवादक</span>
        </button>
        <button class="nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 flex items-center gap-1.5 transition" data-tab="stories">
          <i data-lucide="scroll" class="w-3.5 h-3.5"></i>
          <span>ऑडियो लोक कथाएं</span>
        </button>
        <button class="nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 flex items-center gap-1.5 transition" data-tab="glossary">
          <i data-lucide="book-open-text" class="w-3.5 h-3.5"></i>
          <span>पहाड़ी शब्दकोश</span>
        </button>
        <button class="nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-rose-300 hover:text-rose-200 hover:bg-rose-950/40 flex items-center gap-1.5 transition" data-tab="emergency">
          <i data-lucide="phone-call" class="w-3.5 h-3.5 text-rose-400"></i>
          <span>आपदा केंद्र</span>
        </button>
      </nav>

      <!-- Top Right Controls: Voice Switcher & Settings -->
      <div class="flex items-center gap-2">
        <!-- Voice Model Quick Selector -->
        <div class="relative hidden sm:block">
          <select id="globalVoiceSelect" class="bg-slate-900/80 hover:bg-slate-800/90 text-slate-200 text-xs font-medium py-1.5 pl-2.5 pr-7 rounded-xl border border-white/10 shadow-sm focus:outline-none focus:ring-1 focus:ring-saffron-500/50 appearance-none cursor-pointer">
            <option value="hi-IN-SwaraNeural" selected>👩 स्वरा (Neural)</option>
            <option value="hi-IN-MadhurNeural">👨 मधुर (Neural)</option>
          </select>
          <i data-lucide="volume-2" class="w-3.5 h-3.5 text-saffron-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"></i>
        </div>

        <!-- Settings Modal Trigger -->
        <button id="openSettingsBtn" title="सिस्टम सेटिंग्स (Settings)" class="p-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-white/10 text-slate-300 hover:text-white transition">
          <i data-lucide="sliders-horizontal" class="w-4 h-4"></i>
        </button>
      </div>

    </div>

    <!-- Mobile Navigation Sub-Bar -->
    <div class="md:hidden flex items-center justify-around gap-1 pt-2 mt-2 border-t border-white/5 overflow-x-auto">
      <button class="nav-tab-btn px-2.5 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1 transition bg-saffron-500 text-mist-950" data-tab="chat">
        <i data-lucide="message-square" class="w-3.5 h-3.5"></i>
        <span>संवाद</span>
      </button>
      <button class="nav-tab-btn px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:bg-slate-800/60 flex items-center gap-1 transition" data-tab="translate">
        <i data-lucide="languages" class="w-3.5 h-3.5"></i>
        <span>अनुवाद</span>
      </button>
      <button class="nav-tab-btn px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:bg-slate-800/60 flex items-center gap-1 transition" data-tab="stories">
        <i data-lucide="scroll" class="w-3.5 h-3.5"></i>
        <span>कथाएं</span>
      </button>
      <button class="nav-tab-btn px-2.5 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:bg-slate-800/60 flex items-center gap-1 transition" data-tab="glossary">
        <i data-lucide="book-marked" class="w-3.5 h-3.5"></i>
        <span>शब्दकोश</span>
      </button>
      <button class="nav-tab-btn px-2.5 py-1.5 rounded-lg text-xs font-medium text-rose-400 hover:bg-rose-950/40 flex items-center gap-1 transition" data-tab="emergency">
        <i data-lucide="phone-call" class="w-3.5 h-3.5"></i>
        <span>हेल्पलाइन</span>
      </button>
    </div>
  </header>

  <!-- Main Container -->
  <div class="flex-1 max-w-7xl w-full mx-auto flex overflow-hidden relative">

    <!-- ========================================== -->
    <!-- TAB 1: संवादी AI (Interactive Chat Assistant) -->
    <!-- ========================================== -->
    <div id="tab-chat" class="tab-view active flex-1 flex w-full h-[calc(100vh-105px)] md:h-[calc(100vh-65px)] min-w-0 overflow-hidden">
      
      <!-- Sidebar: Conversation Controls & Dialect Settings -->
      <aside id="chatSidebar" class="fixed lg:static inset-y-0 left-0 z-30 w-72 bg-mist-900/95 lg:bg-transparent backdrop-blur-xl lg:backdrop-blur-none border-r border-white/10 flex flex-col transform -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out">
        <div class="p-4 border-b border-white/10 flex items-center justify-between">
          <button id="newChatBtn" class="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-pine-700 to-pine-800 hover:from-pine-600 hover:to-pine-700 text-white font-medium text-sm shadow-md transition group">
            <i data-lucide="plus-circle" class="w-4 h-4 group-hover:rotate-90 transition-transform"></i>
            <span>नया संवाद (New Chat)</span>
          </button>
          <button id="closeSidebarBtn" class="lg:hidden ml-2 p-2 text-slate-400 hover:text-white">
            <i data-lucide="x" class="w-5 h-5"></i>
          </button>
        </div>

        <div class="p-4 flex-1 overflow-y-auto space-y-4">
          <!-- Dialect Selector -->
          <div>
            <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">पहाड़ी बोली चुनें (Dialect)</span>
            <div class="relative mb-2">
              <select id="dialectSelect" class="w-full bg-slate-900/90 text-slate-200 text-xs sm:text-sm font-medium py-2 pl-3 pr-8 rounded-xl border border-white/10 shadow-sm focus:outline-none focus:ring-1 focus:ring-saffron-500 appearance-none cursor-pointer">
                <option value="hindi" selected>मानक हिन्दी (Hindi)</option>
                <option value="kangri">कांगड़ी (Kangri - कांगड़ा/हमीरपुर)</option>
                <option value="mandeali">मण्डयाली (Mandeali - मंडी)</option>
                <option value="kullui">कुलवी (Kullui - कुल्लू/मनाली)</option>
                <option value="shimla_pahari">महासूवी / शिमला (Mahasuvi - शिमला)</option>
                <option value="chambeali">चम्बियाली (Chambeali - चंबा)</option>
                <option value="sirmauri">सिरमौरी (Sirmauri - नाहन/गिरिपार)</option>
                <option value="garhwali">गढ़वाली (Garhwali - उत्तराखंड)</option>
                <option value="kumaoni">कुमाऊँनी (Kumaoni - अल्मोड़ा/नैनीताल)</option>
                <option value="dogri">डोगरी (Dogri - जम्मू/शिवालिक)</option>
                <option value="jaunsari">जौनसारी (Jaunsari - चकराता)</option>
              </select>
              <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"></i>
            </div>
            
            <div id="dialectBadgeCard" class="p-3 rounded-2xl glass-card border border-saffron-500/20 bg-saffron-500/5">
              <div class="flex items-center gap-2 mb-1">
                <span class="w-2 h-2 rounded-full bg-saffron-400"></span>
                <h4 id="activeDialectTitle" class="text-xs font-bold text-saffron-300">मानक हिन्दी</h4>
              </div>
              <p id="activeDialectDesc" class="text-[11px] text-slate-300 leading-relaxed">
                पारंपरिक व आधुनिक शिष्टाचार युक्त शुद्ध हिन्दी वार्तालाप।
              </p>
            </div>
          </div>

          <!-- Persona Mode Selection -->
          <div>
            <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">संवाद विधा (Persona Mode)</span>
            <select id="personaModeSelect" class="w-full bg-slate-900/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-saffron-500">
              <option value="standard">🏔️ सर्व-सहायक (All-Round Himalayan)</option>
              <option value="elder">👵 बुजुर्ग मित्र (Elder Friendly / आदरयुक्त)</option>
              <option value="student">📚 छात्र व भाषा शोधार्थी (Student Helper)</option>
              <option value="farmer">🍎 बागवान व किसान मित्र (Apple Orchard Expert)</option>
            </select>
          </div>

          <!-- Quick Prompts in Sidebar -->
          <div>
            <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">त्वरित विषय (Quick Prompts)</span>
            <div class="space-y-1.5 text-xs">
              <button class="w-full text-left px-3 py-2 rounded-xl bg-slate-800/40 text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2 transition" onclick="triggerQuickPrompt('मण्डयाली में अभिवादन और हाल-चाल कैसे पूछते हैं?')">
                <i data-lucide="sparkles" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
                <span class="truncate">मण्डयाली में अभिवादन के नियम</span>
              </button>
              <button class="w-full text-left px-3 py-2 rounded-xl bg-slate-800/40 text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2 transition" onclick="triggerQuickPrompt('कांगड़ा किला और बृजेश्वरी शक्तिपीठ का इतिहास बताएं।')">
                <i data-lucide="scroll" class="w-3.5 h-3.5 text-slate-400 shrink-0"></i>
                <span class="truncate">कांगड़ा किला व शक्तिपीठ</span>
              </button>
              <button class="w-full text-left px-3 py-2 rounded-xl bg-slate-800/40 text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2 transition" onclick="triggerQuickPrompt('शिमला व किन्नौर में सेब के बगीचों में प्रूनिंग और खाद प्रबंधन कैसे करें?')">
                <i data-lucide="apple" class="w-3.5 h-3.5 text-emerald-400 shrink-0"></i>
                <span class="truncate">शिमला सेब बागवानी व प्रूनिंग</span>
              </button>
              <button class="w-full text-left px-3 py-2 rounded-xl bg-slate-800/40 text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2 transition" onclick="triggerQuickPrompt('पारंपरिक हिमाचली सिड्डू और धाम की क्या विशेषता है?')">
                <i data-lucide="utensils" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
                <span class="truncate">सिड्डू व हिमाचली धाम</span>
              </button>
            </div>
          </div>

          <!-- Engine Status Info Card -->
          <div class="pt-2">
            <div class="p-3 rounded-2xl bg-slate-900/60 border border-white/5 space-y-1.5">
              <div class="flex items-center justify-between text-xs text-slate-300">
                <span class="flex items-center gap-1.5">
                  <i data-lucide="cpu" class="w-3.5 h-3.5 text-pine-500"></i> AI Engine
                </span>
                <span class="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-emerald-400 font-mono">Edge-TTS + Gemini</span>
              </div>
              <div class="text-[11px] text-slate-400">
                Voice: <span class="text-saffron-300 font-semibold">hi-IN-SwaraNeural</span>
              </div>
            </div>
          </div>
        </div>

        <div class="p-4 border-t border-white/10 flex items-center justify-between">
          <button id="clearChatBtn" class="flex items-center gap-1.5 text-xs text-rose-400 hover:text-rose-300 transition">
            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            <span>संवाद साफ करें</span>
          </button>
          <span class="text-[11px] text-slate-500">v2.5 • देवनागरी</span>
        </div>
      </aside>

      <!-- Main Chat Workspace -->
      <main class="flex-1 flex flex-col h-full min-w-0">
        
        <!-- Chat Messages Scroll Area -->
        <div id="chatContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-5">
          
          <!-- Welcome Hero (Initially visible) -->
          <div id="welcomeHero" class="my-4 max-w-2xl mx-auto text-center space-y-4">
            <div class="inline-flex p-3 rounded-3xl bg-gradient-to-b from-saffron-500/20 to-transparent border border-saffron-500/30 text-saffron-400 mb-1 shadow-glow-saffron">
              <i data-lucide="sparkles" class="w-7 h-7"></i>
            </div>
            <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">
              नमस्ते जी! क्या मदद कर सकता हूँ?
            </h2>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed max-w-lg mx-auto">
              यह AI सहायक हिमाचल प्रदेश व उत्तराखंड की 10 बोलियों—कांगड़ी, मण्डयाली, महासूवी, कुलवी, चम्बियाली, गढ़वाली, कुमाऊँनी—व मानक हिन्दी में संवादात्मक मार्गदर्शन प्रदान करता है।
            </p>

            <!-- Suggested Quick Prompts Grid -->
            <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-left">
              <button class="quick-prompt-btn p-3 rounded-2xl glass-card glass-card-hover flex items-start gap-3" data-prompt="कांगड़ी बोली में रोजमर्रा के हाल-चाल कैसे पूछते हैं? उदाहरण देकर समझाओ।">
                <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 shrink-0">
                  <i data-lucide="message-circle" class="w-4 h-4"></i>
                </span>
                <div>
                  <div class="text-xs font-semibold text-slate-200">कांगड़ी में हाल-चाल पूछना</div>
                  <div class="text-[11px] text-slate-400 line-clamp-1">दैनिक संवाद और अभिवादन के वाक्य</div>
                </div>
              </button>

              <button class="quick-prompt-btn p-3 rounded-2xl glass-card glass-card-hover flex items-start gap-3" data-prompt="मण्डयाली में एक छोटी लोक कथा या कहावत सुनाएं और उसका हिन्दी अर्थ भी बताएं।">
                <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 shrink-0">
                  <i data-lucide="scroll" class="w-4 h-4"></i>
                </span>
                <div>
                  <div class="text-xs font-semibold text-slate-200">पहाड़ी लोक कथा / कहावत</div>
                  <div class="text-[11px] text-slate-400 line-clamp-1">मण्डयाली कथा व हिन्दी अनुवाद</div>
                </div>
              </button>

              <button class="quick-prompt-btn p-3 rounded-2xl glass-card glass-card-hover flex items-start gap-3" data-prompt="हिमाचल के ऊपरी क्षेत्रों (शिमला/किन्नौर) में सेब की मुख्य किस्में कौन सी हैं और उनकी देखभाल कैसे करें?">
                <span class="p-2 rounded-xl bg-pine-900/60 text-emerald-400 shrink-0">
                  <i data-lucide="apple" class="w-4 h-4"></i>
                </span>
                <div>
                  <div class="text-xs font-semibold text-slate-200">हिमाचली सेब और बागवानी</div>
                  <div class="text-[11px] text-slate-400 line-clamp-1">प्रमुख किस्में, प्रूनिंग व सुरक्षा निर्देश</div>
                </div>
              </button>

              <button class="quick-prompt-btn p-3 rounded-2xl glass-card glass-card-hover flex items-start gap-3" data-prompt="महासूवी (शिमला पहाड़ी) बोली के 5 आम शब्द और उनके मानक हिन्दी अर्थ बताएं।">
                <span class="p-2 rounded-xl bg-pine-900/60 text-saffron-400 shrink-0">
                  <i data-lucide="languages" class="w-4 h-4"></i>
                </span>
                <div>
                  <div class="text-xs font-semibold text-slate-200">महासूवी शब्दकोश</div>
                  <div class="text-[11px] text-slate-400 line-clamp-1">शिमला क्षेत्र के प्रचलित स्थानीय शब्द</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Chat History Stream -->
          <div id="messagesList" class="max-w-3xl mx-auto space-y-4">
            <!-- Dynamically populated messages -->
          </div>

          <!-- Typing Indicator -->
          <div id="typingIndicator" class="max-w-3xl mx-auto hidden">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-xl bg-pine-800/80 border border-pine-700/50 flex items-center justify-center text-saffron-400 shrink-0">
                <i data-lucide="sparkles" class="w-4 h-4 animate-spin"></i>
              </div>
              <div class="p-4 rounded-2xl glass-card border border-white/10 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce"></span>
                <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce [animation-delay:0.2s]"></span>
                <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce [animation-delay:0.4s]"></span>
                <span class="text-xs text-slate-300 ml-2">पहाड़ी में उत्तर तैयार हो रहा है...</span>
              </div>
            </div>
          </div>

        </div>

        <!-- Bottom Chat Input Bar -->
        <div class="p-3 sm:p-4 bg-gradient-to-t from-mist-950 via-mist-950/95 to-transparent border-t border-white/5">
          <div class="max-w-3xl mx-auto">
            
            <div class="flex items-center justify-between text-xs px-2 mb-1.5 text-slate-400">
              <div class="flex items-center gap-2">
                <span id="translitBadge" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-800/80 border border-white/5 text-[11px] text-slate-200">
                  <i data-lucide="languages" class="w-3 h-3 text-saffron-400"></i>
                  <span id="targetDialectNameDisplay">मानक हिन्दी</span>
                </span>
                <button id="togglePhoneticsBtn" class="text-[11px] text-slate-400 hover:text-saffron-400 flex items-center gap-1 transition">
                  <i data-lucide="spell-check" class="w-3 h-3"></i>
                  <span>उच्चारण सहायक (Phonetics)</span>
                </button>
              </div>
              <span class="text-[10px] text-slate-500 hidden sm:inline">Enter भेजें • Shift+Enter नई पंक्ति</span>
            </div>

            <!-- Text Input Container -->
            <div class="relative glass-card rounded-2xl border border-white/10 focus-within:border-saffron-500/50 focus-within:ring-2 focus-within:ring-saffron-500/20 shadow-xl transition-all duration-200">
              <textarea
                id="messageInput"
                rows="1"
                placeholder="यहाँ हिन्दी या पहाड़ी में लिखें... (उदा: तुसां केड़े हाल चाला न? / सेब में प्रूनिंग कब करें?)"
                class="w-full bg-transparent text-slate-100 placeholder-slate-500 text-xs sm:text-sm py-3.5 pl-4 pr-24 resize-none max-h-36 focus:outline-none"
              ></textarea>

              <div class="absolute right-2 bottom-2 flex items-center gap-1">
                <!-- Speech Recognition Mic -->
                <button
                  id="micBtn"
                  title="आवाज से बोलें (Voice Input)"
                  class="p-2 rounded-xl text-slate-400 hover:text-saffron-400 hover:bg-white/5 transition"
                >
                  <i data-lucide="mic" class="w-4 h-4"></i>
                </button>

                <!-- Send Button -->
                <button
                  id="sendBtn"
                  title="संदेश भेजें"
                  class="p-2 rounded-xl bg-gradient-to-r from-pine-700 to-pine-800 hover:from-saffron-500 hover:to-saffron-600 text-white hover:text-mist-950 transition shadow-md"
                >
                  <i data-lucide="arrow-up" class="w-4 h-4"></i>
                </button>
              </div>
            </div>

            <p class="text-center text-[10px] text-slate-500 mt-1.5">
              पहाड़ी संगम AI • स्थानीय बोलियों की मिठास, प्रामाणिक जानकारी व न्यूरल आवाज़ (Edge-TTS)
            </p>
          </div>
        </div>

      </main>
    </div>

    <!-- ========================================== -->
    <!-- TAB 2: लाइव अनुवादक (Live Direct Translator) -->
    <!-- ========================================== -->
    <div id="tab-translate" class="tab-view flex-1 flex flex-col w-full h-[calc(100vh-105px)] md:h-[calc(100vh-65px)] p-4 sm:p-6 overflow-y-auto">
      <div class="max-w-4xl mx-auto w-full space-y-6">
        
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/10 pb-4">
          <div>
            <h2 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
              <i data-lucide="languages" class="w-5 h-5 text-saffron-400"></i>
              <span>लाइव पहाड़ी अनुवादक (Live Dialect Translator)</span>
            </h2>
            <p class="text-xs text-slate-400">मानक हिन्दी, अंग्रेजी व 10 पहाड़ी बोलियों के बीच सटीक व सांस्कृतिक अनुवाद</p>
          </div>
          
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">अनुवाद दिशा:</span>
            <button id="swapTranslateDirectionBtn" class="px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 hover:border-saffron-500 text-xs text-slate-200 flex items-center gap-1.5 transition">
              <span id="transDirectionLabel">हिन्दी ➔ पहाड़ी</span>
              <i data-lucide="arrow-right-left" class="w-3.5 h-3.5 text-saffron-400"></i>
            </button>
          </div>
        </div>

        <!-- Translation Workspace Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          <!-- Source Input Box -->
          <div class="glass-card rounded-3xl p-5 border border-white/10 flex flex-col space-y-3">
            <div class="flex items-center justify-between">
              <span id="sourceLangTitle" class="text-xs font-bold uppercase tracking-wider text-saffron-400">स्रोत भाषा (मानक हिन्दी)</span>
              <button id="clearTransInputBtn" class="text-xs text-slate-400 hover:text-rose-400">साफ करें</button>
            </div>
            <textarea
              id="translateSourceText"
              rows="5"
              placeholder="यहाँ वाक्य लिखें... (उदा: आप कहाँ जा रहे हैं? / क्या आपने खाना खा लिया? / कल मौसम कैसा रहेगा?)"
              class="w-full bg-slate-950/60 border border-white/10 rounded-2xl p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-saffron-500 resize-none flex-1"
            ></textarea>
            
            <div class="flex items-center justify-between pt-2">
              <div class="flex items-center gap-2">
                <button id="transMicBtn" class="p-2 rounded-xl bg-slate-900 border border-white/10 text-slate-300 hover:text-saffron-400 transition" title="बोलकर दर्ज करें">
                  <i data-lucide="mic" class="w-4 h-4"></i>
                </button>
              </div>
              <button id="runTranslateBtn" class="px-5 py-2 rounded-xl bg-gradient-to-r from-pine-700 to-pine-800 hover:from-saffron-500 hover:to-saffron-600 text-white hover:text-mist-950 font-bold text-xs flex items-center gap-2 transition shadow-md">
                <span>अनुवाद करें</span>
                <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>

          <!-- Target Output Box -->
          <div class="glass-card rounded-3xl p-5 border border-white/10 flex flex-col space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">लक्षित बोली:</span>
                <select id="transTargetDialect" class="bg-slate-950 border border-white/10 rounded-lg px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-saffron-500">
                  <option value="kangri" selected>कांगड़ी (Kangri)</option>
                  <option value="mandeali">मण्डयाली (Mandeali)</option>
                  <option value="kullui">कुलवी (Kullui)</option>
                  <option value="shimla_pahari">महासूवी / शिमला (Mahasuvi)</option>
                  <option value="chambeali">चम्बियाली (Chambeali)</option>
                  <option value="sirmauri">सिरमौरी (Sirmauri)</option>
                  <option value="garhwali">गढ़वाली (Garhwali)</option>
                  <option value="kumaoni">कुमाऊँनी (Kumaoni)</option>
                  <option value="dogri">डोगरी (Dogri)</option>
                  <option value="jaunsari">जौनसारी (Jaunsari)</option>
                </select>
              </div>
              <div class="flex items-center gap-1">
                <button id="copyTransResultBtn" class="p-1.5 rounded-lg text-slate-400 hover:text-white" title="कॉपी करें">
                  <i data-lucide="copy" class="w-3.5 h-3.5"></i>
                </button>
                <button id="speakTransResultBtn" class="p-1.5 rounded-lg text-slate-400 hover:text-saffron-400" title="उच्चारण सुनें">
                  <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
                </button>
              </div>
            </div>

            <div id="translateResultBox" class="w-full bg-slate-950/60 border border-white/10 rounded-2xl p-4 text-sm text-slate-100 flex-1 min-h-[120px] flex flex-col justify-between">
              <div id="translatedOutputText" class="text-base font-semibold text-saffron-300 whitespace-pre-line">
                अनुवाद यहाँ प्रदर्शित होगा...
              </div>
              
              <div id="transPhoneticBlock" class="mt-3 pt-2 border-t border-white/10 text-xs font-mono text-slate-400 italic flex items-center gap-1.5 hidden">
                <i data-lucide="volume-2" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
                <span id="transPhoneticText"></span>
              </div>
            </div>

            <!-- Cultural Etiquette Note -->
            <div id="transCulturalBlock" class="p-3 rounded-2xl bg-pine-950/60 border border-pine-800/40 text-xs text-slate-300 hidden">
              <div class="font-semibold text-saffron-300 flex items-center gap-1 mb-0.5">
                <i data-lucide="info" class="w-3.5 h-3.5"></i>
                <span>सांस्कृतिक संदर्भ व शिष्टाचार:</span>
              </div>
              <p id="transCulturalText" class="text-[11px] leading-relaxed"></p>
            </div>
          </div>

        </div>

        <!-- Quick Phrase Starters -->
        <div class="space-y-2">
          <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">लोकप्रिय दैनिक वाक्यांश (Quick Starters):</span>
          <div class="flex flex-wrap gap-2">
            <button class="quick-trans-chip px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-300 hover:border-saffron-500 hover:text-white transition" data-text="आप कैसे हैं? सब ठीक है?">
              आप कैसे हैं? सब ठीक है?
            </button>
            <button class="quick-trans-chip px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-300 hover:border-saffron-500 hover:text-white transition" data-text="आप कहाँ जा रहे हैं?">
              आप कहाँ जा रहे हैं?
            </button>
            <button class="quick-trans-chip px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-300 hover:border-saffron-500 hover:text-white transition" data-text="कल मौसम कैसा रहेगा? क्या धूप खिलेगी?">
              कल मौसम कैसा रहेगा?
            </button>
            <button class="quick-trans-chip px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-300 hover:border-saffron-500 hover:text-white transition" data-text="क्या आपने खाना खा लिया?">
              क्या आपने खाना खा लिया?
            </button>
            <button class="quick-trans-chip px-3 py-1.5 rounded-xl bg-slate-900 border border-white/10 text-xs text-slate-300 hover:border-saffron-500 hover:text-white transition" data-text="सादर प्रणाम! आपका बहुत-बहुत धन्यवाद।">
              सादर प्रणाम! धन्यवाद।
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 3: ऑडियो लोक कथाएं (Himalayan Folklore Stories) -->
    <!-- ========================================== -->
    <div id="tab-stories" class="tab-view flex-1 flex flex-col w-full h-[calc(100vh-105px)] md:h-[calc(100vh-65px)] p-4 sm:p-6 overflow-y-auto">
      <div class="max-w-5xl mx-auto w-full space-y-6">
        
        <!-- Header -->
        <div class="border-b border-white/10 pb-4">
          <div class="flex items-center gap-2 mb-1">
            <span class="p-2 rounded-xl bg-saffron-500/20 text-saffron-400">
              <i data-lucide="scroll" class="w-5 h-5"></i>
            </span>
            <h2 class="text-lg sm:text-xl font-bold text-white">पहाड़ी लोक धरोहर व ऑडियो कथाएं (Folklore & Lore)</h2>
          </div>
          <p class="text-xs text-slate-400">देवभूमि हिमाचल व उत्तराखंड के पवित्र धामों, लोक देवताओं और पारंपरिक जीवन की सजीव कथाएं — न्यूरल आवाज़ में सुनें</p>
        </div>

        <!-- Stories Grid -->
        <div id="storiesContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Populated by JavaScript -->
        </div>

      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 4: पहाड़ी शब्दकोश (Living Glossary) -->
    <!-- ========================================== -->
    <div id="tab-glossary" class="tab-view flex-1 flex flex-col w-full h-[calc(100vh-105px)] md:h-[calc(100vh-65px)] p-4 sm:p-6 overflow-y-auto">
      <div class="max-w-5xl mx-auto w-full space-y-5">
        
        <div class="border-b border-white/10 pb-4">
          <h2 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2">
            <i data-lucide="book-open-text" class="w-5 h-5 text-saffron-400"></i>
            <span>पहाड़ी - हिन्दी जीवंत शब्दकोश (Living Glossary)</span>
          </h2>
          <p class="text-xs text-slate-400">कांगड़ी, मण्डयाली, कुलवी, महासूवी, चम्बियाली, गढ़वाली, कुमाऊँनी के प्रामाणिक शब्द व उच्चारण</p>
        </div>

        <!-- Search & Filter Controls -->
        <div class="flex flex-col sm:flex-row gap-3">
          <div class="relative flex-1">
            <input
              id="glossaryTabSearchInput"
              type="text"
              placeholder="शब्द या हिन्दी अर्थ खोजें (उदा: तुसां, मिंजो, किजो, पैलाग, सिड्डू)..."
              class="w-full bg-slate-900 border border-white/10 rounded-2xl px-4 py-2.5 pl-10 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-saffron-500"
            >
            <i data-lucide="search" class="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
          </div>

          <div class="relative min-w-[180px]">
            <select id="glossaryDialectFilter" class="w-full bg-slate-900 border border-white/10 rounded-2xl px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-saffron-500 appearance-none cursor-pointer">
              <option value="all" selected>सभी बोलियां (All Dialects)</option>
              <option value="kangri">कांगड़ी</option>
              <option value="mandeali">मण्डयाली</option>
              <option value="kullui">कुल्लवी</option>
              <option value="shimla_pahari">महासूवी / शिमला</option>
              <option value="chambeali">चम्बियाली</option>
              <option value="garhwali">गढ़वाली</option>
              <option value="kumaoni">कुमाऊँनी</option>
              <option value="dogri">डोगरी</option>
            </select>
            <i data-lucide="filter" class="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"></i>
          </div>
        </div>

        <!-- Word List Grid -->
        <div id="glossaryCardsContainer" class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs sm:text-sm">
          <!-- Populated by JavaScript -->
        </div>

      </div>
    </div>

    <!-- ========================================== -->
    <!-- TAB 5: आपदा व आपातकालीन केंद्र (Emergency Hub) -->
    <!-- ========================================== -->
    <div id="tab-emergency" class="tab-view flex-1 flex flex-col w-full h-[calc(100vh-105px)] md:h-[calc(100vh-65px)] p-4 sm:p-6 overflow-y-auto">
      <div class="max-w-4xl mx-auto w-full space-y-6">
        
        <div class="border-b border-white/10 pb-4">
          <div class="flex items-center gap-2 mb-1">
            <span class="p-2 rounded-xl bg-rose-500/20 text-rose-400">
              <i data-lucide="shield-alert" class="w-5 h-5"></i>
            </span>
            <h2 class="text-lg sm:text-xl font-bold text-white">🚨 आपातकालीन व आपदा प्रबंधन केंद्र (Emergency Hub)</h2>
          </div>
          <p class="text-xs text-slate-400">हिमाचल प्रदेश व उत्तराखंड के 24x7 टोल-फ्री हेल्पलाइन नंबर व पर्वतीय सुरक्षा निर्देश</p>
        </div>

        <!-- Helpline Grid -->
        <div id="emergencyGridContainer" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <!-- Populated by JavaScript -->
        </div>

        <!-- Mountain Pass & Weather Safety Guidelines -->
        <div class="glass-card rounded-3xl p-5 border border-white/10 space-y-4">
          <h3 class="text-sm font-bold text-saffron-300 flex items-center gap-2">
            <i data-lucide="mountain" class="w-4 h-4"></i>
            <span>पर्वतीय यात्रा व मौसम सुरक्षा निर्देश (Travel Advisories)</span>
          </h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300">
            <div class="p-3 rounded-2xl bg-slate-900/60 border border-white/5 space-y-1">
              <div class="font-bold text-amber-400 flex items-center gap-1.5">
                <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i>
                <span>भूस्खलन (Landslides)</span>
              </div>
              <p class="text-[11px] leading-relaxed text-slate-400">
                भारी वर्षा के समय कालका-शिमला NH-5 और चंडीगढ़-मनाली NH-21 पर सतर्क रहें। आपात स्थिति में 1077 डायल करें।
              </p>
            </div>
            
            <div class="p-3 rounded-2xl bg-slate-900/60 border border-white/5 space-y-1">
              <div class="font-bold text-sky-400 flex items-center gap-1.5">
                <i data-lucide="snowflake" class="w-3.5 h-3.5"></i>
                <span>अटल टनल व रोहतांग</span>
              </div>
              <p class="text-[11px] leading-relaxed text-slate-400">
                सर्दियों में बर्फबारी के दौरान 4x4 वाहन या स्नो-चेन अनिवार्य हैं। टनल कंट्रोल रूम 01902-250100।
              </p>
            </div>

            <div class="p-3 rounded-2xl bg-slate-900/60 border border-white/5 space-y-1">
              <div class="font-bold text-emerald-400 flex items-center gap-1.5">
                <i data-lucide="bus" class="w-3.5 h-3.5"></i>
                <span>एचआरटीसी बस अपडेट</span>
              </div>
              <p class="text-[11px] leading-relaxed text-slate-400">
                दुर्गम रूटों पर बस स्थिति व अग्रिम बुकिंग हेतु HRTC कंट्रोल रूम 0177-2803017 पर 24 घंटे जानकारी उपलब्ध है।
              </p>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>

  <!-- Floating Sticky Audio Player Bar (Visible during playback) -->
  <div id="stickyAudioPlayer" class="fixed bottom-4 left-1/2 -translate-x-1/2 z-50 w-[92%] max-w-xl bg-slate-900/95 backdrop-blur-2xl border border-saffron-500/40 rounded-2xl p-3 shadow-2xl flex items-center justify-between gap-3 transform translate-y-32 opacity-0 transition-all duration-300">
    <div class="flex items-center gap-3 min-w-0">
      <div class="w-9 h-9 rounded-xl bg-pine-900 border border-pine-700 text-saffron-400 flex items-center justify-center shrink-0">
        <i data-lucide="volume-2" class="w-5 h-5 animate-pulse"></i>
      </div>
      <div class="min-w-0">
        <div class="flex items-center gap-2">
          <span id="playerTrackTitle" class="text-xs font-bold text-white truncate max-w-[180px] sm:max-w-xs">ऑडियो चल रहा है...</span>
          <span class="inline-flex items-center gap-0.5">
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
            <span class="eq-bar"></span>
          </span>
        </div>
        <div class="text-[10px] text-slate-400 flex items-center gap-2 mt-0.5">
          <span id="playerVoiceBadge">👩 hi-IN-SwaraNeural</span>
          <span>•</span>
          <span id="playerTimeDisplay" class="font-mono">बज रहा है...</span>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-1.5 shrink-0">
      <button id="playerStopBtn" class="p-2 rounded-xl bg-slate-800 hover:bg-rose-900 text-slate-300 hover:text-white transition" title="रोकें (Stop)">
        <i data-lucide="square" class="w-3.5 h-3.5"></i>
      </button>
    </div>
  </div>

  <!-- Settings & API Key Modal -->
  <div id="settingsModal" class="fixed inset-0 z-50 bg-black/65 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-mist-900 border border-white/10 rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-5">
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <i data-lucide="settings" class="w-4 h-4 text-saffron-400"></i>
          <span>सिस्टम व न्यूरल वॉइस सेटिंग्स</span>
        </h3>
        <button id="closeSettingsBtn" class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-4 text-xs sm:text-sm">
        <!-- API Key Input -->
        <div>
          <label class="block text-slate-300 font-medium mb-1">Google Gemini API Key</label>
          <input
            id="apiKeyInput"
            type="password"
            placeholder="AIzaSy..."
            class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-saffron-500 font-mono text-xs"
          >
          <p class="text-[11px] text-slate-400 mt-1">
            Google AI Studio की मुफ़्त Key दर्ज करें। Key आपके लोकल .env में सुरक्षित रहेगी।
          </p>
        </div>

        <div>
          <label class="block text-slate-300 font-medium mb-1">पसंदीदा न्यूरल आवाज़ (Default Voice)</label>
          <select id="modalVoiceSelect" class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-xs">
            <option value="hi-IN-SwaraNeural" selected>👩 hi-IN-SwaraNeural (सौम्य स्त्री स्वर)</option>
            <option value="hi-IN-MadhurNeural">👨 hi-IN-MadhurNeural (शांत पुरुष स्वर)</option>
          </select>
        </div>

        <div>
          <label class="block text-slate-300 font-medium mb-1">आवाज की गति (Speech Rate)</label>
          <select id="voiceSpeedSelect" class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-xs">
            <option value="-10%">धीमी व शांत (-10%)</option>
            <option value="-6%" selected>प्राकृतिक पहाड़ी मिठास (-6%)</option>
            <option value="+0%">सामान्य (0%)</option>
            <option value="+10%">तेज़ (+10%)</option>
          </select>
        </div>

        <div class="pt-2 flex items-center justify-between border-t border-white/5">
          <span class="text-slate-300">रोमनाइज़्ड फ़ोनेटिक्स सदैव दिखाएं</span>
          <input type="checkbox" id="alwaysPhoneticsCheckbox" checked class="w-4 h-4 rounded accent-saffron-500 cursor-pointer">
        </div>
      </div>

      <div class="pt-2">
        <button id="saveSettingsBtn" class="w-full py-2.5 rounded-xl bg-saffron-500 hover:bg-saffron-600 text-mist-950 font-bold transition">
          सेव करें (Save Preferences)
        </button>
      </div>
    </div>
  </div>

  <!-- Toast Notification element -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 bg-slate-900 border border-white/10 shadow-2xl rounded-2xl px-4 py-3 flex items-center gap-3 text-xs text-slate-100 pointer-events-none">
    <i data-lucide="check-circle" class="w-4 h-4 text-emerald-400"></i>
    <span id="toastMsg">क्लिपबोर्ड पर कॉपी किया गया!</span>
  </div>

  <!-- Audio element for TTS -->
  <audio id="globalAudioPlayer" class="hidden"></audio>

  <script>
    // Dialect Knowledge Base & Metadata
    const DIALECT_META = {
      hindi: {
        name: 'मानक हिन्दी',
        desc: 'पारंपरिक व आधुनिक शिष्टाचार युक्त शुद्ध हिन्दी वार्तालाप।',
        greeting: 'नमस्ते! मैं आपकी किस प्रकार सहायता कर सकता हूँ?'
      },
      kangri: {
        name: 'कांगड़ी (Kangri)',
        desc: 'कांगड़ा, हमीरपुर व ऊना क्षेत्र में बोली जाने वाली प्रमुख पश्चिमी पहाड़ी उपबोली। "मिंजो", "तिंजो", "कुथी" आदि।',
        greeting: 'नमस्कार! कुथू चले न तुसां? दसो क्या मदद करां?'
      },
      mandeali: {
        name: 'मण्डयाली (Mandeali)',
        desc: 'मण्डी, द्रंग, जोगिन्दरनगर व बल्ह क्षेत्र की मधुर पहाड़ी बोली। "किजो", "काहा", "तुसां" जैसे शब्द प्रयोग।',
        greeting: 'नमस्ते जी! तुसां केड़े हाल चाला न? आज क्या गल्ल करणी?'
      },
      kullui: {
        name: 'कुलवी (Kullui)',
        desc: 'देवभूमि कुल्लू घाटी व ब्यास तटवर्ती क्षेत्रों की बोली। "जय देव", "हौ", "तुसी", "कबे"।',
        greeting: 'जय देव जी! सब राजी-खुशी? कुल्लू रा कोई समाचार पूछणा?'
      },
      shimla_pahari: {
        name: 'महासूवी / शिमला (Mahasuvi)',
        desc: 'शिमला, ठियोग, कोटखाई, रोहड़ू, सोलन क्षेत्र की पहाड़ी। "आपु", "के हाल च", "स्युब"।',
        greeting: 'नमस्कार जी! आपु किद्दां आ? सब राजी-खुशी आ?'
      },
      chambeali: {
        name: 'चम्बियाली (Chambeali)',
        desc: 'रावी घाटी चंबा व मणिमहेश अंचल की मधुर बोली। "तुहाड़े के हाल न"।',
        greeting: 'नमस्ते जी! तुहाड़े के हाल न? चम्बे री कोई गल्ल पूछणी?'
      },
      sirmauri: {
        name: 'सिरमौरी (Sirmauri)',
        desc: 'नाहन, रेणुका जी, गिरि-पार (हाटी क्षेत्र) की प्राचीन बोली।',
        greeting: 'पैलाग / नमस्कार जी! के हाल-चाल बा?'
      },
      garhwali: {
        name: 'गढ़वाली (Garhwali)',
        desc: 'अलकनंदा व भागीरथी घाटी (श्रीनगर, पौड़ी, टिहरी, चमोली) की पावन बोली।',
        greeting: 'पैलाग जी! कन छौ तुम? सब भल च?'
      },
      kumaoni: {
        name: 'कुमाऊँनी (Kumaoni)',
        desc: 'कत्यूर व मानसखंड (अल्मोड़ा, नैनीताल, पिथौरागढ़) की मिठास। "दगड़्या", "भल छौ"।',
        greeting: 'पैलाग दगड़्या! कसि छा? सब भल छौ?'
      },
      dogri: {
        name: 'डोगरी (Dogri)',
        desc: 'जम्मू व शिवालिक क्षेत्र की संविधान सम्मत मधुर डोगरी।',
        greeting: 'नमस्ते जी! तुंदा के हाल ऐ? सब ठीक-ठाक?'
      },
      jaunsari: {
        name: 'जौनसारी (Jaunsari)',
        desc: 'जौनसार-बावर, चकराता पहाड़ियों की लोक संस्कृति से युक्त बोली।',
        greeting: 'महासू देवता री कृपा! नमस्कार जी, क्या हाल-चाल?'
      }
    };

    // Default Fallback Vocabulary
    let GLOSSARY_ITEMS = [
      { word: 'तुसां / तुसी', dialect: 'कांगड़ी / मण्डयाली', hindi: 'आप (You)', phonetic: 'Tusan / Tusi', category: 'Greetings' },
      { word: 'मिंजो / महां', dialect: 'कांगड़ी / मण्डयाली', hindi: 'मुझे / मुझको (To me)', phonetic: 'Minjo / Mahaan', category: 'Greetings' },
      { word: 'तिंजो', dialect: 'कांगड़ी', hindi: 'तुझे / उसको (To you/him)', phonetic: 'Tinjo', category: 'Relations' },
      { word: 'किजो', dialect: 'मण्डयाली', hindi: 'क्यों (Why)', phonetic: 'Kijo', category: 'Daily' },
      { word: 'कुथी / कुथू', dialect: 'कांगड़ी / मण्डयाली', hindi: 'कहाँ (Where)', phonetic: 'Kuthi / Kuthu', category: 'Daily' },
      { word: 'केड़े हाल चाला / किद्दां', dialect: 'मण्डयाली / शिमला', hindi: 'क्या हाल-चाल हैं (How are you)', phonetic: 'Kede haal chaala / Kiddan', category: 'Greetings' },
      { word: 'बाशठ / बाठ', dialect: 'महासूवी', hindi: 'बातचीत / किस्सा (Conversation)', phonetic: 'Basht / Baath', category: 'Daily' },
      { word: 'सिड्डू (Siddu)', dialect: 'कुल्लू / शिमला', hindi: 'पारंपरिक खमीरयुक्त स्टीम्ड व्यंजन', phonetic: 'Siddu (Himachali dish)', category: 'Food' },
      { word: 'पैलाग', dialect: 'गढ़वाली / कुमाऊँनी', hindi: 'चरण स्पर्श / आदरणीय प्रणाम', phonetic: 'Pailaag', category: 'Greetings' },
      { word: 'दगड़्या', dialect: 'कुमाऊँनी', hindi: 'सच्चा मित्र / सहयात्री (Dear Friend)', phonetic: 'Dagadya', category: 'Relations' },
      { word: 'घाम', dialect: 'समस्त पहाड़ी', hindi: 'खिली हुई धूप (Sunshine)', phonetic: 'Ghaam', category: 'Weather' },
      { word: 'झड़ी', dialect: 'समस्त पहाड़ी', hindi: 'लगातार होने वाली वर्षा (Rainfall)', phonetic: 'Jhadi', category: 'Weather' }
    ];

    let EMERGENCY_CONTACTS = [
      { title: 'राष्ट्रीय आपातकालीन सेवा (National Emergency)', number: '112', desc: 'पुलिस, अग्निशमन व एम्बुलेंस (All-in-one)' },
      { title: 'हिमाचल आपदा प्रबंधन (HP Disaster Helpline)', number: '1077', desc: 'भूस्खलन, बाढ़ व प्राकृतिक आपदा सहायता' },
      { title: 'एम्बुलेंस स्वास्थ्य सेवा (Medical Ambulance)', number: '108', desc: '24x7 मुफ्त आपातकालीन चिकित्सा' },
      { title: 'महिला हेल्पलाइन (Women Emergency)', number: '1091', desc: '24 घंटे महिला सुरक्षा' },
      { title: 'एचआरटीसी बस पूछताछ (HRTC Control Room)', number: '01772803017', desc: 'समय-सारिणी व सड़क स्थिति' },
      { title: 'राज्य आपातकालीन संचालन कक्ष (State Emergency Ops)', number: '1070', desc: 'राज्य स्तरीय आपदा नियंत्रण' }
    ];

    let CULTURAL_STORIES_LIST = [
      {
        id: 'story_golu',
        titleHindi: 'चितई गोलू देवता - न्याय के देवता',
        region: 'कुमाऊं (अल्मोड़ा, चम्पावत)',
        summary: 'कुमाऊं में जब किसी को न्याय नहीं मिलता, तो वह चितई गोलू मंदिर में स्टांप पेपर पर अर्ज़ी लिखकर घंटी बांधता है।',
        fullStory: 'गोलू देवता कुमाऊं के सबसे पूज्य लोक देवता हैं। वे कत्यूरी राजवंश के राजकुमार गौर भैरव थे। लोककथा के अनुसार उन्होंने बाल्यकाल से ही प्रजा को त्वरित व निष्पक्ष न्याय दिलाया।\\n\\nआज भी अल्मोड़ा के प्रसिद्ध चितई मंदिर में हज़ारों घंटियां और भक्तों की अर्ज़ियां बंधी हैं। मनोकामना पूर्ण होने पर श्रद्धालु पीतल की घंटी चढ़ाते हैं।',
        culturalSignificance: 'न्याय, निष्पक्षता और जन-विश्वास का सर्वोच्च प्रतीक।'
      },
      {
        id: 'story_siddu_kullu',
        titleHindi: 'सिड्डू और कुल्लू दशहरा की देव-संस्कृति',
        region: 'कुल्लू-मनाली घाटी, हिमाचल',
        summary: 'ढालपुर मैदान में 300 से अधिक देवी-देवताओं का मिलन और हिमाचली पारंपरिक सिड्डू का उत्सव।',
        fullStory: 'कुल्लू का दशहरा पूरे भारत में अनूठा है। यह विजयादशमी को शुरू होकर पूरे एक सप्ताह चलता है। घाटी के 300 से अधिक देवी-देवता अपने पालकियों में सवार होकर भगवान रघुनाथ जी को नमन करने आते हैं।\\n\\nसर्दियों में पहाड़ी घरों में पारंपरिक सिड्डू बनाया जाता है, जिसमें खमीर उठे आटे में अखरोट, खसखस और मसालों की भरावन देकर भाप में पकाया जाता है और भरपूर देसी घी के साथ खाया जाता है।',
        culturalSignificance: 'हिमाचली देव-परंपरा, समरसता, और शीतकालीन पोषण का संगम।'
      },
      {
        id: 'story_mahasu',
        titleHindi: 'महासू देवता - हनोल व शिमला के अधिपति',
        region: 'हनोल (जौनसार) व शिमला, सिरमौर',
        summary: 'चार महासू भाइयों (बाशिक, पबासी, बूठिया और चालदा) का हनोल में अलौकिक न्याय व लोक-शासन।',
        fullStory: 'टोंस नदी के तट पर स्थित हनोल मंदिर महासू देवता का मुख्य धाम है। किरमिर राक्षस के आतंक से रक्षा हेतु चार महासू भाई प्रकट हुए और दानव का संहार किया। महासू देवता को इस क्षेत्र का सच्चा राजा और न्यायाधीश माना जाता है।',
        culturalSignificance: 'जौनसारी और हिमाचली जनजातीय संस्कृति की एकता और पारम्परिक न्याय का आधार।'
      },
      {
        id: 'story_nanda',
        titleHindi: 'नंदा देवी राजजात - हिमालय का महाकुंभ',
        region: 'गढ़वाल व कुमाऊं (नौटी से होमकुंड)',
        summary: 'हर 12 वर्ष में आयोजित 280 किमी की पैदल यात्रा, जिसमें चार सींगों वाला मेढ़ा (खाडू) स्वतः मार्गदर्शक बनता है।',
        fullStory: 'नंदा देवी को पहाड़ की ध्याणी (बेटी) माना जाता है। यह यात्रा बेटी नंदा को उसके ससुराल (कैलाश) विदा करने की भावुक और पावन यात्रा है। नौटी से 17,500 फीट ऊंचे होमकुंड तक चार सींगों वाला खाडू सबसे आगे चलता है।',
        culturalSignificance: 'गढ़वाल और कुमाऊं को जोड़ने वाली सांस्कृतिक डोर।'
      },
      {
        id: 'story_phooldei',
        titleHindi: 'फूलदेई - बसंत का बाल लोकपर्व',
        region: 'उत्तराखंड व हिमाचल के समस्त पहाड़',
        summary: 'छोटे बच्चे सुबह-सुबह पीले फ्यूंली और बुरांश के फूल चुनकर हर घर की देहरी पर सजाते हैं।',
        fullStory: 'चैत्र मास की संक्रांति पर बच्चे "फूल देई, छम्मा देई, दैणी द्वार, भर भकार" गाते हुए हर घर की देहरी पर फूल सजाते हैं और सबके लिए मंगल व समृद्धि की कामना करते हैं।',
        culturalSignificance: 'प्रकृति के प्रति सम्मान और लोकसंस्कृति के संस्कार।'
      }
    ];

    // State Variables
    let currentDialect = 'hindi';
    let isPhoneticsActive = true;
    let personaMode = 'standard';
    let chatHistory = [];
    let isOnline = false;
    let selectedVoice = 'hi-IN-SwaraNeural';
    let selectedRate = '-6%';
    let isTranslateReverse = false;

    // DOM Elements
    const chatContainer = document.getElementById('chatContainer');
    const messagesList = document.getElementById('messagesList');
    const welcomeHero = document.getElementById('welcomeHero');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const typingIndicator = document.getElementById('typingIndicator');
    const dialectSelect = document.getElementById('dialectSelect');
    const activeDialectTitle = document.getElementById('activeDialectTitle');
    const activeDialectDesc = document.getElementById('activeDialectDesc');
    const targetDialectNameDisplay = document.getElementById('targetDialectNameDisplay');
    const togglePhoneticsBtn = document.getElementById('togglePhoneticsBtn');
    const personaModeSelect = document.getElementById('personaModeSelect');
    const micBtn = document.getElementById('micBtn');
    const clearChatBtn = document.getElementById('clearChatBtn');
    const newChatBtn = document.getElementById('newChatBtn');
    const globalVoiceSelect = document.getElementById('globalVoiceSelect');

    // Sidebar
    const chatSidebar = document.getElementById('chatSidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');

    // Modals & Settings
    const settingsModal = document.getElementById('settingsModal');
    const openSettingsBtn = document.getElementById('openSettingsBtn');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const apiKeyInput = document.getElementById('apiKeyInput');
    const modalVoiceSelect = document.getElementById('modalVoiceSelect');
    const voiceSpeedSelect = document.getElementById('voiceSpeedSelect');

    // Sticky Player
    const stickyAudioPlayer = document.getElementById('stickyAudioPlayer');
    const playerTrackTitle = document.getElementById('playerTrackTitle');
    const playerVoiceBadge = document.getElementById('playerVoiceBadge');
    const playerStopBtn = document.getElementById('playerStopBtn');
    const globalAudioPlayer = document.getElementById('globalAudioPlayer');

    // Translator Tab Elements
    const translateSourceText = document.getElementById('translateSourceText');
    const runTranslateBtn = document.getElementById('runTranslateBtn');
    const transTargetDialect = document.getElementById('transTargetDialect');
    const translatedOutputText = document.getElementById('translatedOutputText');
    const transPhoneticBlock = document.getElementById('transPhoneticBlock');
    const transPhoneticText = document.getElementById('transPhoneticText');
    const transCulturalBlock = document.getElementById('transCulturalBlock');
    const transCulturalText = document.getElementById('transCulturalText');
    const swapTranslateDirectionBtn = document.getElementById('swapTranslateDirectionBtn');
    const transDirectionLabel = document.getElementById('transDirectionLabel');
    const sourceLangTitle = document.getElementById('sourceLangTitle');
    const clearTransInputBtn = document.getElementById('clearTransInputBtn');
    const copyTransResultBtn = document.getElementById('copyTransResultBtn');
    const speakTransResultBtn = document.getElementById('speakTransResultBtn');
    const transMicBtn = document.getElementById('transMicBtn');

    // Toast
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');

    function showToast(message) {
      toastMsg.textContent = message;
      toast.classList.remove('translate-y-20', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-20', 'opacity-0');
      }, 2500);
    }

    // Tab Navigation Logic
    document.querySelectorAll('.nav-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        switchTab(targetTab);
      });
    });

    function switchTab(tabName) {
      document.querySelectorAll('.tab-view').forEach(tab => {
        tab.classList.remove('active');
      });
      const activeTab = document.getElementById(`tab-${tabName}`);
      if (activeTab) {
        activeTab.classList.add('active');
      }

      document.querySelectorAll('.nav-tab-btn').forEach(btn => {
        const t = btn.getAttribute('data-tab');
        if (t === tabName) {
          btn.className = 'nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition bg-saffron-500 text-mist-950 shadow-md';
        } else {
          btn.className = 'nav-tab-btn px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/60 flex items-center gap-1.5 transition';
        }
      });

      if (tabName === 'stories') renderStories();
      if (tabName === 'glossary') renderGlossaryCards();
      if (tabName === 'emergency') renderEmergencyHub();
      lucide.createIcons();
    }

    async function checkBackendStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        isOnline = data.hasKey;
        const text = document.getElementById('headerStatusText');
        const dot = document.getElementById('headerStatusDot');
        if (isOnline) {
          text.textContent = 'ऑनलाइन • Gemini AI';
          dot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping';
        } else {
          text.textContent = 'ऑफ़लाइन शब्दकोश • 8080';
          dot.className = 'w-1.5 h-1.5 rounded-full bg-amber-400';
        }
      } catch (err) {
        console.warn('Status check failed:', err);
      }
    }

    async function loadPhrasesFromBackend() {
      try {
        const res = await fetch('/api/phrases');
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          GLOSSARY_ITEMS = data.map(p => ({
            word: p.translation,
            dialect: p.dialect || 'कांगड़ी',
            hindi: p.hindi,
            phonetic: p.phonetic || '',
            category: p.category || 'General'
          }));
        }
      } catch (err) {
        console.warn('Phrases load failed, using default glossary:', err);
      }
    }

    async function loadStoriesFromBackend() {
      try {
        const res = await fetch('/api/stories');
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          CULTURAL_STORIES_LIST = data;
        }
      } catch (err) {
        console.warn('Stories load failed:', err);
      }
    }

    async function loadEmergencyFromBackend() {
      try {
        const res = await fetch('/api/emergency');
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          EMERGENCY_CONTACTS = data.map(e => ({
            title: e.titleHindi || e.titleEnglish,
            number: e.number,
            desc: e.description
          }));
        }
      } catch (err) {
        console.warn('Emergency load failed, using defaults:', err);
      }
    }

    function updateDialectDisplay(dialectKey) {
      currentDialect = dialectKey;
      const info = DIALECT_META[dialectKey] || DIALECT_META.hindi;
      activeDialectTitle.textContent = info.name;
      activeDialectDesc.textContent = info.desc;
      targetDialectNameDisplay.textContent = info.name;
      dialectSelect.value = dialectKey;
      if (transTargetDialect) transTargetDialect.value = dialectKey;
    }

    // Markdown Parser Helper (formats **bold**, bullet points, linebreaks)
    function formatMarkdown(text) {
      if (!text) return '';
      let formatted = escapeHtml(text);
      // Bold
      formatted = formatted.replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-saffron-300 font-bold">$1</strong>');
      // Bullet points
      formatted = formatted.replace(/^[-•*]\\s+(.*)$/gm, '<li class="ml-4 list-disc text-slate-200">$1</li>');
      return formatted;
    }

    function appendMessage(role, text, phonetic = null, dialect = currentDialect) {
      if (welcomeHero) welcomeHero.style.display = 'none';

      const msgObj = { 
        id: Date.now(), 
        role, 
        text, 
        phonetic, 
        dialect, 
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      };
      chatHistory.push(msgObj);

      const msgEl = document.createElement('div');
      msgEl.className = `flex items-start gap-3 ${role === 'user' ? 'justify-end' : 'justify-start'}`;

      if (role === 'assistant') {
        msgEl.innerHTML = `
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-pine-700 to-pine-900 border border-pine-600/50 flex items-center justify-center text-saffron-400 shrink-0 shadow-sm mt-0.5">
            <i data-lucide="mountain-snow" class="w-4 h-4"></i>
          </div>
          <div class="max-w-[88%] sm:max-w-[80%] space-y-1.5">
            <div class="flex items-center gap-2 text-[11px] text-slate-400 px-1">
              <span class="font-semibold text-saffron-400">${DIALECT_META[dialect]?.name || 'सहायक'}</span>
              <span>•</span>
              <span>${msgObj.timestamp}</span>
            </div>
            <div class="p-4 rounded-3xl rounded-tl-sm glass-card border border-white/10 text-slate-100 text-sm leading-relaxed shadow-lg">
              <div class="whitespace-pre-line leading-relaxed">${formatMarkdown(text)}</div>
              ${phonetic && isPhoneticsActive ? `
                <div class="mt-2.5 pt-2 border-t border-white/10 text-xs font-mono text-slate-400 italic flex items-center gap-1.5">
                  <i data-lucide="volume-2" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
                  <span>${escapeHtml(phonetic)}</span>
                </div>
              ` : ''}
            </div>
            <!-- Message Action Toolbar -->
            <div class="flex items-center gap-1 text-slate-400 text-xs px-1">
              <button class="tts-play-btn p-1.5 rounded-lg hover:bg-slate-800 hover:text-saffron-400 flex items-center gap-1 transition" title="उच्चारण सुनें (Listen Voice)">
                <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
                <span class="text-[11px]">सुनें</span>
              </button>
              <button class="copy-msg-btn p-1.5 rounded-lg hover:bg-slate-800 hover:text-white transition" title="संदेश कॉपी करें">
                <i data-lucide="copy" class="w-3.5 h-3.5"></i>
              </button>
              <button class="feedback-up p-1.5 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition" title="उत्कृष्ट उत्तर">
                <i data-lucide="thumbs-up" class="w-3.5 h-3.5"></i>
              </button>
            </div>
          </div>
        `;

        const copyBtn = msgEl.querySelector('.copy-msg-btn');
        copyBtn.addEventListener('click', () => {
          navigator.clipboard.writeText(text);
          showToast('संदेश क्लिपबोर्ड पर कॉपी हो गया!');
        });

        const ttsBtn = msgEl.querySelector('.tts-play-btn');
        ttsBtn.addEventListener('click', () => {
          speakText(text, DIALECT_META[dialect]?.name || 'पहाड़ी संवाद', ttsBtn);
        });

        const fbUp = msgEl.querySelector('.feedback-up');
        fbUp.addEventListener('click', () => {
          fbUp.classList.toggle('text-emerald-400');
          showToast('धन्यवाद! आपकी प्रतिक्रिया दर्ज कर ली गई है।');
        });

      } else {
        msgEl.innerHTML = `
          <div class="max-w-[88%] sm:max-w-[80%] space-y-1">
            <div class="flex items-center justify-end gap-2 text-[11px] text-slate-400 px-1">
              <span>आप</span>
              <span>•</span>
              <span>${msgObj.timestamp}</span>
            </div>
            <div class="p-4 rounded-3xl rounded-tr-sm bg-gradient-to-r from-pine-800 to-pine-900 border border-pine-700/60 text-white text-sm leading-relaxed shadow-lg">
              <div class="whitespace-pre-line">${escapeHtml(text)}</div>
            </div>
          </div>
          <div class="w-8 h-8 rounded-xl bg-slate-800 border border-white/10 flex items-center justify-center text-slate-300 shrink-0 mt-0.5">
            <i data-lucide="user" class="w-4 h-4"></i>
          </div>
        `;
      }

      messagesList.appendChild(msgEl);
      lucide.createIcons();
      chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
    }

    // High-Fidelity Neural Voice TTS: edge-tts (hi-IN-SwaraNeural / hi-IN-MadhurNeural) + Sticky Player
    async function speakText(text, title = "पहाड़ी आवाज़", triggerBtn = null) {
      if (!text) return;

      const cleanSpokenText = text.replace(/[*_~`#]/g, '').replace(/https?:\\/\\/\\S+/g, '');
      const voice = selectedVoice || 'hi-IN-SwaraNeural';
      const rate = selectedRate || '-6%';

      // Show Sticky Player
      playerTrackTitle.textContent = title;
      playerVoiceBadge.textContent = voice.includes('Swara') ? '👩 स्वरा (Neural)' : '👨 मधुर (Neural)';
      stickyAudioPlayer.classList.remove('translate-y-32', 'opacity-0');
      stickyAudioPlayer.classList.add('translate-y-0', 'opacity-100');

      if (triggerBtn) {
        triggerBtn.innerHTML = '<span class="inline-flex items-center gap-1 text-saffron-400 text-[11px] animate-pulse"><i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> लोड हो रहा है...</span>';
        lucide.createIcons();
      }

      try {
        const res = await fetch('/api/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: cleanSpokenText,
            voice: voice,
            rate: rate,
            pitch: '+0Hz'
          })
        });

        if (res.ok) {
          const data = await res.json();
          const audioUrl = data.audio_url || data.audioUrl;
          if (audioUrl) {
            globalAudioPlayer.src = audioUrl;
            globalAudioPlayer.play();

            if (triggerBtn) {
              triggerBtn.innerHTML = '<span class="inline-flex items-center gap-1 text-emerald-400 text-[11px]"><i data-lucide="volume-2" class="w-3.5 h-3.5"></i> बज रहा है...</span>';
              lucide.createIcons();
            }

            globalAudioPlayer.onended = () => {
              hideStickyPlayer();
              if (triggerBtn) {
                triggerBtn.innerHTML = '<i data-lucide="volume-2" class="w-3.5 h-3.5"></i><span class="text-[11px]">सुनें</span>';
                lucide.createIcons();
              }
            };
            globalAudioPlayer.onerror = () => {
              hideStickyPlayer();
              if (triggerBtn) {
                triggerBtn.innerHTML = '<i data-lucide="volume-2" class="w-3.5 h-3.5"></i><span class="text-[11px]">सुनें</span>';
                lucide.createIcons();
              }
            };
            return;
          }
        }
      } catch (err) {
        console.warn('FastAPI edge-tts error, falling back to Web Speech:', err);
      }

      // Browser Web Speech Fallback
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanSpokenText);
        utterance.lang = 'hi-IN';
        utterance.rate = 0.95;
        utterance.onend = () => {
          hideStickyPlayer();
          if (triggerBtn) {
            triggerBtn.innerHTML = '<i data-lucide="volume-2" class="w-3.5 h-3.5"></i><span class="text-[11px]">सुनें</span>';
            lucide.createIcons();
          }
        };
        window.speechSynthesis.speak(utterance);
      } else {
        hideStickyPlayer();
        if (triggerBtn) {
          triggerBtn.innerHTML = '<i data-lucide="volume-2" class="w-3.5 h-3.5"></i><span class="text-[11px]">सुनें</span>';
          lucide.createIcons();
        }
        showToast('ध्वनि उत्पन्न करने में समस्या हुई।');
      }
    }

    function hideStickyPlayer() {
      stickyAudioPlayer.classList.remove('translate-y-0', 'opacity-100');
      stickyAudioPlayer.classList.add('translate-y-32', 'opacity-0');
      if (globalAudioPlayer) {
        globalAudioPlayer.pause();
        globalAudioPlayer.currentTime = 0;
      }
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
      }
    }

    playerStopBtn.addEventListener('click', hideStickyPlayer);

    // Call Real Gemini Backend Chat API
    async function sendPromptToBackend(prompt) {
      typingIndicator.classList.remove('hidden');
      chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: prompt,
            dialect: currentDialect,
            mode: personaMode,
            history: chatHistory.map(m => ({ role: m.role, isUser: m.role === 'user', text: m.text }))
          })
        });

        const data = await res.json();
        typingIndicator.classList.add('hidden');
        const replyText = data.reply || "उत्तर प्राप्त नहीं हो सका।";
        appendMessage('assistant', replyText, null, currentDialect);
      } catch (err) {
        console.error('Chat error:', err);
        typingIndicator.classList.add('hidden');
        appendMessage('assistant', 'सर्वर से संपर्क करने में समस्या हुई। ऑफ़लाइन शब्दकोश व अनुवादक का उपयोग करें।', null, currentDialect);
      }
    }

    function handleSend() {
      const text = messageInput.value.trim();
      if (!text) return;

      appendMessage('user', text);
      messageInput.value = '';
      messageInput.style.height = 'auto';

      sendPromptToBackend(text);
    }

    function triggerQuickPrompt(prompt) {
      if (window.innerWidth < 1024) {
        chatSidebar.classList.add('-translate-x-full');
      }
      switchTab('chat');
      appendMessage('user', prompt);
      sendPromptToBackend(prompt);
    }

    sendBtn.addEventListener('click', handleSend);
    messageInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    // Quick Prompts Click
    document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const prompt = btn.getAttribute('data-prompt');
        appendMessage('user', prompt);
        sendPromptToBackend(prompt);
      });
    });

    // Dialect Selector Change
    dialectSelect.addEventListener('change', (e) => {
      updateDialectDisplay(e.target.value);
      showToast(`बोली बदलकर '${DIALECT_META[e.target.value]?.name || e.target.value}' कर दी गई`);
    });

    // Global Voice Selector Change
    globalVoiceSelect.addEventListener('change', (e) => {
      selectedVoice = e.target.value;
      modalVoiceSelect.value = e.target.value;
      showToast(`न्यूरल आवाज़: ${selectedVoice.includes('Swara') ? 'स्वरा' : 'मधुर'}`);
    });

    // Persona Mode Switcher
    personaModeSelect.addEventListener('change', (e) => {
      personaMode = e.target.value;
      showToast(`विधा बदलकर '${personaModeSelect.options[personaModeSelect.selectedIndex].text}' कर दी गई`);
    });

    // Phonetics Toggle
    togglePhoneticsBtn.addEventListener('click', () => {
      isPhoneticsActive = !isPhoneticsActive;
      togglePhoneticsBtn.classList.toggle('text-saffron-400', isPhoneticsActive);
      showToast(isPhoneticsActive ? 'उच्चारण सहायक सक्रिय किया गया' : 'उच्चारण सहायक निष्क्रिय');
    });

    // Mic Speech-To-Text Toggle
    micBtn.addEventListener('click', () => startVoiceRecognition(messageInput, micBtn));
    if (transMicBtn) {
      transMicBtn.addEventListener('click', () => startVoiceRecognition(translateSourceText, transMicBtn));
    }

    function startVoiceRecognition(targetInput, triggerButton) {
      if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showToast('स्पीच रिकॉग्निशन आपके ब्राउज़र पर सीधे उपलब्ध नहीं है।');
        return;
      }
      showToast('माइक सक्रिय: बोलिए...');
      try {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRec();
        recognition.lang = 'hi-IN';
        recognition.start();
        triggerButton.classList.add('text-rose-400', 'animate-pulse');
        recognition.onresult = (event) => {
          const speechResult = event.results[0][0].transcript;
          targetInput.value = speechResult;
          targetInput.style.height = 'auto';
          triggerButton.classList.remove('text-rose-400', 'animate-pulse');
        };
        recognition.onerror = () => {
          triggerButton.classList.remove('text-rose-400', 'animate-pulse');
        };
        recognition.onend = () => {
          triggerButton.classList.remove('text-rose-400', 'animate-pulse');
        };
      } catch (err) {
        console.error(err);
        triggerButton.classList.remove('text-rose-400', 'animate-pulse');
      }
    }

    // Reset Chat
    function resetChat() {
      messagesList.innerHTML = '';
      chatHistory = [];
      if (welcomeHero) welcomeHero.style.display = 'block';
      showToast('संवाद सूची साफ कर दी गई है।');
    }
    clearChatBtn.addEventListener('click', resetChat);
    newChatBtn.addEventListener('click', () => {
      resetChat();
      if (window.innerWidth < 1024) {
        chatSidebar.classList.add('-translate-x-full');
      }
    });

    // Sidebar Mobile Toggles
    sidebarToggleBtn.addEventListener('click', () => {
      chatSidebar.classList.remove('-translate-x-full');
    });
    closeSidebarBtn.addEventListener('click', () => {
      chatSidebar.classList.add('-translate-x-full');
    });

    // ==========================================
    // TRANSLATOR TAB LOGIC
    // ==========================================
    async function executeDirectTranslation() {
      const text = translateSourceText.value.trim();
      if (!text) {
        showToast('कृपया पहले अनुवाद हेतु वाक्य दर्ज करें।');
        return;
      }

      const targetCode = transTargetDialect.value;
      runTranslateBtn.disabled = true;
      runTranslateBtn.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i> अनुवाद हो रहा है...';
      lucide.createIcons();

      try {
        const res = await fetch('/api/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: text,
            dialect: targetCode,
            isReverse: isTranslateReverse
          })
        });

        const data = await res.json();
        runTranslateBtn.disabled = false;
        runTranslateBtn.innerHTML = '<span>अनुवाद करें</span><i data-lucide="sparkles" class="w-3.5 h-3.5"></i>';
        lucide.createIcons();

        const translated = data.translatedText || "अनुवाद प्राप्त नहीं हुआ।";
        translatedOutputText.textContent = translated;

        if (data.phoneticText) {
          transPhoneticBlock.classList.remove('hidden');
          transPhoneticText.textContent = data.phoneticText;
        } else {
          transPhoneticBlock.classList.add('hidden');
        }

        if (data.culturalContext) {
          transCulturalBlock.classList.remove('hidden');
          transCulturalText.textContent = data.culturalContext;
        } else {
          transCulturalBlock.classList.add('hidden');
        }

      } catch (err) {
        console.error('Translation error:', err);
        runTranslateBtn.disabled = false;
        runTranslateBtn.innerHTML = '<span>अनुवाद करें</span><i data-lucide="sparkles" class="w-3.5 h-3.5"></i>';
        lucide.createIcons();
        showToast('अनुवाद सर्वर से संपर्क करने में त्रुटि।');
      }
    }

    if (runTranslateBtn) runTranslateBtn.addEventListener('click', executeDirectTranslation);

    if (clearTransInputBtn) {
      clearTransInputBtn.addEventListener('click', () => {
        translateSourceText.value = '';
        translatedOutputText.textContent = 'अनुवाद यहाँ प्रदर्शित होगा...';
        transPhoneticBlock.classList.add('hidden');
        transCulturalBlock.classList.add('hidden');
      });
    }

    if (copyTransResultBtn) {
      copyTransResultBtn.addEventListener('click', () => {
        const txt = translatedOutputText.textContent;
        if (txt && txt !== 'अनुवाद यहाँ प्रदर्शित होगा...') {
          navigator.clipboard.writeText(txt);
          showToast('अनुवाद क्लिपबोर्ड पर कॉपी हो गया!');
        }
      });
    }

    if (speakTransResultBtn) {
      speakTransResultBtn.addEventListener('click', () => {
        const txt = translatedOutputText.textContent;
        if (txt && txt !== 'अनुवाद यहाँ प्रदर्शित होगा...') {
          speakText(txt, 'अनुवादित वाक्य', speakTransResultBtn);
        }
      });
    }

    if (swapTranslateDirectionBtn) {
      swapTranslateDirectionBtn.addEventListener('click', () => {
        isTranslateReverse = !isTranslateReverse;
        if (isTranslateReverse) {
          transDirectionLabel.textContent = 'पहाड़ी ➔ हिन्दी';
          sourceLangTitle.textContent = 'स्रोत भाषा (पहाड़ी बोली)';
        } else {
          transDirectionLabel.textContent = 'हिन्दी ➔ पहाड़ी';
          sourceLangTitle.textContent = 'स्रोत भाषा (मानक हिन्दी)';
        }
        showToast(`अनुवाद दिशा: ${transDirectionLabel.textContent}`);
      });
    }

    // Quick translation starter chips
    document.querySelectorAll('.quick-trans-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const txt = chip.getAttribute('data-text');
        translateSourceText.value = txt;
        executeDirectTranslation();
      });
    });

    // ==========================================
    // CULTURAL STORIES TAB LOGIC
    // ==========================================
    function renderStories() {
      const container = document.getElementById('storiesContainer');
      if (!container) return;
      container.innerHTML = '';

      CULTURAL_STORIES_LIST.forEach(story => {
        const card = document.createElement('div');
        card.className = 'glass-card glass-card-hover rounded-3xl p-5 border border-white/10 flex flex-col justify-between space-y-4';
        card.innerHTML = `
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-saffron-500/20 text-saffron-400 border border-saffron-500/30">
                ${escapeHtml(story.region || 'हिमाचल')}
              </span>
              <span class="text-[10px] text-slate-400 font-serif">लोकगाथा</span>
            </div>
            <h3 class="text-base font-bold text-white leading-snug">${escapeHtml(story.titleHindi)}</h3>
            <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(story.summary)}</p>
            ${story.culturalSignificance ? `
              <div class="pt-1 text-[11px] text-emerald-400 font-medium flex items-center gap-1.5">
                <i data-lucide="award" class="w-3.5 h-3.5 shrink-0"></i>
                <span>${escapeHtml(story.culturalSignificance)}</span>
              </div>
            ` : ''}
          </div>

          <div class="pt-3 border-t border-white/10 flex items-center justify-between gap-2">
            <button class="listen-story-btn px-4 py-2 rounded-xl bg-gradient-to-r from-pine-700 to-pine-800 hover:from-saffron-500 hover:to-saffron-600 text-white hover:text-mist-950 font-bold text-xs flex items-center gap-2 transition shadow-md">
              <i data-lucide="play" class="w-3.5 h-3.5 fill-current"></i>
              <span>पूरी कथा सुनें (Neural Voice)</span>
            </button>
            <button class="expand-story-btn p-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 text-slate-300 hover:text-white transition" title="कथा पढ़ें">
              <i data-lucide="book-open" class="w-4 h-4"></i>
            </button>
          </div>
        `;

        const playBtn = card.querySelector('.listen-story-btn');
        playBtn.addEventListener('click', () => {
          const narrationText = `${story.titleHindi}। क्षेत्र: ${story.region}। ${story.fullStory || story.summary}`;
          speakText(narrationText, story.titleHindi, playBtn);
        });

        const expandBtn = card.querySelector('.expand-story-btn');
        expandBtn.addEventListener('click', () => {
          switchTab('chat');
          triggerQuickPrompt(`${story.titleHindi} की संपूर्ण लोक कथा और इसका सांस्कृतिक महत्व विस्तार से बताएं।`);
        });

        container.appendChild(card);
      });
      lucide.createIcons();
    }

    // ==========================================
    // GLOSSARY TAB LOGIC
    // ==========================================
    function renderGlossaryCards(filterText = '', dialectFilter = 'all') {
      const container = document.getElementById('glossaryCardsContainer');
      if (!container) return;
      container.innerHTML = '';

      const filtered = GLOSSARY_ITEMS.filter(item => {
        const matchText = (item.word && item.word.toLowerCase().includes(filterText.toLowerCase())) ||
          (item.hindi && item.hindi.toLowerCase().includes(filterText.toLowerCase())) ||
          (item.phonetic && item.phonetic.toLowerCase().includes(filterText.toLowerCase()));
        
        const matchDialect = (dialectFilter === 'all') || (item.dialect && item.dialect.toLowerCase().includes(dialectFilter.toLowerCase()));
        return matchText && matchDialect;
      });

      if (filtered.length === 0) {
        container.innerHTML = `
          <div class="col-span-full text-center py-12 text-slate-500 text-xs sm:text-sm">
            कोई शब्द नहीं मिला। अन्य शब्द खोजें।
          </div>`;
        return;
      }

      filtered.forEach(item => {
        const card = document.createElement('div');
        card.className = 'glass-card glass-card-hover rounded-2xl p-4 border border-white/10 flex items-center justify-between gap-3';
        card.innerHTML = `
          <div class="min-w-0 space-y-1">
            <div class="flex items-center gap-2">
              <span class="font-bold text-saffron-400 text-sm">${escapeHtml(item.word)}</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] bg-slate-800 text-slate-300 border border-white/5">${escapeHtml(item.dialect)}</span>
            </div>
            <div class="text-xs text-slate-200">${escapeHtml(item.hindi)}</div>
            ${item.phonetic ? `<div class="text-[11px] font-mono text-slate-400 italic">${escapeHtml(item.phonetic)}</div>` : ''}
          </div>
          <button class="glossary-speak-btn p-2 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-saffron-400 transition shrink-0" title="उच्चारण सुनें">
            <i data-lucide="volume-2" class="w-4 h-4"></i>
          </button>
        `;

        const speakBtn = card.querySelector('.glossary-speak-btn');
        speakBtn.addEventListener('click', () => {
          speakText(item.word, item.word, speakBtn);
        });

        container.appendChild(card);
      });
      lucide.createIcons();
    }

    const glossaryTabSearchInput = document.getElementById('glossaryTabSearchInput');
    const glossaryDialectFilter = document.getElementById('glossaryDialectFilter');

    if (glossaryTabSearchInput) {
      glossaryTabSearchInput.addEventListener('input', (e) => {
        renderGlossaryCards(e.target.value, glossaryDialectFilter.value);
      });
    }
    if (glossaryDialectFilter) {
      glossaryDialectFilter.addEventListener('change', (e) => {
        renderGlossaryCards(glossaryTabSearchInput.value, e.target.value);
      });
    }

    // ==========================================
    // EMERGENCY HUB LOGIC
    // ==========================================
    function renderEmergencyHub() {
      const container = document.getElementById('emergencyGridContainer');
      if (!container) return;
      container.innerHTML = '';

      EMERGENCY_CONTACTS.forEach(item => {
        const row = document.createElement('div');
        row.className = 'p-4 rounded-2xl bg-slate-950/80 border border-white/10 flex items-center justify-between gap-3 hover:border-rose-500/40 transition';
        row.innerHTML = `
          <div>
            <h4 class="font-bold text-white text-sm">${escapeHtml(item.title)}</h4>
            <p class="text-xs text-slate-400 mt-0.5">${escapeHtml(item.desc)}</p>
          </div>
          <a href="tel:${item.number}" class="px-4 py-2 rounded-xl bg-rose-600/30 hover:bg-rose-600/50 border border-rose-500/40 text-rose-300 font-bold text-xs flex items-center gap-1.5 transition shrink-0 shadow-sm">
            <i data-lucide="phone" class="w-3.5 h-3.5"></i>
            <span>${item.number}</span>
          </a>
        `;
        container.appendChild(row);
      });
      lucide.createIcons();
    }

    // ==========================================
    // SETTINGS MODAL
    // ==========================================
    openSettingsBtn.addEventListener('click', () => {
      settingsModal.classList.remove('hidden');
      settingsModal.classList.add('flex');
    });
    closeSettingsBtn.addEventListener('click', () => {
      settingsModal.classList.add('hidden');
      settingsModal.classList.remove('flex');
    });

    saveSettingsBtn.addEventListener('click', async () => {
      const keyVal = apiKeyInput.value.trim();
      selectedVoice = modalVoiceSelect.value;
      selectedRate = voiceSpeedSelect.value;
      globalVoiceSelect.value = selectedVoice;

      if (keyVal) {
        try {
          const res = await fetch('/api/set-key', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: keyVal })
          });
          const data = await res.json();
          if (data.success) {
            showToast('Gemini API Key सुरक्षित हो गई!');
            checkBackendStatus();
          } else {
            showToast('अमान्य API Key दर्ज की गई।');
          }
        } catch (err) {
          showToast('API Key सुरक्षित करने में त्रुटि।');
        }
      } else {
        showToast('सेटिंग्स सुरक्षित कर ली गईं!');
      }
      settingsModal.classList.add('hidden');
      settingsModal.classList.remove('flex');
    });

    function escapeHtml(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    // Auto resize textarea
    messageInput.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 140) + 'px';
    });

    // Window Init
    window.onload = async function() {
      lucide.createIcons();
      updateDialectDisplay('hindi');
      await checkBackendStatus();
      await loadPhrasesFromBackend();
      await loadStoriesFromBackend();
      await loadEmergencyFromBackend();
      renderStories();
      renderGlossaryCards();
      renderEmergencyHub();
    };
  </script>
</body>
</html>
"""
