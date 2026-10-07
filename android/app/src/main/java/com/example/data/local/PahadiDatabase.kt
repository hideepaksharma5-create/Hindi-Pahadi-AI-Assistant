package com.example.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [TranslationEntity::class, CulturalNoteEntity::class, ChatMessageEntity::class],
    version = 2,
    exportSchema = false
)
abstract class PahadiDatabase : RoomDatabase() {
    abstract fun translationDao(): TranslationDao
    abstract fun chatDao(): ChatDao

    companion object {
        @Volatile
        private var INSTANCE: PahadiDatabase? = null

        fun getInstance(context: Context): PahadiDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    PahadiDatabase::class.java,
                    "pahadi_ai_database"
                ).fallbackToDestructiveMigration(true)
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
