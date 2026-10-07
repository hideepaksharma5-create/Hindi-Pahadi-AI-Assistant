# -*- coding: utf-8 -*-
"""
Himachal AI Assistant - Production Modern Web Interface
Crafted with Tailwind CSS, Lucide Icons, Glassmorphism, and Deep Himalayan Pine & Saffron Design.
Integrated with Gemini Generative AI, Real-time Dialect Chat, Voice Synthesis, and Living Glossary.
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="hi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>हिमाचली व हिन्दी AI सहायक | Hindi-Pahadi AI Assistant</title>
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#090d16">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">

  <!-- Google Fonts: Inter & Cinzel / Noto Sans Devanagari for regional typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@300;400;500;600;700&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
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
            'glow-saffron': '0 0 20px -3px rgba(245, 158, 11, 0.25)',
            'glow-pine': '0 0 25px -4px rgba(21, 128, 61, 0.3)',
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
      background: rgba(15, 23, 42, 0.78);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .glass-card {
      background: rgba(30, 41, 59, 0.55);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Himalayan Mountain Pattern Accent */
    .himalaya-pattern {
      background-image: 
        radial-gradient(circle at 1px 1px, rgba(255,255,255,0.04) 1px, transparent 0),
        radial-gradient(circle at 10% 20%, rgba(19, 78, 44, 0.35) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(229, 142, 38, 0.15) 0%, transparent 45%);
      background-size: 24px 24px, 100% 100%, 100% 100%;
    }

    @keyframes pulse-ring {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.05); opacity: 0.4; }
      100% { transform: scale(0.95); opacity: 0.8; }
    }
    .animate-pulse-ring {
      animation: pulse-ring 3s infinite ease-in-out;
    }
  </style>
</head>
<body class="bg-mist-950 text-slate-100 font-sans min-h-screen flex flex-col himalaya-pattern selection:bg-saffron-500/30 selection:text-saffron-400">

  <!-- Main Top Header -->
  <header class="sticky top-0 z-40 w-full glass-panel border-b border-white/10 px-4 lg:px-8 py-3 transition-colors duration-200">
    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      
      <!-- Brand & Status -->
      <div class="flex items-center gap-3">
        <button id="sidebarToggleBtn" class="lg:hidden p-2 rounded-xl hover:bg-slate-800/60 text-slate-300">
          <i data-lucide="menu" class="w-5 h-5"></i>
        </button>
        <div class="relative flex items-center justify-center w-10 h-10 rounded-2xl bg-gradient-to-br from-pine-700 to-pine-900 border border-pine-700/60 shadow-glow-pine">
          <i data-lucide="mountain-snow" class="w-5 h-5 text-saffron-400"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base sm:text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
              <span>हिमाचल</span>
              <span class="text-saffron-400 font-serif">AI</span>
            </h1>
            <span id="headerStatusPill" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <span id="headerStatusDot" class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              <span id="headerStatusText">ऑनलाइन • 8080</span>
            </span>
          </div>
          <p class="text-xs text-slate-400 hidden sm:block">मानक हिन्दी व पहाड़ी बोलियों का संवादात्मक सहायक</p>
        </div>
      </div>

      <!-- Dialect Selector and Action Tools -->
      <div class="flex items-center gap-2 sm:gap-3">
        <!-- Dialect Switcher -->
        <div class="relative">
          <select id="dialectSelect" class="bg-slate-900/80 hover:bg-slate-800/90 text-slate-200 text-xs sm:text-sm font-medium py-1.5 sm:py-2 pl-3 pr-8 rounded-xl border border-white/10 shadow-sm focus:outline-none focus:ring-2 focus:ring-saffron-500/50 appearance-none cursor-pointer">
            <option value="hindi" selected>मानक हिन्दी (Hindi)</option>
            <option value="kangri">कांगड़ी (Kangri)</option>
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
          <i data-lucide="chevron-down" class="w-4 h-4 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none"></i>
        </div>

        <!-- Dictionary Glossary Modal Trigger -->
        <button id="openGlossaryBtn" title="पहाड़ी शब्दकोश (Glossary)" class="p-2 sm:px-3 sm:py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-white/10 text-slate-300 hover:text-saffron-400 flex items-center gap-1.5 text-xs font-medium transition">
          <i data-lucide="book-open-text" class="w-4 h-4"></i>
          <span class="hidden md:inline">शब्दकोश</span>
        </button>

        <!-- Emergency Contacts Trigger -->
        <button id="openEmergencyBtn" title="आपातकालीन नंबर (Helplines)" class="p-2 sm:px-3 sm:py-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-white/10 text-rose-300 hover:text-rose-400 flex items-center gap-1.5 text-xs font-medium transition">
          <i data-lucide="phone-call" class="w-4 h-4"></i>
          <span class="hidden md:inline">हेल्पलाइन</span>
        </button>

        <!-- Settings Modal Trigger -->
        <button id="openSettingsBtn" title="सेटिंग्स (Settings)" class="p-2 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-white/10 text-slate-300 hover:text-white transition">
          <i data-lucide="sliders-horizontal" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  </header>

  <!-- Main Body Wrapper -->
  <div class="flex-1 max-w-7xl w-full mx-auto flex overflow-hidden relative">

    <!-- Sidebar: Conversation History & Regional Knowledge -->
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

      <!-- Dialect Region Selector Cards -->
      <div class="p-4 flex-1 overflow-y-auto space-y-4">
        <div>
          <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">सक्रिय बोली की विशेषता</span>
          <div id="dialectBadgeCard" class="p-3 rounded-2xl glass-card border border-saffron-500/20 bg-saffron-500/5">
            <div class="flex items-center gap-2 mb-1.5">
              <span class="w-2 h-2 rounded-full bg-saffron-400"></span>
              <h4 id="activeDialectTitle" class="text-sm font-semibold text-saffron-300">मानक हिन्दी</h4>
            </div>
            <p id="activeDialectDesc" class="text-xs text-slate-300 leading-relaxed">
              पारंपरिक व आधुनिक शिष्टाचार युक्त शुद्ध हिन्दी वार्तालाप।
            </p>
          </div>
        </div>

        <div>
          <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">संवाद विधा (Persona Mode)</span>
          <select id="personaModeSelect" class="w-full bg-slate-900/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-saffron-500">
            <option value="standard">🏔️ सर्व-सहायक (All-Round)</option>
            <option value="elder">👵 बुजुर्ग मित्र (Elder Friendly)</option>
            <option value="student">📚 छात्र सहायक (Student Helper)</option>
            <option value="farmer">🍎 बागवान व किसान मित्र (Apple Farmer)</option>
          </select>
        </div>

        <div>
          <span class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-2 px-1">हाल के संवाद (Recent Topics)</span>
          <div id="recentChatsList" class="space-y-1 text-xs">
            <button class="w-full text-left px-3 py-2 rounded-xl bg-slate-800/40 text-slate-300 hover:bg-slate-800 hover:text-white flex items-center gap-2 transition" onclick="triggerQuickPrompt('मण्डयाली में अभिवादन और हाल-चाल कैसे पूछते हैं?')">
              <i data-lucide="message-square" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
              <span class="truncate">मण्डयाली में अभिवादन के नियम</span>
            </button>
            <button class="w-full text-left px-3 py-2 rounded-xl text-slate-400 hover:bg-slate-800/40 hover:text-slate-200 flex items-center gap-2 transition" onclick="triggerQuickPrompt('कांगड़ा किला और धौलाधार पर्वत का सांस्कृतिक इतिहास बताएं।')">
              <i data-lucide="message-square" class="w-3.5 h-3.5 text-slate-500 shrink-0"></i>
              <span class="truncate">कांगड़ा किला और इतिहास</span>
            </button>
            <button class="w-full text-left px-3 py-2 rounded-xl text-slate-400 hover:bg-slate-800/40 hover:text-slate-200 flex items-center gap-2 transition" onclick="triggerQuickPrompt('शिमला व किन्नौर में सेब के बगीचों में प्रूनिंग और खाद प्रबंधन कैसे करें?')">
              <i data-lucide="message-square" class="w-3.5 h-3.5 text-slate-500 shrink-0"></i>
              <span class="truncate">शिमला सेब कटाई की ऋतु</span>
            </button>
          </div>
        </div>

        <div class="pt-2">
          <div class="p-3 rounded-2xl bg-slate-900/60 border border-white/5 space-y-2">
            <div class="flex items-center justify-between text-xs text-slate-300">
              <span class="flex items-center gap-1.5">
                <i data-lucide="cpu" class="w-3.5 h-3.5 text-pine-500"></i> AI Inference
              </span>
              <span class="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400">Gemini 3.7 / Offline</span>
            </div>
            <div class="text-[11px] text-slate-400">
              Voice: <span class="text-slate-200 font-mono">Neural TTS + Calibrated Pitch</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Clear Chat & Quick Info -->
      <div class="p-4 border-t border-white/10 flex items-center justify-between">
        <button id="clearChatBtn" class="flex items-center gap-1.5 text-xs text-rose-400 hover:text-rose-300 transition">
          <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
          <span>संवाद साफ करें</span>
        </button>
        <span class="text-[11px] text-slate-500">v2.0 • देवनागरी</span>
      </div>
    </aside>

    <!-- Main Chat Workspace -->
    <main class="flex-1 flex flex-col h-[calc(100vh-65px)] min-w-0">
      
      <!-- Chat Messages Scroll Area -->
      <div id="chatContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        
        <!-- Welcome Hero (Empty State initially visible) -->
        <div id="welcomeHero" class="my-6 max-w-2xl mx-auto text-center space-y-4">
          <div class="inline-flex p-3 rounded-3xl bg-gradient-to-b from-saffron-500/20 to-transparent border border-saffron-500/30 text-saffron-400 mb-1">
            <i data-lucide="sparkles" class="w-8 h-8"></i>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            नमस्ते जी! क्या मदद कर सकता हूँ?
          </h2>
          <p class="text-sm sm:text-base text-slate-300 leading-relaxed max-w-lg mx-auto">
            यह AI सहायक हिमाचल प्रदेश व उत्तराखंड की बोलियों—कांगड़ी, मण्डयाली, महासूवी, कुलवी, चम्बियाली, गढ़वाली, कुमाऊँनी—व मानक हिन्दी में अनुवाद और संवादात्मक मार्गदर्शन प्रदान करता है।
          </p>

          <!-- Suggested Quick Prompts Grid -->
          <div class="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-left">
            <button class="quick-prompt-btn p-3 rounded-2xl glass-card hover:border-saffron-500/40 hover:bg-slate-800/80 transition group flex items-start gap-3" data-prompt="कांगड़ी बोली में रोजमर्रा के हाल-चाल कैसे पूछते हैं? उदाहरण देकर समझाओ।">
              <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 group-hover:text-saffron-400 transition">
                <i data-lucide="message-circle" class="w-4 h-4"></i>
              </span>
              <div>
                <div class="text-xs font-semibold text-slate-200 group-hover:text-saffron-300">कांगड़ी में हाल-चाल पूछना</div>
                <div class="text-[11px] text-slate-400 line-clamp-1">दैनिक संवाद और अभिवादन के वाक्य</div>
              </div>
            </button>

            <button class="quick-prompt-btn p-3 rounded-2xl glass-card hover:border-saffron-500/40 hover:bg-slate-800/80 transition group flex items-start gap-3" data-prompt="मण्डयाली में एक छोटी लोक कथा या कहावत सुनाएं और उसका हिन्दी अर्थ भी बताएं।">
              <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 group-hover:text-saffron-400 transition">
                <i data-lucide="scroll" class="w-4 h-4"></i>
              </span>
              <div>
                <div class="text-xs font-semibold text-slate-200 group-hover:text-saffron-300">पहाड़ी लोक कथा / कहावत</div>
                <div class="text-[11px] text-slate-400 line-clamp-1">मण्डयाली कथा व हिन्दी अनुवाद</div>
              </div>
            </button>

            <button class="quick-prompt-btn p-3 rounded-2xl glass-card hover:border-saffron-500/40 hover:bg-slate-800/80 transition group flex items-start gap-3" data-prompt="हिमाचल के ऊपरी क्षेत्रों (शिमला/किन्नौर) में सेब की मुख्य किस्में कौन सी हैं और उनकी देखभाल कैसे करें?">
              <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 group-hover:text-saffron-400 transition">
                <i data-lucide="apple" class="w-4 h-4"></i>
              </span>
              <div>
                <div class="text-xs font-semibold text-slate-200 group-hover:text-saffron-300">हिमाचली सेब और बागवानी</div>
                <div class="text-[11px] text-slate-400 line-clamp-1">प्रमुख किस्में, प्रूनिंग व सुरक्षा निर्देश</div>
              </div>
            </button>

            <button class="quick-prompt-btn p-3 rounded-2xl glass-card hover:border-saffron-500/40 hover:bg-slate-800/80 transition group flex items-start gap-3" data-prompt="महासूवी (शिमला पहाड़ी) बोली के 5 आम शब्द और उनके मानक हिन्दी अर्थ बताएं।">
              <span class="p-2 rounded-xl bg-pine-900/60 text-pine-500 group-hover:text-saffron-400 transition">
                <i data-lucide="languages" class="w-4 h-4"></i>
              </span>
              <div>
                <div class="text-xs font-semibold text-slate-200 group-hover:text-saffron-300">महासूवी शब्दकोश</div>
                <div class="text-[11px] text-slate-400 line-clamp-1">शिमला क्षेत्र के प्रचलित स्थानीय शब्द</div>
              </div>
            </button>
          </div>
        </div>

        <!-- Chat History Stream -->
        <div id="messagesList" class="max-w-3xl mx-auto space-y-5">
          <!-- Dynamically populated messages -->
        </div>

        <!-- Typing Indicator -->
        <div id="typingIndicator" class="max-w-3xl mx-auto hidden">
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 rounded-xl bg-pine-800/80 border border-pine-700/50 flex items-center justify-center text-saffron-400 shrink-0">
              <i data-lucide="sparkles" class="w-4 h-4 animate-spin"></i>
            </div>
            <div class="p-4 rounded-2xl glass-card border border-white/10 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce"></span>
              <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce [animation-delay:0.2s]"></span>
              <span class="w-2 h-2 rounded-full bg-saffron-400 animate-bounce [animation-delay:0.4s]"></span>
              <span class="text-xs text-slate-400 ml-2">पहाड़ी में उत्तर तैयार हो रहा है...</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Bottom Chat Input Bar -->
      <div class="p-4 bg-gradient-to-t from-mist-950 via-mist-950/95 to-transparent border-t border-white/5">
        <div class="max-w-3xl mx-auto">
          
          <!-- Transliteration / Roman script helper bar -->
          <div class="flex items-center justify-between text-xs px-2 mb-2 text-slate-400">
            <div class="flex items-center gap-2">
              <span id="translitBadge" class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-800/70 border border-white/5 text-[11px] text-slate-300">
                <i data-lucide="sparkles" class="w-3 h-3 text-saffron-400"></i>
                <span id="targetDialectNameDisplay">मानक हिन्दी</span>
              </span>
              <button id="togglePhoneticsBtn" class="text-[11px] text-slate-400 hover:text-saffron-400 flex items-center gap-1 transition">
                <i data-lucide="spell-check" class="w-3 h-3"></i>
                <span>उच्चारण सहायक (Phonetics)</span>
              </button>
            </div>
            <span class="text-[11px] text-slate-500 hidden sm:inline">Shift + Enter नई पंक्ति के लिए</span>
          </div>

          <!-- Input bar wrapper -->
          <div class="relative glass-card rounded-2xl border border-white/10 focus-within:border-saffron-500/50 focus-within:ring-2 focus-within:ring-saffron-500/20 shadow-xl transition-all duration-200">
            <textarea
              id="messageInput"
              rows="1"
              placeholder="यहाँ हिन्दी या पहाड़ी में लिखें... (उदा: तुसां केड़े हाल चाला न? / सेब में प्रूनिंग कब करें?)"
              class="w-full bg-transparent text-slate-100 placeholder-slate-500 text-sm sm:text-base py-3.5 pl-4 pr-24 resize-none max-h-36 focus:outline-none"
            ></textarea>

            <div class="absolute right-2 bottom-2 flex items-center gap-1">
              <!-- Speech Recognition Voice Toggle -->
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
                class="p-2 rounded-xl bg-gradient-to-r from-pine-700 to-pine-800 hover:from-saffron-500 hover:to-saffron-600 text-white transition shadow-md"
              >
                <i data-lucide="arrow-up" class="w-4 h-4"></i>
              </button>
            </div>
          </div>

          <!-- Bottom Footer Disclaimer -->
          <p class="text-center text-[11px] text-slate-500 mt-2">
            पहाड़ी संगम AI • स्थानीय बोलियों की मिठास व प्रामाणिक जानकारी
          </p>
        </div>
      </div>

    </main>
  </div>

  <!-- Glossary Modal -->
  <div id="glossaryModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-mist-900 border border-white/10 rounded-3xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-5 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-pine-900/80 border border-pine-700 text-saffron-400 flex items-center justify-center">
            <i data-lucide="book-marked" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">पहाड़ी - हिन्दी शब्दकोश (Glossary)</h3>
            <p class="text-xs text-slate-400">दैनिक जीवन में प्रयुक्त होने वाले पारंपरिक पहाड़ी शब्द व वाक्यांश</p>
          </div>
        </div>
        <button id="closeGlossaryBtn" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Search in Glossary -->
      <div class="p-4 border-b border-white/5 bg-slate-900/40">
        <div class="relative">
          <input
            id="glossarySearchInput"
            type="text"
            placeholder="शब्द या वाक्यांश खोजें (उदा: तुसां, मिंजो, किजो, राजी-खुशी)..."
            class="w-full bg-slate-950/70 border border-white/10 rounded-xl px-4 py-2 pl-9 text-xs sm:text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-saffron-500"
          >
          <i data-lucide="search" class="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2"></i>
        </div>
      </div>

      <!-- Word Table / Grid -->
      <div class="p-4 flex-1 overflow-y-auto space-y-2.5 text-xs sm:text-sm" id="glossaryList">
        <!-- Rendered via JS -->
      </div>
    </div>
  </div>

  <!-- Emergency Helplines Modal -->
  <div id="emergencyModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-mist-900 border border-white/10 rounded-3xl max-w-lg w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
      <div class="p-5 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-rose-950 border border-rose-800 text-rose-400 flex items-center justify-center">
            <i data-lucide="phone-call" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="text-base font-bold text-white">🚨 आपातकालीन व आपदा हेल्पलाइन</h3>
            <p class="text-xs text-slate-400">हिमाचल प्रदेश व उत्तराखंड आपातकालीन नंबर</p>
          </div>
        </div>
        <button id="closeEmergencyBtn" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>
      <div class="p-4 flex-1 overflow-y-auto space-y-2.5 text-xs sm:text-sm" id="emergencyList">
        <!-- Rendered via JS -->
      </div>
    </div>
  </div>

  <!-- Settings & API Key Modal -->
  <div id="settingsModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-mist-900 border border-white/10 rounded-3xl max-w-md w-full p-6 shadow-2xl space-y-5">
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <h3 class="text-base font-bold text-white flex items-center gap-2">
          <i data-lucide="settings" class="w-4 h-4 text-saffron-400"></i>
          <span>सिस्टम व API सेटिंग्स</span>
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
            class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200 focus:outline-none focus:border-saffron-500"
          >
          <p class="text-[11px] text-slate-500 mt-1">
            Google AI Studio से प्राप्त मुफ़्त Key दर्ज करें। Key आपके लोकल .env में सुरक्षित रहेगी।
          </p>
        </div>

        <div>
          <label class="block text-slate-300 font-medium mb-1">आवाज की गति (TTS Speed)</label>
          <select id="voiceSpeedSelect" class="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-slate-200">
            <option value="0.85">धीमी व स्पष्ट (0.85x)</option>
            <option value="1.0" selected>सामान्य (1.0x)</option>
            <option value="1.2">तेज (1.2x)</option>
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
      { word: 'तुसां / तुसी', dialect: 'कांगड़ी / मण्डयाली', hindi: 'आप (You)', phonetic: 'Tusan / Tusi' },
      { word: 'मिंजो / महां', dialect: 'कांगड़ी / मण्डयाली', hindi: 'मुझे / मुझको (To me)', phonetic: 'Minjo / Mahaan' },
      { word: 'तिंजो', dialect: 'कांगड़ी', hindi: 'तुझे / उसको (To you/him)', phonetic: 'Tinjo' },
      { word: 'किजो', dialect: 'मण्डयाली', hindi: 'क्यों (Why)', phonetic: 'Kijo' },
      { word: 'कुथी / कुथू', dialect: 'कांगड़ी / मण्डयाली', hindi: 'कहाँ (Where)', phonetic: 'Kuthi / Kuthu' },
      { word: 'केड़े हाल चाला / किद्दां', dialect: 'मण्डयाली / शिमला', hindi: 'क्या हाल-चाल हैं (How are you)', phonetic: 'Kede haal chaala / Kiddan' },
      { word: 'बाशठ / बाठ', dialect: 'महासूवी', hindi: 'बातचीत / किस्सा (Conversation)', phonetic: 'Basht / Baath' },
      { word: 'सिड्डू (Siddu)', dialect: 'कुल्लू / शिमला', hindi: 'पारंपरिक खमीरयुक्त स्टीम्ड व्यंजन', phonetic: 'Siddu (Himachali dish)' },
      { word: 'पैलाग', dialect: 'गढ़वाली / कुमाऊँनी', hindi: 'चरण स्पर्श / आदरणीय प्रणाम', phonetic: 'Pailaag' },
      { word: 'दगड़्या', dialect: 'कुमाऊँनी', hindi: 'सच्चा मित्र / सहयात्री (Dear Friend)', phonetic: 'Dagadya' }
    ];

    let EMERGENCY_CONTACTS = [
      { title: 'राष्ट्रीय आपातकालीन सेवा (National Emergency)', number: '112', desc: 'पुलिस, अग्निशमन व एम्बुलेंस (All-in-one)' },
      { title: 'हिमाचल आपदा प्रबंधन (HP Disaster Helpline)', number: '1077', desc: 'भूस्खलन, बाढ़ व प्राकृतिक आपदा सहायता' },
      { title: 'एम्बुलेंस स्वास्थ्य सेवा (Medical Ambulance)', number: '108', desc: '24x7 मुफ्त आपातकालीन चिकित्सा' },
      { title: 'महिला हेल्पलाइन (Women Emergency)', number: '1091', desc: '24 घंटे महिला सुरक्षा' },
      { title: 'एचआरटीसी बस पूछताछ (HRTC Control Room)', number: '01772803017', desc: 'समय-सारिणी व सड़क स्थिति' }
    ];

    // State Variables
    let currentDialect = 'hindi';
    let isPhoneticsActive = true;
    let personaMode = 'standard';
    let chatHistory = [];
    let isOnline = false;

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

    // Sidebar
    const chatSidebar = document.getElementById('chatSidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');

    // Modals
    const glossaryModal = document.getElementById('glossaryModal');
    const openGlossaryBtn = document.getElementById('openGlossaryBtn');
    const closeGlossaryBtn = document.getElementById('closeGlossaryBtn');
    const glossaryList = document.getElementById('glossaryList');
    const glossarySearchInput = document.getElementById('glossarySearchInput');

    const emergencyModal = document.getElementById('emergencyModal');
    const openEmergencyBtn = document.getElementById('openEmergencyBtn');
    const closeEmergencyBtn = document.getElementById('closeEmergencyBtn');
    const emergencyList = document.getElementById('emergencyList');

    const settingsModal = document.getElementById('settingsModal');
    const openSettingsBtn = document.getElementById('openSettingsBtn');
    const closeSettingsBtn = document.getElementById('closeSettingsBtn');
    const saveSettingsBtn = document.getElementById('saveSettingsBtn');
    const apiKeyInput = document.getElementById('apiKeyInput');

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
            word: `${p.hindi} ➔ ${p.translation}`,
            dialect: p.dialect || 'पहाड़ी',
            hindi: p.culturalNote || p.english,
            phonetic: p.phonetic || ''
          }));
        }
      } catch (err) {
        console.warn('Phrases load failed, using default glossary:', err);
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
    }

    // Render Glossary items
    function renderGlossary(filterText = '') {
      glossaryList.innerHTML = '';
      const filtered = GLOSSARY_ITEMS.filter(item => 
        (item.word && item.word.toLowerCase().includes(filterText.toLowerCase())) ||
        (item.hindi && item.hindi.toLowerCase().includes(filterText.toLowerCase())) ||
        (item.dialect && item.dialect.toLowerCase().includes(filterText.toLowerCase())) ||
        (item.phonetic && item.phonetic.toLowerCase().includes(filterText.toLowerCase()))
      );

      if (filtered.length === 0) {
        glossaryList.innerHTML = `
          <div class="text-center py-8 text-slate-500">
            कोई शब्द नहीं मिला। अन्य शब्द खोजें।
          </div>`;
        return;
      }

      filtered.forEach(item => {
        const row = document.createElement('div');
        row.className = 'p-3 rounded-2xl bg-slate-950/60 border border-white/5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 hover:border-saffron-500/30 transition';
        row.innerHTML = `
          <div>
            <div class="flex items-center gap-2">
              <span class="font-bold text-saffron-400 text-sm">${item.word}</span>
              <span class="px-2 py-0.5 rounded-full text-[10px] bg-slate-800 text-slate-400 border border-white/5">${item.dialect}</span>
            </div>
            <div class="text-xs text-slate-300 mt-0.5">${item.hindi}</div>
          </div>
          <div class="text-left sm:text-right">
            <span class="text-[11px] font-mono text-slate-400 italic">${item.phonetic}</span>
          </div>
        `;
        glossaryList.appendChild(row);
      });
    }

    // Render Emergency Contacts
    function renderEmergency() {
      emergencyList.innerHTML = '';
      EMERGENCY_CONTACTS.forEach(item => {
        const row = document.createElement('div');
        row.className = 'p-3.5 rounded-2xl bg-slate-950/60 border border-white/5 flex items-center justify-between gap-3';
        row.innerHTML = `
          <div>
            <h4 class="font-bold text-white text-sm">${item.title}</h4>
            <p class="text-xs text-slate-400 mt-0.5">${item.desc}</p>
          </div>
          <a href="tel:${item.number}" class="px-3.5 py-1.5 rounded-xl bg-rose-600/30 hover:bg-rose-600/50 border border-rose-500/40 text-rose-300 font-bold text-xs flex items-center gap-1.5 transition">
            <i data-lucide="phone" class="w-3.5 h-3.5"></i>
            <span>${item.number}</span>
          </a>
        `;
        emergencyList.appendChild(row);
      });
      lucide.createIcons();
    }

    // Auto resize textarea
    messageInput.addEventListener('input', function() {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 140) + 'px';
    });

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
          <div class="max-w-[85%] sm:max-w-[78%] space-y-1.5">
            <div class="flex items-center gap-2 text-[11px] text-slate-400 px-1">
              <span class="font-semibold text-saffron-400">${DIALECT_META[dialect]?.name || 'सहायक'}</span>
              <span>•</span>
              <span>${msgObj.timestamp}</span>
            </div>
            <div class="p-4 rounded-3xl rounded-tl-sm glass-card border border-white/10 text-slate-100 text-sm leading-relaxed shadow-lg">
              <div class="whitespace-pre-line">${escapeHtml(text)}</div>
              ${phonetic && isPhoneticsActive ? `
                <div class="mt-2.5 pt-2 border-t border-white/10 text-xs font-mono text-slate-400 italic flex items-center gap-1.5">
                  <i data-lucide="volume-2" class="w-3.5 h-3.5 text-saffron-400 shrink-0"></i>
                  <span>${escapeHtml(phonetic)}</span>
                </div>
              ` : ''}
            </div>
            <!-- Message Action Toolbar -->
            <div class="flex items-center gap-1 text-slate-400 text-xs px-1">
              <button class="tts-play-btn p-1.5 rounded-lg hover:bg-slate-800 hover:text-saffron-400 transition" title="उच्चारण सुनें (Listen Voice)">
                <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
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

        // Attach action handlers
        const copyBtn = msgEl.querySelector('.copy-msg-btn');
        copyBtn.addEventListener('click', () => {
          navigator.clipboard.writeText(text);
          showToast('संदेश क्लिपबोर्ड पर कॉपी हो गया!');
        });

        const ttsBtn = msgEl.querySelector('.tts-play-btn');
        ttsBtn.addEventListener('click', () => {
          speakText(text, ttsBtn);
        });

        const fbUp = msgEl.querySelector('.feedback-up');
        fbUp.addEventListener('click', () => {
          fbUp.classList.toggle('text-emerald-400');
          showToast('धन्यवाद! आपकी प्रतिक्रिया दर्ज कर ली गई है।');
        });

      } else {
        // User Message
        msgEl.innerHTML = `
          <div class="max-w-[85%] sm:max-w-[78%] space-y-1">
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

    // High-Fidelity Neural Voice TTS: edge-tts (hi-IN-SwaraNeural) + Web Speech fallback
    async function speakText(text, btn = null) {
      if (!text) return;
      
      const originalHtml = btn ? btn.innerHTML : '';
      if (btn) {
        btn.innerHTML = '<span class="text-xs text-saffron-400 animate-pulse">⏳ लोड हो रहा है...</span>';
        btn.disabled = true;
      }
      showToast('स्वरा न्यूरल आवाज़ (hi-IN-SwaraNeural) तैयार हो रही है...');

      try {
        const res = await fetch('/api/tts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            text: text,
            voice: 'hi-IN-SwaraNeural',
            rate: '-6%',
            pitch: '+0Hz'
          })
        });

        if (res.ok) {
          const data = await res.json();
          const audioUrl = data.audio_url || data.audioUrl;
          if (audioUrl) {
            const audio = new Audio(audioUrl);
            audio.play();

            if (btn) {
              btn.innerHTML = '<span class="text-xs text-emerald-400 animate-pulse">🔊 बज रहा है...</span>';
            }

            audio.onended = () => {
              if (btn) {
                btn.innerHTML = originalHtml;
                btn.disabled = false;
                lucide.createIcons();
              }
            };
            audio.onerror = () => {
              if (btn) {
                btn.innerHTML = originalHtml;
                btn.disabled = false;
                lucide.createIcons();
              }
            };
            return;
          }
        }
      } catch (err) {
        console.warn('FastAPI /api/tts endpoint unavailable, trying fallback:', err);
      }

      // Browser Web Speech API fallback
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'hi-IN';
        const speed = parseFloat(document.getElementById('voiceSpeedSelect')?.value) || 1.0;
        utterance.rate = speed;
        utterance.onend = () => {
          if (btn) {
            btn.innerHTML = originalHtml;
            btn.disabled = false;
            lucide.createIcons();
          }
        };
        window.speechSynthesis.speak(utterance);
      } else {
        if (btn) {
          btn.innerHTML = originalHtml;
          btn.disabled = false;
          lucide.createIcons();
        }
        showToast('ध्वनि उत्पन्न करने में समस्या हुई।');
      }
    }

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
    micBtn.addEventListener('click', () => {
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
        micBtn.classList.add('text-rose-400');
        recognition.onresult = (event) => {
          const speechResult = event.results[0][0].transcript;
          messageInput.value = speechResult;
          messageInput.style.height = 'auto';
          micBtn.classList.remove('text-rose-400');
        };
        recognition.onerror = () => {
          micBtn.classList.remove('text-rose-400');
        };
        recognition.onend = () => {
          micBtn.classList.remove('text-rose-400');
        };
      } catch (err) {
        console.error(err);
        micBtn.classList.remove('text-rose-400');
      }
    });

    // Clear and New Chat
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

    // Modals Handling
    openGlossaryBtn.addEventListener('click', () => {
      glossaryModal.classList.remove('hidden');
      glossaryModal.classList.add('flex');
      renderGlossary();
    });
    closeGlossaryBtn.addEventListener('click', () => {
      glossaryModal.classList.add('hidden');
      glossaryModal.classList.remove('flex');
    });

    openEmergencyBtn.addEventListener('click', () => {
      emergencyModal.classList.remove('hidden');
      emergencyModal.classList.add('flex');
      renderEmergency();
    });
    closeEmergencyBtn.addEventListener('click', () => {
      emergencyModal.classList.add('hidden');
      emergencyModal.classList.remove('flex');
    });

    glossarySearchInput.addEventListener('input', (e) => {
      renderGlossary(e.target.value);
    });

    openSettingsBtn.addEventListener('click', () => {
      settingsModal.classList.remove('hidden');
      settingsModal.classList.add('flex');
    });
    closeSettingsBtn.addEventListener('click', () => {
      settingsModal.classList.add('hidden');
      settingsModal.classList.remove('flex');
    });

    // Save Settings & API Key
    saveSettingsBtn.addEventListener('click', async () => {
      const keyVal = apiKeyInput.value.trim();
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
      return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
    }

    // Initialize Icons and Initial State
    window.onload = async function() {
      lucide.createIcons();
      updateDialectDisplay('hindi');
      await checkBackendStatus();
      await loadPhrasesFromBackend();
      await loadEmergencyFromBackend();
      renderGlossary();
    };
  </script>
</body>
</html>
"""
