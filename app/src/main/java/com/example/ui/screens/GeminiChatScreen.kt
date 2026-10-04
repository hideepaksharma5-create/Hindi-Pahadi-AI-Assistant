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
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.VolumeOff
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Agriculture
import androidx.compose.material.icons.filled.AutoAwesome
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.Elderly
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.School
import androidx.compose.material.icons.filled.SmartToy
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
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
import androidx.compose.runtime.LaunchedEffect
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
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.example.data.local.ChatMessageEntity
import com.example.data.model.AppMode
import com.example.data.model.ChatMessage
import com.example.data.model.VoiceGender
import com.example.ui.components.PahadiDialectDropdown
import com.example.ui.components.SpeechListeningOverlay
import com.example.ui.theme.HimalayanGoldSecondary
import com.example.ui.theme.SaffronHimalaya
import com.example.ui.viewmodel.PahadiViewModel
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GeminiChatScreen(
    viewModel: PahadiViewModel,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val messages by viewModel.chatMessages.collectAsState()
    val culturalQaSessions by viewModel.culturalQaSessions.collectAsState()
    val isGenerating by viewModel.isChatGenerating.collectAsState()
    val chatInput by viewModel.chatInput.collectAsState()
    val currentMode by viewModel.appMode.collectAsState()
    val voiceGender by viewModel.voiceGender.collectAsState()
    val autoSpeak by viewModel.autoSpeakEnabled.collectAsState()
    val activeDialect by viewModel.targetDialect.collectAsState()

    // Live Speech Recognition states
    val isListening by viewModel.isListening.collectAsState()
    val partialTranscript by viewModel.partialSpeechTranscript.collectAsState()
    val rmsDb by viewModel.speechRmsDb.collectAsState()

    val listState = rememberLazyListState()
    var showClearConfirm by remember { mutableStateOf(false) }
    var showCulturalQaSheet by remember { mutableStateOf(false) }
    var showModelInfoDialog by remember { mutableStateOf(false) }

    // Auto-scroll to bottom whenever new messages arrive
    LaunchedEffect(messages.size, isGenerating) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
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
                Toast.makeText(context, "वॉइस इनपुट डिवाइस पर उपलब्ध नहीं है", Toast.LENGTH_SHORT).show()
            }
        } else {
            Toast.makeText(context, "बोलने के लिए माइक्रोफ़ोन की अनुमति आवश्यक है", Toast.LENGTH_SHORT).show()
        }
    }

    // Suggested quick prompt chips based on active mode
    val suggestedPrompts = when (currentMode) {
        AppMode.ELDER -> listOf(
            "🙏 जय देव जी, कैसे हैं?",
            "☀️ आज धूप और मौसम कैसा रहेगा?",
            "🍲 गर्म खान-पान व सेहत सलाह",
            "📞 आपातकालीन एम्बुलेंस नंबर"
        )
        AppMode.STUDENT -> listOf(
            "⛰️ हिमाचल प्रदेश का इतिहास व संस्कृति",
            "📝 पहाड़ी बोलियों की उत्पत्ति बताएं",
            "🔄 English → Hindi अनुवाद",
            "🌱 प्रकाश संश्लेषण समझाएं"
        )
        AppMode.FARMER -> listOf(
            "🍏 सेब के बगीचे में प्रूनिंग का समय",
            "🛡️ सेब स्कैब रोग नियंत्रण",
            "🌱 प्राकृतिक जीवामृत बनाने की विधि",
            "💰 एंटी-हेल नेट सब्सिडी योजना"
        )
        AppMode.STANDARD -> listOf(
            "🏔️ कुल्लू दशहरा व देव परंपरा",
            "🍲 पारंपरिक हिमाचली धाम के व्यंजन",
            "🗣️ कांगड़ी बोली में रोजमर्रा के वाक्य",
            "⚖️ चितई गोलू देवता की कथा"
        )
    }

    Box(modifier = modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.background)
                .testTag("gemini_chat_screen")
        ) {
            // Top Model Status & Controls Header
            Surface(
                tonalElevation = 2.dp,
                color = MaterialTheme.colorScheme.surface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(vertical = 4.dp)) {
                    // Row 1: Gemini AI Model badge & Quick actions
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 14.dp, vertical = 2.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Surface(
                            shape = RoundedCornerShape(20.dp),
                            color = SaffronHimalaya.copy(alpha = 0.12f),
                            border = CardDefaults.outlinedCardBorder().copy(
                                brush = androidx.compose.ui.graphics.SolidColor(SaffronHimalaya.copy(alpha = 0.4f))
                            ),
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp))
                                .clickable { showModelInfoDialog = true }
                                .testTag("gemini_model_status_badge")
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    imageVector = Icons.Default.AutoAwesome,
                                    contentDescription = null,
                                    tint = SaffronHimalaya,
                                    modifier = Modifier.size(15.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(
                                    text = if (viewModel.isGeminiAvailable) "Gemini 2.5 Flash • ऑनलाइन" else "Gemini AI • ऑफ़लाइन मोड",
                                    style = MaterialTheme.typography.labelMedium.copy(
                                        fontWeight = FontWeight.Bold,
                                        fontSize = 12.sp,
                                        color = if (viewModel.isGeminiAvailable) Color(0xFF047857) else SaffronHimalaya
                                    )
                                )
                            }
                        }

                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Surface(
                                shape = RoundedCornerShape(6.dp),
                                color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.6f),
                                modifier = Modifier
                                    .clip(RoundedCornerShape(6.dp))
                                    .clickable { showCulturalQaSheet = true }
                            ) {
                                Text(
                                    text = "🏛️ सत्र (${culturalQaSessions.size})",
                                    style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold, fontSize = 11.sp),
                                    modifier = Modifier.padding(horizontal = 7.dp, vertical = 3.dp)
                                )
                            }

                            Spacer(modifier = Modifier.width(6.dp))

                            IconButton(
                                onClick = { showClearConfirm = true },
                                modifier = Modifier
                                    .size(28.dp)
                                    .testTag("clear_chat_button")
                            ) {
                                Icon(
                                    imageVector = Icons.Default.DeleteSweep,
                                    contentDescription = "Clear Chat",
                                    tint = Color.Gray,
                                    modifier = Modifier.size(18.dp)
                                )
                            }
                        }
                    }

                    // Row 2: Mode Selector Pills & Voice Quick Toggles (Scrollable)
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .horizontalScroll(rememberScrollState())
                            .padding(horizontal = 12.dp, vertical = 2.dp),
                        horizontalArrangement = Arrangement.spacedBy(6.dp),
                        verticalAlignment = Alignment.CenterVertically
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
                                        modifier = Modifier.size(15.dp)
                                    )
                                },
                                label = {
                                    Text(
                                        mode.titleHindi,
                                        fontSize = 11.sp,
                                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal
                                    )
                                }
                            )
                        }

                        // Voice Gender Toggle
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.7f),
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .clickable { viewModel.toggleVoiceGender() }
                        ) {
                            Text(
                                text = if (voiceGender == VoiceGender.FEMALE) "महिला 👩" else "पुरुष 👨",
                                style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.SemiBold, fontSize = 11.sp),
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 6.dp)
                            )
                        }

                        // Auto Speak Toggle
                        Surface(
                            shape = RoundedCornerShape(8.dp),
                            color = if (autoSpeak) Color(0xFF10B981).copy(alpha = 0.2f) else Color.Gray.copy(alpha = 0.2f),
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .clickable { viewModel.toggleAutoSpeak() }
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 6.dp)
                            ) {
                                Icon(
                                    imageVector = if (autoSpeak) Icons.AutoMirrored.Filled.VolumeUp else Icons.AutoMirrored.Filled.VolumeOff,
                                    contentDescription = null,
                                    modifier = Modifier.size(14.dp),
                                    tint = if (autoSpeak) Color(0xFF047857) else Color.DarkGray
                                )
                                Spacer(modifier = Modifier.width(3.dp))
                                Text(
                                    text = if (autoSpeak) "ध्वनि चालू" else "म्यूट",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }
                }
            }

            // Scrollable Message List
            LazyColumn(
                state = listState,
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .padding(horizontal = 14.dp)
                    .testTag("conversational_messages_list"),
                verticalArrangement = Arrangement.spacedBy(10.dp),
                contentPadding = PaddingValues(vertical = 12.dp)
            ) {
                items(messages, key = { it.id }) { message ->
                    GeminiMessageBubble(
                        message = message,
                        isElderMode = currentMode == AppMode.ELDER,
                        onSpeak = { viewModel.speakText(message.text) },
                        onCopy = {
                            val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                            clipboard.setPrimaryClip(ClipData.newPlainText("Chat Message", message.text))
                            Toast.makeText(context, "कॉपी किया गया", Toast.LENGTH_SHORT).show()
                        }
                    )
                }

                if (isGenerating) {
                    item {
                        GeminiThinkingBubble(isElderMode = currentMode == AppMode.ELDER)
                    }
                }
            }

            // Suggested Prompt Chips (Quick Questions)
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(horizontal = 14.dp, vertical = 4.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                suggestedPrompts.forEach { prompt ->
                    SuggestionChip(
                        onClick = { viewModel.sendChatMessage(prompt) },
                        label = { Text(prompt, fontSize = 12.sp) },
                        modifier = Modifier.testTag("prompt_chip_${prompt.hashCode()}")
                    )
                }
            }

            // Conversational Text Input Field & Action Buttons
            Surface(
                tonalElevation = 4.dp,
                color = MaterialTheme.colorScheme.surface,
                modifier = Modifier.fillMaxWidth()
            ) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = chatInput,
                        onValueChange = { viewModel.setChatInput(it) },
                        placeholder = {
                            Text(
                                text = "Gemini से पूछें (उदा. 'कुल्लू का मौसम')...",
                                fontSize = if (currentMode == AppMode.ELDER) 15.sp else 13.sp,
                                maxLines = 1
                            )
                        },
                        leadingIcon = {
                            Icon(
                                imageVector = Icons.Default.AutoAwesome,
                                contentDescription = null,
                                tint = SaffronHimalaya,
                                modifier = Modifier.size(18.dp)
                            )
                        },
                        trailingIcon = {
                            if (chatInput.isNotBlank()) {
                                IconButton(
                                    onClick = { viewModel.setChatInput("") },
                                    modifier = Modifier.size(24.dp)
                                ) {
                                    Icon(
                                        imageVector = Icons.Default.Clear,
                                        contentDescription = "Clear Input",
                                        tint = Color.Gray,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                        },
                        singleLine = true,
                        shape = RoundedCornerShape(24.dp),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                        keyboardActions = KeyboardActions(
                            onSend = {
                                if (chatInput.isNotBlank() && !isGenerating) {
                                    viewModel.sendChatMessage()
                                }
                            }
                        ),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = MaterialTheme.colorScheme.primary,
                            unfocusedBorderColor = MaterialTheme.colorScheme.outlineVariant
                        ),
                        modifier = Modifier
                            .weight(1f)
                            .testTag("conversational_text_input")
                    )

                    Spacer(modifier = Modifier.width(8.dp))

                    // Microphone Voice Input Button
                    Surface(
                        shape = CircleShape,
                        color = if (isListening) Color(0xFFEF4444) else MaterialTheme.colorScheme.secondaryContainer,
                        modifier = Modifier
                            .size(46.dp)
                            .clickable {
                                if (isListening) {
                                    viewModel.stopSpeechRecognition()
                                } else {
                                    val hasRecordPermission = ContextCompat.checkSelfPermission(
                                        context,
                                        Manifest.permission.RECORD_AUDIO
                                    ) == PackageManager.PERMISSION_GRANTED

                                    if (hasRecordPermission) {
                                        viewModel.startSpeechRecognition("hi-IN") { text ->
                                            viewModel.sendChatMessage(text)
                                        }
                                    } else {
                                        permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
                                    }
                                }
                            }
                            .testTag("conversational_mic_button")
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Default.Mic,
                                contentDescription = "Voice Input",
                                tint = if (isListening) Color.White else MaterialTheme.colorScheme.onSecondaryContainer,
                                modifier = Modifier.size(22.dp)
                            )
                        }
                    }

                    Spacer(modifier = Modifier.width(6.dp))

                    // Send Button
                    Surface(
                        shape = CircleShape,
                        color = if (chatInput.isNotBlank() && !isGenerating) {
                            MaterialTheme.colorScheme.primary
                        } else {
                            MaterialTheme.colorScheme.surfaceVariant
                        },
                        modifier = Modifier
                            .size(46.dp)
                            .clickable(enabled = chatInput.isNotBlank() && !isGenerating) {
                                viewModel.sendChatMessage()
                            }
                            .testTag("conversational_send_button")
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            if (isGenerating) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(20.dp),
                                    strokeWidth = 2.dp,
                                    color = MaterialTheme.colorScheme.primary
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.Send,
                                    contentDescription = "Send Message",
                                    tint = if (chatInput.isNotBlank()) Color.White else Color.Gray,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                        }
                    }
                }
            }
        }

        // Live Speech Recognition Pulse & Subtitle Overlay
        SpeechListeningOverlay(
            isListening = isListening,
            partialText = partialTranscript,
            rmsDb = rmsDb,
            targetDialectName = activeDialect.displayNameHindi.substringBefore(" ("),
            onStopListening = { viewModel.stopSpeechRecognition() },
            onCancelListening = { viewModel.cancelSpeechRecognition() },
            modifier = Modifier.align(Alignment.BottomCenter)
        )

        // Clear Chat History Confirmation Dialog
        if (showClearConfirm) {
            AlertDialog(
                onDismissRequest = { showClearConfirm = false },
                title = { Text("बातचीत इतिहास साफ़ करें?", fontWeight = FontWeight.Bold) },
                text = { Text("क्या आप सभी बातचीत और सांस्कृतिक Q&A सत्र हटाना चाहते हैं? यह लोकल Room डेटाबेस से सुरक्षित रूप से साफ़ हो जाएगा।") },
                confirmButton = {
                    TextButton(
                        onClick = {
                            viewModel.clearChatHistory()
                            showClearConfirm = false
                        }
                    ) {
                        Text("हाँ, साफ़ करें", color = MaterialTheme.colorScheme.error, fontWeight = FontWeight.Bold)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showClearConfirm = false }) {
                        Text("रद्द करें")
                    }
                }
            )
        }

        // Gemini AI Model Info Dialog
        if (showModelInfoDialog) {
            AlertDialog(
                onDismissRequest = { showModelInfoDialog = false },
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = SaffronHimalaya)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Google Gemini AI मॉडल", fontWeight = FontWeight.Bold)
                    }
                },
                text = {
                    Column {
                        Text(
                            text = "यह ऐप Google Gemini AI (gemini-2.5-flash) मॉडल का उपयोग करता है, जिससे आप हिमाचली व गढ़वाली-कुमाऊँनी बोलियों में सहज बातचीत कर सकते हैं।",
                            style = MaterialTheme.typography.bodyMedium
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(
                            text = if (viewModel.isGeminiAvailable) {
                                "✅ API Key सक्रिय है। आप लाइव Gemini मॉडल से जुड़े हैं।"
                            } else {
                                "ℹ️ वर्तमान में लोकल ऑफ़लाइन नॉलेज इंजन सक्रिय है। यदि आपके पास Gemini API key है, तो उसे AI Studio के Secrets panel में 'GEMINI_API_KEY' नाम से जोड़ें।"
                            },
                            style = MaterialTheme.typography.bodySmall.copy(color = Color.DarkGray)
                        )
                    }
                },
                confirmButton = {
                    Button(onClick = { showModelInfoDialog = false }) {
                        Text("ठीक है")
                    }
                }
            )
        }

        // Cultural Q&A Sessions Bottom Sheet
        if (showCulturalQaSheet) {
            ModalBottomSheet(
                onDismissRequest = { showCulturalQaSheet = false },
                sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    Text(
                        text = "🏛️ सहेजे गए सांस्कृतिक Q&A सत्र",
                        style = MaterialTheme.typography.titleLarge.copy(
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary
                        )
                    )
                    Text(
                        text = "पहाड़ी मेलों, लोकदेवताओं, परंपराओं और खेती पर आपके प्रश्न Room डेटाबेस में सुरक्षित हैं:",
                        style = MaterialTheme.typography.bodySmall.copy(color = Color.Gray)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    HorizontalDivider()
                    Spacer(modifier = Modifier.height(8.dp))

                    if (culturalQaSessions.isEmpty()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(32.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = "अभी कोई सांस्कृतिक प्रश्न सहेजा नहीं गया है।\nत्योहारों, देव परंपरा या इतिहास के बारे में पूछें!",
                                textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                                color = Color.Gray
                            )
                        }
                    } else {
                        LazyColumn(
                            verticalArrangement = Arrangement.spacedBy(8.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .heightIn(max = 420.dp)
                        ) {
                            items(culturalQaSessions) { qa ->
                                Card(
                                    shape = RoundedCornerShape(12.dp),
                                    colors = CardDefaults.cardColors(
                                        containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                                    ),
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            viewModel.speakText(qa.text)
                                        }
                                ) {
                                    Column(modifier = Modifier.padding(12.dp)) {
                                        Row(
                                            modifier = Modifier.fillMaxWidth(),
                                            horizontalArrangement = Arrangement.SpaceBetween
                                        ) {
                                            Text(
                                                text = if (qa.isUser) "प्रश्न (User Q):" else "उत्तर (Gemini AI):",
                                                style = MaterialTheme.typography.labelSmall.copy(
                                                    color = if (qa.isUser) MaterialTheme.colorScheme.primary else SaffronHimalaya,
                                                    fontWeight = FontWeight.Bold
                                                )
                                            )
                                            Text(
                                                text = "🔊 टैप करके सुनें",
                                                style = MaterialTheme.typography.labelSmall.copy(
                                                    color = Color.Gray,
                                                    fontSize = 10.sp
                                                )
                                            )
                                        }
                                        Spacer(modifier = Modifier.height(4.dp))
                                        Text(
                                            text = qa.text,
                                            style = MaterialTheme.typography.bodyMedium
                                        )
                                    }
                                }
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
    }
}

@Composable
fun GeminiMessageBubble(
    message: ChatMessage,
    isElderMode: Boolean,
    onSpeak: () -> Unit,
    onCopy: () -> Unit
) {
    val isUser = message.isUser
    val timeFormatter = remember { SimpleDateFormat("hh:mm a", Locale.getDefault()) }
    val formattedTime = remember(message.timestamp) { timeFormatter.format(Date(message.timestamp)) }

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
                        imageVector = Icons.Default.AutoAwesome,
                        contentDescription = "Gemini AI",
                        tint = SaffronHimalaya,
                        modifier = Modifier.size(if (isElderMode) 22.dp else 18.dp)
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
                containerColor = if (isUser) {
                    MaterialTheme.colorScheme.primary
                } else {
                    MaterialTheme.colorScheme.surfaceVariant
                }
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
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "Gemini AI",
                                style = MaterialTheme.typography.labelSmall.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = SaffronHimalaya
                                )
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Surface(
                                shape = RoundedCornerShape(4.dp),
                                color = SaffronHimalaya.copy(alpha = 0.15f)
                            ) {
                                Text(
                                    text = "2.5 Flash",
                                    style = MaterialTheme.typography.labelSmall.copy(
                                        fontSize = 9.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = SaffronHimalaya
                                    ),
                                    modifier = Modifier.padding(horizontal = 4.dp, vertical = 1.dp)
                                )
                            }
                        }

                        Text(
                            text = formattedTime,
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = Color.Gray,
                                fontSize = 10.sp
                            )
                        )
                    }
                    Spacer(modifier = Modifier.height(4.dp))
                }

                Text(
                    text = message.text,
                    style = if (isElderMode) {
                        MaterialTheme.typography.bodyLarge.copy(
                            fontSize = 18.sp,
                            lineHeight = 26.sp,
                            fontWeight = FontWeight.Medium
                        )
                    } else {
                        MaterialTheme.typography.bodyMedium.copy(
                            lineHeight = 22.sp
                        )
                    },
                    color = if (isUser) Color.White else MaterialTheme.colorScheme.onSurface
                )

                Spacer(modifier = Modifier.height(6.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (isUser) {
                        Text(
                            text = formattedTime,
                            style = MaterialTheme.typography.labelSmall.copy(
                                color = Color.White.copy(alpha = 0.7f),
                                fontSize = 10.sp
                            )
                        )
                    } else {
                        Spacer(modifier = Modifier.width(4.dp))
                    }

                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        IconButton(
                            onClick = onCopy,
                            modifier = Modifier.size(28.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.ContentCopy,
                                contentDescription = "Copy Text",
                                tint = if (isUser) Color.White.copy(alpha = 0.8f) else Color.Gray,
                                modifier = Modifier.size(15.dp)
                            )
                        }

                        if (!isUser) {
                            IconButton(
                                onClick = onSpeak,
                                modifier = Modifier.size(28.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                                    contentDescription = "Speak Text",
                                    tint = SaffronHimalaya,
                                    modifier = Modifier.size(17.dp)
                                )
                            }
                        }
                    }
                }
            }
        }

        if (isUser) {
            Spacer(modifier = Modifier.width(8.dp))
            Surface(
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier
                    .size(if (isElderMode) 40.dp else 34.dp)
                    .padding(top = 2.dp)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        imageVector = Icons.Default.Person,
                        contentDescription = "User",
                        tint = MaterialTheme.colorScheme.onPrimaryContainer,
                        modifier = Modifier.size(if (isElderMode) 22.dp else 18.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun GeminiThinkingBubble(isElderMode: Boolean) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Start,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(
            shape = CircleShape,
            color = SaffronHimalaya.copy(alpha = 0.2f),
            modifier = Modifier.size(if (isElderMode) 40.dp else 34.dp)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Icon(
                    imageVector = Icons.Default.AutoAwesome,
                    contentDescription = "Thinking",
                    tint = SaffronHimalaya,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
        Spacer(modifier = Modifier.width(8.dp))
        Surface(
            shape = RoundedCornerShape(16.dp),
            color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.7f)
        ) {
            Row(
                modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                CircularProgressIndicator(
                    modifier = Modifier.size(14.dp),
                    strokeWidth = 2.dp,
                    color = SaffronHimalaya
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "Gemini AI उत्तर तैयार कर रहा है...",
                    style = MaterialTheme.typography.bodySmall.copy(
                        color = Color.Gray,
                        fontStyle = androidx.compose.ui.text.font.FontStyle.Italic
                    )
                )
            }
        }
    }
}
