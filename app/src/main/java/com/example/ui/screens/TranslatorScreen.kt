package com.example.ui.screens

import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.speech.RecognizerIntent
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Lightbulb
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.SwapHoriz
import androidx.compose.material.icons.filled.Translate
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledTonalIconButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.SuggestionChip
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.PahadiDialect
import com.example.data.model.SourceLanguage
import com.example.ui.theme.HimalayanGoldSecondary
import com.example.ui.theme.SaffronHimalaya
import com.example.ui.viewmodel.PahadiViewModel

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun TranslatorScreen(
    viewModel: PahadiViewModel,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val inputText by viewModel.inputText.collectAsState()
    val sourceLang by viewModel.sourceLang.collectAsState()
    val targetDialect by viewModel.targetDialect.collectAsState()
    val isTranslating by viewModel.isTranslating.collectAsState()
    val currentTranslation by viewModel.currentTranslation.collectAsState()
    val isSaved by viewModel.isCurrentSaved.collectAsState()

    var showDialectSheet by remember { mutableStateOf(false) }
    var showSourceMenu by remember { mutableStateOf(false) }

    // Speech-to-text launcher
    val speechRecognizerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val spoken = result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val recognizedText = spoken?.firstOrNull()
            if (!recognizedText.isNullOrBlank()) {
                viewModel.setInputText(recognizedText)
                viewModel.translateNow()
            }
        }
    }

    val quickPhrases = listOf(
        "नमस्ते, आप कैसे हैं?",
        "क्या आपने खाना खा लिया?",
        "यह रास्ता कहाँ जाता है?",
        "इसका क्या भाव है?",
        "आपसे मिलकर बहुत अच्छा लगा",
        "धूप निकल आई है, बाहर आओ"
    )

    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp)
            .testTag("translator_screen")
    ) {
        // Language Selector Row
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .testTag("language_selector_card"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.6f)
            )
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 12.dp, vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Source Language
                Box {
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.surface,
                        modifier = Modifier
                            .clip(RoundedCornerShape(10.dp))
                            .clickable { showSourceMenu = true }
                            .padding(horizontal = 12.dp, vertical = 8.dp)
                            .testTag("source_lang_picker")
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = sourceLang.take(14),
                                style = MaterialTheme.typography.labelLarge.copy(
                                    fontWeight = FontWeight.SemiBold
                                )
                            )
                            Icon(
                                imageVector = Icons.Default.ArrowDropDown,
                                contentDescription = "Select Source Language",
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    }

                    DropdownMenu(
                        expanded = showSourceMenu,
                        onDismissRequest = { showSourceMenu = false }
                    ) {
                        for (lang in SourceLanguage.entries) {
                            DropdownMenuItem(
                                text = { Text(lang.displayName) },
                                onClick = {
                                    viewModel.setSourceLang(lang.displayName)
                                    showSourceMenu = false
                                }
                            )
                        }
                    }
                }

                // Swap Button
                FilledTonalIconButton(
                    onClick = { viewModel.swapLanguages() },
                    modifier = Modifier
                        .size(42.dp)
                        .testTag("swap_languages_button")
                ) {
                    Icon(
                        imageVector = Icons.Default.SwapHoriz,
                        contentDescription = "Swap Languages"
                    )
                }

                // Target Dialect Selector
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.primaryContainer,
                    modifier = Modifier
                        .clip(RoundedCornerShape(10.dp))
                        .clickable { showDialectSheet = true }
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                        .testTag("target_dialect_picker")
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = targetDialect.displayNameHindi.substringBefore(" ("),
                            style = MaterialTheme.typography.labelLarge.copy(
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onPrimaryContainer
                            )
                        )
                        Icon(
                            imageVector = Icons.Default.ArrowDropDown,
                            contentDescription = "Select Dialect",
                            tint = MaterialTheme.colorScheme.onPrimaryContainer,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        // Input Card
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .testTag("translation_input_card"),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
        ) {
            Column(modifier = Modifier.padding(14.dp)) {
                OutlinedTextField(
                    value = inputText,
                    onValueChange = { viewModel.setInputText(it) },
                    placeholder = {
                        Text(
                            "हिंदी या अंग्रेज़ी में लिखें या बोलें...\n(उदा. 'नमस्ते! आप कैसे हैं?')",
                            style = MaterialTheme.typography.bodyMedium.copy(color = Color.Gray)
                        )
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(115.dp)
                        .testTag("translator_text_input"),
                    shape = RoundedCornerShape(12.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = Color.Transparent
                    )
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Quick mic button
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        IconButton(
                            onClick = {
                                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")
                                    putExtra(RecognizerIntent.EXTRA_PROMPT, "पहाड़ी अनुवाद के लिए बोलें...")
                                }
                                try {
                                    speechRecognizerLauncher.launch(intent)
                                } catch (e: Exception) {
                                    Toast.makeText(context, "Voice input not available", Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.testTag("mic_input_button")
                        ) {
                            Icon(
                                imageVector = Icons.Default.Mic,
                                contentDescription = "Voice Input",
                                tint = MaterialTheme.colorScheme.primary
                            )
                        }

                        if (inputText.isNotEmpty()) {
                            IconButton(
                                onClick = { viewModel.setInputText("") },
                                modifier = Modifier.testTag("clear_input_button")
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Clear,
                                    contentDescription = "Clear Input",
                                    tint = Color.Gray
                                )
                            }
                        }
                    }

                    // Translate CTA
                    Button(
                        onClick = { viewModel.translateNow() },
                        enabled = inputText.isNotBlank() && !isTranslating,
                        shape = RoundedCornerShape(12.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary),
                        modifier = Modifier.testTag("translate_action_button")
                    ) {
                        if (isTranslating) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(18.dp),
                                color = Color.White,
                                strokeWidth = 2.dp
                            )
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("अनुवाद हो रहा है...")
                        } else {
                            Icon(
                                imageVector = Icons.Default.AutoAwesome,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("अनुवाद करें")
                        }
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(10.dp))

        // Quick Suggestion Chips
        Text(
            text = "शीघ्र अनुवाद (Quick Prompts):",
            style = MaterialTheme.typography.labelMedium.copy(color = MaterialTheme.colorScheme.primary),
            fontWeight = FontWeight.SemiBold
        )
        Spacer(modifier = Modifier.height(6.dp))
        FlowRow(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp)
        ) {
            quickPhrases.forEach { phrase ->
                SuggestionChip(
                    onClick = {
                        viewModel.setInputText(phrase)
                        viewModel.translateNow()
                    },
                    label = { Text(phrase, fontSize = 12.sp) }
                )
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        // Output Result Section
        AnimatedVisibility(
            visible = currentTranslation != null,
            enter = fadeIn() + slideInVertically()
        ) {
            val translation = currentTranslation ?: return@AnimatedVisibility

            Column(modifier = Modifier.fillMaxWidth()) {
                // Dialect Output Card
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("translation_output_card"),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = MaterialTheme.colorScheme.surface
                    ),
                    elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Surface(
                                shape = RoundedCornerShape(8.dp),
                                color = MaterialTheme.colorScheme.secondaryContainer
                            ) {
                                Text(
                                    text = translation.targetDialect.displayNameHindi,
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.onSecondaryContainer
                                    ),
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                                )
                            }

                            Row {
                                // Speak button
                                IconButton(
                                    onClick = { viewModel.speakText(translation.translatedText) },
                                    modifier = Modifier.testTag("audio_speak_button")
                                ) {
                                    Icon(
                                        imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                                        contentDescription = "Speak translation",
                                        tint = MaterialTheme.colorScheme.primary
                                    )
                                }

                                // Copy button
                                IconButton(
                                    onClick = {
                                        val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                                        val clip = ClipData.newPlainText("Pahadi Translation", translation.translatedText)
                                        clipboard.setPrimaryClip(clip)
                                        Toast.makeText(context, "अनुवाद कॉपी हो गया", Toast.LENGTH_SHORT).show()
                                    },
                                    modifier = Modifier.testTag("copy_translation_button")
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.ContentCopy,
                                        contentDescription = "Copy Translation"
                                    )
                                }

                                // Favorite button
                                IconButton(
                                    onClick = {
                                        viewModel.toggleCurrentFavorite()
                                        Toast.makeText(
                                            context,
                                            if (!isSaved) "सहेज लिया गया!" else "हटा दिया गया",
                                            Toast.LENGTH_SHORT
                                        ).show()
                                    },
                                    modifier = Modifier.testTag("favorite_translation_button")
                                ) {
                                    Icon(
                                        imageVector = if (isSaved) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                                        contentDescription = "Save to favorites",
                                        tint = if (isSaved) SaffronHimalaya else Color.Gray
                                    )
                                }

                                // Share button
                                IconButton(
                                    onClick = {
                                        val shareText = "पहाड़ी संगम अनुवाद:\n" +
                                                "मूल: ${translation.sourceText}\n" +
                                                "बोली (${translation.targetDialect.displayNameHindi}): ${translation.translatedText}\n" +
                                                "उच्चारण: ${translation.phoneticText}\n" +
                                                "सांस्कृतिक संदर्भ: ${translation.culturalContext}"
                                        val sendIntent = Intent().apply {
                                            action = Intent.ACTION_SEND
                                            putExtra(Intent.EXTRA_TEXT, shareText)
                                            type = "text/plain"
                                        }
                                        context.startActivity(Intent.createChooser(sendIntent, "साझा करें"))
                                    },
                                    modifier = Modifier.testTag("share_translation_button")
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Share,
                                        contentDescription = "Share translation"
                                    )
                                }
                            }
                        }

                        Spacer(modifier = Modifier.height(10.dp))

                        // Translated Devanagari Text
                        Text(
                            text = translation.translatedText,
                            style = MaterialTheme.typography.headlineSmall.copy(
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary,
                                lineHeight = 32.sp
                            ),
                            modifier = Modifier.testTag("translated_text_display")
                        )

                        if (translation.phoneticText.isNotBlank()) {
                            Spacer(modifier = Modifier.height(6.dp))
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text(
                                    text = "उच्चारण (Pronunciation): ${translation.phoneticText}",
                                    style = MaterialTheme.typography.bodyMedium.copy(
                                        fontStyle = androidx.compose.ui.text.font.FontStyle.Italic,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant
                                    ),
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 6.dp)
                                )
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Cultural Context Card (anthropological breakdown)
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("cultural_context_card"),
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(
                        containerColor = HimalayanGoldSecondary.copy(alpha = 0.08f)
                    ),
                    border = CardDefaults.outlinedCardBorder().copy(
                        brush = androidx.compose.ui.graphics.SolidColor(HimalayanGoldSecondary.copy(alpha = 0.35f))
                    )
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Surface(
                                shape = CircleShape,
                                color = HimalayanGoldSecondary.copy(alpha = 0.2f),
                                modifier = Modifier.size(28.dp)
                            ) {
                                Box(contentAlignment = Alignment.Center) {
                                    Icon(
                                        imageVector = Icons.Default.Lightbulb,
                                        contentDescription = null,
                                        tint = HimalayanGoldSecondary,
                                        modifier = Modifier.size(18.dp)
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = "सांस्कृतिक संदर्भ एवं शिष्टाचार (Cultural Context)",
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = HimalayanGoldSecondary
                                )
                            )
                        }

                        Spacer(modifier = Modifier.height(10.dp))

                        Text(
                            text = translation.culturalContext,
                            style = MaterialTheme.typography.bodyMedium.copy(
                                lineHeight = 22.sp,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                        )

                        if (translation.etiquetteTip.isNotBlank()) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Row(
                                verticalAlignment = Alignment.Top,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .background(Color.White.copy(alpha = 0.7f), RoundedCornerShape(8.dp))
                                    .padding(8.dp)
                            ) {
                                Text("💡 ", fontSize = 14.sp)
                                Text(
                                    text = translation.etiquetteTip,
                                    style = MaterialTheme.typography.bodySmall.copy(
                                        fontWeight = FontWeight.Medium
                                    )
                                )
                            }
                        }

                        if (translation.regionalVariation.isNotBlank()) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "क्षेत्रीय विस्तार: ${translation.regionalVariation}",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    color = Color.Gray
                                )
                            )
                        }
                    }
                }
            }
        }
    }

    // Modal Bottom Sheet for selecting Pahadi Dialect
    if (showDialectSheet) {
        ModalBottomSheet(
            onDismissRequest = { showDialectSheet = false },
            sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Text(
                    text = "पहाड़ी बोली चुनें (Select Dialect)",
                    style = MaterialTheme.typography.titleLarge.copy(fontWeight = FontWeight.Bold)
                )
                Text(
                    text = "उत्तराखंड व हिमाचल की 8 प्रमुख बोलियां व भाषाएं:",
                    style = MaterialTheme.typography.bodySmall.copy(color = Color.Gray)
                )
                Spacer(modifier = Modifier.height(14.dp))

                PahadiDialect.entries.forEach { dialect ->
                    val isSelected = dialect == targetDialect
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                            .clickable {
                                viewModel.setTargetDialect(dialect)
                                showDialectSheet = false
                            },
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = if (isSelected) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface
                        ),
                        border = if (isSelected) CardDefaults.outlinedCardBorder() else null
                    ) {
                        Column(modifier = Modifier.padding(12.dp)) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = dialect.displayNameHindi,
                                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold)
                                )
                                Surface(
                                    shape = RoundedCornerShape(6.dp),
                                    color = MaterialTheme.colorScheme.outline.copy(alpha = 0.2f)
                                ) {
                                    Text(
                                        text = dialect.state.substringBefore(" "),
                                        style = MaterialTheme.typography.labelSmall,
                                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                                    )
                                }
                            }
                            Spacer(modifier = Modifier.height(3.dp))
                            Text(
                                text = dialect.description,
                                style = MaterialTheme.typography.bodySmall.copy(color = Color.DarkGray)
                            )
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
        }
    }
}
