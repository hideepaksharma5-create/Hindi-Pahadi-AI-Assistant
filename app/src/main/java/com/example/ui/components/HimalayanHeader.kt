package com.example.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Landscape
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.PahadiDialect
import com.example.ui.theme.SaffronHimalaya

@Composable
fun HimalayanHeader(
    modifier: Modifier = Modifier,
    isAiConnected: Boolean = true,
    currentDialect: PahadiDialect? = null,
    onDialectSelected: ((PahadiDialect) -> Unit)? = null
) {
    var showInfoDialog by remember { mutableStateOf(false) }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .background(
                brush = Brush.verticalGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.primary,
                        MaterialTheme.colorScheme.primary.copy(alpha = 0.88f)
                    )
                )
            )
            .testTag("himalayan_header")
    ) {
        // Decorative Mountain Ridge Canvas
        Canvas(
            modifier = Modifier
                .fillMaxWidth()
                .height(96.dp)
                .align(Alignment.BottomCenter)
        ) {
            val w = size.width
            val h = size.height

            // Distant mountain silhouette
            val distantPath = Path().apply {
                moveTo(0f, h)
                lineTo(0f, h * 0.55f)
                lineTo(w * 0.22f, h * 0.28f)
                lineTo(w * 0.44f, h * 0.48f)
                lineTo(w * 0.68f, h * 0.22f)
                lineTo(w * 0.88f, h * 0.42f)
                lineTo(w, h * 0.30f)
                lineTo(w, h)
                close()
            }
            drawPath(
                path = distantPath,
                color = Color.White.copy(alpha = 0.08f)
            )

            // Foreground snow-peak outline
            val forePath = Path().apply {
                moveTo(0f, h)
                lineTo(0f, h * 0.72f)
                lineTo(w * 0.32f, h * 0.42f)
                lineTo(w * 0.52f, h * 0.65f)
                lineTo(w * 0.80f, h * 0.38f)
                lineTo(w, h * 0.60f)
                lineTo(w, h)
                close()
            }
            drawPath(
                path = forePath,
                color = Color.White.copy(alpha = 0.14f)
            )

            // Prayer flag dots across ridge
            val flagColors = listOf(Color(0xFF3B82F6), Color.White, Color(0xFFEF4444), Color(0xFF10B981), Color(0xFFF59E0B))
            for (i in 0..12) {
                val cx = (w / 12) * i
                val cy = h * 0.45f + (if (i % 2 == 0) -4f else 4f)
                drawCircle(
                    color = flagColors[i % flagColors.size].copy(alpha = 0.7f),
                    radius = 3.5f,
                    center = Offset(cx, cy)
                )
            }
        }

        // Header Content
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .statusBarsPadding()
                .padding(horizontal = 16.dp, vertical = 10.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Surface(
                        shape = RoundedCornerShape(12.dp),
                        color = Color.White.copy(alpha = 0.2f),
                        modifier = Modifier.size(44.dp)
                    ) {
                        Box(contentAlignment = Alignment.Center) {
                            Icon(
                                imageVector = Icons.Default.Landscape,
                                contentDescription = "Pahadi Logo",
                                tint = SaffronHimalaya,
                                modifier = Modifier.size(28.dp)
                            )
                        }
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                text = "पहाड़ी संगम",
                                style = MaterialTheme.typography.titleLarge.copy(
                                    fontWeight = FontWeight.Bold,
                                    color = Color.White
                                )
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Surface(
                                shape = RoundedCornerShape(4.dp),
                                color = SaffronHimalaya
                            ) {
                                Text(
                                    text = "AI",
                                    color = Color.White,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    modifier = Modifier.padding(horizontal = 5.dp, vertical = 1.dp)
                                )
                            }
                        }
                        Text(
                            text = "Himalayan Dialects & Cultural Guide",
                            style = MaterialTheme.typography.bodySmall.copy(
                                color = Color.White.copy(alpha = 0.85f)
                            )
                        )
                    }
                }

                Row(verticalAlignment = Alignment.CenterVertically) {
                    if (currentDialect != null && onDialectSelected != null) {
                        PahadiDialectDropdown(
                            selectedDialect = currentDialect,
                            onDialectSelected = onDialectSelected,
                            compact = true
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                    }

                    IconButton(
                        onClick = { showInfoDialog = true },
                        modifier = Modifier.testTag("header_info_button")
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info,
                            contentDescription = "About Pahadi Languages",
                            tint = Color.White
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(6.dp))

            // Sub-bar showing supported regions
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "गढ़वाली • कुमाऊँनी • कांगड़ी • मंडीयाली • कुल्लवी • डोगरी",
                    style = MaterialTheme.typography.labelSmall.copy(
                        color = Color.White.copy(alpha = 0.8f)
                    )
                )

                Surface(
                    shape = RoundedCornerShape(12.dp),
                    color = if (isAiConnected) Color(0xFF10B981).copy(alpha = 0.25f) else Color(0xFFF59E0B).copy(alpha = 0.25f)
                ) {
                    Text(
                        text = if (isAiConnected) "● Gemini AI Active" else "● Hybrid Engine",
                        style = MaterialTheme.typography.labelSmall.copy(
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold
                        ),
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 2.dp)
                    )
                }
            }
        }
    }

    if (showInfoDialog) {
        AlertDialog(
            onDismissRequest = { showInfoDialog = false },
            title = {
                Text("हिमालयी बोलियां व सांस्कृतिक धरोहर", fontWeight = FontWeight.Bold)
            },
            text = {
                Column {
                    Text(
                        "यह ऐप उत्तराखंड और हिमाचल प्रदेश की समृद्ध पहाड़ी बोलियों के संरक्षण, सटीक अनुवाद और सांस्कृतिक समझ के लिए समर्पित है।\n\n" +
                                "• गढ़वाली व कुमाऊँनी (उत्तराखंड)\n" +
                                "• कांगड़ी, मंडीयाली, कुल्लवी, महासूवी (हिमाचल प्रदेश)\n" +
                                "• डोगरी व जौनसारी\n\n" +
                                "प्रत्येक अनुवाद के साथ आपको लोक-शिष्टाचार (पैलाग, दगड़्या), सामाजिक संदर्भ और देवभूमि की लोकगाथाओं का समृद्ध ज्ञान प्राप्त होगा।",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            },
            confirmButton = {
                TextButton(onClick = { showInfoDialog = false }) {
                    Text("धन्यवाद (समझ गए)")
                }
            }
        )
    }
}
