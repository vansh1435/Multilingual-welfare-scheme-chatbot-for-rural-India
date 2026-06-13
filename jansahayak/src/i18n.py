"""Small translation table used by the offline chatbot engine."""

SUPPORTED_LANGUAGES = ("hi", "ta", "en")

LANGUAGE_NAMES = {
    "hi": "हिंदी",
    "ta": "தமிழ்",
    "en": "English",
}

MESSAGES = {
    "choose_language": {
        "en": "Choose language: 1 Hindi, 2 Tamil, 3 English.",
        "hi": "भाषा चुनें: 1 हिंदी, 2 தமிழ், 3 English.",
        "ta": "மொழி தேர்வு: 1 हिंदी, 2 தமிழ், 3 English.",
    },
    "welcome": {
        "en": "Namaste. I will ask 5 short questions and then show schemes with document checklists.",
        "hi": "नमस्ते। मैं 5 छोटे सवाल पूछूंगा और फिर योजनाएं व कागजों की सूची बताऊंगा।",
        "ta": "வணக்கம். 5 குறுகிய கேள்விகள் கேட்டு, திட்டங்கள் மற்றும் ஆவணப் பட்டியலை சொல்கிறேன்.",
    },
    "q_age_gender": {
        "en": "Q1/5: Your age and gender? Example: 32 woman / 45 man.",
        "hi": "सवाल 1/5: आपकी उम्र और लिंग? जैसे: 32 महिला / 45 पुरुष।",
        "ta": "கேள்வி 1/5: உங்கள் வயது மற்றும் பாலினம்? உதா: 32 பெண் / 45 ஆண்.",
    },
    "q_location_work": {
        "en": "Q2/5: Where do you live and what is your main work? Example: village farmer with land / village labour / city delivery.",
        "hi": "सवाल 2/5: आप कहां रहते हैं और मुख्य काम क्या है? जैसे: गांव किसान-भूमि / गांव मजदूर / शहर डिलीवरी।",
        "ta": "கேள்வி 2/5: எங்கு வாழ்கிறீர்கள், முக்கிய வேலை என்ன? உதா: கிராம விவசாயி நிலம் / கிராம கூலி / நகர டெலிவரி.",
    },
    "q_income_assets": {
        "en": "Q3/5: Household condition? Say any that apply: ration/BPL, kutcha house, no LPG, low income, none.",
        "hi": "सवाल 3/5: घर/आय की स्थिति? जो लागू हो लिखें: राशन/BPL, कच्चा घर, गैस नहीं, कम आय, नहीं।",
        "ta": "கேள்வி 3/5: குடும்ப நிலை? பொருந்துவதை எழுதுங்கள்: ரேஷன்/BPL, குடிசை வீடு, LPG இல்லை, குறைந்த வருமானம், இல்லை.",
    },
    "q_family_needs": {
        "en": "Q4/5: Any family need? pregnant/lactating woman, girl below 10, 60+ elder, widow, disability, hospital need, none.",
        "hi": "सवाल 4/5: परिवार में क्या जरूरत है? गर्भवती/स्तनपान, 10 साल से कम बेटी, 60+ बुजुर्ग, विधवा, दिव्यांग, इलाज, नहीं।",
        "ta": "கேள்வி 4/5: குடும்பத் தேவை? கர்ப்பிணி/பாலூட்டும் பெண், 10 வயதுக்கு குறைவான பெண் குழந்தை, 60+ முதியோர், விதவை, மாற்றுத்திறன், மருத்துவ தேவை, இல்லை.",
    },
    "q_docs": {
        "en": "Q5/5: Which documents do you have? Aadhaar, bank account, ration card. Mention missing/lost documents too.",
        "hi": "सवाल 5/5: कौन से कागज हैं? आधार, बैंक खाता, राशन कार्ड। जो खो गया/नहीं है वह भी लिखें।",
        "ta": "கேள்வி 5/5: எந்த ஆவணங்கள் உள்ளன? ஆதார், வங்கி கணக்கு, ரேஷன் கார்டு. இல்லாதது/தொலைந்ததும் எழுதுங்கள்.",
    },
    "recommendations_intro": {
        "en": "Personalised shortlist based on your answers. Final approval depends on official verification:",
        "hi": "आपके जवाबों के आधार पर निजी सूची। अंतिम मंजूरी सरकारी सत्यापन पर निर्भर है:",
        "ta": "உங்கள் பதில்களின் அடிப்படையில் தனிப்பட்ட பட்டியல். இறுதி ஒப்புதல் அரசு சரிபார்ப்பை பொறுத்தது:",
    },
    "no_recommendations": {
        "en": "I could not safely shortlist a scheme from the current answers. Send more details or visit CSC/Panchayat for a full check.",
        "hi": "इन जवाबों से मैं सुरक्षित रूप से योजना नहीं चुन पाया। और जानकारी भेजें या पूरी जांच के लिए CSC/पंचायत जाएं।",
        "ta": "இந்த பதில்களால் பாதுகாப்பாக திட்டம் தேர்வு செய்ய முடியவில்லை. மேலும் விவரம் அனுப்பவும் அல்லது CSC/பஞ்சாயத்து செல்லவும்.",
    },
    "checklist_prompt": {
        "en": "Reply with a number for the document checklist, or type another question.",
        "hi": "कागजों की सूची के लिए नंबर भेजें, या अपना सवाल लिखें।",
        "ta": "ஆவணப் பட்டியலுக்கு எண்ணை அனுப்பவும், அல்லது வேறு கேள்வி எழுதவும்.",
    },
    "checklist_title": {
        "en": "Document checklist",
        "hi": "कागजों की सूची",
        "ta": "ஆவணப் பட்டியல்",
    },
    "steps_title": {
        "en": "Where to apply",
        "hi": "कहां आवेदन करें",
        "ta": "எங்கு விண்ணப்பிக்கலாம்",
    },
    "source_title": {
        "en": "Source",
        "hi": "स्रोत",
        "ta": "மூலம்",
    },
    "honesty_note": {
        "en": "I only answer from the local scheme catalogue. For state-specific or unclear cases, I will ask you to verify at CSC/Panchayat/official portal.",
        "hi": "मैं केवल स्थानीय योजना-सूची से जवाब देता हूं। राज्य-विशेष या अस्पष्ट मामलों में CSC/पंचायत/सरकारी पोर्टल पर सत्यापन जरूरी है।",
        "ta": "நான் உள்ளூர் திட்டப் பட்டியலிலிருந்து மட்டுமே பதில் தருகிறேன். மாநில விதி/தெளிவில்லாத விஷயங்களுக்கு CSC/பஞ்சாயத்து/அரசு தளத்தில் சரிபார்க்கவும்.",
    },
    "aadhaar_lost": {
        "en": "Aadhaar seems missing/lost. Do not stop the flow. For schemes that require Aadhaar/eKYC, visit CSC/Aadhaar Seva Kendra to retrieve/update it. Carry any ID, ration card, bank passbook, and mobile if available.",
        "hi": "लगता है आधार खो गया/नहीं है। बातचीत जारी रखें। जिन योजनाओं में आधार/eKYC चाहिए, उसके लिए CSC/आधार सेवा केंद्र पर पुनःप्राप्ति/अपडेट कराएं। कोई पहचान पत्र, राशन कार्ड, बैंक पासबुक और मोबाइल साथ रखें।",
        "ta": "ஆதார் இல்லை/தொலைந்தது போல உள்ளது. உரையாடலை தொடரலாம். ஆதார்/eKYC தேவைப்படும் திட்டங்களுக்கு CSC/ஆதார் சேவை மையத்தில் மீட்டெடுக்க/புதுப்பிக்கவும். அடையாள ஆவணம், ரேஷன், வங்கி பாஸ்புக், மொபைல் எடுத்துச் செல்லவும்.",
    },
    "unknown": {
        "en": "I do not have enough grounded information to answer that safely. I can help with PM-KISAN, PM-JAY, PMAY-G, PMUY, MGNREGA, SSY, PMMVY, e-Shram, APY, and NSAP.",
        "hi": "इसका सुरक्षित जवाब देने के लिए मेरे पास पर्याप्त स्रोत-आधारित जानकारी नहीं है। मैं PM-KISAN, PM-JAY, PMAY-G, PMUY, मनरेगा, सुकन्या, PMMVY, e-Shram, APY और NSAP में मदद कर सकता हूं।",
        "ta": "இதற்கு பாதுகாப்பாக பதில் தர போதுமான ஆதாரத் தகவல் இல்லை. PM-KISAN, PM-JAY, PMAY-G, PMUY, MGNREGA, SSY, PMMVY, e-Shram, APY, NSAP பற்றி உதவ முடியும்.",
    },
    "restart": {
        "en": "Restarted.",
        "hi": "फिर से शुरू किया।",
        "ta": "மீண்டும் தொடங்கியது.",
    },
}


def t(key, lang="en"):
    """Return translated message, falling back to English."""
    return MESSAGES.get(key, {}).get(lang) or MESSAGES.get(key, {}).get("en", key)
