#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pahadi AI Assistant (पहाड़ी संगम)
A comprehensive AI assistant and translator for Hindi and Himalayan Pahadi dialects.
Zero external dependencies - runs on Python standard library!
"""

import os
import sys
import json
import urllib.request
import urllib.error
import http.server
import socketserver
import webbrowser
from typing import Dict, Any, List

PORT = 8080

# Load .env if present
def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
        except Exception as e:
            print(f"Notice: Could not read .env: {e}")

load_env_file()

DIALECTS = [
    {
        "code": "kangri",
        "displayNameHindi": "कांगड़ी (Kangri)",
        "displayNameEnglish": "Kangri",
        "region": "कांगड़ा घाटी, हमीरपुर, ऊना",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "कांगड़ा घाटी की मिठास भरी पश्चिमी पहाड़ी भाषा। 'मिंजो-तिंजो' और 'कुथी चले' इसके प्रमुख पहचान हैं।"
    },
    {
        "code": "mandeali",
        "displayNameHindi": "मंडीयाली (Mandeali)",
        "displayNameEnglish": "Mandeali",
        "region": "मंडी, सुंदरनगर, छोटी काशी",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "ब्यास तट पर स्थित छोटी काशी मंडी की समृद्ध बोली। विशिष्ट स्वरलहरी और 'भल-भलाई' इसका स्वभाव है।"
    },
    {
        "code": "kullui",
        "displayNameHindi": "कुल्लवी (Kullui)",
        "displayNameEnglish": "Kullui",
        "region": "कुल्लू घाटी, मनाली, बंजार",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "देवभूमि कुल्लू की भाषा। रघुनाथ जी व हडिम्बा देवी की कृपा से जुड़ी, 'जय देव' से हर संवाद का आरंभ होता है।"
    },
    {
        "code": "shimla_pahari",
        "displayNameHindi": "शिमला / महासूवी (Shimla Pahari)",
        "displayNameEnglish": "Shimla Pahari / Mahasuvi",
        "region": "शिमला, ठियोग, कोटखाई, रोहड़ू, सोलन",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "सेब की बेल्ट और महासू देवता की पावन घाटी की पहाड़ी। 'आपु' और 'के हाल च' इसके आत्मीय मुहावरे हैं।"
    },
    {
        "code": "chambeali",
        "displayNameHindi": "चम्बियाली (Chambeali)",
        "displayNameEnglish": "Chambeali",
        "region": "चंबा, रावी घाटी, भरमौर",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "रावी नदी की गोद में बसे ऐतिहासिक चंबा की मधुर बोली। मिंजर मेला और मणिमहेश यात्रा से जुड़ी समृद्ध भाषा।"
    },
    {
        "code": "sirmauri",
        "displayNameHindi": "सिरमौरी (Sirmauri)",
        "displayNameEnglish": "Sirmauri / Giripar",
        "region": "नाहन, रेणुका जी, गिरि-पार (हाटी क्षेत्र)",
        "state": "हिमाचल प्रदेश (Himachal Pradesh)",
        "description": "रेणुका जी और गिरि-पार के हाटी समुदाय की प्राचीन पारम्परिक बोली। बूढ़ी दीवाली और लोकगीतों की धरोहर।"
    },
    {
        "code": "garhwali",
        "displayNameHindi": "गढ़वाली (Garhwali)",
        "displayNameEnglish": "Garhwali",
        "region": "अलकनंदा व भागीरथी घाटी (श्रीनगर, पौड़ी, टिहरी, चमोली)",
        "state": "उत्तराखंड (Uttarakhand)",
        "description": "गढ़वाल मंडल की प्रमुख भाषा। 'पैलाग', 'भुलि', 'दाजु' और 'कख जाणा' इसके विशिष्ट शब्द हैं।"
    },
    {
        "code": "kumaoni",
        "displayNameHindi": "कुमाऊँनी (Kumaoni)",
        "displayNameEnglish": "Kumaoni",
        "region": "कत्यूर व मानसखंड (अल्मोड़ा, नैनीताल, पिथौरागढ़)",
        "state": "उत्तराखंड (Uttarakhand)",
        "description": "कुमाऊं मंडल की मिठास। 'पैलाग', 'भल छौ' और 'मेरो प्यारो दगड़्या' इसके प्रसिद्ध रूप हैं।"
    },
    {
        "code": "dogri",
        "displayNameHindi": "डोगरी (Dogri)",
        "displayNameEnglish": "Dogri",
        "region": "जम्मू व हिमाचल शिवालिक बेल्ट",
        "state": "जम्मू / हिमाचल (Dogra Belt)",
        "description": "संविधान की 8वीं अनुसूची में शामिल मधुर डोगरी भाषा।"
    },
    {
        "code": "jaunsari",
        "displayNameHindi": "जौनसारी (Jaunsari)",
        "displayNameEnglish": "Jaunsari",
        "region": "जौनसार-बावर (चकराता, देहरादून पहाड़ियां)",
        "state": "उत्तराखंड (Uttarakhand)",
        "description": "महासू देवता के उपासक हाटी-जौनसार क्षेत्र की विशिष्ट सांस्कृतिक बोली।"
    }
]

EMERGENCY_CONTACTS = [
    {
        "titleHindi": "राष्ट्रीय आपातकालीन सेवा (National Emergency)",
        "titleEnglish": "National Emergency",
        "number": "112",
        "description": "पुलिस, अग्निशमन व आपातकालीन सहायता (All-in-one Emergency)",
        "icon": "🚨"
    },
    {
        "titleHindi": "हिमाचल आपदा प्रबंधन (HP Disaster Helpline)",
        "titleEnglish": "HP Disaster Authority (Landslides/Floods)",
        "number": "1077",
        "description": "भूस्खलन, बाढ़, भारी बर्फबारी व प्राकृतिक आपदा की स्थिति में तुरंत संपर्क करें",
        "icon": "⚠️"
    },
    {
        "titleHindi": "एम्बुलेंस सेवा (Ambulance Health)",
        "titleEnglish": "Emergency Medical Ambulance",
        "number": "108",
        "description": "मुफ्त 24x7 आपातकालीन चिकित्सा व एम्बुलेंस सेवा",
        "icon": "🚑"
    },
    {
        "titleHindi": "राज्य आपातकालीन कक्ष (State Disaster Ops)",
        "titleEnglish": "State Emergency Operations",
        "number": "1070",
        "description": "हिमाचल प्रदेश राज्य आपदा संचालन केंद्र",
        "icon": "🛡️"
    },
    {
        "titleHindi": "महिला हेल्पलाइन (Women Helpline)",
        "titleEnglish": "Women Emergency Helpline",
        "number": "1091",
        "description": "24 घंटे महिलाओं की सुरक्षा व सहायता",
        "icon": "🌸"
    },
    {
        "titleHindi": "एचआरटीसी बस पूछताछ (HRTC Helpline)",
        "titleEnglish": "HRTC Bus Enquiry & Control Room",
        "number": "01772803017",
        "description": "हिमाचल पथ परिवहन निगम बस समय-सारिणी व पूछताछ केंद्र",
        "icon": "🚌"
    }
]

KNOWLEDGE_TOPICS = [
    {
        "id": "hrtc_info",
        "title": "एचआरटीसी (HRTC) बस सेवा व समय-सारणी",
        "category": "HRTC / परिवहन",
        "summary": "हिमाचल पथ परिवहन निगम (HRTC) की बसें हिमाचल के दुर्गम से दुर्गम गांव तक कनेक्टिविटी प्रदान करती हैं।",
        "details": "• प्रमुख रूट: दिल्ली (ISBT कश्मीरी गेट) से शिमला, मनाली, धर्मशाला, चंबा, कुल्लू, मंडी, किन्नौर (रेकॉन्ग पियो)।\n• ऑनलाइन बुकिंग: hrtchp.com या HRTC मोबाइल ऐप से अग्रिम सीट आरक्षित की जा सकती है।\n• महिला छूट: हिमाचल राज्य के भीतर महिलाओं को सामान्य बसों के किराये में 50% की विशेष छूट दी जाती है।\n• हिम-सफर: सर्दियों में बर्फबारी के दौरान रोहतांग/अटल टनल व कुंजुम पास के रास्तों पर विशेष बुलेटिन जारी होते हैं।\n• मुख्य नियंत्रण कक्ष: 0177-2803017, आईएसबीटी शिमला: 0177-2658322।",
        "contactOrLink": "01772803017"
    },
    {
        "id": "himcare_scheme",
        "title": "हिमकेयर योजना (Himcare Scheme)",
        "category": "सरकारी योजनाएं",
        "summary": "हिमाचल प्रदेश सरकार द्वारा आयुष्मान भारत से छूटे परिवारों को 5 लाख रुपये तक का कैशलेस स्वास्थ्य सुरक्षा कवर।",
        "details": "• लाभ: प्रति वर्ष परिवार को 5 लाख रुपये तक का मुफ्त इलाज अधिकृत सरकारी व निजी अस्पतालों में।\n• पात्रता: हिमाचल प्रदेश के वे सभी नागरिक जो आयुष्मान भारत योजना में कवर नहीं हैं।\n• आवश्यक दस्तावेज: राशन कार्ड, आधार कार्ड और श्रेणी प्रमाण पत्र।\n• रिन्यूअल: ऑनलाइन पोर्टल www.hpsbys.in पर जाकर आसानी से रिन्यू किया जा सकता है।",
        "contactOrLink": "104"
    },
    {
        "id": "apple_farming",
        "title": "सेब की खेती व बागवानी सलाह (Apple Orchard Guide)",
        "category": "कृषि व बागवानी",
        "summary": "हिमाचल की आर्थिकी की रीढ़ 'सेब की खेती' के लिए वैज्ञानिक देखभाल व मौसमी निर्देश।",
        "details": "• किस्में: रॉयल डिलीशियस, रेड गाला, किंग रॉट, जेरोमाइन, डार्क बैरन गाला।\n• प्रूनिंग (सर्दियों की काट-छांट): दिसंबर से फरवरी के बीच जब पेड़ सुप्तावस्था (dormancy) में हों।\n• चिलिंग आवर्स: उच्च गुणवत्ता के लिए 800 से 1200 घंटे 7°C से कम तापमान आवश्यक है।\n• रोग नियंत्रण: स्कैब (Apple Scab) से बचाव के लिए पत्तियों के गिरने पर 5% यूरिया का छिड़काव और कली खिलने से पहले बोर्डो मिश्रण या कॉपर ऑक्सीक्लोराइड का स्प्रे।\n• एंटी-हेल नेट सब्सिडी: ओलावृष्टि से सुरक्षा हेतु उद्यान विभाग द्वारा जाली पर 80% तक अनुदान मिलता है।",
        "contactOrLink": "18001801551"
    },
    {
        "id": "sahara_yojna",
        "title": "मुख्यमंत्री सहारा योजना (Sahara Yojna)",
        "category": "सरकारी योजनाएं",
        "summary": "गंभीर बीमारियों (कैंसर, पक्षाघात, पार्किंसन, मस्कुलर डिस्ट्रॉफी) से पीड़ित रोगियों को ₹3,000 प्रतिमाह वित्तीय सहायता।",
        "details": "• वित्तीय सहायता: पात्र रोगियों को ₹3,000 प्रति माह सीधे बैंक खाते में।\n• उद्देश्य: बिस्तर पर आश्रित गंभीर रोगियों के पोषण व तीमारदार की सहायता।\n• आवेदन: खंड चिकित्सा अधिकारी (BMO) या मुख्य चिकित्सा अधिकारी (CMO) कार्यालय में आवेदन जमा करें।",
        "contactOrLink": "104"
    },
    {
        "id": "himachal_dhaam",
        "title": "पारंपरिक हिमाचली 'धाम' (Himachali Dhaam)",
        "category": "संस्कृति व खानपान",
        "summary": "पहाड़ी शादी-ब्याह व उत्सवों में परोसा जाने वाला शुद्ध पारंपरिक सात्विक शाही भोज।",
        "details": "• बोटी (रसोइए): धाम केवल विशेष रसोइए (जिन्हें 'बोटी' कहा जाता है) पीतल के बड़े बर्तनों (देग/चरोटी) में बनाते हैं।\n• कांगड़ी धाम: मद्रा (काबुली चना व दही), मांह की दाल, चने की खट्टी दाल (अमचूर), और मीठे चावल।\n• मंडीयाली धाम: सेपू बड़ी (उड़द दाल की बड़ी), कद्दू का खट्टा, उड़द दाल का मद्रा और झोल।\n• चंबियाली धाम: राजमा का मद्रा (देसी घी में पके लाल राजमा) और खट्टा कद्दू।\n• परंपरा: यह ज़मीन पर बैठकर पत्तलों में खाई जाती है। इसमें लहसुन-प्याज का प्रयोग वर्जित होता है।",
        "contactOrLink": ""
    },
    {
        "id": "prakritik_kheti",
        "title": "प्राकृतिक खेती खुशहाल किसान योजना (SPNF)",
        "category": "कृषि व बागवानी",
        "summary": "सुभाष पालेकर प्राकृतिक खेती विधि पर हिमाचल सरकार द्वारा देशी गाय खरीद व ड्रम पर भारी अनुदान।",
        "details": "• देशी गाय खरीद: देशी नस्ल की गाय खरीदने पर 50% (अधिकतम ₹25,000) का अनुदान।\n• ड्रम किट: जीवामृत व बीजामृत बनाने के लिए 3 प्लास्टिक ड्रम 75% सब्सिडी पर।\n• लाभ: कीटनाशकों और रासायनिक खादों से मुक्ति, ज़मीन की उर्वरता और फसलों का प्रीमियम मूल्य।",
        "contactOrLink": "18001801551"
    },
    {
        "id": "himachal_tourism",
        "title": "हिमाचल के प्रमुख पर्यटन स्थल व सुरक्षित यात्रा",
        "category": "पर्यटन व यात्रा",
        "summary": "शिमला, मनाली, स्पीति, पराशर, धर्मशाला, चंबा और किन्नौर की मनमोहक वादियां।",
        "details": "• अटल टनल रोहतांग: 9.02 किमी लंबी टनल जो कुल्लू घाटी को लाहौल से वर्ष भर जोड़ती है।\n• स्पीति घाटी: की गोम्पा, धनकर, चंद्रताल झील, काज़ा और दुनिया का सबसे ऊंचा डाकघर 'हिक्किम'।\n• पराशर झील (मंडी): 2730 मीटर की ऊंचाई पर तैरते हुए टापू वाली रहस्यमयी झील और त्रिमंजिला पगोड़ा मंदिर।\n• खज्जियार (चंबा): देवदार के वनों से घिरी 'मिनी स्विट्जरलैंड' नाम से विख्यात झील।\n• सावधानियां: बरसात में संवेदनशील लैंडस्लाइड क्षेत्रों से बचें, मौसम विभाग (IMD) की चेतावनी देखकर ही यात्रा करें।",
        "contactOrLink": "112"
    }
]

CURATED_PHRASES = [
    {
        "id": "shimla_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "नमस्ते! आप कैसे हैं? सब ठीक-ठाक है?",
        "english": "Hello! How are you? Is everything fine?",
        "dialect": "shimla_pahari",
        "translation": "नमस्कार जी! आपु किद्दां आ? सब राजी-खुशी आ?",
        "phonetic": "Namaskar ji! Aapu kiddan aa? Sab raaji-khushi aa?",
        "culturalNote": "शिमला व महासू क्षेत्र में बड़ों को 'आपु' कहकर आदर दिया जाता है और 'राजी-खुशी' कुशल-क्षेम का प्रतीक है।"
    },
    {
        "id": "shimla_2",
        "category": "Weather",
        "categoryHindi": "मौसम",
        "hindi": "आज पहाड़ों पर बर्फ गिर रही है",
        "english": "Snow is falling on the mountains today",
        "dialect": "shimla_pahari",
        "translation": "आज डांड्या मथि हिम (बर्फ) पोए री आ",
        "phonetic": "Aaj daandya mathi him (barf) poe ree aa",
        "culturalNote": "शिमला और कोटखाई की पहाड़ियों पर बर्फबारी को सेब के बगीचों के लिए 'सफेद सोना' माना जाता है।"
    },
    {
        "id": "shimla_3",
        "category": "Farming",
        "categoryHindi": "बागवानी",
        "hindi": "सेब के पेड़ों की काट-छांट (प्रूनिंग) शुरू हो गई है",
        "english": "Apple pruning has started in orchards",
        "dialect": "shimla_pahari",
        "translation": "स्युबे रे बागां री काट-छांट (प्रूनिंग) शुरू होई गी",
        "phonetic": "Syube re baagaan ree kaat-chhaant shuru hoee gee",
        "culturalNote": "सेब को स्थानीय भाषा में 'स्युब' कहते हैं। सर्दियों में प्रूनिंग बागवानों का सबसे महत्वपूर्ण कार्य है।"
    },
    {
        "id": "mandeali_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "नमस्ते जी, आप कहाँ जा रहे हैं?",
        "english": "Greetings, where are you going?",
        "dialect": "mandeali",
        "translation": "नमस्कार जी, तुसीं कुथी चले?",
        "phonetic": "Namaskar ji, tusin kuthi chale?",
        "culturalNote": "मंडीयाली में 'तुसीं' सम्मानसूचक है। छोटी काशी मंडी के 81 प्राचीन शिव मंदिरों की संस्कृति से यह जुड़ा है।"
    },
    {
        "id": "mandeali_2",
        "category": "Food",
        "categoryHindi": "खानपान",
        "hindi": "मंडी की प्रसिद्ध सेपू बड़ी और धाम खाइए",
        "english": "Taste Mandi's famous Sepu Badi and Dhaam",
        "dialect": "mandeali",
        "translation": "मंडी री मश्हूर सेपू बड़ी कने धाम खावा जी",
        "phonetic": "Mandi ree mashhoor Sepu Badi kane Dhaam khaawa ji",
        "culturalNote": "सेपू बड़ी उड़द दाल को पीसकर, उबालकर और तलकर बनाई जाने वाली मंडी की सबसे प्रिय डिश है।"
    },
    {
        "id": "kangri_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "नमस्ते! आपका क्या हाल-चाल है?",
        "english": "Hello! How are you doing?",
        "dialect": "kangri",
        "translation": "नमस्ते जी! तुहाड़ा के हाल-चाल ऐ?",
        "phonetic": "Namaste ji! Tuhaada ke haal-chaal ai?",
        "culturalNote": "कांगड़ी में स्वर का माधुर्य और 'तुहाड़ा' की मिठास कांगड़ा घाटी की पहचान है।"
    },
    {
        "id": "kangri_2",
        "category": "Relations",
        "categoryHindi": "रिश्ते-नाते",
        "hindi": "मुझे तुमसे बहुत प्यार है, मेरे भाई",
        "english": "I love you very much, my brother",
        "dialect": "kangri",
        "translation": "मिंजो तुहाड़े कन्ने बड़ा प्यार ऐ, मेरे भाई",
        "phonetic": "Minjo tuhaade kanne bada pyaar ai, mere bhai",
        "culturalNote": "कांगड़ी में 'मिंजो' (मुझे) और 'तिंजो' (तुम्हें) पश्चिमी पहाड़ी के अद्वितीय सर्वनाम हैं।"
    },
    {
        "id": "kangri_3",
        "category": "Proverbs",
        "categoryHindi": "कहावतें",
        "hindi": "जैसा बोओगे वैसा काटोगे",
        "english": "As you sow, so shall you reap",
        "dialect": "kangri",
        "translation": "जेहा बीजोगे, तेहा ही बड्डोगे",
        "phonetic": "Jeha beejoge, teha hee baddoge",
        "culturalNote": "कांगड़ी लोक-कहावत जो कर्म की प्रधानता पर जोर देती है।"
    },
    {
        "id": "kullui_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "जय देव जी! सब कुशल मंगल?",
        "english": "Greetings to the gods! All well?",
        "dialect": "kullui",
        "translation": "जय देव जी! सब भल-भलाई च?",
        "phonetic": "Jai Dev ji! Sab bhal-bhalai cha?",
        "culturalNote": "कुल्लू में मिलते ही 'जय देव' कहा जाता है, जो घाटी के सैकड़ों देवी-देवताओं के प्रति नमन है।"
    },
    {
        "id": "kullui_2",
        "category": "Food",
        "categoryHindi": "खानपान",
        "hindi": "गरम सिड्डू देसी घी के साथ खाइए",
        "english": "Eat hot Siddu with pure desi ghee",
        "dialect": "kullui",
        "translation": "ताता सिड्डू कने शुद्घ घी खावा जी",
        "phonetic": "Taata Siddu kane shuddh ghee khaawa ji",
        "culturalNote": "सिड्डू कुल्लू-मनाली का पारम्परिक भाप में पका व्यंजन है जो सर्दियों में शरीर को गर्माहट देता है।"
    },
    {
        "id": "chambeali_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "नमस्ते! आप कैसे हैं?",
        "english": "Hello! How are you?",
        "dialect": "chambeali",
        "translation": "नमस्ते जी! तुहाड़े के हाल न?",
        "phonetic": "Namaste ji! Tuhaade ke haal na?",
        "culturalNote": "चम्बियाली बोली रावी घाटी की संस्कृति, मिंजर मेले और मणिमहेश यात्रा से जुड़ी है।"
    },
    {
        "id": "chambeali_2",
        "category": "Food",
        "categoryHindi": "खानपान",
        "hindi": "चंबा का प्रसिद्ध राजमा मद्रा बहुत स्वादिष्ट है",
        "english": "Chamba's Rajma Madra is very delicious",
        "dialect": "chambeali",
        "translation": "चम्बे रा राजमा मद्रा बड़ा सुआदी हुंदा",
        "phonetic": "Chambe ra Rajma Madra bada suaadee hunda",
        "culturalNote": "मद्रा चंबा की धाम का मुख्य व्यंजन है जिसमें दही, घी और मसालों में राजमा धीमी आंच पर पकता है।"
    },
    {
        "id": "sirmauri_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "प्रणाम! क्या हाल-चाल है?",
        "english": "Greetings! What's up?",
        "dialect": "sirmauri",
        "translation": "पैलाग / नमस्कार जी! के हाल-चाल बा?",
        "phonetic": "Pailaag / Namaskar ji! Ke haal-chaal ba?",
        "culturalNote": "सिरमौर और गिरि-पार के हाटी क्षेत्र में आदरणीय बुजुर्गों को नमन किया जाता है।"
    },
    {
        "id": "garhwali_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "प्रणाम (बड़ों के चरण स्पर्श)",
        "english": "Respectful Salutation to elders",
        "dialect": "garhwali",
        "translation": "पैलाग जी / दण्डोत",
        "phonetic": "Pailaag ji / Dandot",
        "culturalNote": "गढ़वाल में बड़ों को 'पैलाग' कहा जाता है, उत्तर में 'जी रया, जाग रया' का आशीर्वाद मिलता है।"
    },
    {
        "id": "garhwali_2",
        "category": "Food",
        "categoryHindi": "खानपान",
        "hindi": "काफुली और झंगोरे की खीर खाइए",
        "english": "Taste Kafuli and Jhangora kheer",
        "dialect": "garhwali",
        "translation": "काफुली अर झंगोरा री खीर खै ल्या",
        "phonetic": "Kaafuli ar Jhangora ree kheer khai lyaa",
        "culturalNote": "काफुली पालक-मेथी का पौष्टिक साग है जिसे लोहे की कड़ाही में पकाया जाता है।"
    },
    {
        "id": "kumaoni_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "प्रणाम! आप कैसे हैं?",
        "english": "Greetings! How are you?",
        "dialect": "kumaoni",
        "translation": "पैलाग जी! कसि छा? सब भल छौ?",
        "phonetic": "Pailaag ji! Kasi chha? Sab bhal chhau?",
        "culturalNote": "कुमाऊं में 'पैलाग' सबसे पावन अभिवादन है और 'भल छौ' कुशलता की पुष्टि करता है।"
    },
    {
        "id": "kumaoni_2",
        "category": "Relations",
        "categoryHindi": "रिश्ते-नाते",
        "hindi": "मेरे प्यारे दोस्त, तुम कहाँ जा रहे हो?",
        "english": "My dear friend, where are you going?",
        "dialect": "kumaoni",
        "translation": "अरे दगड़्या, तू कख जाणै छै?",
        "phonetic": "Are dagadya, tu kakh jaanai chhai?",
        "culturalNote": "'दगड़्या' का अर्थ है साथ चलने वाला सच्चा साथी। कुमाऊँनी भाषा का सबसे आत्मीय शब्द।"
    },
    {
        "id": "dogri_1",
        "category": "Greetings",
        "categoryHindi": "अभिवादन",
        "hindi": "नमस्ते जी! क्या हाल-चाल हैं?",
        "english": "Hello! What is your condition?",
        "dialect": "dogri",
        "translation": "नमस्ते जी! तुंदा के हाल ऐ?",
        "phonetic": "Namaste ji! Tunda ke haal ai?",
        "culturalNote": "डोगरी में 'तुंदा' का अर्थ 'आपका' होता है। शिवालिक क्षेत्र की मधुर भाषा।"
    }
]

CULTURAL_STORIES = [
    {
        "id": "story_golu",
        "titleHindi": "चितई गोलू देवता - न्याय के देवता",
        "titleEnglish": "Golu Devta - The God of Justice",
        "region": "कुमाऊं (अल्मोड़ा, चम्पावत)",
        "summary": "कुमाऊं में जब किसी को न्याय नहीं मिलता, तो वह चितई गोलू मंदिर में स्टांप पेपर पर अर्ज़ी लिखकर घंटी बांधता है।",
        "fullStory": "गोलू देवता कुमाऊं के सबसे पूज्य लोक देवता हैं। वे कत्यूरी राजवंश के राजकुमार गौर भैरव थे। लोककथा के अनुसार उन्होंने बाल्यकाल से ही प्रजा को त्वरित व निष्पक्ष न्याय दिलाया।\n\nआज भी अल्मोड़ा के प्रसिद्ध चितई मंदिर में हज़ारों घंटियां और भक्तों की अर्ज़ियां बंधी हैं। मनोकामना पूर्ण होने पर श्रद्धालु पीतल की घंटी चढ़ाते हैं।",
        "culturalSignificance": "न्याय, निष्पक्षता और जन-विश्वास का सर्वोच्च प्रतीक।",
        "associatedFestivals": "चैत्र नवरात्र, गोलू देवता जातरा, उत्तरायणी"
    },
    {
        "id": "story_siddu_kullu",
        "titleHindi": "सिड्डू और कुल्लू दशहरा की देव-संस्कृति",
        "titleEnglish": "Siddu & Living Deities of Kullu",
        "region": "कुल्लू-मनाली घाटी, हिमाचल",
        "summary": "ढालपुर मैदान में 300 से अधिक देवी-देवताओं का मिलन और हिमाचली पारंपरिक सिड्डू का उत्सव।",
        "fullStory": "कुल्लू का दशहरा पूरे भारत में अनूठा है। यह विजयादशमी को शुरू होकर पूरे एक सप्ताह चलता है। घाटी के 300 से अधिक देवी-देवता अपने पालकियों में सवार होकर भगवान रघुनाथ जी को नमन करने आते हैं।\n\nसर्दियों में पहाड़ी घरों में पारंपरिक 'सिड्डू' बनाया जाता है, जिसमें खमीर उठे आटे में अखरोट, खसखस और मसालों की भरावन देकर भाप में पकाया जाता है और भरपूर देसी घी के साथ खाया जाता है।",
        "culturalSignificance": "हिमाचली देव-परंपरा, समरसता, और शीतकालीन पोषण का संगम।",
        "associatedFestivals": "कुल्लू दशहरा, माघ साजा, फागली"
    },
    {
        "id": "story_mahasu",
        "titleHindi": "महासू देवता - हनोल व शिमला के अधिपति",
        "titleEnglish": "Mahasu Devta - Ruler of Jaunsar & Shimla",
        "region": "हनोल (जौनसार) व शिमला, सिरमौर",
        "summary": "चार महासू भाइयों (बाशिक, पबासी, बूठिया और चालदा) का हनोल में अलौकिक न्याय व लोक-शासन।",
        "fullStory": "टोंस नदी के तट पर स्थित हनोल मंदिर महासू देवता का मुख्य धाम है। किरमिर राक्षस के आतंक से रक्षा हेतु चार महासू भाई प्रकट हुए और दानव का संहार किया।\n\nमहासू देवता को इस क्षेत्र का सच्चा राजा और न्यायाधीश माना जाता है। यहाँ आज भी सदियों पुरानी काष्ठकला का भव्य मंदिर विद्यमान है।",
        "culturalSignificance": "जौनसारी और हिमाचली जनजातीय संस्कृति की एकता और पारम्परिक न्याय का आधार।",
        "associatedFestivals": "जागड़ा उत्सव, बिशू मेला"
    },
    {
        "id": "story_nanda",
        "titleHindi": "नंदा देवी राजजात - हिमालय का महाकुंभ",
        "titleEnglish": "Nanda Devi Raj Jat - Himalayan Pilgrimage",
        "region": "गढ़वाल व कुमाऊं (नौटी से होमकुंड)",
        "summary": "हर 12 वर्ष में आयोजित 280 किमी की पैदल यात्रा, जिसमें चार सींगों वाला मेढ़ा (खाडू) स्वतः मार्गदर्शक बनता है।",
        "fullStory": "नंदा देवी को पहाड़ की ध्याणी (बेटी) माना जाता है। यह यात्रा बेटी नंदा को उसके ससुराल (कैलाश) विदा करने की भावुक और पावन यात्रा है।\n\nनौटी से 17,500 फीट ऊंचे होमकुंड तक चार सींगों वाला खाडू (मेढ़ा) सबसे आगे चलता है और होमकुंड में देवी के वस्त्र लेकर कैलाश की ओर विदा हो जाता है।",
        "culturalSignificance": "गढ़वाल और कुमाऊं को जोड़ने वाली सांस्कृतिक डोर।",
        "associatedFestivals": "नंदा अष्टमी, भाद्रपद राजजात"
    },
    {
        "id": "story_phooldei",
        "titleHindi": "फूलदेई - बसंत का बाल लोकपर्व",
        "titleEnglish": "Phooldei - The Spring Flower Festival",
        "region": "उत्तराखंड व हिमाचल के समस्त पहाड़",
        "summary": "छोटे बच्चे सुबह-सुबह पीले फ्यूंली और बुरांश के फूल चुनकर हर घर की देहरी पर सजाते हैं।",
        "fullStory": "चैत्र मास की संक्रांति पर बच्चे 'फूल देई, छम्मा देई, दैणी द्वार, भर भकार' गाते हुए हर घर की देहरी पर फूल सजाते हैं और सबके लिए मंगल कामना करते हैं।",
        "culturalSignificance": "प्रकृति के प्रति सम्मान और लोकसंस्कृति के संस्कार।",
        "associatedFestivals": "चैत्र संक्रांति"
    }
]

def get_dialect_meta(code: str) -> Dict[str, Any]:
    for d in DIALECTS:
        if d["code"].lower() == code.lower():
            return d
    return DIALECTS[0]

def offline_translate(query: str, dialect_code: str, is_reverse: bool = False) -> Dict[str, Any]:
    q = query.strip().lower()
    dialect = get_dialect_meta(dialect_code)
    
    if is_reverse:
        # Pahadi to Hindi
        for p in CURATED_PHRASES:
            if p["dialect"] == dialect_code and (
                p["translation"].lower() in q or q in p["translation"].lower() or p["phonetic"].lower() in q
            ):
                return {
                    "sourceText": query,
                    "sourceLanguage": f"{dialect['displayNameHindi']} (पहाड़ी)",
                    "targetDialect": dialect_code,
                    "translatedText": p["hindi"],
                    "phoneticText": p["english"],
                    "culturalContext": f"पहाड़ी शब्द '{p['translation']}' का हिंदी अर्थ: '{p['hindi']}'। {p['culturalNote']}",
                    "etiquetteTip": f"यह {dialect['displayNameHindi']} का आत्मीय व पारम्परिक वाक्य है।",
                    "regionalVariation": f"{dialect['region']} में बोली जाती है",
                    "exampleUsage": p["translation"],
                    "isAiPowered": False
                }
        
        # Heuristics for Pahadi -> Hindi
        if any(w in q for w in ["कुथी", "कुथू", "कुतै"]):
            hi = "आप कहाँ जा रहे हैं?"
            ctx = "पहाड़ी में 'कुथी / कुथू' का अर्थ 'कहाँ' और 'चले' का अर्थ 'जा रहे हैं' होता है।"
        elif any(w in q for w in ["हाल", "किद्दां", "कन छौ", "कसि छा"]):
            hi = "आपके क्या हाल-चाल हैं? आप कैसे हैं?"
            ctx = "पहाड़ी में कुशल-क्षेम पूछने का पारंपरिक तरीका।"
        elif "पैलाग" in q:
            hi = "सादर प्रणाम / चरण स्पर्श (बड़ों के प्रति आदर)"
            ctx = "'पैलाग' कुमाऊँनी और गढ़वाली का सबसे पवित्र व आदरणीय अभिवादन है जिसका अर्थ 'पांव लगना / चरण स्पर्श' होता है।"
        elif "जय देव" in q:
            hi = "नमस्कार जी! ईश्वर आपका कल्याण करें।"
            ctx = "कुल्लू, शिमला व मंडी में 'जय देव' देवताओं के प्रति नमन और एक-दूसरे के अभिवादन के लिए बोला जाता है।"
        elif any(w in q for w in ["खाधी", "खाणा", "खावा", "रोटी"]):
            hi = "क्या आपने खाना खा लिया? / भोजन कर रहे हैं।"
            ctx = "पहाड़ी घरों में आने वाले हर व्यक्ति से सबसे पहले आदरपूर्वक भोजन और चाय के लिए पूछा जाता है।"
        elif any(w in q for w in ["घाम", "झड़ी", "काल्हे", "भोल"]):
            hi = "मौसम का हाल: कल धूप खिलेगी / पहाड़ में वर्षा हो रही है।"
            ctx = "'घाम' का अर्थ खिली हुई धूप और 'झड़ी' का अर्थ लगातार होने वाली पहाड़ी वर्षा है।"
        else:
            hi = f"पहाड़ी कथन: \"{query}\" — कुशलक्षेम और बातचीत का सौम्य वाक्य।"
            ctx = f"{dialect['displayNameHindi']} में बोला गया यह वाक्य पहाड़ी संस्कृति और आत्मीयता को दर्शाता है।"
            
        return {
            "sourceText": query,
            "sourceLanguage": f"{dialect['displayNameHindi']} (पहाड़ी)",
            "targetDialect": dialect_code,
            "translatedText": hi,
            "phoneticText": "Pahadi to Hindi Translation",
            "culturalContext": ctx,
            "etiquetteTip": "पहाड़ी में संवाद करते समय सौम्यता और स्थानीय आदर का ध्यान रखें।",
            "regionalVariation": dialect["region"],
            "exampleUsage": query,
            "isAiPowered": False
        }

    else:
        # Hindi to Pahadi
        for p in CURATED_PHRASES:
            if p["dialect"] == dialect_code and (
                p["hindi"].lower() in q or q in p["hindi"].lower() or p["english"].lower() in q
            ):
                return {
                    "sourceText": query,
                    "sourceLanguage": "Hindi",
                    "targetDialect": dialect_code,
                    "translatedText": p["translation"],
                    "phoneticText": p["phonetic"],
                    "culturalContext": p["culturalNote"],
                    "etiquetteTip": "स्थानीय लोगों से संवाद करते समय चेहरे पर मुस्कान और 'जी' का प्रयोग करें।",
                    "regionalVariation": f"{dialect['region']} में प्रचलित",
                    "exampleUsage": p["translation"],
                    "isAiPowered": False
                }
        
        # Dialect heuristics
        if dialect_code == "kangri":
            if "मौसम" in q or "weather" in q:
                res = ("कल मौसम बड़ा खरा (साफ) रहणा ऐ", "Kal mausam bada khara (saaf) rehana ai", "कांगड़ी में साफ मौसम को 'खरा मौसम' और बारिश को 'झड़ी' कहते हैं।")
            elif "कहाँ" in q or "where" in q:
                res = ("तुसीं कुथी चले?", "Tusin kuthi chale?", "कांगड़ी में 'कहाँ' को 'कुथी' और 'आप' को 'तुसीं' कहा जाता है।")
            elif "खाना" in q or "food" in q:
                res = ("तुसीं रोटी खाधी?", "Tusin roti khaadhi?", "कांगड़ा में अतिथियों को सबसे पहले भोजन और चाय के लिए पूछा जाता है।")
            else:
                res = ("तुहाड़ा के हाल-चाल ऐ जी?", "Tuhaada ke haal-chaal ai ji?", "कांगड़ी संवाद में सौम्यता और मधुरता पर विशेष बल दिया जाता है।")
        elif dialect_code == "mandeali":
            if "मौसम" in q:
                res = ("काल्हे मौसम ठीक-ठाक रौहणा", "Kaalhe mausam theek-thaak rauhna", "मंडी में मौसम की बात करते समय ब्यास नदी की बयार का ध्यान रखा जाता है।")
            elif "कहाँ" in q:
                res = ("तुसीं कुथी चले हो?", "Tusin kuthi chale ho?", "मंडीयाली में 'कुथी' कहाँ के लिए प्रयोग होता है।")
            else:
                res = ("तुसीं किद्दां हो? सब ठीक-ठाक आ?", "Tusin kiddan ho? Sab theek-thaak aa?", "मंडीयाली में कुशल-क्षेम के लिए यह वाक्य सर्वप्रिय है।")
        elif dialect_code == "kullui":
            if "मौसम" in q:
                res = ("काल्हे डांड्या मथि घाम (धूप) खिलणा", "Kaalhe daandya mathi ghaam khilna", "कुल्लू में पहाड़ों पर खिली धूप को 'घाम' कहते हैं।")
            else:
                res = ("जय देव जी! सब राजी-खुशी आ?", "Jai Dev ji! Sab raaji-khushi aa?", "कुल्लू में बातचीत की शुरुआत सदैव 'जय देव' से होती है।")
        elif dialect_code == "shimla_pahari":
            if "मौसम" in q:
                res = ("काल्हे मौसम साफ रौहणे री उम्मीद आ", "Kaalhe mausam saaf rauhne ree umeed aa", "शिमला में सेब के बगीचों के लिए मौसम की जानकारी अत्यंत महत्वपूर्ण होती है।")
            elif "कहाँ" in q:
                res = ("आपु कुथी चले?", "Aapu kuthi chale?", "शिमला पहाड़ी में आदरणीय व्यक्ति को 'आपु' कहा जाता है।")
            else:
                res = ("नमस्कार जी! आपु किद्दां आ?", "Namaskar ji! Aapu kiddan aa?", "महासूवी शिष्टाचार का सौम्य वाक्य।")
        elif dialect_code == "garhwali":
            if "मौसम" in q:
                res = ("भोल डांड्यूं मा घाम खिललू", "Bhol daandyun ma ghaam khilalu", "गढ़वाली में कल को 'भोल' और धूप को 'घाम' बोलते हैं।")
            else:
                res = ("कन छौ तुम? सब भल च?", "Kan chhau tum? Sab bhal cha?", "गढ़वाली में 'भल च' कुशलता का सूचक है।")
        elif dialect_code == "kumaoni":
            if "मौसम" in q:
                res = ("भोल मौसम भौत नीक रौलो", "Bhol mausam bhout neek raulo", "कुमाऊंनी में 'नीक' का अर्थ बहुत अच्छा होता है।")
            else:
                res = ("पैलाग दगड़्या! कसि छा?", "Pailaag dagadya! Kasi chha?", "कुमाऊं में 'पैलाग' और 'दगड़्या' सबसे प्रिय शब्द हैं।")
        else:
            res = (f"नमस्ते जी! {dialect['displayNameHindi']} में आपका स्वागत है।", f"Namaste ji! Welcome to {dialect['displayNameEnglish']}", f"{dialect['region']} का पावन शिष्टाचार।")

        return {
            "sourceText": query,
            "sourceLanguage": "Hindi",
            "targetDialect": dialect_code,
            "translatedText": res[0],
            "phoneticText": res[1],
            "culturalContext": res[2],
            "etiquetteTip": "बातचीत में 'जी' और स्थानीय आदरसूचक शब्दों का प्रयोग करें।",
            "regionalVariation": dialect["region"],
            "exampleUsage": res[0],
            "isAiPowered": False
        }

def call_gemini_api(prompt: str, system_prompt: str, json_mode: bool = False) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "MY_GEMINI_API_KEY":
        raise ValueError("GEMINI_API_KEY is not configured")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
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
            "temperature": 0.3
        }
    }
    if json_mode:
        payload["generationConfig"]["responseMimeType"] = "application/json"
        
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        candidates = data.get("candidates", [])
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts:
            return ""
        return parts[0].get("text", "")

def gemini_translate(source_text: str, dialect_code: str, is_reverse: bool = False) -> Dict[str, Any]:
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
    parsed = json.loads(raw_json)
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
    dialect = get_dialect_meta(dialect_code)
    mode_instructions = {
        "elder": "MODE: ELDER FRIENDLY (बुजुर्ग मित्र मोड)\n- Speak in very warm, respectful, clear, and reassuring language with traditional greetings like 'पैलाग जी', 'नमस्कार जी', 'जय देव जी'. Keep sentences short and sweet.",
        "student": "MODE: STUDENT HELPER (छात्र सहायक मोड)\n- Help students understand concepts clearly, provide revision notes, Q&A points, and bilingual English ↔ Hindi/Pahadi explanations with clear bullet points.",
        "farmer": "MODE: FARMER & ORCHARD HELPER (किसान व बागवान मित्र)\n- Provide expert guidance on Apple orchards (pruning, royal delicious, scab management, chilling hours, anti-hail net subsidy, Himcare, natural farming SPNF).",
        "standard": "MODE: ALL-ROUND HIMALAYAN AI ASSISTANT\n- Help with general Q&A, HRTC bus routes, government schemes, tourism, local culture, and folk traditions across Himachal & Uttarakhand."
    }
    mode_inst = mode_instructions.get(mode, mode_instructions["standard"])
    
    system_prompt = f"""
    You are 'Pahadi AI' (पहाड़ी संगम) — the friendly and authentic AI assistant for Himachal Pradesh and Uttarakhand.
    Active Dialect Context: {dialect['displayNameHindi']} ({dialect['region']}, {dialect['state']}).
    
    Core Rules:
    1. Reply in a natural, polite blend of Hindi and local dialect phrases.
    2. {mode_inst}
    3. Keep responses helpful, culturally authentic, and uplifting.
    """
    
    # Simple history compilation
    history_text = ""
    for msg in history[-4:]:
        role = "User" if msg.get("isUser") else "Assistant"
        history_text += f"{role}: {msg.get('text', '')}\n"
        
    full_prompt = f"{history_text}User: {user_msg}\nAssistant:"
    return call_gemini_api(full_prompt, system_prompt)

# HTML UI
INDEX_HTML = """<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Pahadi AI - पहाड़ी संगम (AI Assistant & Translator)</title>
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
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }
    .modal-overlay.active { display: flex; }
    .modal-box {
      background: #1e293b;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 2rem;
      max-width: 480px;
      width: 90%;
      box-shadow: var(--shadow);
    }
    .modal-box h3 { margin-bottom: 1rem; color: #fcd34d; }
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
            <button id="speakResultBtn" class="btn-icon" onclick="speakTranslation()" title="उच्चारण सुनें (Listen)" style="display:none;">🔊</button>
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
        <div class="mode-bar">
          <button class="mode-chip active" onclick="setChatMode('standard', this)">🌟 सर्वज्ञ मित्र (Standard)</button>
          <button class="mode-chip" onclick="setChatMode('elder', this)">👴 बुजुर्ग मित्र (Elder Friendly)</button>
          <button class="mode-chip" onclick="setChatMode('farmer', this)">🍎 किसान व बागवान (Apple/Farm)</button>
          <button class="mode-chip" onclick="setChatMode('student', this)">📚 छात्र सहायक (Student)</button>
        </div>

        <div id="chatMessages" class="chat-messages">
          <div class="message assistant">
            नमस्कार जी! पैलाग! मैं 'पहाड़ी मित्र' हूँ। आप मुझसे हिमाचली व गढ़वाली-कुमाऊंनी बोलियों, सेब के बगीचों, पारंपरिक धाम, लोककथाओं या सामान्य सहायता के बारे में पूछ सकते हैं।
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
    <div class="modal-box">
      <h3>🔑 Gemini API Key Configuration</h3>
      <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 1rem;">
        Enter your Google Gemini API Key to enable advanced AI dialect generation & chatbot intelligence. If left blank, Pahadi AI runs fully on its built-in offline engine!
      </p>
      <input type="password" id="geminiKeyInput" placeholder="Paste your AI Studio API key here" />
      <div class="modal-actions">
        <button class="btn-secondary" onclick="closeKeyModal()">रद्द करें (Cancel)</button>
        <button class="btn-primary" onclick="saveGeminiKey()">सुरक्षित करें (Save)</button>
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

      // Check key
      checkKeyStatus();
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
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = isPahadiToHindi ? 'hi-IN' : 'hi-IN';
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
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
      aDiv.textContent = 'विचार कर रहा हूँ... 🏔️';
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
        aDiv.textContent = data.reply;
        chatHistory.push({ isUser: false, text: data.reply });
      } catch (e) {
        aDiv.textContent = "क्षमा करें, प्रतिक्रिया प्राप्त करने में समस्या हुई।";
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
      const r = await fetch('/api/status');
      const st = await r.json();
      const text = document.getElementById('keyStatusText');
      if (st.hasKey) {
        text.textContent = "Gemini AI Active ✨";
        text.style.color = "#34d399";
      } else {
        text.textContent = "Set API Key";
        text.style.color = "#fcd34d";
      }
    }

    async function saveGeminiKey() {
      const key = document.getElementById('geminiKeyInput').value.trim();
      await fetch('/api/set-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: key })
      });
      closeKeyModal();
      checkKeyStatus();
    }

    window.onload = init;
  </script>
