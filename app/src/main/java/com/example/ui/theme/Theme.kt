package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DarkColorScheme = darkColorScheme(
    primary = HimalayanTealDarkPrimary,
    onPrimary = HimalayanTealDarkOnPrimary,
    primaryContainer = HimalayanTealDarkContainer,
    onPrimaryContainer = HimalayanTealDarkOnContainer,
    secondary = HimalayanGoldDarkSecondary,
    onSecondary = HimalayanGoldDarkOnSecondary,
    secondaryContainer = HimalayanGoldDarkContainer,
    onSecondaryContainer = HimalayanGoldDarkOnContainer,
    tertiary = HimalayanPineDarkTertiary,
    onTertiary = HimalayanPineDarkOnTertiary,
    tertiaryContainer = HimalayanPineDarkContainer,
    onTertiaryContainer = HimalayanPineDarkOnContainer,
    background = HimalayanBackgroundDark,
    surface = HimalayanSurfaceDark,
    surfaceVariant = HimalayanSurfaceVariantDark,
    onSurface = HimalayanOnSurfaceDark,
    outline = HimalayanOutlineDark
)

private val LightColorScheme = lightColorScheme(
    primary = HimalayanTealPrimary,
    onPrimary = HimalayanTealOnPrimary,
    primaryContainer = HimalayanTealContainer,
    onPrimaryContainer = HimalayanTealOnContainer,
    secondary = HimalayanGoldSecondary,
    onSecondary = HimalayanGoldOnSecondary,
    secondaryContainer = HimalayanGoldContainer,
    onSecondaryContainer = HimalayanGoldOnContainer,
    tertiary = HimalayanPineTertiary,
    onTertiary = HimalayanPineOnTertiary,
    tertiaryContainer = HimalayanPineContainer,
    onTertiaryContainer = HimalayanPineOnContainer,
    background = HimalayanBackgroundLight,
    surface = HimalayanSurfaceLight,
    surfaceVariant = HimalayanSurfaceVariantLight,
    onSurface = HimalayanOnSurfaceLight,
    outline = HimalayanOutlineLight
)

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false, // Use our rich Himalayan palette by default
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
