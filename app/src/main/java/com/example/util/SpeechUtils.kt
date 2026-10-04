package com.example.util

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import com.example.data.model.VoiceGender
import java.util.Locale

class PahadiTtsManager(context: Context) : TextToSpeech.OnInitListener {
    private val tts: TextToSpeech = TextToSpeech(context.applicationContext, this)
    private var isReady = false

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val hindiLocale = Locale.Builder().setLanguage("hi").setRegion("IN").build()
            val result = tts.setLanguage(hindiLocale)
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                tts.language = Locale.ENGLISH
            }
            tts.setPitch(1.0f)
            tts.setSpeechRate(0.92f)
            isReady = true
        } else {
            Log.e("PahadiTtsManager", "TTS init failed: $status")
        }
    }

    fun applyVoiceSettings(gender: VoiceGender, isElderMode: Boolean) {
        if (!isReady) return
        val pitch = if (gender == VoiceGender.FEMALE) 1.15f else 0.82f
        val rate = if (isElderMode) 0.80f else 0.95f
        tts.setPitch(pitch)
        tts.setSpeechRate(rate)
    }

    fun speak(text: String, gender: VoiceGender = VoiceGender.FEMALE, isElderMode: Boolean = false) {
        if (!isReady || text.isBlank()) return
        applyVoiceSettings(gender, isElderMode)
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, "PahadiTtsUtterance")
    }

    fun stop() {
        if (isReady) {
            tts.stop()
        }
    }

    fun shutdown() {
        try {
            tts.stop()
            tts.shutdown()
        } catch (e: Exception) {
            Log.e("PahadiTtsManager", "TTS shutdown error", e)
        }
    }
}
