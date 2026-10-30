"""
i18n.py
-------
Multi-language support for AgriDoctor AI (English, Tamil, Hindi).

This is intentionally a plain Python dictionary rather than a translation
framework/library -- for a hackathon prototype with a fixed set of UI
strings, that keeps the feature dependency-free and easy for a non-native
speaker to review, correct, or extend (just edit the strings below).

Three lookups are provided:
  - t(key, lang)                         -> a UI label/sentence
  - localize_disease_info(class_name, info, lang) -> a translated copy of
    the crop/disease/description/remedy dict returned by
    database.get_disease_info(), for display only (the English version is
    still what gets logged to the database, so history stays consistent
    across language switches)
  - SEVERITY_LABELS / t_severity(severity, lang) -> translated severity word
"""

LANGUAGES = {
    "en": "English",
    "ta": "தமிழ் (Tamil)",
    "hi": "हिंदी (Hindi)",
}

# Maps to BCP-47 language codes for the browser's speech recognition / TTS.
TTS_LANG_CODE = {
    "en": "en-IN",
    "ta": "ta-IN",
    "hi": "hi-IN",
}

TRANSLATIONS = {
    # ---- App shell / sidebar ----
    "app_title": {"en": "AgriDoctor AI", "ta": "அக்ரிடாக்டர் AI", "hi": "एग्रीडॉक्टर AI"},
    "tagline": {
        "en": "AI-based crop disease detection, from any smartphone camera.",
        "ta": "எந்த ஸ்மார்ட்போன் கேமராவிலிருந்தும் AI அடிப்படையிலான பயிர் நோய் கண்டறிதல்.",
        "hi": "किसी भी स्मार्टफ़ोन कैमरे से AI-आधारित फ़सल रोग पहचान।",
    },
    "nav_scan": {"en": "🩺 Scan a Leaf", "ta": "🩺 இலையை ஸ்கேன் செய்யவும்", "hi": "🩺 पत्ती स्कैन करें"},
    "nav_reports": {"en": "📊 Reports & History", "ta": "📊 அறிக்கைகள் & வரலாறு", "hi": "📊 रिपोर्ट और इतिहास"},
    "nav_about": {"en": "ℹ️ About", "ta": "ℹ️ பற்றி", "hi": "ℹ️ जानकारी"},
    "navigate_label": {"en": "Navigate", "ta": "வழிசெலுத்தல்", "hi": "नेविगेट करें"},
    "crop_label": {"en": "Crop", "ta": "பயிர்", "hi": "फ़सल"},
    "language_label": {"en": "Language", "ta": "மொழி", "hi": "भाषा"},
    "demo_mode_warning": {
        "en": "**Demo mode** — no trained model found at `models/agridoctor_model.h5`. "
              "Predictions come from an image-heuristic stand-in. "
              "Run `train_model.py` on a labeled dataset to enable real predictions.",
        "ta": "**டெமோ பயன்முறை** — `models/agridoctor_model.h5` இல் பயிற்சி பெற்ற மாடல் இல்லை. "
              "முன்கணிப்புகள் ஒரு படப் பகுப்பாய்வு மாற்றீட்டிலிருந்து வருகின்றன. "
              "உண்மையான முன்கணிப்புகளுக்கு லேபிள் செய்யப்பட்ட தரவுத்தொகுப்பில் `train_model.py` ஐ இயக்கவும்.",
        "hi": "**डेमो मोड** — `models/agridoctor_model.h5` पर कोई प्रशिक्षित मॉडल नहीं मिला। "
              "पूर्वानुमान एक इमेज-हेयुरिस्टिक विकल्प से आ रहे हैं। "
              "वास्तविक पूर्वानुमान के लिए लेबल किए गए डेटा पर `train_model.py` चलाएं।",
    },
    "trained_mode_success": {
        "en": "Trained model loaded — running real predictions.",
        "ta": "பயிற்சி பெற்ற மாடல் ஏற்றப்பட்டது — உண்மையான முன்கணிப்புகள் இயங்குகின்றன.",
        "hi": "प्रशिक्षित मॉडल लोड हो गया — वास्तविक पूर्वानुमान चल रहे हैं।",
    },
    "weather_expander": {"en": "🌦 Weather advice", "ta": "🌦 வானிலை ஆலோசனை", "hi": "🌦 मौसम सलाह"},
    "city_label": {"en": "City", "ta": "நகரம்", "hi": "शहर"},
    "check_forecast_button": {"en": "Check rain forecast", "ta": "மழை முன்னறிவிப்பைச் சரிபார்க்கவும்", "hi": "बारिश का पूर्वानुमान देखें"},
    "weather_unavailable": {
        "en": "Weather advice isn't available right now.",
        "ta": "இப்போது வானிலை ஆலோசனை கிடைக்கவில்லை.",
        "hi": "अभी मौसम सलाह उपलब्ध नहीं है।",
    },
    "weather_city_not_found": {
        "en": "Couldn't find weather for '{city}'.",
        "ta": "'{city}' க்கான வானிலையைக் கண்டறிய முடியவில்லை.",
        "hi": "'{city}' के लिए मौसम नहीं मिला।",
    },
    "weather_forecast_failed": {
        "en": "Couldn't fetch the forecast for {city}.",
        "ta": "{city} க்கான முன்னறிவிப்பைப் பெற முடியவில்லை.",
        "hi": "{city} के लिए पूर्वानुमान नहीं मिल सका।",
    },
    "weather_delay": {
        "en": "Rain expected in {city} in the next 24h (up to {pct}% chance) — consider delaying fungicide or pesticide spraying until after it clears.",
        "ta": "அடுத்த 24 மணி நேரத்தில் {city} இல் மழை எதிர்பார்க்கப்படுகிறது ({pct}% வாய்ப்பு வரை) — மழை தெளிவடையும் வரை பூஞ்சைக்கொல்லி அல்லது பூச்சிக்கொல்லி தெளிப்பதை தாமதப்படுத்தவும்.",
        "hi": "अगले 24 घंटों में {city} में बारिश की संभावना है ({pct}% तक) — बारिश साफ़ होने तक फफूंदनाशी या कीटनाशक छिड़काव टालने पर विचार करें।",
    },
    "weather_ok": {
        "en": "No significant rain expected in {city} in the next 24h (up to {pct}% chance) — a reasonable window for spraying if needed.",
        "ta": "அடுத்த 24 மணி நேரத்தில் {city} இல் குறிப்பிடத்தக்க மழை எதிர்பார்க்கப்படவில்லை ({pct}% வாய்ப்பு வரை) — தேவைப்பட்டால் தெளிக்க இது ஒரு நல்ல நேரம்.",
        "hi": "अगले 24 घंटों में {city} में ज़्यादा बारिश की संभावना नहीं है ({pct}% तक) — ज़रूरत पड़ने पर छिड़काव के लिए उचित समय है।",
    },

    # ---- Scan page ----
    "scan_heading": {"en": "Scan a Leaf", "ta": "இலையை ஸ்கேன் செய்யவும்", "hi": "पत्ती स्कैन करें"},
    "scan_caption": {
        "en": "Upload a photo or use your camera. AgriDoctor AI will diagnose it in seconds.",
        "ta": "புகைப்படத்தை பதிவேற்றவும் அல்லது கேமராவைப் பயன்படுத்தவும். AgriDoctor AI சில நொடிகளில் கண்டறியும்.",
        "hi": "फ़ोटो अपलोड करें या कैमरा उपयोग करें। AgriDoctor AI कुछ ही सेकंड में जांच देगा।",
    },
    "image_source_label": {"en": "Image source", "ta": "படத்தின் மூலம்", "hi": "छवि स्रोत"},
    "upload_option": {"en": "Upload a photo", "ta": "புகைப்படத்தை பதிவேற்றவும்", "hi": "फ़ोटो अपलोड करें"},
    "camera_option": {"en": "Use camera", "ta": "கேமராவைப் பயன்படுத்தவும்", "hi": "कैमरा उपयोग करें"},
    "choose_image_label": {"en": "Choose a leaf image", "ta": "ஒரு இலைப் படத்தைத் தேர்ந்தெடுக்கவும்", "hi": "एक पत्ती की छवि चुनें"},
    "camera_input_label": {"en": "Take a photo of the leaf", "ta": "இலையின் புகைப்படம் எடுக்கவும்", "hi": "पत्ती की फ़ोटो लें"},
    "selected_image_caption": {"en": "Selected image", "ta": "தேர்ந்தெடுக்கப்பட்ட படம்", "hi": "चयनित छवि"},
    "analyze_button": {"en": "🔍 Analyze leaf", "ta": "🔍 இலையை பகுப்பாய்வு செய்யவும்", "hi": "🔍 पत्ती का विश्लेषण करें"},
    "analyzing_spinner": {"en": "Analyzing your leaf...", "ta": "உங்கள் இலை பகுப்பாய்வு செய்யப்படுகிறது...", "hi": "आपकी पत्ती का विश्लेषण हो रहा है..."},
    "listen_button": {"en": "🔊 Listen to diagnosis", "ta": "🔊 கண்டறிதலைக் கேளுங்கள்", "hi": "🔊 निदान सुनें"},
    "voice_crop_button": {"en": "🎤 Say your crop name", "ta": "🎤 உங்கள் பயிர் பெயரைச் சொல்லுங்கள்", "hi": "🎤 अपनी फ़सल का नाम बोलें"},
    "voice_no_support": {
        "en": "Voice input needs Chrome on Android/desktop.",
        "ta": "குரல் உள்ளீட்டிற்கு Android/டெஸ்க்டாப்பில் Chrome தேவை.",
        "hi": "वॉइस इनपुट के लिए एंड्रॉइड/डेस्कटॉप पर Chrome चाहिए।",
    },
    "voice_listening": {"en": "Listening...", "ta": "கேட்கிறது...", "hi": "सुन रहा है..."},
    "voice_no_match": {
        "en": "Didn't catch a crop name. Heard:",
        "ta": "பயிர் பெயரைப் புரிந்துகொள்ள முடியவில்லை. கேட்டது:",
        "hi": "फ़सल का नाम समझ नहीं आया। सुना:",
    },
    "voice_error": {"en": "Error:", "ta": "பிழை:", "hi": "त्रुटि:"},
    "analyzed_now": {"en": "analyzed just now", "ta": "இப்போதுதான் பகுப்பாய்வு செய்யப்பட்டது", "hi": "अभी-अभी विश्लेषण किया गया"},
    "demo_mode_tag": {"en": "demo mode", "ta": "டெமோ பயன்முறை", "hi": "डेमो मोड"},
    "severity_prefix": {"en": "Severity", "ta": "தீவிரம்", "hi": "गंभीरता"},
    "about_heading": {"en": "About this condition", "ta": "இந்த நிலை பற்றி", "hi": "इस स्थिति के बारे में"},
    "treatment_heading": {"en": "Recommended treatment", "ta": "பரிந்துரைக்கப்பட்ட சிகிச்சை", "hi": "अनुशंसित उपचार"},
    "saved_message": {
        "en": "Saved to your crop log — see Reports & History.",
        "ta": "உங்கள் பயிர் பதிவில் சேமிக்கப்பட்டது — அறிக்கைகள் & வரலாறு பார்க்கவும்.",
        "hi": "आपके फ़सल लॉग में सहेजा गया — रिपोर्ट और इतिहास देखें।",
    },
    "scan_placeholder": {
        "en": "Upload or capture a leaf photo, then click **Analyze leaf** to see results here.",
        "ta": "ஒரு இலைப் புகைப்படத்தைப் பதிவேற்றவும் அல்லது எடுக்கவும், பின்னர் முடிவுகளைப் பார்க்க **இலையை பகுப்பாய்வு செய்யவும்** என்பதைக் கிளிக் செய்யவும்.",
        "hi": "पत्ती की फ़ोटो अपलोड या कैप्चर करें, फिर परिणाम देखने के लिए **पत्ती का विश्लेषण करें** पर क्लिक करें।",
    },

    # ---- Compare with last scan ----
    "compare_same": {
        "en": "↔️ Same as last {crop} scan ({disease}); confidence {direction} {delta} pts since {date}.",
        "ta": "↔️ கடைசி {crop} ஸ்கேன் ({disease}) போலவே; {date} முதல் நம்பகத்தன்மை {delta} புள்ளிகள் {direction}.",
        "hi": "↔️ पिछले {crop} स्कैन ({disease}) जैसा ही; {date} से विश्वास स्तर {delta} अंक {direction}।",
    },
    "compare_up": {"en": "up", "ta": "அதிகரித்தது", "hi": "बढ़ा"},
    "compare_down": {"en": "down", "ta": "குறைந்தது", "hi": "घटा"},
    "compare_unchanged": {"en": "unchanged", "ta": "மாறவில்லை", "hi": "अपरिवर्तित"},
    "compare_improved": {
        "en": "📈 Improved since last scan on {date}: {prev} → Healthy.",
        "ta": "📈 {date} அன்றைய கடைசி ஸ்கேனிலிருந்து மேம்பட்டுள்ளது: {prev} → ஆரோக்கியமானது.",
        "hi": "📈 {date} के पिछले स्कैन से सुधार हुआ: {prev} → स्वस्थ।",
    },
    "compare_worsened": {
        "en": "📉 New issue since last scan on {date}: Healthy → {curr}.",
        "ta": "📉 {date} அன்றைய கடைசி ஸ்கேனிலிருந்து புதிய பிரச்சனை: ஆரோக்கியமானது → {curr}.",
        "hi": "📉 {date} के पिछले स्कैन के बाद नई समस्या: स्वस्थ → {curr}।",
    },
    "compare_other": {
        "en": "Last {crop} scan on {date}: {prev} ({pct}%).",
        "ta": "கடைசி {crop} ஸ்கேன் {date} அன்று: {prev} ({pct}%).",
        "hi": "पिछला {crop} स्कैन {date} को: {prev} ({pct}%)।",
    },

    # ---- Reports page ----
    "reports_heading": {"en": "Reports & History", "ta": "அறிக்கைகள் & வரலாறு", "hi": "रिपोर्ट और इतिहास"},
    "no_scans_yet": {
        "en": "No scans yet. Head to **Scan a Leaf** to analyze your first photo.",
        "ta": "இதுவரை ஸ்கேன்கள் இல்லை. உங்கள் முதல் புகைப்படத்தை பகுப்பாய்வு செய்ய **இலையை ஸ்கேன் செய்யவும்** க்குச் செல்லவும்.",
        "hi": "अभी तक कोई स्कैन नहीं। अपनी पहली फ़ोटो जांचने के लिए **पत्ती स्कैन करें** पर जाएं।",
    },
    "metric_scans_done": {"en": "Scans done", "ta": "ஸ்கேன்கள் முடிந்தது", "hi": "स्कैन पूरे हुए"},
    "metric_issues_found": {"en": "Issues found", "ta": "பிரச்சனைகள் கண்டறியப்பட்டன", "hi": "समस्याएं मिलीं"},
    "metric_avg_confidence": {"en": "Avg. confidence", "ta": "சராசரி நம்பகத்தன்மை", "hi": "औसत विश्वास स्तर"},
    "scans_over_time": {"en": "Scans over time", "ta": "காலப்போக்கில் ஸ்கேன்கள்", "hi": "समय के साथ स्कैन"},
    "most_common_issues": {"en": "Most common issues", "ta": "மிகவும் பொதுவான பிரச்சனைகள்", "hi": "सबसे आम समस्याएं"},
    "no_issues_yet": {
        "en": "No issues detected yet — every scan so far came back healthy.",
        "ta": "இதுவரை பிரச்சனைகள் எதுவும் கண்டறியப்படவில்லை — இதுவரையிலான ஒவ்வொரு ஸ்கேனும் ஆரோக்கியமாகவே வந்துள்ளது.",
        "hi": "अभी तक कोई समस्या नहीं मिली — अब तक हर स्कैन स्वस्थ आया है।",
    },
    "full_history": {"en": "Full scan history", "ta": "முழு ஸ்கேன் வரலாறு", "hi": "पूरा स्कैन इतिहास"},
    "download_csv_button": {"en": "⬇️ Download history as CSV", "ta": "⬇️ வரலாற்றை CSV ஆக பதிவிறக்கவும்", "hi": "⬇️ इतिहास CSV के रूप में डाउनलोड करें"},
    "manage_entries": {"en": "Manage entries", "ta": "பதிவுகளை நிர்வகிக்கவும்", "hi": "प्रविष्टियां प्रबंधित करें"},
    "manage_entries_caption": {
        "en": "Delete a single scan without clearing everything.",
        "ta": "எல்லாவற்றையும் அழிக்காமல் ஒரு ஸ்கேனை மட்டும் நீக்கவும்.",
        "hi": "सब कुछ मिटाए बिना एक स्कैन हटाएं।",
    },
    "select_entry_label": {"en": "Select an entry", "ta": "ஒரு பதிவைத் தேர்ந்தெடுக்கவும்", "hi": "एक प्रविष्टि चुनें"},
    "delete_entry_button": {"en": "🗑️ Delete this entry", "ta": "🗑️ இந்த பதிவை நீக்கவும்", "hi": "🗑️ यह प्रविष्टि हटाएं"},
    "reset_all_expander": {"en": "Reset all demo data", "ta": "அனைத்து டெமோ தரவையும் மீட்டமைக்கவும்", "hi": "सभी डेमो डेटा रीसेट करें"},
    "reset_all_caption": {
        "en": "Clears all logged scans. Cannot be undone.",
        "ta": "பதிவு செய்யப்பட்ட அனைத்து ஸ்கேன்களையும் அழிக்கும். செயல்தவிர்க்க முடியாது.",
        "hi": "सभी लॉग किए गए स्कैन मिटा देगा। यह पूर्ववत नहीं किया जा सकता।",
    },
    "clear_all_button": {"en": "🗑️ Clear entire scan history", "ta": "🗑️ முழு ஸ்கேன் வரலாற்றையும் அழிக்கவும்", "hi": "🗑️ पूरा स्कैन इतिहास मिटाएं"},

    # ---- About page ----
    "about_title": {"en": "About AgriDoctor AI", "ta": "அக்ரிடாக்டர் AI பற்றி", "hi": "एग्रीडॉक्टर AI के बारे में"},
    "about_intro": {
        "en": "AgriDoctor AI is an AI-powered app that detects crop diseases from a leaf photo and instantly suggests remedies — turning any smartphone into a plant doctor.",
        "ta": "அக்ரிடாக்டர் AI என்பது ஒரு இலைப் புகைப்படத்திலிருந்து பயிர் நோய்களைக் கண்டறிந்து உடனடியாக தீர்வுகளை பரிந்துரைக்கும் AI-இயங்கும் பயன்பாடு — எந்த ஸ்மார்ட்போனையும் ஒரு தாவர மருத்துவராக மாற்றுகிறது.",
        "hi": "एग्रीडॉक्टर AI एक AI-संचालित ऐप है जो पत्ती की फ़ोटो से फ़सल की बीमारियों का पता लगाता है और तुरंत उपचार सुझाता है — किसी भी स्मार्टफ़ोन को पौधों के डॉक्टर में बदल देता है।",
    },
    "how_it_works_heading": {"en": "How it works", "ta": "இது எவ்வாறு செயல்படுகிறது", "hi": "यह कैसे काम करता है"},
    "how_it_works_steps": {
        "en": "1. Upload or capture a leaf photo from any smartphone (or speak your crop name instead of using the dropdown).\n"
              "2. A MobileNetV2-based CNN classifies the disease in seconds.\n"
              "3. The app returns a diagnosis, confidence score, colour-coded severity, and treatment advice — readable or spoken aloud.\n"
              "4. Every scan is logged so you can track crop health over time, compare against your last scan, and export your history.\n"
              "5. A weather check flags whether rain in the next 24h means spraying should wait.",
        "ta": "1. எந்த ஸ்மார்ட்போனிலிருந்தும் ஒரு இலைப் புகைப்படத்தைப் பதிவேற்றவும் அல்லது எடுக்கவும் (அல்லது டிராப்டவுனுக்குப் பதிலாக உங்கள் பயிர் பெயரைச் சொல்லவும்).\n"
              "2. MobileNetV2 அடிப்படையிலான CNN சில நொடிகளில் நோயை வகைப்படுத்துகிறது.\n"
              "3. பயன்பாடு ஒரு கண்டறிதல், நம்பகத்தன்மை மதிப்பெண், வண்ண-குறியிடப்பட்ட தீவிரம் மற்றும் சிகிச்சை ஆலோசனையை வழங்குகிறது — படிக்கக்கூடியது அல்லது சத்தமாகப் பேசப்படுகிறது.\n"
              "4. ஒவ்வொரு ஸ்கேனும் பதிவு செய்யப்படுகிறது, இதனால் காலப்போக்கில் பயிர் ஆரோக்கியத்தைக் கண்காணிக்கவும், உங்கள் கடைசி ஸ்கேனுடன் ஒப்பிடவும், உங்கள் வரலாற்றை ஏற்றுமதி செய்யவும் முடியும்.\n"
              "5. அடுத்த 24 மணி நேரத்தில் மழை பெய்தால் தெளிப்பதை காத்திருக்க வேண்டுமா என்பதை வானிலை சரிபார்ப்பு காட்டுகிறது.",
        "hi": "1. किसी भी स्मार्टफ़ोन से पत्ती की फ़ोटो अपलोड या कैप्चर करें (या ड्रॉपडाउन के बजाय अपनी फ़सल का नाम बोलें)।\n"
              "2. MobileNetV2 आधारित CNN कुछ ही सेकंड में बीमारी को वर्गीकृत करता है।\n"
              "3. ऐप निदान, विश्वास स्कोर, रंग-कोडित गंभीरता, और उपचार सलाह देता है — पढ़ने या सुनने दोनों के लिए।\n"
              "4. हर स्कैन लॉग होता है ताकि आप समय के साथ फ़सल स्वास्थ्य ट्रैक कर सकें, पिछले स्कैन से तुलना कर सकें, और अपना इतिहास निर्यात कर सकें।\n"
              "5. एक मौसम जांच बताती है कि अगले 24 घंटों में बारिश के कारण छिड़काव रोकना चाहिए या नहीं।",
    },
    "tech_stack_heading": {"en": "Technology stack", "ta": "தொழில்நுட்ப அடுக்கு", "hi": "तकनीकी स्टैक"},
    "built_for_caption": {"en": "Built for Idhaya Hacks 2K26 · Session started", "ta": "Idhaya Hacks 2K26 க்காக உருவாக்கப்பட்டது · அமர்வு தொடங்கியது", "hi": "Idhaya Hacks 2K26 के लिए बनाया गया · सत्र शुरू हुआ"},

    "login_heading": {"en": "Sign in to AgriDoctor AI", "ta": "AgriDoctor AI இல் உள்நுழையவும்", "hi": "AgriDoctor AI में साइन इन करें"},

    # ---- Login page ----
    "login_welcome": {
        "en": "Sign in to check on your crops and pick up where you left off.",
        "ta": "உங்கள் பயிர்களை சரிபார்க்கவும், நீங்கள் விட்ட இடத்திலிருந்து தொடரவும் உள்நுழையவும்.",
        "hi": "अपनी फ़सलों को देखने और जहां छोड़ा था वहीं से जारी रखने के लिए साइन इन करें।",
    },
    "login_name_label": {"en": "Your name", "ta": "உங்கள் பெயர்", "hi": "आपका नाम"},
    "login_phone_label": {"en": "Mobile number", "ta": "மொபைல் எண்", "hi": "मोबाइल नंबर"},
    "login_send_otp": {"en": "Send OTP", "ta": "OTP அனுப்பவும்", "hi": "OTP भेजें"},
    "login_otp_label": {"en": "Enter the OTP sent to your phone", "ta": "உங்கள் மொபைலுக்கு அனுப்பப்பட்ட OTP ஐ உள்ளிடவும்", "hi": "आपके फ़ोन पर भेजा गया OTP दर्ज करें"},
    "login_verify_button": {"en": "Verify & continue", "ta": "சரிபார்த்து தொடரவும்", "hi": "सत्यापित करें और आगे बढ़ें"},
    "login_otp_hint": {
        "en": "Prototype note: any 4-digit code works here — no real SMS is sent.",
        "ta": "முன்மாதிரி குறிப்பு: எந்த 4-இலக்க குறியீடும் இங்கு வேலை செய்யும் — உண்மையான SMS அனுப்பப்படாது.",
        "hi": "प्रोटोटाइप नोट: यहां कोई भी 4-अंकीय कोड काम करेगा — कोई वास्तविक SMS नहीं भेजा जाता।",
    },
    "login_or": {"en": "or continue with", "ta": "அல்லது இதன் மூலம் தொடரவும்", "hi": "या इसके साथ जारी रखें"},
    "login_guest": {"en": "Continue without an account", "ta": "கணக்கு இல்லாமல் தொடரவும்", "hi": "बिना खाते के जारी रखें"},
    "login_please_enter_name": {
        "en": "Please enter your name to continue.",
        "ta": "தொடர உங்கள் பெயரை உள்ளிடவும்.",
        "hi": "जारी रखने के लिए कृपया अपना नाम दर्ज करें।",
    },
    "login_please_enter_phone": {
        "en": "Please enter a mobile number to continue.",
        "ta": "தொடர ஒரு மொபைல் எண்ணை உள்ளிடவும்.",
        "hi": "जारी रखने के लिए कृपया मोबाइल नंबर दर्ज करें।",
    },
    "login_invalid_otp": {
        "en": "Please enter the 4-digit code shown above.",
        "ta": "மேலே காட்டப்பட்டுள்ள 4-இலக்க குறியீட்டை உள்ளிடவும்.",
        "hi": "कृपया ऊपर दिखाया गया 4-अंकीय कोड दर्ज करें।",
    },
    "welcome_back": {"en": "Welcome, {name}", "ta": "வரவேற்கிறோம், {name}", "hi": "स्वागत है, {name}"},
    "guest_name": {"en": "Guest", "ta": "விருந்தினர்", "hi": "अतिथि"},
    "logout_button": {"en": "🚪 Log out", "ta": "🚪 வெளியேறு", "hi": "🚪 लॉग आउट"},

    # ---- Notifications page ----
    "nav_notifications": {"en": "🔔 Notifications", "ta": "🔔 அறிவிப்புகள்", "hi": "🔔 सूचनाएं"},
    "notifications_heading": {"en": "Notifications", "ta": "அறிவிப்புகள்", "hi": "सूचनाएं"},
    "notif_none_yet": {
        "en": "No notifications yet — scan a leaf to start getting crop health updates here.",
        "ta": "இதுவரை அறிவிப்புகள் இல்லை — இங்கு பயிர் ஆரோக்கிய புதுப்பிப்புகளைப் பெற ஒரு இலையை ஸ்கேன் செய்யவும்.",
        "hi": "अभी तक कोई सूचना नहीं — यहां फ़सल स्वास्थ्य अपडेट पाने के लिए एक पत्ती स्कैन करें।",
    },
    "notif_recheck_title": {
        "en": "Recheck your {crop} plants",
        "ta": "உங்கள் {crop} செடிகளை மீண்டும் சரிபார்க்கவும்",
        "hi": "अपने {crop} के पौधों की दोबारा जांच करें",
    },
    "notif_recheck_sub": {
        "en": "{disease} was detected on {date} — see if it has spread.",
        "ta": "{date} அன்று {disease} கண்டறியப்பட்டது — அது பரவியுள்ளதா என்று பாருங்கள்.",
        "hi": "{date} को {disease} मिला था — देखें कि यह फैला है या नहीं।",
    },
    "notif_healthy_title": {
        "en": "{crop} patch looks healthy",
        "ta": "{crop} தோட்டம் ஆரோக்கியமாக உள்ளது",
        "hi": "{crop} की क्यारी स्वस्थ लग रही है",
    },
    "notif_healthy_sub": {
        "en": "Last scan on {date} found no issues.",
        "ta": "{date} அன்றைய கடைசி ஸ்கேனில் பிரச்சனைகள் எதுவும் இல்லை.",
        "hi": "{date} के आखिरी स्कैन में कोई समस्या नहीं मिली।",
    },
    "notif_weather_title": {
        "en": "Rain expected in {city}",
        "ta": "{city} இல் மழை எதிர்பார்க்கப்படுகிறது",
        "hi": "{city} में बारिश की संभावना",
    },
    "notif_weather_sub": {
        "en": "Up to {pct}% chance in the next 24h — consider delaying spraying.",
        "ta": "அடுத்த 24 மணி நேரத்தில் {pct}% வாய்ப்பு வரை — தெளிப்பதை தாமதப்படுத்த பரிசீலிக்கவும்.",
        "hi": "अगले 24 घंटों में {pct}% तक संभावना — छिड़काव में देरी करने पर विचार करें।",
    },
    "notif_tip_title": {
        "en": "Tip for better results",
        "ta": "சிறந்த முடிவுகளுக்கான உதவிக்குறிப்பு",
        "hi": "बेहतर परिणामों के लिए सुझाव",
    },
    "notif_tip_sub": {
        "en": "Clear, well-lit close-up photos of a single leaf give the most reliable diagnosis.",
        "ta": "தெளிவான, நல்ல வெளிச்சத்துடன் கூடிய ஒரு இலையின் அருகிலிருந்து எடுக்கப்பட்ட புகைப்படங்கள் மிகவும் நம்பகமான கண்டறிதலை அளிக்கும்.",
        "hi": "एक पत्ती की स्पष्ट, अच्छी रोशनी वाली नज़दीकी फ़ोटो सबसे विश्वसनीय निदान देती है।",
    },
    "notif_rescan_button": {"en": "Re-scan now", "ta": "இப்போது மீண்டும் ஸ்கேன் செய்யவும்", "hi": "अभी दोबारा स्कैन करें"},
    "group_today": {"en": "Today", "ta": "இன்று", "hi": "आज"},
    "group_earlier": {"en": "Earlier", "ta": "முன்பு", "hi": "पहले"},
    "logged_in_as": {"en": "Signed in as", "ta": "இவராக உள்நுழைந்துள்ளீர்கள்", "hi": "इस रूप में साइन इन किया"},
}


