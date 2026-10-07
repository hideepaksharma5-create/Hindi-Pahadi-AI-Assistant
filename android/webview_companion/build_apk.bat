@echo off
setlocal
echo ===================================================
echo   Building Pahadi AI Android APK (पहाड़ी संगम)
echo ===================================================

rem 1. Set JAVA_HOME to Android Studio JBR
if exist "C:\Program Files\Android\Android Studio\jbr" (
    set "JAVA_HOME=C:\Program Files\Android\Android Studio\jbr"
) else (
    echo [Notice] Android Studio JBR not found in default path, using system JAVA_HOME.
)

rem 2. Set ANDROID_HOME to standard SDK location
if exist "%LOCALAPPDATA%\Android\Sdk" (
    set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
)

echo Using JAVA_HOME: %JAVA_HOME%
echo Using ANDROID_HOME: %ANDROID_HOME%
echo.

cd /d "%~dp0"
call gradlew.bat assembleDebug

echo.
if exist "app\build\outputs\apk\debug\app-debug.apk" (
    echo ===================================================
    echo   BUILD SUCCESSFUL! 🎉
    echo   APK Generated at:
    echo   %~dp0app\build\outputs\apk\debug\app-debug.apk
    echo ===================================================
) else (
    echo.
    echo If building from command-line needs SDK packages, you can
    echo open this folder directly in Android Studio:
    echo File -^> Open -^> "%~dp0"
    echo and click "Build -^> Build Bundle(s) / APK(s) -^> Build APK(s)"
)
pause
