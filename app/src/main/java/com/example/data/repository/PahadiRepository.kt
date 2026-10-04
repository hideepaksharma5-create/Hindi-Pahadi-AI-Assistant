package com.example.data.repository

import com.example.data.dictionary.PahadiOfflineEngine
import com.example.data.local.CulturalNoteEntity
import com.example.data.local.PahadiDatabase
import com.example.data.local.TranslationEntity
import com.example.data.model.AppMode
import com.example.data.model.ChatMessage
import com.example.data.model.CulturalStory
import com.example.data.model.EmergencyContact
import com.example.data.model.LocalKnowledgeTopic
import com.example.data.model.PahadiDialect
import com.example.data.model.PhraseCategory
import com.example.data.model.PhraseItem
import com.example.data.model.ResponseDetail
import com.example.data.model.TranslationResult
import com.example.data.remote.GeminiClient
import kotlinx.coroutines.flow.Flow

class PahadiRepository(private val database: PahadiDatabase) {

    private val dao = database.translationDao()

    fun getAllHistory(): Flow<List<TranslationEntity>> = dao.getAllHistory()
    fun getFavorites(): Flow<List<TranslationEntity>> = dao.getFavorites()
    fun getAllNotes(): Flow<List<CulturalNoteEntity>> = dao.getAllNotes()

    suspend fun insertNote(title: String, dialect: String, content: String) {
        dao.insertNote(CulturalNoteEntity(title = title, dialect = dialect, content = content))
    }

    suspend fun deleteNote(id: Long) = dao.deleteNote(id)
    suspend fun setFavorite(id: Long, isFavorite: Boolean) = dao.setFavorite(id, isFavorite)
    suspend fun deleteTranslation(id: Long) = dao.deleteById(id)
    suspend fun clearHistory() = dao.clearHistoryOnly()

    suspend fun translate(
        sourceText: String,
        sourceLang: String,
        targetDialect: PahadiDialect
    ): TranslationResult {
        val result = if (GeminiClient.isApiKeyConfigured()) {
            val apiResult = GeminiClient.translateWithCulturalContext(sourceText, sourceLang, targetDialect)
            apiResult.getOrElse { PahadiOfflineEngine.findOfflineTranslation(sourceText, targetDialect) }
        } else {
            PahadiOfflineEngine.findOfflineTranslation(sourceText, targetDialect)
        }

        dao.insertTranslation(
            TranslationEntity(
                sourceText = result.sourceText,
                sourceLanguage = result.sourceLanguage,
                targetDialectCode = result.targetDialect.code,
                targetDialectName = result.targetDialect.displayNameHindi,
                translatedText = result.translatedText,
                phoneticText = result.phoneticText,
                culturalContext = result.culturalContext,
                etiquetteTip = result.etiquetteTip,
                isFavorite = false
            )
        )
        return result
    }

