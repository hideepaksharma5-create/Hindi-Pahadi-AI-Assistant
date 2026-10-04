package com.example.data.remote

import android.util.Log
import com.example.BuildConfig
import com.example.data.model.AppMode
import com.example.data.model.ChatMessage
import com.example.data.model.PahadiDialect
import com.example.data.model.ResponseDetail
import com.example.data.model.TranslationResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

object GeminiClient {
    private const val TAG = "GeminiClient"
    private const val MODEL_NAME = "gemini-3.5-flash"
    private const val BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(60, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .build()

    fun isApiKeyConfigured(): Boolean {
        val key = BuildConfig.GEMINI_API_KEY
        return key.isNotBlank() && key != "MY_GEMINI_API_KEY"
    }

    suspend fun translateWithCulturalContext(
        sourceText: String,
        sourceLang: String,
        targetDialect: PahadiDialect,
        isPahadiToHindi: Boolean = false
    ): Result<TranslationResult> = withContext(Dispatchers.IO) {
        val apiKey = BuildConfig.GEMINI_API_KEY
        if (!isApiKeyConfigured()) {
            return@withContext Result.failure(IllegalStateException("Gemini API key is not configured"))
        }

        try {
            val systemInstruction = """
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
            """.trimIndent()

            val prompt = if (isPahadiToHindi) {
                """
                The following text is in the Pahadi dialect: ${targetDialect.displayNameHindi} (${targetDialect.displayNameEnglish} - ${targetDialect.region}).
                Translate this authentic Pahadi dialect text accurately into natural, clean standard Hindi (मानक हिंदी).
                In culturalContext, explain the meaning of any unique Pahadi words, dialect grammar patterns, or idioms used.
                Pahadi Text: "$sourceText"
                """.trimIndent()
            } else {
                """
                Translate the following text from $sourceLang to ${targetDialect.displayNameHindi} (${targetDialect.displayNameEnglish}):
                "$sourceText"
                """.trimIndent()
            }

            val rootJson = JSONObject().apply {
                put("contents", JSONArray().apply {
                    put(JSONObject().apply {
                        put("role", "user")
                        put("parts", JSONArray().apply {
                            put(JSONObject().apply { put("text", prompt) })
                        })
                    })
                })
                put("systemInstruction", JSONObject().apply {
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply { put("text", systemInstruction) })
                    })
                })
                put("generationConfig", JSONObject().apply {
                    put("responseMimeType", "application/json")
                    put("temperature", 0.3)
                })
            }

            val requestBody = rootJson.toString().toRequestBody("application/json".toMediaType())
            val request = Request.Builder()
                .url("$BASE_URL/$MODEL_NAME:generateContent?key=$apiKey")
                .post(requestBody)
                .build()

            val response = okHttpClient.newCall(request).execute()
            val responseBody = response.body?.string() ?: ""

            if (!response.isSuccessful) {
                Log.e(TAG, "Gemini translation failed: ${response.code}")
                return@withContext Result.failure(Exception("Gemini error ${response.code}"))
            }

            val respJson = JSONObject(responseBody)
            val candidates = respJson.optJSONArray("candidates")
            val firstCandidate = candidates?.optJSONObject(0)
            val content = firstCandidate?.optJSONObject("content")
            val parts = content?.optJSONArray("parts")
            val rawTextBuilder = java.lang.StringBuilder()
            if (parts != null) {
                for (i in 0 until parts.length()) {
                    rawTextBuilder.append(parts.optJSONObject(i)?.optString("text", "") ?: "")
                }
            }
            val rawText = rawTextBuilder.toString()
            val cleanJson = rawText.trim()
                .removePrefix("```json")
                .removePrefix("```")
                .removeSuffix("```")
                .trim()

            val parsed = JSONObject(cleanJson)
            val result = TranslationResult(
                sourceText = sourceText,
                sourceLanguage = if (isPahadiToHindi) "${targetDialect.displayNameHindi} (पहाड़ी)" else sourceLang,
                targetDialect = targetDialect,
                translatedText = parsed.optString("translatedText", sourceText),
                phoneticText = parsed.optString("phoneticText", ""),
                culturalContext = parsed.optString("culturalContext", "पहाड़ी भाषा और संस्कृति का सुंदर स्वरूप।"),
                etiquetteTip = parsed.optString("etiquetteTip", "बातचीत में आदर और 'जी' का प्रयोग करें।"),
                regionalVariation = parsed.optString("regionalVariation", targetDialect.region),
                exampleUsage = parsed.optString("exampleUsage", ""),
                isAiPowered = true
            )

