package com.example.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "translations")
data class TranslationEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val sourceText: String,
    val sourceLanguage: String,
    val targetDialectCode: String,
    val targetDialectName: String,
    val translatedText: String,
    val phoneticText: String,
    val culturalContext: String,
    val etiquetteTip: String,
    val isFavorite: Boolean = false,
    val timestamp: Long = System.currentTimeMillis()
)

@Entity(tableName = "saved_notes")
data class CulturalNoteEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val title: String,
    val dialect: String,
    val content: String,
    val timestamp: Long = System.currentTimeMillis()
)

@Entity(tableName = "chat_messages")
data class ChatMessageEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val clientMessageId: String,
    val sessionId: String = "cultural_qa_session",
    val sessionTitle: String = "पहाड़ी संवाद व सांस्कृतिक Q&A",
    val text: String,
    val isUser: Boolean,
    val timestamp: Long = System.currentTimeMillis(),
    val appMode: String = "STANDARD",
    val relatedDialectCode: String? = null,
    val isCulturalQa: Boolean = false
)

fun ChatMessageEntity.toChatMessage(): com.example.data.model.ChatMessage {
    val mode = try {
        com.example.data.model.AppMode.valueOf(appMode)
    } catch (_: Exception) {
        com.example.data.model.AppMode.STANDARD
    }
    val dialect = relatedDialectCode?.let { com.example.data.model.PahadiDialect.fromCode(it) }
    return com.example.data.model.ChatMessage(
        id = if (id > 0) "db_msg_${id}" else clientMessageId.ifEmpty { "msg_${timestamp}_${text.hashCode()}" },
        text = text,
        isUser = isUser,
        timestamp = timestamp,
        appMode = mode,
        relatedDialect = dialect
    )
}

fun com.example.data.model.ChatMessage.toEntity(sessionId: String = "cultural_qa_session", isCulturalQa: Boolean = false): ChatMessageEntity {
    return ChatMessageEntity(
        clientMessageId = id,
        sessionId = sessionId,
        sessionTitle = "पहाड़ी संवाद व सांस्कृतिक Q&A",
        text = text,
        isUser = isUser,
        timestamp = timestamp,
        appMode = appMode.name,
        relatedDialectCode = relatedDialect?.code,
        isCulturalQa = isCulturalQa
    )
}
