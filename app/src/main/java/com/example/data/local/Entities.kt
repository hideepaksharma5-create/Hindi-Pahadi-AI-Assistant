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