    suspend fun askPahadiAi(
        history: List<ChatMessage>,
        question: String,
        mode: AppMode,
        dialect: PahadiDialect,
        detail: ResponseDetail
    ): String {
        if (GeminiClient.isApiKeyConfigured()) {
            val geminiResult = GeminiClient.chatWithPahadiAi(history, question, mode, dialect, detail)
            geminiResult.onSuccess { return it }
        }

        // Offline knowledge engine fallback tailored to active mode
        val q = question.lowercase()

        // 1. Check local knowledge topics first
        val matchingTopic = PahadiOfflineEngine.localKnowledgeTopics.find {
            q.contains(it.title.lowercase()) ||
            it.title.lowercase().contains(q) ||
            (q.contains("hrtc") && it.category == "HRTC") ||
            (q.contains("बस") && it.category == "HRTC") ||
            (q.contains("सेब") && it.category == "Agriculture") ||
            (q.contains("हिमकेयर") && it.id == "himcare_scheme") ||
            (q.contains("धाम") && it.id == "himachal_dhaam") ||
            (q.contains("सहारा") && it.id == "sahara_yojna")
        }

        if (matchingTopic != null) {
            return "${matchingTopic.title}\n\n${matchingTopic.summary}\n\n${matchingTopic.details}"
        }

        // 2. Mode specific responses
        return when (mode) {
            AppMode.ELDER -> {
                when {
                    q.contains("दवा") || q.contains("तबियत") || q.contains("स्वास्थ्य") ->
                        "नमस्कार जी! 🙏 अपनी सेहत का पूरा ध्यान रखें। समय पर गरम पानी पिएं और दवा लें। किसी भी जरूरत पर 108 पर मुफ्त एम्बुलेंस बुलाई जा सकती है। हमेशा खुश और स्वस्थ रहें!"
                    q.contains("मौसम") || q.contains("weather") ->
                        "पहाड़ों पर मौसम ठंडा है जी! गर्म कपड़े पहनकर रहें और सुबह धूप जरूर सेंकें। कल मौसम सामान्य रहने का अनुमान है।"
                    else ->
                        "जय देव जी! पैलाग! 🙏 मैं आपका पहाड़ी साथी हूँ। आप बिना लिखे बस बोलकर मुझसे कुछ भी पूछ सकते हैं—गाँव की बातें, भजन, मौसम या मदद!"
                }
            }
            AppMode.STUDENT -> {
                when {
                    q.contains("प्रकाश संश्लेषण") || q.contains("photosynthesis") ->
                        "📚 प्रकाश संश्लेषण (Photosynthesis):\n\nपौधे सूर्य के प्रकाश, जल (H2O) और कार्बन डाइऑक्साइड (CO2) की मदद से पत्तियों में मौजूद क्लोरोफिल द्वारा अपना भोजन (ग्लूकोज) बनाते हैं और ऑक्सीजन गैस छोड़ते हैं।\n\nसमीकरण: 6CO2 + 6H2O + धूप → C6H12O6 + 6O2"
                    q.contains("हिमाचल") || q.contains("गठन") || q.contains("gk") ->
                        "📚 हिमाचल प्रदेश सामान्य ज्ञान:\n• गठन: 15 अप्रैल 1948 (मुख्य आयुक्त प्रांत)\n• पूर्ण राज्यत्व: 25 जनवरी 1971 (18वां राज्य)\n• राजधानी: शिमला (ग्रीष्मकालीन), धर्मशाला (शीतकालीन)\n• जिले: 12 जिले\n• सबसे ऊंची चोटी: शीला (7,025 मीटर, किन्नौर)"
                    else ->
                        "नमस्ते विद्यार्थी मित्र! 📚 मैं आपके अध्ययन, सारांश बनाने, अंग्रेज़ी-हिंदी अनुवाद और परीक्षा की तैयारी में सहायता के लिए तैयार हूँ। अपना प्रश्न पूछें!"
                }
            }
            AppMode.FARMER -> {
                when {
                    q.contains("स्कैब") || q.contains("रोग") || q.contains("scab") ->
                        "🧑‍🌾 सेब स्कैब (Apple Scab) प्रबंधन:\n1. सर्दियों में गिरी पत्तियों को इकट्ठा कर नष्ट करें या 5% यूरिया का छिड़काव करें ताकि फंगस खत्म हो जाए।\n2. कलिका प्रस्फुटन (Silver Tip stage) पर कैप्टन या मैन्कोजेब का छिड़काव करें।\n3. बगीचे में वायु संचार हेतु उचित प्रूनिंग (कटाई-छंटाई) अवश्य करें।"
                    q.contains("खाद") || q.contains("जीवामृत") || q.contains("प्राकृतिक") ->
                        "🧑‍🌾 जीवामृत बनाने की विधि (सुभाष पालेकर विधि):\n• 200 लीटर पानी + 10 किग्रा देसी गाय का गोबर + 5-10 लीटर गोमूत्र + 1 किग्रा गुड़ + 1 किग्रा बेसन + मुट्ठी भर उपजाऊ मिट्टी।\n• 48 घंटे छांव में रखें और दिन में दो बार हिलाएं। सिंचाई के साथ पौधों को दें।"
                    else ->
                        "जय किसान! 🍏 मैं सेब बागवानी, मौसम पूर्वानुमान, एंटी-हेल नेट सब्सिडी और प्राकृतिक खेती की जानकारी के लिए आपका सहायक हूँ।"
                }
            }
            AppMode.STANDARD -> {
                when {
                    q.contains("मौसम") -> "कल पहाड़ों पर मौसम सुहावना रहेगा। सुबह धूप खिलेगी और शाम को हल्की ठंडी बयार चलेगी।"
                    q.contains("hrtc") || q.contains("बस") -> "एचआरटीसी बस पूछताछ के लिए शिमला हेल्पलाइन 0177-2803017 पर कॉल कर सकते हैं, या hrtchp.com पर ऑनलाइन सीट बुक कर सकते हैं।"
                    else -> "नमस्कार! मैं 'पहाड़ी AI' हूँ। आप मुझसे दैनिक सहायता, अनुवाद, एचआरटीसी बस रूट, सरकारी योजनाएं, लोक परंपराएं या सामान्य ज्ञान कुछ भी पूछ सकते हैं।"
                }
            }
        }
    }

    fun getFilteredPhrases(
        dialect: PahadiDialect?,
        category: PhraseCategory?,
        searchQuery: String
    ): List<PhraseItem> {
        return PahadiOfflineEngine.curatedPhrases.filter { item ->
            val matchesDialect = dialect == null || item.dialect == dialect
            val matchesCategory = category == null || item.category == category
            val matchesSearch = searchQuery.isBlank() ||
                    item.hindi.contains(searchQuery, ignoreCase = true) ||
                    item.english.contains(searchQuery, ignoreCase = true) ||
                    item.translation.contains(searchQuery, ignoreCase = true) ||
                    item.phonetic.contains(searchQuery, ignoreCase = true)
            matchesDialect && matchesCategory && matchesSearch
        }
    }

    fun getStories(): List<CulturalStory> = PahadiOfflineEngine.culturalStories
    fun getEmergencyContacts(): List<EmergencyContact> = PahadiOfflineEngine.emergencyContacts
    fun getLocalKnowledge(): List<LocalKnowledgeTopic> = PahadiOfflineEngine.localKnowledgeTopics
}
