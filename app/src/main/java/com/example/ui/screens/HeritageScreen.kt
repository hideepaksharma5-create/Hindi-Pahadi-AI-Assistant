package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.size
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Landscape
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.data.model.PahadiDialect
import com.example.ui.viewmodel.PahadiViewModel

@Composable
fun HeritageScreen(
    viewModel: PahadiViewModel,
    onNavigateToTranslator: (String, PahadiDialect) -> Unit,
    onAskInChat: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var selectedSubTab by remember { mutableIntStateOf(0) }

    Column(
        modifier = modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        TabRow(selectedTabIndex = selectedSubTab) {
            Tab(
                selected = selectedSubTab == 0,
                onClick = { selectedSubTab = 0 },
                text = { Text("पहाड़ी शब्दकोश (Phrases)") },
                icon = { Icon(Icons.Default.MenuBook, contentDescription = null, modifier = Modifier.size(18.dp)) }
            )
            Tab(
                selected = selectedSubTab == 1,
                onClick = { selectedSubTab = 1 },
                text = { Text("लोक गाथाएं (Folk Lore)") },
                icon = { Icon(Icons.Default.Landscape, contentDescription = null, modifier = Modifier.size(18.dp)) }
            )
        }

        Box(modifier = Modifier.fillMaxSize()) {
            when (selectedSubTab) {
                0 -> PhrasebookScreen(
                    viewModel = viewModel,
                    onNavigateToTranslator = onNavigateToTranslator,
                    modifier = Modifier.fillMaxSize()
                )
                1 -> CulturalLoreScreen(
                    viewModel = viewModel,
                    onAskInChat = onAskInChat,
                    modifier = Modifier.fillMaxSize()
                )
            }
        }
    }
}
