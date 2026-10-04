package com.example.ui.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.local.ChatMessageEntity
import com.example.data.local.CulturalNoteEntity
import com.example.data.local.PahadiDatabase
import com.example.data.local.TranslationEntity
import com.example.data.local.toChatMessage
import com.example.data.model.AppMode
import com.example.data.model.ChatMessage
import com.example.data.model.CulturalStory
import com.example.data.model.EmergencyContact
import com.example.data.model.LocalKnowledgeTopic
import com.example.data.model.PahadiDialect
import com.example.data.model.PhraseCategory
import com.example.data.model.PhraseItem
import com.example.data.model.ResponseDetail
import com.example.data.model.SourceLanguage
import com.example.data.model.TranslationDirection
import com.example.data.model.TranslationResult
import com.example.data.model.VoiceGender
import com.example.data.remote.GeminiClient
import com.example.data.repository.PahadiRepository
import com.example.util.PahadiSpeechRecognizerManager
import com.example.util.PahadiTtsManager
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class PahadiViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = PahadiRepository(PahadiDatabase.getInstance(application))
    private val ttsManager = PahadiTtsManager(application)
    private val speechManager = PahadiSpeechRecognizerManager(application)

    val isGeminiAvailable = GeminiClient.isApiKeyConfigured()
    val isSpeechAvailable = speechManager.isRecognitionAvailable

    // Live Speech Recognition states
    val isListening: StateFlow<Boolean> = speechManager.isListening
    val partialSpeechTranscript: StateFlow<String> = speechManager.partialTranscript
    val speechRmsDb: StateFlow<Float> = speechManager.rmsDb
    val speechError: StateFlow<String?> = speechManager.lastError

    // ----------------- Modes & Personalization -----------------
    private val _appMode = MutableStateFlow(AppMode.STANDARD)
    val appMode: StateFlow<AppMode> = _appMode.asStateFlow()

    private val _voiceGender = MutableStateFlow(VoiceGender.FEMALE)
    val voiceGender: StateFlow<VoiceGender> = _voiceGender.asStateFlow()

    private val _responseDetail = MutableStateFlow(ResponseDetail.CONCISE)
    val responseDetail: StateFlow<ResponseDetail> = _responseDetail.asStateFlow()

    private val _autoSpeakEnabled = MutableStateFlow(true)
    val autoSpeakEnabled: StateFlow<Boolean> = _autoSpeakEnabled.asStateFlow()

    private val _showPremiumDialog = MutableStateFlow(false)
    val showPremiumDialog: StateFlow<Boolean> = _showPremiumDialog.asStateFlow()

    // ----------------- Translator State -----------------
    private val _inputText = MutableStateFlow("")
    val inputText: StateFlow<String> = _inputText.asStateFlow()

    private val _sourceLang = MutableStateFlow(SourceLanguage.HINDI.displayName)
    val sourceLang: StateFlow<String> = _sourceLang.asStateFlow()

    private val _targetDialect = MutableStateFlow(PahadiDialect.KANGRI)
    val targetDialect: StateFlow<PahadiDialect> = _targetDialect.asStateFlow()

    private val _translationDirection = MutableStateFlow(TranslationDirection.HINDI_TO_PAHADI)
    val translationDirection: StateFlow<TranslationDirection> = _translationDirection.asStateFlow()

    private val _isTranslating = MutableStateFlow(false)
    val isTranslating: StateFlow<Boolean> = _isTranslating.asStateFlow()

    private val _currentTranslation = MutableStateFlow<TranslationResult?>(null)
    val currentTranslation: StateFlow<TranslationResult?> = _currentTranslation.asStateFlow()

    private val _isCurrentSaved = MutableStateFlow(false)
    val isCurrentSaved: StateFlow<Boolean> = _isCurrentSaved.asStateFlow()

    // ----------------- Room Persisted Chat (Pahadi Voice AI & Cultural Q&A) -----------------
    val chatMessages: StateFlow<List<ChatMessage>> = repository.getAllChatMessages()
        .map { entities ->
            if (entities.isEmpty()) {
                listOf(
                    ChatMessage(
                        id = "welcome_msg",
                        text = "नमस्कार! जय देव! 🙏\n\n🎤 \"बोलो, Pahadi AI समझेगा!\"\nआप हिंदी या अपनी पहाड़ी बोली (कांगड़ी, मंडीयाली, कुल्लवी, शिमला, चम्बियाली, गढ़वाली आदि) में बोलकर पूछ सकते हैं।\n\nऊपर से मोड चुनें: बुजुर्ग मित्र | छात्र | किसान | सामान्य",
                        isUser = false
                    )
                )
            } else {
                entities.map { it.toChatMessage() }
            }
        }
        .stateIn(
            viewModelScope,
            SharingStarted.WhileSubscribed(5000),
            listOf(
                ChatMessage(
                    id = "welcome_msg",
                    text = "नमस्कार! जय देव! 🙏\n\n🎤 \"बोलो, Pahadi AI समझेगा!\"\nआप हिंदी या अपनी पहाड़ी बोली (कांगड़ी, मंडीयाली, कुल्लवी, शिमला, चम्बियाली, गढ़वाली आदि) में बोलकर पूछ सकते हैं।\n\nऊपर से मोड चुनें: बुजुर्ग मित्र | छात्र | किसान | सामान्य",
                    isUser = false
                )
            )
        )

    val culturalQaSessions: StateFlow<List<ChatMessageEntity>> = repository.getCulturalQaSessions()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    private val _isChatGenerating = MutableStateFlow(false)
    val isChatGenerating: StateFlow<Boolean> = _isChatGenerating.asStateFlow()

    private val _chatInput = MutableStateFlow("")
    val chatInput: StateFlow<String> = _chatInput.asStateFlow()

    // ----------------- Static & Local Knowledge Data -----------------
    val emergencyContacts: List<EmergencyContact> = repository.getEmergencyContacts()
    val localKnowledgeTopics: List<LocalKnowledgeTopic> = repository.getLocalKnowledge()
    val stories: List<CulturalStory> = repository.getStories()

    // ----------------- Phrasebook State -----------------
    private val _phraseCategory = MutableStateFlow<PhraseCategory?>(null)
    val phraseCategory: StateFlow<PhraseCategory?> = _phraseCategory.asStateFlow()

    private val _phraseDialect = MutableStateFlow<PahadiDialect?>(null)
    val phraseDialect: StateFlow<PahadiDialect?> = _phraseDialect.asStateFlow()

    private val _phraseSearch = MutableStateFlow("")
    val phraseSearch: StateFlow<String> = _phraseSearch.asStateFlow()

    private val _filteredPhrases = MutableStateFlow<List<PhraseItem>>(emptyList())
    val filteredPhrases: StateFlow<List<PhraseItem>> = _filteredPhrases.asStateFlow()

    // ----------------- Stories State -----------------
    private val _selectedStory = MutableStateFlow<CulturalStory?>(null)
    val selectedStory: StateFlow<CulturalStory?> = _selectedStory.asStateFlow()

    // ----------------- Room Persisted State -----------------
    val historyList: StateFlow<List<TranslationEntity>> = repository.getAllHistory()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val favoritesList: StateFlow<List<TranslationEntity>> = repository.getFavorites()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val notesList: StateFlow<List<CulturalNoteEntity>> = repository.getAllNotes()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    init {
        updatePhrasebook()
        viewModelScope.launch {
            repository.ensureDefaultWelcomeMessage()
        }
    }

    // ----------------- Personalization Actions -----------------
    fun setAppMode(mode: AppMode) {
        _appMode.value = mode
        val modeAnnouncement = when (mode) {
            AppMode.ELDER -> "बुजुर्ग मित्र मोड सक्रिय हो गया है। बड़े अक्षर और आवाज सहायता उपलब्ध है।"
            AppMode.STUDENT -> "छात्र सहायक मोड सक्रिय है। पाठ सारांश, अनुवाद और परीक्षा नोट्स पूछें।"
            AppMode.FARMER -> "किसान मित्र मोड सक्रिय है। सेब बागवानी, मौसम और योजनाओं की जानकारी लें।"
            AppMode.STANDARD -> "दैनिक सहायक मोड सक्रिय है।"
        }
        val systemNote = ChatMessage(
            id = System.currentTimeMillis().toString(),
            text = "⚡ $modeAnnouncement",
            isUser = false,
            appMode = mode
        )
        viewModelScope.launch {
            repository.saveChatMessage(systemNote)
        }
        if (_autoSpeakEnabled.value) {
            speakText(modeAnnouncement)
        }
    }

    fun toggleVoiceGender() {
        _voiceGender.value = if (_voiceGender.value == VoiceGender.FEMALE) VoiceGender.MALE else VoiceGender.FEMALE
    }

    fun toggleResponseDetail() {
        _responseDetail.value = if (_responseDetail.value == ResponseDetail.CONCISE) ResponseDetail.DETAILED else ResponseDetail.CONCISE
    }

    fun toggleAutoSpeak() {
        _autoSpeakEnabled.value = !_autoSpeakEnabled.value
    }

    fun setPremiumDialog(show: Boolean) {
        _showPremiumDialog.value = show
    }

    // ----------------- Translator Actions -----------------
    fun setInputText(text: String) {
        _inputText.value = text
    }

    fun setTargetDialect(dialect: PahadiDialect) {
        _targetDialect.value = dialect
        if (_inputText.value.isNotBlank()) {
            translateNow()
        }
    }

    fun setSourceLang(lang: String) {
        _sourceLang.value = lang
    }

    fun setTranslationDirection(direction: TranslationDirection) {
        _translationDirection.value = direction
        if (direction == TranslationDirection.PAHADI_TO_HINDI) {
            _sourceLang.value = _targetDialect.value.displayNameHindi
        } else {
            _sourceLang.value = SourceLanguage.HINDI.displayName
        }
        if (_inputText.value.isNotBlank()) {
            translateNow()
        }
    }

    fun swapLanguages() {
        val nextDirection = if (_translationDirection.value == TranslationDirection.HINDI_TO_PAHADI) {
            TranslationDirection.PAHADI_TO_HINDI
        } else {
            TranslationDirection.HINDI_TO_PAHADI
        }
        val currentTrans = _currentTranslation.value?.translatedText
        _translationDirection.value = nextDirection

        if (nextDirection == TranslationDirection.PAHADI_TO_HINDI) {
            _sourceLang.value = _targetDialect.value.displayNameHindi
        } else {
            _sourceLang.value = SourceLanguage.HINDI.displayName
        }

        if (!currentTrans.isNullOrBlank()) {
            _inputText.value = currentTrans
            translateNow()
        }
    }

    fun translateNow() {
        val text = _inputText.value.trim()
        if (text.isBlank()) return

        viewModelScope.launch {
            _isTranslating.value = true
            _isCurrentSaved.value = false
            try {
                val isPahadiToHindi = _translationDirection.value == TranslationDirection.PAHADI_TO_HINDI
                val result = repository.translate(
                    sourceText = text,
                    sourceLang = if (isPahadiToHindi) "${_targetDialect.value.displayNameHindi} (पहाड़ी)" else _sourceLang.value,
                    targetDialect = _targetDialect.value,
                    isPahadiToHindi = isPahadiToHindi
                )
                _currentTranslation.value = result

                if (_autoSpeakEnabled.value) {
                    speakText(result.translatedText)
                }
            } catch (e: Exception) {
                // Handled gracefully in repo
            } finally {
                _isTranslating.value = false
            }
        }
    }

    fun toggleCurrentFavorite() {
        val trans = _currentTranslation.value ?: return
        val newFav = !_isCurrentSaved.value
        _isCurrentSaved.value = newFav
        viewModelScope.launch {
            val recent = historyList.value.firstOrNull {
                it.sourceText == trans.sourceText && it.targetDialectCode == trans.targetDialect.code
            }
            if (recent != null) {
                repository.setFavorite(recent.id, newFav)
            }
        }
    }

    fun toggleItemFavorite(id: Long, currentFav: Boolean) {
        viewModelScope.launch { repository.setFavorite(id, !currentFav) }
    }

    fun deleteItem(id: Long) {
        viewModelScope.launch { repository.deleteTranslation(id) }
    }

    fun clearAllHistory() {
        viewModelScope.launch { repository.clearHistory() }
    }

    // ----------------- Voice & Chat Actions -----------------
    fun setChatInput(text: String) {
        _chatInput.value = text
    }

    fun sendChatMessage(text: String? = null) {
        val query = (text ?: _chatInput.value).trim()
        if (query.isBlank()) return

        val userMsg = ChatMessage(
            id = System.currentTimeMillis().toString(),
            text = query,
            isUser = true,
            appMode = _appMode.value,
            relatedDialect = _targetDialect.value
        )
        _chatInput.value = ""

        viewModelScope.launch {
            repository.saveChatMessage(
                message = userMsg,
                sessionId = "cultural_qa_session",
                isCulturalQa = isCulturalQuestion(query)
            )
            _isChatGenerating.value = true
            try {
                val currentHistory = chatMessages.value
                val reply = repository.askPahadiAi(
                    history = currentHistory,
                    question = query,
                    mode = _appMode.value,
                    dialect = _targetDialect.value,
                    detail = _responseDetail.value
                )
                val aiMsg = ChatMessage(
                    id = (System.currentTimeMillis() + 1).toString(),
                    text = reply,
                    isUser = false,
                    appMode = _appMode.value,
                    relatedDialect = _targetDialect.value
                )
                repository.saveChatMessage(
                    message = aiMsg,
                    sessionId = "cultural_qa_session",
                    isCulturalQa = isCulturalQuestion(query)
                )

                if (_autoSpeakEnabled.value) {
                    speakText(reply)
                }
            } finally {
                _isChatGenerating.value = false
            }
        }
    }

    fun clearChatHistory() {
        viewModelScope.launch {
            repository.clearChatHistory()
            repository.ensureDefaultWelcomeMessage()
        }
    }

    private fun isCulturalQuestion(text: String): Boolean {
        val lower = text.lowercase()
        val keywords = listOf(
            "संस्कृति", "त्योहार", "मेला", "मंदिर", "देवता", "गीत", "इतिहास", "पहाड़",
            "परंपरा", "धाम", "सिड्डू", "नाटी", "मिंजर", "दशहरा", "जातर", "फूलदेई",
            "कांगड़ा", "मंडी", "कुल्लू", "चंबा", "गढ़वाल", "कुमाऊं", "culture", "festival", "temple"
        )
        return keywords.any { lower.contains(it) }
    }

    // ----------------- Phrasebook Actions -----------------
    fun setPhraseCategory(cat: PhraseCategory?) {
        _phraseCategory.value = cat
        updatePhrasebook()
    }

    fun setPhraseDialect(dialect: PahadiDialect?) {
        _phraseDialect.value = dialect
        updatePhrasebook()
    }

    fun setPhraseSearch(query: String) {
        _phraseSearch.value = query
        updatePhrasebook()
    }

    private fun updatePhrasebook() {
        _filteredPhrases.value = repository.getFilteredPhrases(
            dialect = _phraseDialect.value,
            category = _phraseCategory.value,
            searchQuery = _phraseSearch.value
        )
    }

    // ----------------- Stories Actions -----------------
    fun selectStory(story: CulturalStory?) {
        _selectedStory.value = story
    }

    // ----------------- Notes Actions -----------------
    fun addNote(title: String, dialect: String, content: String) {
        viewModelScope.launch { repository.insertNote(title, dialect, content) }
    }

    fun deleteNote(id: Long) {
        viewModelScope.launch { repository.deleteNote(id) }
    }

    // ----------------- Audio TTS -----------------
    fun speakText(text: String) {
        ttsManager.speak(
            text = text,
            gender = _voiceGender.value,
            isElderMode = _appMode.value == AppMode.ELDER
        )
    }

    fun stopSpeaking() {
        ttsManager.stop()
    }

    // ----------------- Speech Recognition -----------------
    fun startSpeechRecognition(langCode: String = "hi-IN", onFinalResult: (String) -> Unit) {
        stopSpeaking()
        speechManager.startListening(langCode, onFinalResult)
    }

    fun stopSpeechRecognition() {
        speechManager.stopListening()
    }

    fun cancelSpeechRecognition() {
        speechManager.cancel()
    }

    override fun onCleared() {
        super.onCleared()
        speechManager.destroy()
        ttsManager.shutdown()
    }
}