            Result.success(result)
        } catch (e: Exception) {
            Log.e(TAG, "Translation error", e)
            Result.failure(e)
        }
    }

    suspend fun chatWithPahadiAi(
        history: List<ChatMessage>,
        userMessage: String,
        mode: AppMode,
        dialect: PahadiDialect,
        detail: ResponseDetail
    ): Result<String> = withContext(Dispatchers.IO) {
        val apiKey = BuildConfig.GEMINI_API_KEY
        if (!isApiKeyConfigured()) {
            return@withContext Result.failure(IllegalStateException("Gemini API key is not configured"))
        }

        try {
            val modeInstruction = when (mode) {
                AppMode.ELDER -> """
                    MODE: ELDER FRIENDLY (बुजुर्ग मित्र मोड)
                    - Speak in very warm, respectful, clear, and reassuring language with traditional greetings like 'पैलाग जी', 'नमस्कार जी', 'जय देव जी'.
                    - Keep sentences short, sweet, easily listenable via Voice-First Text-to-Speech.
                    - Avoid heavy jargon; explain everything simply.
                    - The user is speaking by voice; respond so that it sounds beautiful when spoken aloud.
                """.trimIndent()

                AppMode.STUDENT -> """
                    MODE: STUDENT HELPER (छात्र सहायक मोड)
                    - Help students understand school/college chapters, science, history, geography, and concepts clearly.
                    - Provide short revision notes, question-answer bullet points, and English ↔ Hindi/Pahadi explanations.
                    - Format with clear headings, bullet points, and quick memory tricks.
                """.trimIndent()

                AppMode.FARMER -> """
                    MODE: FARMER & ORCHARD HELPER (किसान व बागवान मित्र)
                    - Provide expert guidance on Apple orchards (pruning, royal delicious, spur varieties, scab management, chilling hours).
                    - Weather-based agricultural advice and frost/hailstorm protection.
                    - Explain Himachal Government agricultural schemes (Himcare, Prakritik Kheti Khushhal Kisan Yojna, Anti-Hail Net Subsidy).
                    - Use local farming terms (स्युब, बगीचे, काट-छांट, बोर्डो मिश्रण, जीवामृत).
                """.trimIndent()

                AppMode.STANDARD -> """
                    MODE: ALL-ROUND HIMALAYAN AI ASSISTANT
                    - Help with general Q&A, HRTC bus routes & inquiries, government schemes, tourism, writing messages, calculations, and local culture.
                    - Seamlessly understand queries spoken in Hindi, English, or Pahadi dialects.
                """.trimIndent()
            }

            val lengthInstruction = if (detail == ResponseDetail.CONCISE) {
                "Keep the answer concise, crisp, and to the point (2-4 sentences or short bullet points), perfect for quick voice listening."
            } else {
                "Provide a detailed, thorough, and well-structured answer with local context."
            }

            val systemInstruction = """
                You are 'Pahadi AI' (पहाड़ी संगम) — the voice-first AI assistant for Himachal Pradesh and Uttarakhand.
                Active Dialect Context: ${dialect.displayNameHindi} (${dialect.region}, ${dialect.state}).
                
                Core Rules:
                1. Voice-First Experience: The user speaks or types. Reply in a natural, polite blend of Hindi and local dialect phrases.
                2. $modeInstruction
                3. $lengthInstruction
                4. Always be helpful, culturally authentic, and uplifting.
            """.trimIndent()

            val contentsArray = JSONArray()
            val recent = history.takeLast(6)
            for (msg in recent) {
                contentsArray.put(JSONObject().apply {
                    put("role", if (msg.isUser) "user" else "model")
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply { put("text", msg.text) })
                    })
                })
            }

            contentsArray.put(JSONObject().apply {
                put("role", "user")
                put("parts", JSONArray().apply {
                    put(JSONObject().apply { put("text", userMessage) })
                })
            })

            val rootJson = JSONObject().apply {
                put("contents", contentsArray)
                put("systemInstruction", JSONObject().apply {
                    put("parts", JSONArray().apply {
                        put(JSONObject().apply { put("text", systemInstruction) })
                    })
                })
                put("generationConfig", JSONObject().apply {
                    put("temperature", 0.7)
                })
            }

            val requestBody = rootJson.toString().toRequestBody("application/json".toMediaType())
            val request = Request.Builder()
                .url("$BASE_URL/$MODEL_NAME:generateContent?key=$apiKey")
                .post(requestBody)
                .build()

            val response = okHttpClient.newCall(request).execute()
            val responseBody = response.body?.string() ?: ""

            if (!response.isSuccessful) {
                Log.e(TAG, "Chat failed: ${response.code}")
                return@withContext Result.failure(Exception("Gemini error ${response.code}"))
            }

            val respJson = JSONObject(responseBody)
            val candidates = respJson.optJSONArray("candidates")
            val candidate = candidates?.optJSONObject(0)
            val parts = candidate?.optJSONObject("content")?.optJSONArray("parts")
            val textBuilder = java.lang.StringBuilder()
            if (parts != null) {
                for (i in 0 until parts.length()) {
                    textBuilder.append(parts.optJSONObject(i)?.optString("text", "") ?: "")
                }
            }
            val text = textBuilder.toString()

            Result.success(text)
        } catch (e: Exception) {
            Log.e(TAG, "Chat error", e)
            Result.failure(e)
        }
    }
}
