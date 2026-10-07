package com.example.data.dictionary

import com.example.data.model.CulturalStory
import com.example.data.model.EmergencyContact
import com.example.data.model.LocalKnowledgeTopic
import com.example.data.model.PahadiDialect
import com.example.data.model.PhraseCategory
import com.example.data.model.PhraseItem
import com.example.data.model.TranslationResult

object PahadiOfflineEngine {

    val emergencyContacts: List<EmergencyContact> = listOf(
        EmergencyContact(
            titleHindi = "राष्ट्रीय आपातकालीन सेवा (National Emergency)",
            titleEnglish = "National Emergency",
            number = "112",
            description = "पुलिस, अग्निशमन व आपातकालीन सहायता (All-in-one Emergency)",
            iconName = "emergency"
        ),
        EmergencyContact(
            titleHindi = "हिमाचल आपदा प्रबंधन (HP Disaster Helpline)",
            titleEnglish = "HP Disaster Authority (Landslides/Floods)",
            number = "1077",
            description = "भूस्खलन, बाढ़, भारी बर्फबारी व प्राकृतिक आपदा की स्थिति में तुरंत संपर्क करें",
            iconName = "warning"
        ),
        EmergencyContact(
            titleHindi = "एम्बुलेंस सेवा (Ambulance Health)",
            titleEnglish = "Emergency Medical Ambulance",
            number = "108",
            description = "मुफ्त 24x7 आपातकालीन चिकित्सा व एम्बुलेंस सेवा",
            iconName = "medical_services"
        ),
        EmergencyContact(
            titleHindi = "राज्य आपातकालीन कक्ष (State Disaster Ops)",
            titleEnglish = "State Emergency Operations",
            number = "1070",
            description = "हिमाचल प्रदेश राज्य आपदा संचालन केंद्र",
            iconName = "shield"
        ),
        EmergencyContact(
            titleHindi = "महिला हेल्पलाइन (Women Helpline)",
            titleEnglish = "Women Emergency Helpline",
            number = "1091",
            description = "24 घंटे महिलाओं की सुरक्षा व सहायता",
            iconName = "support"
        ),
        EmergencyContact(
            titleHindi = "एचआरटीसी बस पूछताछ (HRTC Helpline)",
            titleEnglish = "HRTC Bus Enquiry & Control Room",
            number = "01772803017",
            description = "हिमाचल पथ परिवहन निगम बस समय-सारिणी व पूछताछ केंद्र",
            iconName = "directions_bus"
        )
    )

