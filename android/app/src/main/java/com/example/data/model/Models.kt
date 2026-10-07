package com.example.data.model

enum class PahadiDialect(
    val code: String,
    val displayNameHindi: String,
    val displayNameEnglish: String,
    val region: String,
    val state: String,
    val description: String
) {
    KANGRI(
        code = "kangri",
        displayNameHindi = "कांगड़ी (Kangri)",
        displayNameEnglish = "Kangri",
        region = "कांगड़ा घाटी, हमीरपुर, ऊना",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "कांगड़ा घाटी की मिठास भरी पश्चिमी पहाड़ी भाषा। 'मिंजो-तिंजो' और 'कुथी चले' इसके प्रमुख पहचान हैं।"
    ),
    MANDEALI(
        code = "mandeali",
        displayNameHindi = "मंडीयाली (Mandeali)",
        displayNameEnglish = "Mandeali",
        region = "मंडी, सुंदरनगर, छोटी काशी",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "ब्यास तट पर स्थित छोटी काशी मंडी की समृद्ध बोली। विशिष्ट स्वरलहरी और 'भल-भलाई' इसका स्वभाव है।"
    ),
    KULLUI(
        code = "kullui",
        displayNameHindi = "कुल्लवी (Kullui)",
        displayNameEnglish = "Kullui",
        region = "कुल्लू घाटी, मनाली, बंजार",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "देवभूमि कुल्लू की भाषा। रघुनाथ जी व हडिम्बा देवी की कृपा से जुड़ी, 'जय देव' से हर संवाद का आरंभ होता है।"
    ),
    SHIMLA_PAHARI(
        code = "shimla_pahari",
        displayNameHindi = "शिमला / महासूवी (Shimla Pahari)",
        displayNameEnglish = "Shimla Pahari / Mahasuvi",
        region = "शिमला, ठियोग, कोटखाई, रोहड़ू, सोलन",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "सेब की बेल्ट और महासू देवता की पावन घाटी की पहाड़ी। 'आपु' और 'के हाल च' इसके आत्मीय मुहावरे हैं।"
    ),
    CHAMBEALI(
        code = "chambeali",
        displayNameHindi = "चम्बियाली (Chambeali)",
        displayNameEnglish = "Chambeali",
        region = "चंबा, रावी घाटी, भरमौर",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "रावी नदी की गोद में बसे ऐतिहासिक चंबा की मधुर बोली। मिंजर मेला और मणिमहेश यात्रा से जुड़ी समृद्ध भाषा।"
    ),
    SIRMAURI(
        code = "sirmauri",
        displayNameHindi = "सिरमौरी (Sirmauri)",
        displayNameEnglish = "Sirmauri / Giripar",
        region = "नाहन, रेणुका जी, गिरि-पार (हाटी क्षेत्र)",
        state = "हिमाचल प्रदेश (Himachal Pradesh)",
        description = "रेणुका जी और गिरि-पार के हाटी समुदाय की प्राचीन पारम्परिक बोली। बूढ़ी दीवाली और लोकगीतों की धरोहर।"
    ),
    GARHWALI(
        code = "garhwali",
        displayNameHindi = "गढ़वाली (Garhwali)",
        displayNameEnglish = "Garhwali",
        region = "अलकनंदा व भागीरथी घाटी (श्रीनगर, पौड़ी, टिहरी, चमोली)",
        state = "उत्तराखंड (Uttarakhand)",
        description = "गढ़वाल मंडल की प्रमुख भाषा। 'पैलाग', 'भुलि', 'दाजु' और 'कख जाणा' इसके विशिष्ट शब्द हैं।"
    ),
    KUMAONI(
        code = "kumaoni",
        displayNameHindi = "कुमाऊँनी (Kumaoni)",
        displayNameEnglish = "Kumaoni",
        region = "कत्यूर व मानसखंड (अल्मोड़ा, नैनीताल, पिथौरागढ़)",
        state = "उत्तराखंड (Uttarakhand)",
        description = "कुमाऊं मंडल की मिठास। 'पैलाग', 'भल छौ' और 'मेरो प्यारो दगड़्या' इसके प्रसिद्ध रूप हैं।"
    ),
    DOGRI(
        code = "dogri",
        displayNameHindi = "डोगरी (Dogri)",
        displayNameEnglish = "Dogri",
        region = "जम्मू व हिमाचल शिवालिक बेल्ट",
        state = "जम्मू / हिमाचल (Dogra Belt)",
        description = "संविधान की 8वीं अनुसूची में शामिल मधुर डोगरी भाषा।"
    ),
    JAUNSARI(
        code = "jaunsari",
        displayNameHindi = "जौनसारी (Jaunsari)",
        displayNameEnglish = "Jaunsari",
        region = "जौनसार-बावर (चकराता, देहरादून पहाड़ियां)",
        state = "उत्तराखंड (Uttarakhand)",
        description = "महासू देवता के उपासक हाटी-जौनसार क्षेत्र की विशिष्ट सांस्कृतिक बोली।"
    );

    companion object {
        fun fromCode(code: String): PahadiDialect =
            entries.find { it.code.equals(code, ignoreCase = true) } ?: KANGRI
    }
}

