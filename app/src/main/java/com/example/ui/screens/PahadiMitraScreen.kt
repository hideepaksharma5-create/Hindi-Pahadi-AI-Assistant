package com.example.ui.screens

import android.Manifest
import android.app.Activity
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.speech.RecognizerIntent
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Chat
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.VolumeOff
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Elderly
import androidx.compose.material.icons.filled.Landscape
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.SuggestionChip
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.data.model.AppMode
import com.example.data.model.ChatMessage
import com.example.data.model.VoiceGender
import com.example.ui.components.PahadiDialectDropdown
import com.example.ui.components.SpeechListeningOverlay
import com.example.ui.theme.SaffronHimalaya
import com.example.ui.viewmodel.PahadiViewModel

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun PahadiMitraScreen(
    viewModel: PahadiViewModel,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val messages by viewModel.chatMessages.collectAsState()
    val isGenerating by viewModel.isChatGenerating.collectAsState()
    val chatInput by viewModel.chatInput.collectAsState()
    val currentMode by viewModel.appMode.collectAsState()
    val voiceGender by viewModel.voiceGender.collectAsState()
    val autoSpeak by viewModel.autoSpeakEnabled.collectAsState()
    val activeDialect by viewModel.targetDialect.collectAsState()

    // Live Speech Recognition states from SpeechRecognizer API
    val isListening by viewModel.isListening.collectAsState()
    val partialTranscript by viewModel.partialSpeechTranscript.collectAsState()
    val rmsDb by viewModel.speechRmsDb.collectAsState()
    val speechError by viewModel.speechError.collectAsState()

    val listState = rememberLazyListState()

    // Fallback external dialog launcher
    val fallbackRecognizerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val spoken = result.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val recognizedText = spoken?.firstOrNull()
            if (!recognizedText.isNullOrBlank()) {
                viewModel.sendChatMessage(recognizedText)
            }
        }
    }

    // Permission launcher for RECORD_AUDIO
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            if (viewModel.isSpeechAvailable) {
                viewModel.startSpeechRecognition("hi-IN") { text ->
                    viewModel.sendChatMessage(text)
                }
            } else {
                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")
                    putExtra(RecognizerIntent.EXTRA_PROMPT, "बोलें, Pahadi AI सुन रहा है...")
                }
                fallbackRecognizerLauncher.launch(intent)
            }
        } else {
            Toast.makeText(context, "बोलने के लिए माइक्रोफोन अनुमति आवश्यक है", Toast.LENGTH_SHORT).show()
        }
    }

    fun startVoiceInput() {
        val permissionCheck = ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO)
        if (permissionCheck == PackageManager.PERMISSION_GRANTED) {
            if (viewModel.isSpeechAvailable) {
                viewModel.startSpeechRecognition("hi-IN") { text ->
                    viewModel.sendChatMessage(text)
                }
            } else {
                val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                    putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")
                    putExtra(RecognizerIntent.EXTRA_PROMPT, "बोलें, Pahadi AI सुन रहा है...")
                }
                try {
                    fallbackRecognizerLauncher.launch(intent)
                } catch (e: Exception) {
                    Toast.makeText(context, "स्पीच सेवा उपलब्ध नहीं है", Toast.LENGTH_SHORT).show()
                }
            }
        } else {
            permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        }
    }

    LaunchedEffect(speechError) {
        speechError?.let {
            Toast.makeText(context, it, Toast.LENGTH_SHORT).show()
        }
    }

    LaunchedEffect(messages.size) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }

    val modePrompts = when (currentMode) {
        AppMode.ELDER -> listOf(
            "🙏 जय देव जी, कैसे हैं?",
            "☀️ आज धूप कब निकलेगी?",
            "🍲 गरम खाना व सेहत की सलाह",
            "📞 आपातकालीन एम्बुलेंस नंबर"
        )
        AppMode.STUDENT -> listOf(
            "🌱 प्रकाश संश्लेषण समझाएं",
            "⛰️ हिमाचल प्रदेश सामान्य ज्ञान",
            "📝 परीक्षा हेतु संक्षिप्त नोट्स",
            "🔄 English → Hindi अनुवाद"
        )
        AppMode.FARMER -> listOf(
            "🍏 सेब के बगीचे में प्रूनिंग का समय",
            "🛡️ सेब स्कैब रोग नियंत्रण",
            "🌱 जीवामृत बनाने की विधि",
            "💰 एंटी-हेल नेट सब्सिडी"
        )
        AppMode.STANDARD -> listOf(
            "🚌 एचआरटीसी बस समय-सारणी",
            "🏥 हिमकेयर योजना की जानकारी",
            "🍲 पारंपरिक हिमाचली धाम",
            "⚖️ चितई गोलू देवता की कथा"
        )
    }

    Box(modifier = modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .testTag("pahadi_mitra_screen")
        ) {
            // Mode Selector Bar
            Surface(
                tonalElevation = 2.dp,
                color = MaterialTheme.colorScheme.surface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(vertical = 6.dp)) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(horizontal = 12.dp),
                        horizontalArrangement = Arrangement.spacedBy(6.dp)
                    ) {
                        AppMode.entries.forEach { mode ->
                            val isSelected = currentMode == mode
                            FilterChip(
                                selected = isSelected,
                                onClick = { viewModel.setAppMode(mode) },
                                leadingIcon = {
                                    Icon(
                                        imageVector = when (mode) {
                                            AppMode.ELDER -> Icons.Default.Elderly
                                            AppMode.STUDENT -> Icons.Default.School
                                            AppMode.FARMER -> Icons.Default.Agriculture
                                            AppMode.STANDARD -> Icons.Default.SmartToy
                                        },
                                        contentDescription = null,
                                        modifier = Modifier.size(16.dp)
                                    )
                                },
                                label = {
                                    Text(
                                        mode.titleHindi,
                                        fontSize = 12.sp,
                                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                                    )
                                }
                            )
                        }
                    }

                    // Voice & Personalization Quick Toggles
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 2.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.primaryContainer,
                                modifier = Modifier.clickable { viewModel.toggleVoiceGender() }
                            ) {
                                Text(
                                    text = if (voiceGender == VoiceGender.FEMALE) "आवाज़: महिला 👩" else "आवाज़: पुरुष 👨",
                                    style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.SemiBold),
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                                )
                            }

                            Spacer(modifier = Modifier.width(8.dp))

                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = if (autoSpeak) Color(0xFF10B981).copy(alpha = 0.2f) else Color.Gray.copy(alpha = 0.2f),
                                modifier = Modifier.clickable { viewModel.toggleAutoSpeak() }
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    modifier = Modifier.padding(horizontal = 6.dp, vertical = 3.dp)
                                ) {
                                    Icon(
                                        imageVector = if (autoSpeak) Icons.AutoMirrored.Filled.VolumeUp else Icons.AutoMirrored.Filled.VolumeOff,
                                        contentDescription = null,
                                        modifier = Modifier.size(14.dp),
                                        tint = if (autoSpeak) Color(0xFF047857) else Color.DarkGray
                                    )
                                    Spacer(modifier = Modifier.width(3.dp))
                                    Text(
                                        text = if (autoSpeak) "आवाज ऑन" else "आवाज म्यूट",
                                        fontSize = 11.sp,
                                        fontWeight = FontWeight.Medium
                                    )
                                }
                            }
                        }

                        // Interactive Dialect Selection Dropdown
                        PahadiDialectDropdown(
                            selectedDialect = activeDialect,
                            onDialectSelected = { viewModel.setTargetDialect(it) },
                            compact = true
                        )
                    }
                }
            }

            // Messages List
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 14.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                item {
                    Spacer(modifier = Modifier.height(6.dp))

                    FlowRow(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        modePrompts.forEach { prompt ->
                            SuggestionChip(
                                onClick = { viewModel.sendChatMessage(prompt.substringAfter(" ")) },
                                label = { Text(prompt, fontSize = if (currentMode == AppMode.ELDER) 13.sp else 12.sp) }
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(8.dp))
                }

                items(messages, key = { it.id }) { msg ->
                    ChatBubble(
                        message = msg,
                        isElderMode = currentMode == AppMode.ELDER,
                        onSpeak = { viewModel.speakText(msg.text) },
                        onCopy = {
                            val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                            val clip = ClipData.newPlainText("Pahadi AI", msg.text)
                            clipboard.setPrimaryClip(clip)
                            Toast.makeText(context, "संदेश कॉपी हुआ", Toast.LENGTH_SHORT).show()
                        }
                    )
                }

                if (isGenerating) {
                    item {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(start = 12.dp, top = 6.dp)
                        ) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(18.dp),
                                color = SaffronHimalaya,
                                strokeWidth = 2.dp
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = "Pahadi AI सोच रहा है...",
                                style = MaterialTheme.typography.bodySmall.copy(
                                    fontStyle = androidx.compose.ui.text.font.FontStyle.Italic,
                                    color = Color.Gray
                                )
                            )
                        }
                    }
                }

                item { Spacer(modifier = Modifier.height(10.dp)) }
            }

            // Bottom controls
            if (currentMode == AppMode.ELDER) {
                // Giant Voice button for Elders
                Surface(
                    tonalElevation = 6.dp,
                    color = MaterialTheme.colorScheme.surface,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(14.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Button(
                            onClick = {
                                if (isListening) viewModel.stopSpeechRecognition() else startVoiceInput()
                            },
                            shape = RoundedCornerShape(20.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (isListening) SaffronHimalaya else MaterialTheme.colorScheme.primary
                            ),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(64.dp)
                                .testTag("giant_elder_mic_button")
                        ) {
                            Icon(
                                imageVector = Icons.Default.Mic,
                                contentDescription = "Speak now",
                                modifier = Modifier.size(32.dp),
                                tint = Color.White
                            )
                            Spacer(modifier = Modifier.width(12.dp))
                            Text(
                                text = if (isListening) "🛑 सुनना समाप्त करें (Stop)" else "🎤 यहाँ दबाकर बोलें (Tap to Speak)",
                                style = MaterialTheme.typography.titleMedium.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = Color.White,
                                    fontSize = 18.sp
                                )
                            )
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "बोलें, Pahadi AI आपकी बात सुनकर आवाज़ में उत्तर देगा।",
                            style = MaterialTheme.typography.bodySmall.copy(color = Color.DarkGray)
                        )
                    }
                }
            } else {
                // Standard mode input bar
                Surface(
                    tonalElevation = 4.dp,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(
                            onClick = {
                                if (isListening) viewModel.stopSpeechRecognition() else startVoiceInput()
                            },
                            modifier = Modifier
                                .background(
                                    if (isListening) SaffronHimalaya else MaterialTheme.colorScheme.primaryContainer,
                                    CircleShape
                                )
                                .size(42.dp)
                                .testTag("chat_mic_button")
                        ) {
                            Icon(
                                imageVector = Icons.Default.Mic,
                                contentDescription = "Speak in dialect",
                                tint = if (isListening) Color.White else MaterialTheme.colorScheme.onPrimaryContainer,
                                modifier = Modifier.size(24.dp)
                            )
                        }

                        Spacer(modifier = Modifier.width(8.dp))

                        OutlinedTextField(
                            value = chatInput,
                            onValueChange = { viewModel.setChatInput(it) },
                            placeholder = {
                                Text(
                                    "बोलें या लिखें (उदा. 'कल मौसम कैसा रहेगा?')...",
                                    fontSize = 13.sp
                                )
                            },
                            modifier = Modifier
                                .weight(1f)
                                .testTag("chat_text_input"),
                            shape = RoundedCornerShape(24.dp),
                            colors = OutlinedTextFieldDefaults.colors(
                                focusedBorderColor = MaterialTheme.colorScheme.primary,
                                unfocusedBorderColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.5f)
                            ),
                            maxLines = 3
                        )

                        Spacer(modifier = Modifier.width(6.dp))

                        IconButton(
                            onClick = { viewModel.sendChatMessage() },
                            enabled = chatInput.isNotBlank() && !isGenerating,
                            modifier = Modifier
                                .background(
                                    if (chatInput.isNotBlank()) MaterialTheme.colorScheme.primary else Color.LightGray,
                                    CircleShape
                                )
                                .size(42.dp)
                                .testTag("send_chat_button")
                        ) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Filled.Send,
                                contentDescription = "Send",
                                tint = Color.White,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                    }
                }
            }
        }

        // Live Real-Time Speech Recognition Pulse & Subtitle Overlay
        SpeechListeningOverlay(
            isListening = isListening,
            partialText = partialTranscript,
            rmsDb = rmsDb,
            targetDialectName = activeDialect.displayNameHindi.substringBefore(" ("),
            onStopListening = { viewModel.stopSpeechRecognition() },
            onCancelListening = { viewModel.cancelSpeechRecognition() },
            modifier = Modifier.align(Alignment.BottomCenter)
        )
    }
}