    val localKnowledgeTopics: List<LocalKnowledgeTopic> = listOf(
        LocalKnowledgeTopic(
            id = "hrtc_info",
            title = "एचआरटीसी (HRTC) बस सेवा व समय-सारणी",
            category = "HRTC",
            summary = "हिमाचल पथ परिवहन निगम (HRTC) की बसें हिमाचल के दुर्गम से दुर्गम गांव तक कनेक्टिविटी प्रदान करती हैं।",
            details = "• प्रमुख रूट: दिल्ली (ISBT कश्मीरी गेट) से शिमला, मनाली, धर्मशाला, चंबा, कुल्लू, मंडी, किन्नौर (रेकॉन्ग पियो)।\n• ऑनलाइन बुकिंग: hrtchp.com या HRTC मोबाइल ऐप से अग्रिम सीट आरक्षित की जा सकती है।\n• महिला छूट: हिमाचल राज्य के भीतर महिलाओं को सामान्य बसों के किराये में 50% की विशेष छूट दी जाती है।\n• हिम-सफर: सर्दियों में बर्फबारी के दौरान रोहतांग/अटल टनल व कुंजुम पास के रास्तों पर विशेष बुलेटिन जारी होते हैं।\n• मुख्य नियंत्रण कक्ष: 0177-2803017, आईएसबीटी शिमला: 0177-2658322।",
            contactOrLink = "01772803017"
        ),
        LocalKnowledgeTopic(
            id = "himcare_scheme",
            title = "हिमकेयर योजना (Himcare Scheme)",
            category = "Schemes",
            summary = "हिमाचल प्रदेश सरकार द्वारा आयुष्मान भारत से छूटे परिवारों को 5 लाख रुपये तक का कैशलेस स्वास्थ्य सुरक्षा कवर।",
            details = "• लाभ: प्रति वर्ष परिवार को 5 लाख रुपये तक का मुफ्त इलाज अधिकृत सरकारी व निजी अस्पतालों में।\n• पात्रता: हिमाचल प्रदेश के वे सभी नागरिक जो आयुष्मान भारत योजना में कवर नहीं हैं।\n• आवश्यक दस्तावेज: राशन कार्ड, आधार कार्ड और श्रेणी प्रमाण पत्र।\n• रिन्यूअल: ऑनलाइन पोर्टल www.hpsbys.in पर जाकर आसानी से रिन्यू किया जा सकता है।",
            contactOrLink = "104"
        ),
        LocalKnowledgeTopic(
            id = "apple_farming",
            title = "सेब की खेती व बागवानी सलाह (Apple Orchard Guide)",
            category = "Agriculture",
            summary = "हिमाचल की आर्थिकी की रीढ़ 'सेब की खेती' के लिए वैज्ञानिक देखभाल व मौसमी निर्देश।",
            details = "• किस्में: रॉयल डिलीशियस, रेड गाला, किंग रॉट, जेरोमाइन, डार्क बैरन गाला।\n• प्रूनिंग (सर्दियों की काट-छांट): दिसंबर से फरवरी के बीच जब पेड़ सुप्तावस्था (dormancy) में हों।\n• चिलिंग आवर्स: उच्च गुणवत्ता के लिए 800 से 1200 घंटे 7°C से कम तापमान आवश्यक है।\n• रोग नियंत्रण: स्कैब (Apple Scab) से बचाव के लिए पत्तियों के गिरने पर 5% यूरिया का छिड़काव और कली खिलने से पहले बोर्डो मिश्रण या कॉपर ऑक्सीक्लोराइड का स्प्रे।\n• एंटी-हेल नेट सब्सिडी: ओलावृष्टि से सुरक्षा हेतु उद्यान विभाग द्वारा जाली पर 80% तक अनुदान मिलता है।",
            contactOrLink = "18001801551"
        ),
        LocalKnowledgeTopic(
            id = "sahara_yojna",
            title = "मुख्यमंत्री सहारा योजना (Sahara Yojna)",
            category = "Schemes",
            summary = "गंभीर बीमारियों (कैंसर, पक्षाघात, पार्किंसन, मस्कुलर डिस्ट्रॉफी) से पीड़ित रोगियों को ₹3,000 प्रतिमाह वित्तीय सहायता।",
            details = "• वित्तीय सहायता: पात्र रोगियों को ₹3,000 प्रति माह सीधे बैंक खाते में।\n• उद्देश्य: बिस्तर पर आश्रित गंभीर रोगियों के पोषण व तीमारदार की सहायता।\n• आवेदन: खंड चिकित्सा अधिकारी (BMO) या मुख्य चिकित्सा अधिकारी (CMO) कार्यालय में आवेदन जमा करें।",
            contactOrLink = "104"
        ),
        LocalKnowledgeTopic(
            id = "himachal_dhaam",
            title = "पारंपरिक हिमाचली 'धाम' (Himachali Dhaam)",
            category = "Tradition",
            summary = "पहाड़ी शादी-ब्याह व उत्सवों में परोसा जाने वाला शुद्ध पारंपरिक सात्विक शाही भोज।",
            details = "• बोटी (रसोइए): धाम केवल विशेष रसोइए (जिन्हें 'बोटी' कहा जाता है) पीतल के बड़े बर्तनों (देग/चरोटी) में बनाते हैं।\n• कांगड़ी धाम: मद्रा (काबुली चना व दही), मांह की दाल, चने की खट्टी दाल (अमचूर), और मीठे चावल।\n• मंडीयाली धाम: सेपू बड़ी (उड़द दाल की बड़ी), कद्दू का खट्टा, उड़द दाल का मद्रा और झोल।\n• चंबियाली धाम: राजमा का मद्रा (देसी घी में पके लाल राजमा) और खट्टा कद्दू।\n• परंपरा: यह ज़मीन पर बैठकर पत्तलों (पत्तल) में खाई जाती है। इसमें लहसुन-प्याज का प्रयोग वर्जित होता है।",
            contactOrLink = ""
        ),
        LocalKnowledgeTopic(
            id = "prakritik_kheti",
            title = "प्राकृतिक खेती खुशहाल किसान योजना (SPNF)",
            category = "Agriculture",
            summary = "सुभाष पालेकर प्राकृतिक खेती विधि पर हिमाचल सरकार द्वारा देशी गाय खरीद व ड्रम पर भारी अनुदान।",
            details = "• देशी गाय खरीद: देशी नस्ल की गाय खरीदने पर 50% (अधिकतम ₹25,000) का अनुदान।\n• ड्रम किट: जीवामृत व बीजामृत बनाने के लिए 3 प्लास्टिक ड्रम 75% सब्सिडी पर।\n• लाभ: कीटनाशकों और रासायनिक खादों से मुक्ति, ज़मीन की उर्वरता और सेब/फसलों का प्रीमियम मूल्य।",
            contactOrLink = "18001801551"
        ),
        LocalKnowledgeTopic(
            id = "himachal_tourism",
            title = "हिमाचल के प्रमुख पर्यटन स्थल व सुरक्षित यात्रा",
            category = "Tourism",
            summary = "शिमला, मनाली, स्पीति, पराशर, धर्मशाला, चंबा और किन्नौर की मनमोहक वादियां।",
            details = "• अटल टनल रोहतांग: 9.02 किमी लंबी टनल जो कुल्लू घाटी को लाहौल से वर्ष भर जोड़ती है।\n• स्पीति घाटी: की गोम्पा, धनकर, चंद्रताल झील, काज़ा और दुनिया का सबसे ऊंचा डाकघर 'हिक्किम'।\n• पराशर झील (मंडी): 2730 मीटर की ऊंचाई पर तैरते हुए टापू वाली रहस्यमयी झील और त्रिमंजिला पगोड़ा मंदिर।\n• खज्जियार (चंबा): देवदार के वनों से घिरी 'मिनी स्विट्जरलैंड' नाम से विख्यात झील।\n• सावधानियां: बरसात में संवेदनशील लैंडस्लाइड क्षेत्रों से बचें, मौसम विभाग (IMD) की चेतावनी देखकर ही यात्रा करें।",
            contactOrLink = "112"
        )
    )

