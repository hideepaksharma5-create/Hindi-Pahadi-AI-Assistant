package com.example.util

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.util.Log
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class PahadiSpeechRecognizerManager(private val context: Context) : RecognitionListener {

    private val mainHandler = Handler(Looper.getMainLooper())
    private var speechRecognizer: SpeechRecognizer? = null
    private var onFinalResult: ((String) -> Unit)? = null

    private val _isListening = MutableStateFlow(false)
    val isListening: StateFlow<Boolean> = _isListening.asStateFlow()

    private val _partialTranscript = MutableStateFlow("")
    val partialTranscript: StateFlow<String> = _partialTranscript.asStateFlow()

    private val _rmsDb = MutableStateFlow(0f)
    val rmsDb: StateFlow<Float> = _rmsDb.asStateFlow()

    private val _lastError = MutableStateFlow<String?>(null)
    val lastError: StateFlow<String?> = _lastError.asStateFlow()

    val isRecognitionAvailable: Boolean
        get() = SpeechRecognizer.isRecognitionAvailable(context)

    fun startListening(
        languageCode: String = "hi-IN",
        onResult: (String) -> Unit
    ) {
        mainHandler.post {
            try {
                _lastError.value = null
                _partialTranscript.value = ""
                _rmsDb.value = 0f
                onFinalResult = onResult

                if (speechRecognizer == null) {
                    speechRecognizer = SpeechRecognizer.createSpeechRecognizer(context.applicationContext).apply {
                        setRecognitionListener(this@PahadiSpeechRecognizerManager)
                    }
                }

                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, languageCode)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, languageCode)
                    putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, false)
                    putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, true)
                    putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 3)
                    putExtra(RecognizerIntent.EXTRA_CALLING_PACKAGE, context.packageName)
                }

                speechRecognizer?.startListening(intent)
                _isListening.value = true
            } catch (e: Exception) {
                Log.e("PahadiSpeechRecognizer", "Error starting listening", e)
                _isListening.value = false
                _lastError.value = "माइक्रोफोन शुरू करने में समस्या आई: ${e.localizedMessage}"
            }
        }
    }

    fun stopListening() {
        mainHandler.post {
            try {
                speechRecognizer?.stopListening()
            } catch (e: Exception) {
                Log.e("PahadiSpeechRecognizer", "Error stopping listening", e)
            }
            _isListening.value = false
        }
    }

    fun cancel() {
        mainHandler.post {
            try {
                speechRecognizer?.cancel()
            } catch (e: Exception) {
                Log.e("PahadiSpeechRecognizer", "Error cancelling listening", e)
            }
            _isListening.value = false
            _partialTranscript.value = ""
            _rmsDb.value = 0f
        }
    }

    fun destroy() {
        mainHandler.post {
            try {
                speechRecognizer?.destroy()
                speechRecognizer = null
            } catch (e: Exception) {
                Log.e("PahadiSpeechRecognizer", "Error destroying speech recognizer", e)
            }
            _isListening.value = false
        }
    }

    // --- RecognitionListener Callbacks ---

    override fun onReadyForSpeech(params: Bundle?) {
        _isListening.value = true
        _lastError.value = null
    }

    override fun onBeginningOfSpeech() {
        _isListening.value = true
    }

    override fun onRmsChanged(rmsdB: Float) {
        _rmsDb.value = rmsdB.coerceIn(0f, 10f)
    }

    override fun onBufferReceived(buffer: ByteArray?) {}

    override fun onEndOfSpeech() {
        _isListening.value = false
        _rmsDb.value = 0f
    }

    override fun onError(errorCode: Int) {
        _isListening.value = false
        _rmsDb.value = 0f

        val errorDesc = when (errorCode) {
            SpeechRecognizer.ERROR_AUDIO -> "ऑडियो रिकॉर्डिंग में त्रुटि"
            SpeechRecognizer.ERROR_CLIENT -> "क्लाइंट त्रुटि"
            SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "माइक्रोफोन अनुमति नहीं है"
            SpeechRecognizer.ERROR_NETWORK -> "नेटवर्क कनेक्शन की आवश्यकता है"
            SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "नेटवर्क टाइमआउट"
            SpeechRecognizer.ERROR_NO_MATCH -> "आवाज़ स्पष्ट सुनाई नहीं दी, कृपया पुनः बोलें"
            SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "स्पीच सेवा व्यस्त है"
            SpeechRecognizer.ERROR_SERVER -> "सर्वर त्रुटि"
            SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "कोई आवाज़ नहीं मिली"
            else -> "त्रुटि कोड: $errorCode"
        }
        _lastError.value = errorDesc
        Log.w("PahadiSpeechRecognizer", "Speech error ($errorCode): $errorDesc")
    }

    override fun onResults(results: Bundle?) {
        _isListening.value = false
        _rmsDb.value = 0f
        val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
        val text = matches?.firstOrNull()?.trim()
        if (!text.isNullOrBlank()) {
            _partialTranscript.value = text
            onFinalResult?.invoke(text)
        }
    }

    override fun onPartialResults(partialResults: Bundle?) {
        val matches = partialResults?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
        val partial = matches?.firstOrNull()?.trim()
        if (!partial.isNullOrBlank()) {
            _partialTranscript.value = partial
        }
    }

    override fun onEvent(eventType: Int, params: Bundle?) {}
}
