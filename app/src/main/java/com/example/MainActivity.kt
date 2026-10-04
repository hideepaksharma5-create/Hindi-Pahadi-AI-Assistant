package com.example

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Mic
import androidx.compose.material.icons.filled.Translate
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.unit.dp
import com.example.ui.components.HimalayanHeader
import com.example.ui.screens.HeritageScreen
import com.example.ui.screens.HimachalKnowledgeScreen
import com.example.ui.screens.PahadiMitraScreen
import com.example.ui.screens.SavedScreen
import com.example.ui.screens.TranslatorScreen
import com.example.ui.theme.MyApplicationTheme
import com.example.ui.viewmodel.PahadiViewModel

enum class PahadiNavTab(
    val titleRes: Int,
    val hindiTitle: String,
    val icon: ImageVector,
    val testTag: String
) {
    TRANSLATE(R.string.tab_translate, "अनुवाद", Icons.Default.Translate, "nav_translate"),
    VOICE_AI(R.string.tab_assistant, "पहाड़ी AI", Icons.Default.Mic, "nav_mitra"),
    HIMACHAL(R.string.tab_knowledge, "स्थानिक ज्ञान", Icons.Default.Info, "nav_himachal"),
    HERITAGE(R.string.tab_phrasebook, "धरोहर", Icons.Default.MenuBook, "nav_heritage"),
    SAVED(R.string.tab_saved, "सहेजे गए", Icons.Default.Bookmark, "nav_saved")
}

class MainActivity : ComponentActivity() {

    private val viewModel: PahadiViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyApplicationTheme {
                PahadiAppRoot(viewModel = viewModel)
            }
        }
    }
}

@Composable
fun PahadiAppRoot(viewModel: PahadiViewModel) {
    var selectedTabIndex by rememberSaveable { mutableIntStateOf(0) }
    val tabs = PahadiNavTab.entries

    val currentDialect by viewModel.targetDialect.collectAsState()

    BackHandler(enabled = selectedTabIndex != 0) {
        selectedTabIndex = 0
    }

    Scaffold(
        modifier = Modifier.fillMaxSize(),
        topBar = {
            HimalayanHeader(
                isAiConnected = viewModel.isGeminiAvailable,
                currentDialect = currentDialect,
                onDialectSelected = { viewModel.setTargetDialect(it) }
            )
        },
        bottomBar = {
            NavigationBar(
                modifier = Modifier.testTag("pahadi_bottom_nav"),
                containerColor = MaterialTheme.colorScheme.surface,
                tonalElevation = 8.dp
            ) {
                tabs.forEachIndexed { index, tab ->
                    val isSelected = selectedTabIndex == index
                    NavigationBarItem(
                        selected = isSelected,
                        onClick = { selectedTabIndex = index },
                        icon = {
                            Icon(
                                imageVector = tab.icon,
                                contentDescription = tab.hindiTitle
                            )
                        },
                        label = { Text(tab.hindiTitle) },
                        colors = NavigationBarItemDefaults.colors(
                            selectedIconColor = MaterialTheme.colorScheme.primary,
                            selectedTextColor = MaterialTheme.colorScheme.primary,
                            indicatorColor = MaterialTheme.colorScheme.primaryContainer
                        ),
                        modifier = Modifier.testTag(tab.testTag)
                    )
                }
            }
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(MaterialTheme.colorScheme.background)
        ) {
            when (selectedTabIndex) {
                0 -> TranslatorScreen(
                    viewModel = viewModel,
                    modifier = Modifier.fillMaxSize()
                )
                1 -> PahadiMitraScreen(
                    viewModel = viewModel,
                    modifier = Modifier.fillMaxSize()
                )
                2 -> HimachalKnowledgeScreen(
                    viewModel = viewModel,
                    onAskInChat = { question ->
                        viewModel.setChatInput(question)
                        selectedTabIndex = 1
                        viewModel.sendChatMessage(question)
                    },
                    modifier = Modifier.fillMaxSize()
                )
                3 -> HeritageScreen(
                    viewModel = viewModel,
                    onNavigateToTranslator = { text, dialect ->
                        viewModel.setInputText(text)
                        viewModel.setTargetDialect(dialect)
                        selectedTabIndex = 0
                        viewModel.translateNow()
                    },
                    onAskInChat = { question ->
                        viewModel.setChatInput(question)
                        selectedTabIndex = 1
                        viewModel.sendChatMessage(question)
                    },
                    modifier = Modifier.fillMaxSize()
                )
                4 -> SavedScreen(
                    viewModel = viewModel,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    }
}