    val curatedPhrases: List<PhraseItem> = listOf(
        // Shimla / Mahasuvi
        PhraseItem(
            id = "shimla_1",
            category = PhraseCategory.GREETINGS,
            hindi = "नमस्ते! आप कैसे हैं? सब ठीक-ठाक है?",
            english = "Hello! How are you? Is everything fine?",
            dialect = PahadiDialect.SHIMLA_PAHARI,
            translation = "नमस्कार जी! आपु किद्दां आ? सब राजी-खुशी आ?",
            phonetic = "Namaskar ji! Aapu kiddan aa? Sab raaji-khushi aa?",
            culturalNote = "शिमला व महासू क्षेत्र में बड़ों को 'आपु' कहकर आदर दिया जाता है और 'राजी-खुशी' कुशल-क्षेम का प्रतीक है।"
        ),
        PhraseItem(
            id = "shimla_2",
            category = PhraseCategory.WEATHER,
            hindi = "आज पहाड़ों पर बर्फ गिर रही है",
            english = "Snow is falling on the mountains today",
            dialect = PahadiDialect.SHIMLA_PAHARI,
            translation = "आज डांड्या मथि हिम (बर्फ) पोए री आ",
            phonetic = "Aaj daandya mathi him (barf) poe ree aa",
            culturalNote = "शिमला और कोटखाई की पहाड़ियों पर बर्फबारी को सेब के बगीचों के लिए 'सफेद सोना' माना जाता है।"
        ),
        PhraseItem(
            id = "shimla_3",
            category = PhraseCategory.FARMING,
            hindi = "सेब के पेड़ों की काट-छांट (प्रूनिंग) शुरू हो गई है",
            english = "Apple pruning has started in orchards",
            dialect = PahadiDialect.SHIMLA_PAHARI,
            translation = "स्युबे रे बागां री काट-छांट (प्रूनिंग) शुरू होई गी",
            phonetic = "Syube re baagaan ree kaat-chhaant shuru hoee gee",
            culturalNote = "सेब को स्थानीय भाषा में 'स्युब' कहते हैं। सर्दियों में प्रूनिंग बागवानों का सबसे महत्वपूर्ण कार्य है।"
        ),

        // Mandeali
        PhraseItem(
            id = "mandeali_1",
            category = PhraseCategory.GREETINGS,
            hindi = "नमस्ते जी, आप कहाँ जा रहे हैं?",
            english = "Greetings, where are you going?",
            dialect = PahadiDialect.MANDEALI,
            translation = "नमस्कार जी, तुसीं कुथी चले?",
            phonetic = "Namaskar ji, tusin kuthi chale?",
            culturalNote = "मंडीयाली में 'तुसीं' सम्मानसूचक है। छोटी काशी मंडी के 81 प्राचीन शिव मंदिरों की संस्कृति से यह जुड़ा है।"
        ),
        PhraseItem(
            id = "mandeali_2",
            category = PhraseCategory.FOOD,
            hindi = "मंडी की प्रसिद्ध सेपू बड़ी और धाम खाइए",
            english = "Taste Mandi's famous Sepu Badi and Dhaam",
            dialect = PahadiDialect.MANDEALI,
            translation = "मंडी री मश्हूर सेपू बड़ी कने धाम खावा जी",
            phonetic = "Mandi ree mashhoor Sepu Badi kane Dhaam khaawa ji",
            culturalNote = "सेपू बड़ी उड़द दाल को पीसकर, उबालकर और तलकर बनाई जाने वाली मंडी की सबसे प्रिय डिश है।"
        ),

        // Kangri
        PhraseItem(
            id = "kangri_1",
            category = PhraseCategory.GREETINGS,
            hindi = "नमस्ते! आपका क्या हाल-चाल है?",
            english = "Hello! How are you doing?",
            dialect = PahadiDialect.KANGRI,
            translation = "नमस्ते जी! तुहाड़ा के हाल-चाल ऐ?",
            phonetic = "Namaste ji! Tuhaada ke haal-chaal ai?",
            culturalNote = "कांगड़ी में स्वर का माधुर्य और 'तुहाड़ा' की मिठास कांगड़ा घाटी की पहचान है।"
        ),
        PhraseItem(
            id = "kangri_2",
            category = PhraseCategory.RELATIONS,
            hindi = "मुझे तुमसे बहुत प्यार है, मेरे भाई",
            english = "I love you very much, my brother",
            dialect = PahadiDialect.KANGRI,
            translation = "मिंजो तुहाड़े कन्ने बड़ा प्यार ऐ, मेरे भाई",
            phonetic = "Minjo tuhaade kanne bada pyaar ai, mere bhai",
            culturalNote = "कांगड़ी में 'मिंजो' (मुझे) और 'तिंजो' (तुम्हें) पश्चिमी पहाड़ी के अद्वितीय सर्वनाम हैं।"
        ),
        PhraseItem(
            id = "kangri_3",
            category = PhraseCategory.PROVERBS,
            hindi = "जैसा बोओगे वैसा काटोगे",
            english = "As you sow, so shall you reap",
            dialect = PahadiDialect.KANGRI,
            translation = "जेहा बीजोगे, तेहा ही बड्डोगे",
            phonetic = "Jeha beejoge, teha hee baddoge",
            culturalNote = "कांगड़ी लोक-कहावत जो कर्म की प्रधानता पर जोर देती है।"
        ),

        // Kullui
        PhraseItem(
            id = "kullui_1",
            category = PhraseCategory.GREETINGS,
            hindi = "जय देव जी! सब कुशल मंगल?",
            english = "Greetings to the gods! All well?",
            dialect = PahadiDialect.KULLUI,
            translation = "जय देव जी! सब भल-भलाई च?",
            phonetic = "Jai Dev ji! Sab bhal-bhalai cha?",
            culturalNote = "कुल्लू में मिलते ही 'जय देव' कहा जाता है, जो घाटी के सैकड़ों देवी-देवताओं के प्रति नमन है।"
        ),
        PhraseItem(
            id = "kullui_2",
            category = PhraseCategory.FOOD,
            hindi = "गरम सिड्डू देसी घी के साथ खाइए",
            english = "Eat hot Siddu with pure desi ghee",
            dialect = PahadiDialect.KULLUI,
            translation = "ताता सिड्डू कने शुद्घ घी खावा जी",
            phonetic = "Taata Siddu kane shuddh ghee khaawa ji",
            culturalNote = "सिड्डू कुल्लू-मनाली का पारम्परिक भाप में पका व्यंजन है जो सर्दियों में शरीर को गर्माहट देता है।"
        ),

        // Chambeali
        PhraseItem(
            id = "chambeali_1",
            category = PhraseCategory.GREETINGS,
            hindi = "नमस्ते! आप कैसे हैं?",
            english = "Hello! How are you?",
            dialect = PahadiDialect.CHAMBEALI,
            translation = "नमस्ते जी! तुहाड़े के हाल न?",
            phonetic = "Namaste ji! Tuhaade ke haal na?",
            culturalNote = "चम्बियाली बोली रावी घाटी की संस्कृति, मिंजर मेले और मणिमहेश यात्रा से जुड़ी है।"
        ),
        PhraseItem(
            id = "chambeali_2",
            category = PhraseCategory.FOOD,
            hindi = "चंबा का प्रसिद्ध राजमा मद्रा बहुत स्वादिष्ट है",
            english = "Chamba's Rajma Madra is very delicious",
            dialect = PahadiDialect.CHAMBEALI,
            translation = "चम्बे रा राजमा मद्रा बड़ा सुआदी हुंदा",
            phonetic = "Chambe ra Rajma Madra bada suaadee hunda",
            culturalNote = "मद्रा चंबा की धाम का मुख्य व्यंजन है जिसमें दही, घी और मसालों में राजमा धीमी आंच पर पकता है।"
        ),

        // Sirmauri
        PhraseItem(
            id = "sirmauri_1",
            category = PhraseCategory.GREETINGS,
            hindi = "प्रणाम! क्या हाल-चाल है?",
            english = "Greetings! What's up?",
            dialect = PahadiDialect.SIRMAURI,
            translation = "पैलाग / नमस्कार जी! के हाल-चाल बा?",
            phonetic = "Pailaag / Namaskar ji! Ke haal-chaal ba?",
            culturalNote = "सिरमौर और गिरि-पार के हाटी क्षेत्र में आदरणीय बुजुर्गों को नमन किया जाता है।"
        ),
        PhraseItem(
            id = "sirmauri_2",
            category = PhraseCategory.WEATHER,
            hindi = "आज बहुत ठंडी बयार चल रही है",
            english = "Very cold mountain wind is blowing today",
            dialect = PahadiDialect.SIRMAURI,
            translation = "आज बड़ी ठंडी सीर (हवा) चाली री",
            phonetic = "Aaj badi thandi seer (hawa) chaali ree",
            culturalNote = "पहाड़ी में बर्फीली ठंडी हवा को 'सीर' या 'सिरी' कहा जाता है।"
        ),

        // Garhwali
        PhraseItem(
            id = "garhwali_1",
            category = PhraseCategory.GREETINGS,
            hindi = "प्रणाम (बड़ों के चरण स्पर्श)",
            english = "Respectful Salutation to elders",
            dialect = PahadiDialect.GARHWALI,
            translation = "पैलाग जी / दण्डोत",
            phonetic = "Pailaag ji / Dandot",
            culturalNote = "गढ़वाल में बड़ों को 'पैलाग' कहा जाता है, उत्तर में 'जी रया, जाग रया' का आशीर्वाद मिलता है।"
        ),
        PhraseItem(
            id = "garhwali_2",
            category = PhraseCategory.FOOD,
            hindi = "काफुली और झंगोरे की खीर खाइए",
            english = "Taste Kafuli and Jhangora kheer",
            dialect = PahadiDialect.GARHWALI,
            translation = "काफुली अर झंगोरा री खीर खै ल्या",
            phonetic = "Kaafuli ar Jhangora ree kheer khai lyaa",
            culturalNote = "काफुली पालक-मेथी का पौष्टिक साग है जिसे लोहे की कड़ाही में पकाया जाता है।"
        ),

        // Kumaoni
        PhraseItem(
            id = "kumaoni_1",
            category = PhraseCategory.GREETINGS,
            hindi = "प्रणाम! आप कैसे हैं?",
            english = "Greetings! How are you?",
            dialect = PahadiDialect.KUMAONI,
            translation = "पैलाग जी! कसि छा? सब भल छौ?",
            phonetic = "Pailaag ji! Kasi chha? Sab bhal chhau?",
            culturalNote = "कुमाऊं में 'पैलाग' सबसे पावन अभिवादन है और 'भल छौ' कुशलता की पुष्टि करता है।"
        ),
        PhraseItem(
            id = "kumaoni_2",
            category = PhraseCategory.RELATIONS,
            hindi = "मेरे प्यारे दोस्त, तुम कहाँ जा रहे हो?",
            english = "My dear friend, where are you going?",
            dialect = PahadiDialect.KUMAONI,
            translation = "अरे दगड़्या, तू कख जाणै छै?",
            phonetic = "Are dagadya, tu kakh jaanai chhai?",
            culturalNote = "'दगड़्या' का अर्थ है साथ चलने वाला सच्चा साथी। कुमाऊंनी भाषा का सबसे आत्मीय शब्द।"
        ),

        // Dogri
        PhraseItem(
            id = "dogri_1",
            category = PhraseCategory.GREETINGS,
            hindi = "नमस्ते जी! क्या हाल-चाल हैं?",
            english = "Hello! What is your condition?",
            dialect = PahadiDialect.DOGRI,
            translation = "नमस्ते जी! तुंदा के हाल ऐ?",
            phonetic = "Namaste ji! Tunda ke haal ai?",
            culturalNote = "डोगरी में 'तुंदा' का अर्थ 'आपका' होता है। शिवालिक क्षेत्र की मधुर भाषा।"
        )
    )