enum class SourceLanguage(val code: String, val displayName: String) {
    HINDI("hi", "मानक हिंदी (Hindi)"),
    ENGLISH("en", "English"),
    PAHADI("pahadi", "पहाड़ी (Pahadi)"),
    KANGRI("kangri", "कांगड़ी (Kangri)"),
    MANDEALI("mandeali", "मंडीयाली (Mandeali)"),
    KULLUI("kullui", "कुल्लवी (Kullui)"),
    SHIMLA("shimla", "शिमला पहाड़ी (Shimla)"),
    GARHWALI("garhwali", "गढ़वाली (Garhwali)"),
    KUMAONI("kumaoni", "कुमाऊँनी (Kumaoni)")
}

enum class TranslationDirection(
    val titleHindi: String,
    val titleEnglish: String,
    val sourceLabel: String,
    val targetLabel: String
) {
    HINDI_TO_PAHADI(
        titleHindi = "हिंदी ➔ पहाड़ी",
        titleEnglish = "Hindi to Pahadi",
        sourceLabel = "हिंदी / English",
        targetLabel = "पहाड़ी बोली"
    ),
    PAHADI_TO_HINDI(
        titleHindi = "पहाड़ी ➔ हिंदी",
        titleEnglish = "Pahadi to Hindi",
        sourceLabel = "पहाड़ी बोली",
        targetLabel = "मानक हिंदी (Hindi)"
    )
}

enum class AppMode(
    val titleHindi: String,
    val titleEnglish: String,
    val description: String,
    val iconName: String
) {
    STANDARD(
        titleHindi = "दैनिक सहायक",
        titleEnglish = "All-Round AI",
        description = "दैनिक प्रश्नोत्तर, अनुवाद, संदेश लेखन, गणना और सामान्य ज्ञान",
        iconName = "smart_toy"
    ),
    ELDER(
        titleHindi = "बुजुर्ग मित्र (Voice-First)",
        titleEnglish = "Elder Friendly",
        description = "बड़े अक्षर, विशाल बटन, 'बोलो और सुनो' बिना टाइप किए सहज आवाज में बात करें",
        iconName = "elderly"
    ),
    STUDENT(
        titleHindi = "छात्र सहायक",
        titleEnglish = "Student Mode",
        description = "पाठ समझना, प्रश्न बनाना, सारांश, अंग्रेज़ी-हिंदी अनुवाद, परीक्षा तैयारी",
        iconName = "school"
    ),
    FARMER(
        titleHindi = "किसान मित्र (कृषि व सेब)",
        titleEnglish = "Farmer & Orchard",
        description = "सेब बागवानी, मौसम सलाह, सरकारी योजनाएं, खाद व प्राकृतिक खेती",
        iconName = "agriculture"
    )
}

enum class VoiceGender {
    FEMALE, MALE
}

enum class ResponseDetail {
    CONCISE, DETAILED
}

data class EmergencyContact(
    val titleHindi: String,
    val titleEnglish: String,
    val number: String,
    val description: String,
    val iconName: String
)

data class LocalKnowledgeTopic(
    val id: String,
    val title: String,
    val category: String, // HRTC, Tourism, Schemes, Agriculture, Tradition
    val summary: String,
    val details: String,
    val contactOrLink: String = ""
)

data class TranslationResult(
    val sourceText: String,
    val sourceLanguage: String,
    val targetDialect: PahadiDialect,
    val translatedText: String,
    val phoneticText: String,
    val culturalContext: String,
    val etiquetteTip: String = "",
    val regionalVariation: String = "",
    val exampleUsage: String = "",
    val isAiPowered: Boolean = true
)

data class PhraseItem(
    val id: String,
    val category: PhraseCategory,
    val hindi: String,
    val english: String,
    val dialect: PahadiDialect,
    val translation: String,
    val phonetic: String,
    val culturalNote: String
)

enum class PhraseCategory(val titleHindi: String, val titleEnglish: String) {
    GREETINGS("नमस्ते व अभिवादन", "Greetings"),
    RELATIONS("पारिवारिक रिश्ते व आदर", "Family & Honorifics"),
    TRAVEL("मार्ग व पहाड़ी दिशाएं", "Travel & Directions"),
    FOOD("पहाड़ी खान-पान", "Food & Dining"),
    MARKET("बाज़ार व मोल-भाव", "Market & Shopping"),
    WEATHER("मौसम व पहाड़", "Weather & Mountains"),
    FARMING("खेती व बागवानी", "Farming & Apples"),
    PROVERBS("पहाड़ी आखाण (कहावतें)", "Folk Proverbs")
}

data class CulturalStory(
    val id: String,
    val titleHindi: String,
    val titleEnglish: String,
    val region: String,
    val summary: String,
    val fullStory: String,
    val culturalSignificance: String,
    val associatedFestivals: String
)

data class ChatMessage(
    val id: String,
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val appMode: AppMode = AppMode.STANDARD,
    val relatedDialect: PahadiDialect? = null
)