@Composable
fun ChatBubble(
    message: ChatMessage,
    isElderMode: Boolean,
    onSpeak: () -> Unit,
    onCopy: () -> Unit
) {
    val isUser = message.isUser

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = if (isUser) Arrangement.End else Arrangement.Start,
        verticalAlignment = Alignment.Top
    ) {
        if (!isUser) {
            Surface(
                shape = CircleShape,
                color = SaffronHimalaya.copy(alpha = 0.2f),
                modifier = Modifier
                    .size(if (isElderMode) 40.dp else 34.dp)
                    .padding(top = 2.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.Landscape,
                        contentDescription = "Pahadi AI Avatar",
                        tint = SaffronHimalaya,
                        modifier = Modifier.size(if (isElderMode) 24.dp else 20.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.width(8.dp))
        }

        Card(
            shape = RoundedCornerShape(
                topStart = 16.dp,
                topEnd = 16.dp,
                bottomStart = if (isUser) 16.dp else 4.dp,
                bottomEnd = if (isUser) 4.dp else 16.dp
            ),
            colors = CardDefaults.cardColors(
                containerColor = if (isUser) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
            ),
            modifier = Modifier.fillMaxWidth(if (isElderMode) 0.90f else 0.85f)
        ) {
            Column(modifier = Modifier.padding(if (isElderMode) 14.dp else 12.dp)) {
                if (!isUser) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "Pahadi AI",
                            style = MaterialTheme.typography.labelSmall.copy(
                                fontWeight = FontWeight.Bold,
                                color = SaffronHimalaya
                            )
                        )
                        Row {
                            IconButton(
                                onClick = onSpeak,
                                modifier = Modifier.size(30.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                                    contentDescription = "Listen",
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                            IconButton(
                                onClick = onCopy,
                                modifier = Modifier.size(30.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.ContentCopy,
                                    contentDescription = "Copy",
                                    tint = Color.Gray,
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                }

                Text(
                    text = message.text,
                    style = MaterialTheme.typography.bodyMedium.copy(
                        color = if (isUser) Color.White else MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = if (isElderMode) 17.sp else 14.sp,
                        lineHeight = if (isElderMode) 26.sp else 22.sp,
                        fontWeight = if (isElderMode) FontWeight.Medium else FontWeight.Normal
                    )
                )
            }
        }

        if (isUser) {
            Spacer(modifier = Modifier.width(8.dp))
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primary.copy(alpha = 0.15f),
                modifier = Modifier
                    .size(32.dp)
                    .padding(top = 2.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.Person,
                        contentDescription = "User Avatar",
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.size(18.dp)
                    )
                }
            }
        }
    }
}