    val culturalStories: List<CulturalStory> = listOf(
        CulturalStory(
            id = "story_golu",
            titleHindi = "चितई गोलू देवता - न्याय के देवता",
            titleEnglish = "Golu Devta - The God of Justice",
            region = "कुमाऊं (अल्मोड़ा, चम्पावत)",
            summary = "कुमाऊं में जब किसी को न्याय नहीं मिलता, तो वह चितई गोलू मंदिर में स्टांप पेपर पर अर्ज़ी लिखकर घंटी बांधता है।",
            fullStory = "गोलू देवता कुमाऊं के सबसे पूज्य लोक देवता हैं। वे कत्यूरी राजवंश के राजकुमार गौर भैरव थे। लोककथा के अनुसार उन्होंने बाल्यकाल से ही प्रजा को त्वरित व निष्पक्ष न्याय दिलाया।\n\nआज भी अल्मोड़ा के प्रसिद्ध चितई मंदिर में हज़ारों घंटियां और भक्तों की अर्ज़ियां बंधी हैं। मनोकामना पूर्ण होने पर श्रद्धालु पीतल की घंटी चढ़ाते हैं।",
            culturalSignificance = "न्याय, निष्पक्षता और जन-विश्वास का सर्वोच्च प्रतीक।",
            associatedFestivals = "चैत्र नवरात्र, गोलू देवता जातरा, उत्तरायणी"
        ),
        CulturalStory(
            id = "story_siddu_kullu",
            titleHindi = "सिड्डू और कुल्लू दशहरा की देव-संस्कृति",
            titleEnglish = "Siddu & Living Deities of Kullu",
            region = "कुल्लू-मनाली घाटी, हिमाचल",
            summary = "ढालपुर मैदान में 300 से अधिक देवी-देवताओं का मिलन और हिमाचली पारंपरिक सिड्डू का उत्सव।",
            fullStory = "कुल्लू का दशहरा पूरे भारत में अनूठा है। यह विजयादशमी को शुरू होकर पूरे एक सप्ताह चलता है। घाटी के 300 से अधिक देवी-देवता अपने पालकियों में सवार होकर भगवान रघुनाथ जी को नमन करने आते हैं।\n\nसर्दियों में पहाड़ी घरों में पारंपरिक 'सिड्डू' बनाया जाता है, जिसमें खमीर उठे आटे में अखरोट, खसखस और मसालों की भरावन देकर भाप में पकाया जाता है और भरपूर देसी घी के साथ खाया जाता है।",
            culturalSignificance = "हिमाचली देव-परंपरा, समरसता, और शीतकालीन पोषण का संगम।",
            associatedFestivals = "कुल्लू दशहरा, माघ साजा, फागली"
        ),
        CulturalStory(
            id = "story_mahasu",
            titleHindi = "महासू देवता - हनोल व शिमला के अधिपति",
            titleEnglish = "Mahasu Devta - Ruler of Jaunsar & Shimla",
            region = "हनोल (जौनसार) व शिमला, सिरमौर",
            summary = "चार महासू भाइयों (बाशिक, पबासी, बूठिया और चालदा) का हनोल में अलौकिक न्याय व लोक-शासन।",
            fullStory = "टोंस नदी के तट पर स्थित हनोल मंदिर महासू देवता का मुख्य धाम है। किरमिर राक्षस के आतंक से रक्षा हेतु चार महासू भाई प्रकट हुए और दानव का संहार किया।\n\nमहासू देवता को इस क्षेत्र का सच्चा राजा और न्यायाधीश माना जाता है। यहाँ आज भी सदियों पुरानी काष्ठकला का भव्य मंदिर विद्यमान है।",
            culturalSignificance = "जौनसारी और हिमाचली जनजातीय संस्कृति की एकता और पारम्परिक न्याय का आधार।",
            associatedFestivals = "जागड़ा उत्सव, बिशू मेला"
        ),
        CulturalStory(
            id = "story_nanda",
            titleHindi = "नंदा देवी राजजात - हिमालय का महाकुंभ",
            titleEnglish = "Nanda Devi Raj Jat - Himalayan Pilgrimage",
            region = "गढ़वाल व कुमाऊं (नौटी से होमकुंड)",
            summary = "हर 12 वर्ष में आयोजित 280 किमी की पैदल यात्रा, जिसमें चार सींगों वाला मेढ़ा (खाडू) स्वतः मार्गदर्शक बनता है।",
            fullStory = "नंदा देवी को पहाड़ की ध्याणी (बेटी) माना जाता है। यह यात्रा बेटी नंदा को उसके ससुराल (कैलाश) विदा करने की भावुक और पावन यात्रा है।\n\nनौटी से 17,500 फीट ऊंचे होमकुंड तक चार सींगों वाला खाडू (मेढ़ा) सबसे आगे चलता है और होमकुंड में देवी के वस्त्र लेकर कैलाश की ओर विदा हो जाता है।",
            culturalSignificance = "गढ़वाल और कुमाऊं को जोड़ने वाली सांस्कृतिक डोर।",
            associatedFestivals = "नंदा अष्टमी, भाद्रपद राजजात"
        ),
        CulturalStory(
            id = "story_rajula",
            titleHindi = "राजुला-मालूशाही की अमर प्रेम गाथा",
            titleEnglish = "The Legend of Rajula and Malushahi",
            region = "कत्यूर घाटी (बैजनाथ, बागेश्वर, जोहार शौका घाटी)",
            summary = "हिमालय की सबसे प्रसिद्ध ऐतिहासिक लोकगाथा, जिसे हुड़किया बौल और जागर में गाया जाता है।",
            fullStory = "कत्यूरी राजकुमार मालूशाही और शौका व्यापारी सुनपति की रूपवती कन्या राजुला के बीच अमर प्रेम गाथा। मालूशाही ने जोगी बनकर जोहार घाटी की दुर्गम बर्फीली यात्रा की और प्रेम को प्राप्त किया।",
            culturalSignificance = "गढ़वाल और कुमाऊं के लोकगीतों का प्राण।",
            associatedFestivals = "बैजनाथ मेला, उत्तरायणी"
        ),
        CulturalStory(
            id = "story_phooldei",
            titleHindi = "फूलदेई - बसंत का बाल लोकपर्व",
            titleEnglish = "Phooldei - The Spring Flower Festival",
            region = "उत्तराखंड व हिमाचल के समस्त पहाड़",
            summary = "छोटे बच्चे सुबह-सुबह पीले फ्यूंली और बुरांश के फूल चुनकर हर घर की देहरी पर सजाते हैं।",
            fullStory = "चैत्र मास की संक्रांति पर बच्चे 'फूल देई, छम्मा देई, दैणी द्वार, भर भकार' गाते हुए हर घर की देहरी पर फूल सजाते हैं और सबके लिए मंगल कामना करते हैं।",
            culturalSignificance = "प्रकृति के प्रति सम्मान और लोकसंस्कृति के संस्कार।",
            associatedFestivals = "चैत्र संक्रांति"
        )
    )

