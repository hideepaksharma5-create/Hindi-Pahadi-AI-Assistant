# 🏔️ Pahadi AI Assistant - Android APK Project (पहाड़ी संगम)

यह Pahadi AI Assistant का आधिकारिक Android Studio प्रोजेक्ट है। इसमें सम्पूर्ण नेटिव WebView, माइक्रोफ़ोन व आवाज़ रिकॉर्डिंग अनुमति (Audio Permissions), ऑफ़लाइन फ़ॉलबैक और सर्वर सेलेक्टर पहले से कॉन्फ़िगर किया गया है।

---

## 📱 APK बनाने के 2 आसान तरीके (How to Build APK)

### तरीका 1: Android Studio से (सबसे आसान - 1 Click Build)

1. अपने कंप्यूटर पर **Android Studio** खोलें।
2. **File -> Open...** पर क्लिक करें और इस फ़ोल्डर को चुनें:
   ```
   C:\A_I assistant\Hindi-Pahadi-AI-Assistant\android_app
   ```
3. Android Studio प्रोजेक्ट को लोड और सिंक (Sync) करेगा।
4. ऊपर मेनू बार से क्लिक करें:
   ```
   Build -> Build Bundle(s) / APK(s) -> Build APK(s)
   ```
5. कुछ ही पलों में नीचे दाएँ कोने में संदेश आएगा:
   **`APK(s) generated successfully. locate`**
6. **locate** पर क्लिक करें — आपका **`app-debug.apk`** तैयार है!
7. इस APK फ़ाइल को अपने Android फ़ोन में भेजकर इंस्टॉल करें।

---

### तरीका 2: एक क्लिक में कमांड से (One-Click Batch Script)

इस फ़ोल्डर में दी गई `build_apk.bat` फ़ाइल पर **Double-Click** करें:
```
build_apk.bat
```
यह स्वचालित रूप से Android Studio के Java/JBR का उपयोग करके APK तैयार कर देगा:
```
android_app\app\build\outputs\apk\debug\app-debug.apk
```

---

## ⚙️ मुख्य विशेषताएं (Key Features):

1. **🎙️ माइक्रोफ़ोन और आवाज़ क्लोनिंग (Microphone & Voice Clone)**:
   - ऐप में `RECORD_AUDIO` और `MODIFY_AUDIO_SETTINGS` अनुमतियाँ शामिल हैं।
   - WebView का `WebChromeClient` आंतरिक रूप से HTML5 माइक एक्सेस को स्वतः अनुमति देता है, जिससे वॉइस रिकॉर्डिंग और वॉइस क्लोनिंग बिना किसी रुकावट के काम करती है।

2. **🌐 ऑटो वाई-फ़ाई सर्वर कनेक्शन (Auto Wi-Fi Connect)**:
   - ऐप में आपका लोकल वाई-फ़ाई IP (`http://10.255.7.20:8080`) डिफ़ॉल्ट रूप से सेट है।
   - यदि आप Android Emulator में चला रहे हैं, तो यह `http://10.0.2.2:8080` पर कनेक्ट होता है।
   - ऐप में ऊपर दिए गए मेनू से **"सर्वर सेटिंग्स (Server Settings)"** दबाकर आप कभी भी अपना सर्वर URL बदल सकते हैं।

3. **🏔️ सुंदर हिमालयन UI और ऑफ़लाइन रिकवरी**:
   - यदि कभी कंप्यूटर पर सर्वर बंद हो या वाई-फ़ाई डिस्कनेक्ट हो, तो ऐप सुंदर पहाड़ी थीम वाला ऑफ़लाइन संदेश और "पुनः प्रयास करें (Retry)" का बटन दिखाता है।