# Severity words used in data/diseases.csv, translated for display. The
# English word is still what severity_color() in app.py keys off, so the
# colour logic never changes with the language.
SEVERITY_LABELS = {
    "none": {"en": "None", "ta": "ஏதுமில்லை", "hi": "कोई नहीं"},
    "mild": {"en": "Mild", "ta": "லேசான", "hi": "हल्का"},
    "moderate": {"en": "Moderate", "ta": "மிதமான", "hi": "मध्यम"},
    "severe": {"en": "Severe", "ta": "கடுமையான", "hi": "गंभीर"},
}


# Per-class translated crop/disease/description/remedy text, keyed exactly
# like model.CLASS_NAMES. Only "ta" and "hi" need entries here -- English
# always comes from the database (data/diseases.csv), which stays the
# single source of truth for the base content.
DISEASE_TRANSLATIONS = {
    "Tomato_Healthy": {
        "ta": {"crop": "தக்காளி", "disease": "ஆரோக்கியமானது",
               "description": "இந்த இலையில் நோய் அறிகுறிகள் இல்லை.",
               "remedy": "நல்ல நீர்ப்பாசனம் மற்றும் இடைவெளி பழக்கங்களைத் தொடரவும். ஒவ்வொரு 1-2 வாரங்களுக்கும் மீண்டும் ஸ்கேன் செய்யவும்."},
        "hi": {"crop": "टमाटर", "disease": "स्वस्थ",
               "description": "इस पत्ती पर रोग के कोई लक्षण नहीं मिले।",
               "remedy": "अच्छी सिंचाई और उचित दूरी बनाए रखें। समस्याओं को जल्दी पकड़ने के लिए हर 1-2 सप्ताह में दोबारा स्कैन करें।"},
    },
    "Tomato_Early_Blight": {
        "ta": {"crop": "தக்காளி", "disease": "முன்கூட்டிய கருகல் நோய்",
               "description": "பழைய இலைகளில் அடர் வளையங்களுடன் கூடிய புள்ளிகள் தோன்றி மஞ்சளாகி உதிர்கின்றன.",
               "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி அழிக்கவும். ஒவ்வொரு 7-10 நாட்களுக்கும் காப்பர் அடிப்படையிலான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும். வேரின் அடிப்பகுதியில் நீர் ஊற்றவும், இலைகளின் மேல் ஊற்ற வேண்டாம்."},
        "hi": {"crop": "टमाटर", "disease": "अगेती झुलसा रोग",
               "description": "पुरानी पत्तियों पर गहरे घेरेदार धब्बे बनते हैं जो पीले होकर गिर जाते हैं।",
               "remedy": "संक्रमित पत्तियों को हटाकर नष्ट करें। हर 7-10 दिन में कॉपर आधारित फफूंदनाशी का प्रयोग करें। पौधे की जड़ में पानी दें, पत्तियों पर नहीं।"},
    },
    "Tomato_Late_Blight": {
        "ta": {"crop": "தக்காளி", "disease": "பிந்திய கருகல் நோய்",
               "description": "ஈரப்பதமான வானிலையில் விரைவாகப் பரவும் நீர் தோய்ந்த பழுப்பு-கருப்பு புள்ளிகள்.",
               "remedy": "அருகிலுள்ள பயிர்களைப் பாதுகாக்க பாதிக்கப்பட்ட செடிகளை உடனடியாக அகற்றவும். காப்பர் அல்லது குளோரோதலோனில் கொண்ட பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும். மேலிருந்து நீர்ப்பாசனம் செய்வதைத் தவிர்க்கவும்."},
        "hi": {"crop": "टमाटर", "disease": "पछेती झुलसा रोग",
               "description": "नम मौसम में तेज़ी से फैलने वाले पानी से भीगे भूरे-काले धब्बे।",
               "remedy": "आस-पास की फसलों को बचाने के लिए संक्रमित पौधों को तुरंत हटाएं। कॉपर या क्लोरोथालोनिल युक्त फफूंदनाशी का प्रयोग करें। ऊपर से सिंचाई करने से बचें।"},
    },
    "Tomato_Leaf_Mold": {
        "ta": {"crop": "தக்காளி", "disease": "இலை பூஞ்சணம்",
               "description": "இலையின் மேற்பரப்பில் வெளிர் மஞ்சள் புள்ளிகள், அடியில் ஆலிவ்-பச்சை பூஞ்சணம்.",
               "remedy": "காற்றோட்டத்தை மேம்படுத்தி ஈரப்பதத்தைக் குறைக்கவும். பாதிக்கப்பட்ட இலைகளை அகற்றவும். தேவைப்பட்டால் பொருத்தமான பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும்."},
        "hi": {"crop": "टमाटर", "disease": "पत्ती फफूंदी",
               "description": "पत्ती के ऊपर हल्के पीले धब्बे और नीचे जैतूनी-हरी फफूंद।",
               "remedy": "हवा का प्रवाह बढ़ाएं और नमी कम करें। संक्रमित पत्तियों को हटाएं। ज़रूरत पड़ने पर उपयुक्त फफूंदनाशी का प्रयोग करें।"},
    },
    "Potato_Healthy": {
        "ta": {"crop": "உருளைக்கிழங்கு", "disease": "ஆரோக்கியமானது",
               "description": "இந்த இலையில் நோய் அறிகுறிகள் இல்லை.",
               "remedy": "தற்போதைய பராமரிப்பைத் தொடரவும். மழைக்குப் பிறகு குறிப்பாக அவ்வப்போது மீண்டும் ஸ்கேன் செய்யவும்."},
        "hi": {"crop": "आलू", "disease": "स्वस्थ",
               "description": "इस पत्ती पर रोग के कोई लक्षण नहीं मिले।",
               "remedy": "मौजूदा देखभाल जारी रखें। विशेष रूप से बारिश के बाद समय-समय पर दोबारा स्कैन करें।"},
    },
    "Potato_Early_Blight": {
        "ta": {"crop": "உருளைக்கிழங்கு", "disease": "முன்கூட்டிய கருகல் நோய்",
               "description": "பொதுவாக கீழ் இலைகளில் முதலில் தோன்றும் இலக்கு போன்ற வளையங்களுடன் கூடிய பழுப்புப் புள்ளிகள்.",
               "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றவும். முன்கூட்டிய கருகலுக்கான பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும். காற்றோட்டத்திற்காக செடிகளுக்கு இடையே சரியான இடைவெளியை உறுதி செய்யவும்."},
        "hi": {"crop": "आलू", "disease": "अगेती झुलसा रोग",
               "description": "आमतौर पर निचली पत्तियों पर पहले दिखने वाले लक्ष्य जैसे घेरेदार भूरे धब्बे।",
               "remedy": "संक्रमित पत्तियों को हटाएं। अगेती झुलसा के लिए अनुशंसित फफूंदनाशी का प्रयोग करें। हवा के प्रवाह के लिए पौधों के बीच उचित दूरी सुनिश्चित करें।"},
    },
    "Potato_Late_Blight": {
        "ta": {"crop": "உருளைக்கிழங்கு", "disease": "பிந்திய கருகல் நோய்",
               "description": "குளிர்ந்த, ஈரமான காலநிலையில் விரைவாகப் பரவும் அடர், ஒழுங்கற்ற, நீர் தோய்ந்த புண்கள்.",
               "remedy": "பாதிக்கப்பட்ட செடிகளை உடனடியாக அகற்றி அழிக்கவும். அடுத்த மழைக்கு முன் பாதுகாப்பு பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும். இலைகள் ஈரமாக இருக்கும்போது வயலில் வேலை செய்வதைத் தவிர்க்கவும்."},
        "hi": {"crop": "आलू", "disease": "पछेती झुलसा रोग",
               "description": "ठंडे, नम मौसम में तेज़ी से फैलने वाले गहरे, अनियमित, पानी से भीगे घाव।",
               "remedy": "संक्रमित पौधों को तुरंत हटाकर नष्ट करें। अगली बारिश से पहले सुरक्षात्मक फफूंदनाशी का प्रयोग करें। पत्तियां गीली होने पर खेत में काम करने से बचें।"},
    },
    "Corn_Healthy": {
        "ta": {"crop": "சோளம்", "disease": "ஆரோக்கியமானது",
               "description": "இந்த இலையில் நோய் அறிகுறிகள் இல்லை.",
               "remedy": "எந்த நடவடிக்கையும் தேவையில்லை. ஈரப்பதமான வளரும் காலங்களில் தொடர்ந்து கண்காணிக்கவும்."},
        "hi": {"crop": "मक्का", "disease": "स्वस्थ",
               "description": "इस पत्ती पर रोग के कोई लक्षण नहीं मिले।",
               "remedy": "किसी कार्रवाई की आवश्यकता नहीं। विशेष रूप से नम मौसम में निगरानी जारी रखें।"},
    },
    "Corn_Common_Rust": {
        "ta": {"crop": "சோளம்", "disease": "பொதுவான துரு நோய்",
               "description": "இலையின் இரு பரப்புகளிலும் சிதறிக்கிடக்கும் சிறிய சிவப்பு-பழுப்பு கொப்புளங்கள்.",
               "remedy": "பெரும்பாலான நவீன வகைகள் லேசான துருவைத் தாங்கும். கடுமையாக இருந்தால், இலைப் பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும். எதிர்கால நடவுக்கு துருவை எதிர்க்கும் வகைகளைத் தேர்ந்தெடுக்கவும்."},
        "hi": {"crop": "मक्का", "disease": "सामान्य रतुआ रोग",
               "description": "पत्ती की दोनों सतहों पर बिखरे छोटे लाल-भूरे फुंसी जैसे धब्बे।",
               "remedy": "अधिकांश आधुनिक किस्में हल्के रतुआ को सहन कर लेती हैं। गंभीर होने पर पत्ती फफूंदनाशी का प्रयोग करें। भविष्य की बुवाई के लिए रतुआ-प्रतिरोधी किस्में चुनें।"},
    },
    "Corn_Gray_Leaf_Spot": {
        "ta": {"crop": "சோளம்", "disease": "சாம்பல் இலைப்புள்ளி நோய்",
               "description": "இலை நரம்புகளுக்கு இணையாக ஓடும் செவ்வக சாம்பல்-தான் புள்ளிகள்.",
               "remedy": "குறைந்தது ஒரு பருவத்திற்கு சோளத்திலிருந்து பயிர் சுழற்சியை மாற்றவும். பரவத் தொடங்கியவுடன் பூஞ்சைக்கொல்லியைப் பயன்படுத்தவும். எதிர்ப்பு வகைகளைத் தேர்ந்தெடுத்து வயல் எச்சங்களைக் குறைக்கவும்."},
        "hi": {"crop": "मक्का", "disease": "ग्रे लीफ स्पॉट रोग",
               "description": "पत्ती की नसों के समांतर चलने वाले आयताकार धूसर-तन धब्बे।",
               "remedy": "कम से कम एक सीज़न के लिए मक्का से फसल चक्र बदलें। फैलने के पहले संकेत पर फफूंदनाशी का प्रयोग करें। प्रतिरोधी किस्में चुनें और खेत में बचे अवशेष कम करें।"},
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """Look up a UI string by key for the given language, falling back to
    English (and then the raw key) if a translation is missing. Any kwargs
    are used to .format() placeholders like {city} or {pct} in the string."""
    entry = TRANSLATIONS.get(key)
    text = (entry.get(lang) or entry.get("en") or key) if entry else key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def t_severity(severity: str, lang: str = "en") -> str:
    """Translate a severity word (None/Mild/Moderate/Severe) for display."""
    key = (severity or "none").strip().lower()
    entry = SEVERITY_LABELS.get(key)
    if entry is None:
        return severity or ""
    return entry.get(lang) or entry.get("en") or severity


# Crop names for the sidebar dropdown. The English key ("Tomato", "Potato",
# "Corn") is still what the rest of the code uses internally -- it must
# match model.CROP_CLASSES and database rows exactly -- this is purely for
# what the user sees in the dropdown.
CROP_NAMES = {
    "Tomato": {"en": "Tomato", "ta": "தக்காளி", "hi": "टमाटर"},
    "Potato": {"en": "Potato", "ta": "உருளைக்கிழங்கு", "hi": "आलू"},
    "Corn": {"en": "Corn", "ta": "சோளம்", "hi": "मक्का"},
}


def t_crop(crop: str, lang: str = "en") -> str:
    """Translate a crop name for display (dropdown, headings, messages)."""
    entry = CROP_NAMES.get(crop)
    if entry is None:
        return crop
    return entry.get(lang) or entry.get("en") or crop


# Disease-name-only translations, independent of crop -- used for the
# "Most common issues" chart, which aggregates scans by disease name alone
# (the same disease name, e.g. "Late Blight", can apply to more than one
# crop, so that chart can't key off a single class_name).
DISEASE_NAME_ONLY = {
    "Healthy": {"ta": "ஆரோக்கியமானது", "hi": "स्वस्थ"},
    "Early Blight": {"ta": "முன்கூட்டிய கருகல் நோய்", "hi": "अगेती झुलसा रोग"},
    "Late Blight": {"ta": "பிந்திய கருகல் நோய்", "hi": "पछेती झुलसा रोग"},
    "Leaf Mold": {"ta": "இலை பூஞ்சணம்", "hi": "पत्ती फफूंदी"},
    "Common Rust": {"ta": "பொதுவான துரு நோய்", "hi": "सामान्य रतुआ रोग"},
    "Gray Leaf Spot": {"ta": "சாம்பல் இலைப்புள்ளி நோய்", "hi": "ग्रे लीफ स्पॉट रोग"},
}


def t_disease_name(disease: str, lang: str = "en") -> str:
    """Translate a plain disease name (no crop context needed), used for
    aggregate views like the 'Most common issues' chart."""
    if lang == "en" or not disease:
        return disease
    entry = DISEASE_NAME_ONLY.get(disease)
    if entry is None:
        return disease
    return entry.get(lang) or disease


def translate_disease_name(class_name: str, lang: str, fallback: str) -> str:
    """Translate just the disease-name portion for a given class, used to
    display a *previous* scan's disease name in the current language for
    the 'compare with last scan' feature."""
    if lang == "en" or not class_name:
        return fallback
    overrides = DISEASE_TRANSLATIONS.get(class_name, {}).get(lang)
    if overrides:
        return overrides.get("disease", fallback)
    return fallback


def localize_disease_info(class_name: str, info: dict, lang: str) -> dict:
    """
    Returns a copy of `info` (as returned by database.get_disease_info)
    with crop/disease/description/remedy translated for display, and a
    new "severity_label" key with the translated severity word.

    `info["severity"]` is left untouched (English) so severity_color() in
    app.py keeps working regardless of language -- only severity_label is
    for display.
    """
    localized = dict(info)
    localized["severity_label"] = t_severity(info.get("severity"), lang)

    if lang == "en":
        return localized

    overrides = DISEASE_TRANSLATIONS.get(class_name, {}).get(lang)
    if overrides:
        localized.update({
            "crop": overrides.get("crop", info.get("crop")),
            "disease": overrides.get("disease", info.get("disease")),
            "description": overrides.get("description", info.get("description")),
            "remedy": overrides.get("remedy", info.get("remedy")),
        })
    return localized