</body>
</html>
"""

class PahadiServerHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json", status=200):
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(status=204)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ["/", "/index.html"]:
            self._set_headers("text/html")
            self.wfile.write(INDEX_HTML.encode("utf-8"))
        elif path == "/api/dialects":
            self._set_headers()
            self.wfile.write(json.dumps(DIALECTS).encode("utf-8"))
        elif path == "/api/phrases":
            self._set_headers()
            self.wfile.write(json.dumps(CURATED_PHRASES).encode("utf-8"))
        elif path == "/api/stories":
            self._set_headers()
            self.wfile.write(json.dumps(CULTURAL_STORIES).encode("utf-8"))
        elif path == "/api/knowledge":
            self._set_headers()
            self.wfile.write(json.dumps(KNOWLEDGE_TOPICS).encode("utf-8"))
        elif path == "/api/emergency":
            self._set_headers()
            self.wfile.write(json.dumps(EMERGENCY_CONTACTS).encode("utf-8"))
        elif path == "/api/status":
            key = os.environ.get("GEMINI_API_KEY", "").strip()
            has_key = bool(key and key != "MY_GEMINI_API_KEY")
            self._set_headers()
            self.wfile.write(json.dumps({"hasKey": has_key}).encode("utf-8"))
        else:
            self._set_headers("text/plain", 404)
            self.wfile.write(b"Not Found")

    def do_POST(self):
        path = self.path.split("?")[0]
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len).decode("utf-8")
        body = json.loads(post_data) if post_data else {}

        if path == "/api/translate":
            query = body.get("query", "")
            dialect_code = body.get("dialect", "kangri")
            is_reverse = body.get("isReverse", False)

            # Try Gemini API if key is set, else use offline engine
            result = None
            key = os.environ.get("GEMINI_API_KEY", "").strip()
            if key and key != "MY_GEMINI_API_KEY":
                try:
                    result = gemini_translate(query, dialect_code, is_reverse)
                except Exception as e:
                    print(f"Gemini API error, falling back to offline: {e}")

            if not result:
                result = offline_translate(query, dialect_code, is_reverse)

            self._set_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))

        elif path == "/api/chat":
            msg = body.get("message", "")
            mode = body.get("mode", "standard")
            dialect_code = body.get("dialect", "kangri")
            history = body.get("history", [])

            reply = None
            key = os.environ.get("GEMINI_API_KEY", "").strip()
            if key and key != "MY_GEMINI_API_KEY":
                try:
                    reply = gemini_chat(history, msg, mode, dialect_code)
                except Exception as e:
                    print(f"Gemini chat error: {e}")

            if not reply:
                # Friendly offline fallback response
                d = get_dialect_meta(dialect_code)
                reply = (
                    f"नमस्कार जी! ({d['displayNameHindi']})\n"
                    f"आपका संदेश प्राप्त हुआ: \"{msg}\"।\n\n"
                    f"वर्तमान में AI सेवा ऑफलाइन मोड में संचालित है। "
                    f"यदि आप पूर्ण संवादी AI का उपयोग करना चाहते हैं, तो ऊपर 'Gemini Key' बटन से अपनी API कुंजी दर्ज करें। "
                    f"तब तक आप अनुवादक, प्रामाणिक वाक्यांश और लोकधरोहर का आनंद ले सकते हैं!"
                )

            self._set_headers()
            self.wfile.write(json.dumps({"reply": reply}).encode("utf-8"))

        elif path == "/api/set-key":
            new_key = body.get("key", "").strip()
            if new_key:
                os.environ["GEMINI_API_KEY"] = new_key
                # Also save to .env
                env_path = os.path.join(os.path.dirname(__file__), ".env")
                try:
                    with open(env_path, "w", encoding="utf-8") as f:
                        f.write(f"GEMINI_API_KEY={new_key}\n")
                except Exception as e:
                    print(f"Could not persist to .env: {e}")

            self._set_headers()
            self.wfile.write(json.dumps({"success": True}).encode("utf-8"))

        else:
            self._set_headers("text/plain", 404)
            self.wfile.write(b"Not Found")

def run(port=PORT):
    server_address = ("", port)
    try:
        httpd = socketserver.TCPServer(server_address, PahadiServerHandler)
    except OSError:
        # If port 8080 is occupied, try 8081
        port = 8081
        server_address = ("", port)
        httpd = socketserver.TCPServer(server_address, PahadiServerHandler)

    url = f"http://localhost:{port}"
    print("=" * 64)
    print("  🏔️  Pahadi AI Assistant (पहाड़ी संगम) is Running!")
    print(f"  👉 Web App URL: {url}")
    print("  ⭐ Press Ctrl+C in this terminal to stop the server.")
    print("=" * 64)

    # Open browser automatically
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
    run()