    fun findOfflineTranslation(query: String, targetDialect: PahadiDialect): TranslationResult {
        val q = query.trim().lowercase()

        // 1. Direct phrasebook match
        val direct = curatedPhrases.find {
            it.dialect == targetDialect && (
                it.hindi.lowercase().contains(q) ||
                it.english.lowercase().contains(q) ||
                q.contains(it.hindi.lowercase().take(4))
            )
        }

        if (direct != null) {
            return TranslationResult(
                sourceText = query,
                sourceLanguage = "Hindi",
                targetDialect = targetDialect,
                translatedText = direct.translation,
                phoneticText = direct.phonetic,
                culturalContext = direct.culturalNote,
                etiquetteTip = "स्थानीय लोगों से संवाद करते समय चेहरे पर मुस्कान और 'जी' का प्रयोग करें।",
                regionalVariation = "${targetDialect.region} में प्रचलित",
                exampleUsage = direct.translation,
                isAiPowered = false
            )
        }

        // 2. Dialect-specific generation
        val (trans, phonetic, context) = when (targetDialect) {
            PahadiDialect.KANGRI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("कल मौसम बड़ा खरा (साफ) रहणा ऐ", "Kal mausam bada khara (saaf) rehana ai", "कांगड़ी में साफ मौसम को 'खरा मौसम' और बारिश को 'झड़ी' कहते हैं।")
                q.contains("कहाँ") || q.contains("where") ->
                    Triple("तुसीं कुथी चले?", "Tusin kuthi chale?", "कांगड़ी में 'कहाँ' को 'कुथी' और 'आप' को 'तुसीं' कहा जाता है।")
                q.contains("खाना") || q.contains("food") ->
                    Triple("तुसीं रोटी खाधी?", "Tusin roti khaadhi?", "कांगड़ा में अतिथियों को सबसे पहले भोजन और चाय के लिए पूछा जाता है।")
                else ->
                    Triple("तुहाड़ा के हाल-चाल ऐ जी?", "Tuhaada ke haal-chaal ai ji?", "कांगड़ी संवाद में सौम्यता और मधुरता पर विशेष बल दिया जाता है।")
            }
            PahadiDialect.MANDEALI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("काल्हे मौसम ठीक-ठाक रौहणा", "Kaalhe mausam theek-thaak rauhna", "मंडी में मौसम की बात करते समय ब्यास नदी की बयार का ध्यान रखा जाता है।")
                q.contains("कहाँ") || q.contains("where") ->
                    Triple("तुसीं कुथी चले हो?", "Tusin kuthi chale ho?", "मंडीयाली में 'कुथी' कहाँ के लिए प्रयोग होता है।")
                else ->
                    Triple("तुसीं किद्दां हो? सब ठीक-ठाक आ?", "Tusin kiddan ho? Sab theek-thaak aa?", "मंडीयाली में कुशल-क्षेम के लिए यह वाक्य सर्वप्रिय है।")
            }
            PahadiDialect.KULLUI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("काल्हे डांड्या मथि घाम (धूप) खिलणा", "Kaalhe daandya mathi ghaam khilna", "कुल्लू में पहाड़ों पर खिली धूप को 'घाम' कहते हैं।")
                else ->
                    Triple("जय देव जी! सब राजी-खुशी आ?", "Jai Dev ji! Sab raaji-khushi aa?", "कुल्लू में बातचीत की शुरुआत सदैव 'जय देव' से होती है।")
            }
            PahadiDialect.SHIMLA_PAHARI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("काल्हे मौसम साफ रौहणे री उम्मीद आ", "Kaalhe mausam saaf rauhne ree umeed aa", "शिमला में सेब के बगीचों के लिए मौसम की जानकारी अत्यंत महत्वपूर्ण होती है।")
                q.contains("कहाँ") || q.contains("where") ->
                    Triple("आपु कुथी चले?", "Aapu kuthi chale?", "शिमला पहाड़ी में आदरणीय व्यक्ति को 'आपु' कहा जाता है।")
                else ->
                    Triple("नमस्कार जी! आपु किद्दां आ?", "Namaskar ji! Aapu kiddan aa?", "महासूवी शिष्टाचार का सौम्य वाक्य।")
            }
            PahadiDialect.CHAMBEALI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("काल्हे मौसम सुहावणा रौहणा", "Kaalhe mausam suhaavana rauhna", "चंबा में सुहावने मौसम को 'सुहावणा' कहा जाता है।")
                else ->
                    Triple("नमस्ते जी! तुहाड़े के हाल न?", "Namaste ji! Tuhaade ke haal na?", "चम्बियाली में रावी घाटी की पारम्परिक मिठास है।")
            }
            PahadiDialect.SIRMAURI -> when {
                else ->
                    Triple("नमस्कार जी! के हाल-चाल बा?", "Namaskar ji! Ke haal-chaal ba?", "सिरमौर और गिरि-पार हाटी क्षेत्र का पारम्परिक शिष्टाचार।")
            }
            PahadiDialect.GARHWALI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("भोल डांड्यूं मा घाम खिललू", "Bhol daandyun ma ghaam khilalu", "गढ़वाली में कल को 'भोल' और धूप को 'घाम' बोलते हैं।")
                else ->
                    Triple("कन छौ तुम? सब भल च?", "Kan chhau tum? Sab bhal cha?", "गढ़वाली में 'भल च' कुशलता का सूचक है।")
            }
            PahadiDialect.KUMAONI -> when {
                q.contains("मौसम") || q.contains("weather") ->
                    Triple("भोल मौसम भौत नीक रौलो", "Bhol mausam bhout neek raulo", "कुमाऊंनी में 'नीक' का अर्थ बहुत अच्छा होता है।")
                else ->
                    Triple("पैलाग दगड़्या! कसि छा?", "Pailaag dagadya! Kasi chha?", "कुमाऊं में 'पैलाग' और 'दगड़्या' सबसे प्रिय शब्द हैं।")
            }
            PahadiDialect.DOGRI -> when {
                else ->
                    Triple("नमस्ते जी! तुंदा के हाल ऐ?", "Namaste ji! Tunda ke haal ai?", "डोगरी में 'तुंदा' का अर्थ 'आपका' होता है।")
            }
            PahadiDialect.JAUNSARI -> when {
                else ->
                    Triple("महासू देवता की कृपा! के हाल चाल च?", "Mahasu Devta ki kripa! Ke haal chaal cha?", "जौनसार-बावर में महासू देवता का स्मरण कर संवाद शुरू होता है।")
            }
        }

        return TranslationResult(
            sourceText = query,
            sourceLanguage = "Hindi",
            targetDialect = targetDialect,
            translatedText = trans,
            phoneticText = phonetic,
            culturalContext = context,
            etiquetteTip = "बातचीत में 'जी' और स्थानीय आदरसूचक शब्दों का प्रयोग करें।",
            regionalVariation = targetDialect.region,
            exampleUsage = trans,
            isAiPowered = false
        )
    }

    fun translatePahadiToHindi(pahadiQuery: String, sourceDialect: PahadiDialect): TranslationResult {
        val q = pahadiQuery.trim().lowercase()

        // 1. Direct reverse lookup in curated phrases
        val matchedPhrase = curatedPhrases.find {
            it.dialect == sourceDialect && (
                it.translation.lowercase().contains(q) ||
                q.contains(it.translation.lowercase().take(4)) ||
                it.phonetic.lowercase().contains(q)
            )
        } ?: curatedPhrases.find {
            it.translation.lowercase().contains(q) || q.contains(it.translation.lowercase().take(4))
        }

        if (matchedPhrase != null) {
            return TranslationResult(
                sourceText = pahadiQuery,
                sourceLanguage = "${sourceDialect.displayNameHindi} (पहाड़ी)",
                targetDialect = sourceDialect,
                translatedText = matchedPhrase.hindi,
                phoneticText = matchedPhrase.english,
                culturalContext = "पहाड़ी शब्द '${matchedPhrase.translation}' का हिंदी अर्थ: '${matchedPhrase.hindi}'। ${matchedPhrase.culturalNote}",
                etiquetteTip = "यह ${sourceDialect.displayNameHindi} का आत्मीय व पारम्परिक वाक्य है।",
                regionalVariation = "${sourceDialect.region} में बोली जाती है",
                exampleUsage = matchedPhrase.translation,
                isAiPowered = false
            )
        }

        // 2. Dialect Vocabulary Analysis & Hindi Translation
        val (hindiTranslation, explanation) = when {
            q.contains("कुथी") || q.contains("कुथू") || q.contains("कुतै") ->
                Pair("आप कहाँ जा रहे हैं?", "पहाड़ी में 'कुथी / कुथू' का अर्थ 'कहाँ' और 'चले' का अर्थ 'जा रहे हैं' होता है।")
            q.contains("हाल") || q.contains("किद्दां") || q.contains("कन छौ") || q.contains("कसि छा") ->
                Pair("आपके क्या हाल-चाल हैं? आप कैसे हैं?", "पहाड़ी में कुशल-क्षेम पूछने का पारंपरिक तरीका।")
            q.contains("पैलाग") ->
                Pair("सादर प्रणाम / चरण स्पर्श (बड़ों के प्रति आदर)", "'पैलाग' कुमाऊँनी और गढ़वाली का सबसे पवित्र व आदरणीय अभिवादन है जिसका अर्थ 'पांव लगना / चरण स्पर्श' होता है।")
            q.contains("जय देव") ->
                Pair("नमस्कार जी! ईश्वर आपका कल्याण करें।", "कुल्लू, शिमला व मंडी में 'जय देव' देवताओं के प्रति नमन और एक-दूसरे के अभिवादन के लिए बोला जाता है।")
            q.contains("खाधी") || q.contains("खाणा") || q.contains("खावा") || q.contains("रोटी") ->
                Pair("क्या आपने खाना खा लिया? / भोजन कर रहे हैं।", "पहाड़ी घरों में आने वाले हर व्यक्ति से सबसे पहले आदरपूर्वक भोजन और चाय के लिए पूछा जाता है।")
            q.contains("घाम") || q.contains("झड़ी") || q.contains("काल्हे") || q.contains("भोल") ->
                Pair("मौसम का हाल: कल धूप खिलेगी / पहाड़ में वर्षा हो रही है।", "'घाम' का अर्थ खिली हुई धूप और 'झड़ी' का अर्थ लगातार होने वाली पहाड़ी वर्षा है।")
            q.contains("भल च") || q.contains("राजी-खुशी") || q.contains("भल-भलाई") || q.contains("ठीक-ठाक") ->
                Pair("सब कुशल-मंगल है, सब बिल्कुल ठीक-ठाक है।", "पहाड़ी में 'भल' का अर्थ 'अच्छा / मंगलकारी' होता है।")
            q.contains("दाज्यू") || q.contains("भुलि") || q.contains("ध्याणी") ->
                Pair("बड़े भाई (दाज्यू) / छोटी बहन (भुलि) / पहाड़ की बेटी (ध्याणी)", "पारिवारिक रिश्तों और सम्मान के सबसे मधुर पहाड़ी शब्द।")
            q.contains("सिड्डू") || q.contains("मद्रा") || q.contains("धाम") ->
                Pair("पारंपरिक हिमाचली व्यंजन (सिड्डू / राजमा मद्रा / शाही धाम)", "हिमाचल का प्रसिद्ध पारंपरिक भाप में पका अखरोट भरा सिड्डू व धाम के व्यंजन।")
            else ->
                Pair(
                    "पहाड़ी कथन: \"$pahadiQuery\" — कुशलक्षेम और बातचीत का सौम्य वाक्य।",
                    "${sourceDialect.displayNameHindi} में बोला गया यह वाक्य पहाड़ी संस्कृति और आत्मीयता को दर्शाता है।"
                )
        }

        return TranslationResult(
            sourceText = pahadiQuery,
            sourceLanguage = "${sourceDialect.displayNameHindi} (पहाड़ी)",
            targetDialect = sourceDialect,
            translatedText = hindiTranslation,
            phoneticText = "Pahadi to Hindi Translation",
            culturalContext = explanation,
            etiquetteTip = "पहाड़ी में संवाद करते समय सौम्यता और स्थानीय आदर का ध्यान रखें।",
            regionalVariation = sourceDialect.region,
            exampleUsage = pahadiQuery,
            isAiPowered = false
        )
    }
}
