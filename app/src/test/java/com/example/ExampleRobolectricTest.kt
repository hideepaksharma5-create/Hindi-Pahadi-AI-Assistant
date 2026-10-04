package com.example

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import com.example.data.dictionary.PahadiOfflineEngine
import com.example.data.model.PahadiDialect
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [36])
class ExampleRobolectricTest {

  @Test
  fun `read string from context`() {
    val context = ApplicationProvider.getApplicationContext<Context>()
    val appName = context.getString(R.string.app_name)
    assertEquals("Pahadi AI", appName)
  }

  @Test
  fun `verify garhwali and kumaoni offline translation`() {
    val garhwaliResult = PahadiOfflineEngine.findOfflineTranslation("नमस्ते", PahadiDialect.GARHWALI)
    assertNotNull(garhwaliResult)
    assertTrue(garhwaliResult.translatedText.isNotEmpty())
    assertTrue(garhwaliResult.culturalContext.isNotEmpty())

    val kumaoniResult = PahadiOfflineEngine.findOfflineTranslation("नमस्ते", PahadiDialect.KUMAONI)
    assertNotNull(kumaoniResult)
    assertTrue(kumaoniResult.translatedText.contains("पैलाग") || kumaoniResult.translatedText.isNotEmpty())
  }

  @Test
  fun `verify curated stories and phrasebook content`() {
    assertTrue(PahadiOfflineEngine.curatedPhrases.isNotEmpty())
    assertTrue(PahadiOfflineEngine.culturalStories.size >= 5)

    val goluStory = PahadiOfflineEngine.culturalStories.find { it.id == "story_golu" }
    assertNotNull(goluStory)
    assertTrue(goluStory!!.fullStory.contains("चितई"))
  }

  @Test
  fun `verify pahadi to hindi translation`() {
    val resultPailaag = PahadiOfflineEngine.translatePahadiToHindi("पैलाग", PahadiDialect.KUMAONI)
    assertNotNull(resultPailaag)
    assertTrue(resultPailaag.translatedText.contains("प्रणाम") || resultPailaag.translatedText.contains("चरण स्पर्श"))

    val resultHaal = PahadiOfflineEngine.translatePahadiToHindi("तुहाड़े के हाल न?", PahadiDialect.MANDEALI)
    assertNotNull(resultHaal)
    assertTrue(resultHaal.translatedText.contains("हाल-चाल") || resultHaal.translatedText.contains("कैसे"))
  }
}
