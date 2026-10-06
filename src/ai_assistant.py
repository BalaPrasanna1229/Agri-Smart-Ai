from pathlib import Path

# Automatically load environment variables from .env
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
    else:
        load_dotenv()
except ImportError:
    pass

import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

from src.database import (
    get_user_by_id,
    get_user_farms,
    get_user_crop_predictions,
    get_user_yield_predictions,
    get_user_disease_lookups,
    save_assistant_message,
    get_user_assistant_messages,
)
from src.weather_analysis import get_weather_analyzer
from src.market_analysis import get_market_analyzer


UNCONFIGURED_MESSAGE = "AI Assistant is not configured yet. Please add the required API key to enable AI responses."

# Comprehensive Multilingual Agricultural Vocabulary
AGRICULTURAL_KEYWORDS_EN = {
    "crop", "crops", "plant", "plants", "agriculture", "agricultural", "agronomy", "agronomist",
    "farming", "farmer", "farm", "farms", "field", "fields", "land", "holding", "holdings",
    "rice", "paddy", "wheat", "maize", "corn", "cotton", "sugarcane", "sugar cane",
    "tomato", "potato", "onion", "garlic", "chilli", "chili", "mirchi", "pepper", "capsicum",
    "brinjal", "eggplant", "aubergine", "okra", "bhendi", "bhindi", "ladyfinger", "ladies finger",
    "cabbage", "cauliflower", "carrot", "radish", "cucumber", "watermelon", "water melon",
    "muskmelon", "melon", "cantaloupe", "banana", "mango", "grape", "grapes", "orange",
    "citrus", "papaya", "coconut", "apple", "pomegranate", "guava", "sapota", "chiku",
    "lemon", "lime", "turmeric", "ginger", "coriander", "cumin", "mustard", "groundnut",
    "peanut", "peanuts", "soybean", "soy", "soya", "chickpea", "chana", "pigeonpea", "tur",
    "arhar", "red gram", "green gram", "moong", "black gram", "urad", "lentil", "masoor",
    "cowpea", "lobia", "jute", "tobacco", "coffee", "tea", "rubber", "cashew", "cardamom",
    "arecanut", "betel", "betelnut", "sunflower", "sesame", "castor", "barley", "sorghum",
    "jowar", "pearl millet", "bajra", "finger millet", "ragi", "foxtail millet", "korra",
    "pulses", "grain", "grains", "cereal", "cereals", "legume", "legumes", "oilseed", "oilseeds",
    "vegetable", "vegetables", "fruit", "fruits", "horticulture", "floriculture", "fodder",
    "soil", "soils", "dirt", "clay", "sand", "sandy", "loam", "loamy", "silt", "silty",
    "alluvial", "black soil", "red soil", "laterite", "saline", "alkaline", "ph", "soil ph",
    "soil test", "soil health", "soil fertility", "humus", "organic matter", "nitrogen",
    "phosphorus", "potassium", "calcium", "magnesium", "sulfur", "sulphur", "zinc", "boron",
    "iron", "copper", "manganese", "nutrient", "nutrients", "micronutrient", "micronutrients",
    "macronutrient", "macronutrients", "tillage", "plough", "ploughing", "plow", "plowing",
    "bed", "furrow", "ridge", "acre", "acres", "hectare", "hectares", "bigha", "guntha",
    "cent", "parcel", "fertilizer", "fertilizers", "fertiliser", "fertilisers", "manure",
    "manures", "fym", "farmyard manure", "compost", "vermicompost", "jeevamrutham",
    "biofertilizer", "biofertilizers", "urea", "dap", "ssp", "mop", "npk", "potash",
    "phosphate", "gypsum", "foliar", "fertigation", "top dressing", "basal dose", "green manure",
    "neem cake", "castor cake", "zinc sulfate", "zinc sulphate", "borax",
    "pest", "pests", "insect", "insects", "bug", "bugs", "worm", "worms", "caterpillar",
    "borer", "stem borer", "fruit borer", "pod borer", "bollworm", "pink bollworm",
    "armyworm", "fall armyworm", "spodoptera", "helicoverpa", "aphid", "aphids", "whitefly",
    "whiteflies", "thrips", "jassid", "jassids", "mite", "mites", "mealybug", "mealybugs",
    "scale insect", "weevil", "weevils", "beetle", "beetles", "nematode", "nematodes",
    "leafminer", "gall midge", "blast", "blight", "early blight", "late blight", "leaf spot",
    "tikka", "rust", "smut", "wilt", "fusarium", "damping off", "rot", "root rot",
    "fruit rot", "stem rot", "collar rot", "anthracnose", "powdery mildew", "downy mildew",
    "mosaic", "leaf curl", "yellow vein", "canker", "scab", "sheath blight", "dieback",
    "die-back", "weed", "weeds", "herbicide", "herbicides", "weedicide", "weedicides",
    "pesticide", "pesticides", "insecticide", "insecticides", "fungicide", "fungicides",
    "spray", "spraying", "dosage", "dose", "chemical", "active ingredient",
    "chlorantraniliprole", "coragen", "emamectin", "spinetoram", "imidacloprid", "acetamiprid",
    "thiamethoxam", "diafenthiuron", "pegasus", "fipronil", "mancozeb", "carbendazim",
    "saaf", "tricyclazole", "hexaconazole", "propiconazole", "azoxystrobin", "copper oxychloride",
    "streptocycline", "neem oil", "pheromone", "sticky trap", "ipm", "trichoderma", "pseudomonas",
    "irrigation", "water", "watering", "drip", "sprinkler", "flood", "basin", "borewell",
    "bore well", "canal", "pump", "evapotranspiration", "moisture", "drought",
    "weather", "climate", "rain", "rainfall", "monsoon", "temperature", "humidity", "wind",
    "mandi", "market", "apmc", "price", "prices", "msp", "rate", "rates", "cost", "profit",
    "yield", "yields", "harvest", "harvesting", "sowing", "seed", "seeds", "nursery",
    "germination", "intercropping", "crop rotation", "mulching", "polyhouse", "greenhouse",
    "hydroponics", "kvk", "icar", "rythu", "kisan", "vivasayi",
    "hi", "hello", "hey", "namaste", "namaskar", "namaskaram", "vanakkam", "help",
    "who are you", "what can you do", "agrismart", "assistant", "guide", "menu", "options",
    "my farm", "registered farm", "recommended crop", "my crop", "my yield", "soil test"
}

AGRICULTURAL_KEYWORDS_TE = {
    "పంట", "పంటలు", "వరి", "ధాన్యం", "గోధుమ", "మొక్కజొన్న", "జొన్న", "సజ్జ", "రాగి", "కొర్ర",
    "పత్తి", "చెరకు", "టమోటా", "బంగాళాదుంప", "ఆలూ", "ఉల్లి", "ఉల్లిపాయ", "మిరప", "మిర్చి",
    "వంకాయ", "బెండకాయ", "క్యాబేజీ", "క్యాలీఫ్లవర్", "క్యారెట్", "ముల్లంగి", "దోసకాయ",
    "పుచ్చకాయ", "కర్బూజ", "అరటి", "మామిడి", "ద్రాక్ష", "నారింజ", "బత్తాయి", "బొప్పాయి",
    "కొబ్బరి", "ఆపిల్", "దానిమ్మ", "జామ", "సపోటా", "నిమ్మ", "పసుపు", "అల్లం", "వెల్లుల్లి",
    "కొత్తిమీర", "జీలకర్ర", "ఆవాలు", "వేరుశనగ", "సోయాబీన్", "శనగ", "కంది", "పెసర", "మినుము",
    "ఎర్రకంది", "బొబ్బర్లు", "జనపనార", "పొగాకు", "కాఫీ", "టీ", "జీడిమామిడి", "ఆయిల్ పామ్",
    "పొద్దుతిరుగుడు", "నువ్వులు", "ఆముదం", "కూరగాయలు", "ఆకుకూరలు", "పండ్లు", "పూలు",
    "నేల", "మట్టి", "భూమి", "పొలం", "చేను", "నల్లరేగడి", "ఎర్ర నేల", "ఒండ్రు నేల", "ఇసుక నేల",
    "బంకమన్ను", "నేల పరీక్ష", "సారం", "పోషకాలు", "నత్రజని", "భాస్వరం", "పొటాష్", "ఎరువు",
    "ఎరువులు", "యూరియా", "డీఏపీ", "పశువుల ఎరువు", "వర్మీకంపోస్ట్", "జీవామృతం", "జింక్", "బోరాన్",
    "జిప్సం", "ఆఖరి దుక్కి", "దుక్కి", "పైపాటు",
    "పురుగు", "పురుగులు", "కీటకాలు", "లద్దెపురుగు", "కాండం", "గులాబీ", "కత్తెర పురుగు",
    "పేనుబంక", "తెల్లదోమ", "తామర పురుగులు", "పచ్చదోమ", "నల్లి", "పిండినల్లి", "తెగులు",
    "తెగుళ్లు", "అగ్గితెగులు", "మాడ తెగులు", "ఆకుమచ్చ", "తిక్కా", "తుప్పు", "ఎండు తెగులు",
    "వేరు కుళ్లు", "కాయ కుళ్లు", "బూడిద తెగులు", "ఆకుముడత", "ముడత", "కలుపు", "పురుగు మందు",
    "తెగులు మందు", "పిచికారీ", "మోతాదు", "మందులు", "వేపనూనె", "ట్రైకోడెర్మా",
    "సాగునీరు", "నీరు", "నీటి", "డ్రిప్", "బోరు", "కాల్వ", "వర్షం", "వాతావరణం", "ఉష్ణోగ్రత",
    "తేమ", "దిగుబడి", "మార్కెట్", "మండీ", "ధర", "మద్దతు ధర", "విత్తనం", "విత్తనాలు",
    "నాట్లు", "కోత", "రైతు", "వ్యవసాయం", "సాగు", "నమస్తే", "హలో", "నమస్కారం"
}

AGRICULTURAL_KEYWORDS_HI = {
    "फसल", "फसलें", "धान", "चावल", "गेहूं", "मक्का", "ज्वार", "बाजरा", "कपास", "गन्ना",
    "टमाटर", "आलू", "प्याज", "मिर्च", "बैंगन", "भिंडी", "गोभी", "गाजर", "मूली", "खीरा",
    "तरबूज", "खरबूजा", "केला", "आम", "अंगूर", "पपीता", "नारियल", "सेब", "अनार", "अमरूद",
    "नींबू", "हल्दी", "अदरक", "लहसुन", "सरसों", "मूंगफली", "सोयाबीन", "चना", "अरहर", "मूंग",
    "उड़द", "मिट्टी", "जमीन", "खेत", "दोमट", "काली मिट्टी", "मृदा", "उर्वरक", "खाद", "यूरिया",
    "डीएपी", "पोटाश", "कीट", "कीड़े", "इल्ली", "सुंडी", "माहू", "सफेद मक्खी", "रोग", "झुलसा",
    "ब्लास्ट", "टिक्का", "उकठा", "सड़न", "कीटनाशक", "फफूंदनाशक", "खरपतवार", "छिड़काव",
    "सिंचाई", "ड्रिप", "पानी", "बारिश", "मौसम", "तापमान", "मंडी", "भाव", "एमएसपी", "पैदावार",
    "उपज", "बीज", "बुवाई", "कटाई", "किसान", "कृषि", "खेती", "नमस्ते", "प्रणाम"
}

AGRICULTURAL_KEYWORDS_TA = {
    "பயிர்", "பயிர்கள்", "நெல்", "அரிசி", "கோதுமை", "சோளம்", "கம்பு", "ராகி", "பருத்தி",
    "கரும்பு", "தக்காளி", "உருளைக்கிழங்கு", "வெங்காயம்", "மிளகாய்", "கத்தரிக்காய்", "வெண்டைக்காய்",
    "முட்டைக்கோஸ்", "கேரட்", "முள்ளங்கி", "வெள்ளரிக்காய்", "தர்பூசணி", "வாழை", "மாம்பழம்",
    "திராட்சை", "பப்பாளி", "தேங்காய்", "மாதுளை", "கொய்யா", "எலுமிச்சை", "மஞ்சள்", "இஞ்சி",
    "பூண்டு", "கடுகு", "நிலக்கடலை", "சோயாபீன்", "கொண்டைக்கடலை", "துவரை", "பாசிப்பயறு", "உளுந்து",
    "மண்", "நிலம்", "வயல்", "செம்மண்", "கரிசல் மண்", "உரம்", "உரங்கள்", "யூரியா", "டிஏபி",
    "பொட்டாஷ்", "தொழு உரம்", "பூச்சி", "புழு", "துளைப்பான்", "அசுவினி", "வெள்ளை ஈ", "நோய்",
    "கருகல்", "குலைநோய்", "புள்ளி", "வாடல்", "அழுகல்", "பூச்சிக்கொல்லி", "பூஞ்சாணக்கொல்லி",
    "களை", "தெளித்தல்", "பாசனம்", "சொட்டு நீர்", "தண்ணீர்", "மழை", "வானிலை", "சந்தை",
    "மண்டி", "விலை", "விளைச்சல்", "விதை", "விதைப்பு", "அறுவடை", "விவசாயி", "விவசாயம்",
    "வணக்கம்", "பண்ணை"
}


def detect_user_language(user_message: str) -> str:
    """
    Strictly detects the active language of the user's message.
    Returns: 'te' (Telugu), 'hi' (Hindi), 'ta' (Tamil), or 'en' (English).
    """
    if not user_message:
        return 'en'

    # 1. Native Unicode Script Checks (Definitive)
    has_telugu = any('\u0c00' <= char <= '\u0c7f' for char in user_message)
    if has_telugu:
        return 'te'

    has_hindi = any('\u0900' <= char <= '\u097f' for char in user_message)
    if has_hindi:
        return 'hi'

    has_tamil = any('\u0b80' <= char <= '\u0bff' for char in user_message)
    if has_tamil:
        return 'ta'

    # 2. Transliterated phrase & keyword checks (Distinctive regional words only, NEVER standard English terms)
    msg_lower = user_message.lower().strip()
    words = set(msg_lower.replace('?', ' ').replace('.', ' ').replace('!', ' ').replace(',', ' ').split())

    tanglish_phrases = [
        "na polam", "na bhoomi", "panta sifarusu", "digubadi", "eruvulu", "purugu mandu",
        "thegulu mandu", "cheppu", "ela unnav", "paniki vastunda", "kavalenu", "chesukovali",
        "pettali", "vesukovali", "nela pariksha", "vithanalu", "saguneeru", "work avadam ledhu"
    ]
    tanglish_words = {
        "polam", "bhoomi", "panta", "pantalu", "eruvulu", "purugulu", "thegulu",
        "mandulu", "digubadi", "mokkajonna", "verusanaga", "cheraku", "mamidi",
        "arati", "kobbari", "danimma", "puchakaya", "puchakayi", "dhara", "varsham",
        "vathavaranam", "namaskaram", "cheppandi"
    }
    if any(p in msg_lower for p in tanglish_phrases) or any(w in words for w in tanglish_words):
        return 'te'

    hinglish_phrases = [
        "mera khet", "fasal ki jankari", "khad kitna dale", "dawai batao", "kaise kare",
        "pani kitna", "paidawar badhaye", "keet niyantran"
    ]
    hinglish_words = {
        "khet", "mitti", "fasal", "faslein", "paidawar", "dawai", "keede", "kisaan",
        "sinchai", "barish", "mausam"
    }
    if any(p in msg_lower for p in hinglish_phrases) or any(w in words for w in hinglish_words):
        return 'hi'

    thanglish_phrases = [
        "en nilam", "en pannai", "payir setham", "uram poda", "marunthu adikkanum",
        "thanni pachanum", "solunga"
    ]
    thanglish_words = {
        "nilam", "pannai", "payir", "thakkali", "karumbu", "vivasayi", "marundhu",
        "pasanam", "vanakkam"
    }
    if any(p in msg_lower for p in thanglish_phrases) or any(w in words for w in thanglish_words):
        return 'ta'

    # Default to English
    return 'en'


def is_agricultural_query(user_message: str) -> bool:
    """
    Evaluates whether the user's message is an agricultural, farming, soil,
    crop, pest, fertilizer, irrigation, market price, weather, farm profile, or greeting inquiry.
    Returns False for out-of-domain queries (e.g. people, entertainment, coding, non-farming topics).
    """
    if not user_message or not user_message.strip():
        return False

    msg_lower = user_message.lower().strip()

    # 1. Direct match on English keywords/phrases
    for kw in AGRICULTURAL_KEYWORDS_EN:
        if kw in msg_lower:
            return True

    # 2. Match on Telugu keywords
    for kw in AGRICULTURAL_KEYWORDS_TE:
        if kw in msg_lower:
            return True

    # 3. Match on Hindi keywords
    for kw in AGRICULTURAL_KEYWORDS_HI:
        if kw in msg_lower:
            return True

    # 4. Match on Tamil keywords
    for kw in AGRICULTURAL_KEYWORDS_TA:
        if kw in msg_lower:
            return True

    # 5. Check if query asks for system/greeting/assistance
    greeting_tokens = ["hi", "hello", "hey", "namaste", "namaskar", "namaskaram", "vanakkam", "help", "who are you", "what can you do"]
    if any(token == msg_lower or msg_lower.startswith(token + " ") or msg_lower.endswith(" " + token) for token in greeting_tokens):
        return True

    return False


def _get_out_of_domain_refusal(user_message: str) -> str:
    """
    Returns a polite, localized domain refusal message when the user asks a non-agricultural query.
    Strictly matches user's active language.
    """
    lang = detect_user_language(user_message)

    if lang == 'te':
        return (
            "❌ **క్షమించండి, నేను వ్యవసాయేతర ప్రశ్నలకు సమాధానం ఇవ్వలేను.**\n\n"
            "నేను **AgriSmart AI** వ్యవసాయ నిపుణుడిని (Agronomist AI). నేను కేవలం వ్యవసాయం, పంటలు, మరియు నేల యాజమాన్యానికి సంబంధించిన ప్రశ్నలకు మాత్రమే సమాధానం ఇవ్వగలను.\n\n"
            "🌾 **నేను సహాయం చేయగల అంశాలు:**\n"
            "• 🌾 **పంటలు & సాగు పద్ధతులు:** వరి, పత్తి, టమోటా, మిరప, పుచ్చకాయ, మొక్కజొన్న, వేరుశనగ మొదలైనవి.\n"
            "• 🧪 **ఎరువులు & నేల పోషకాలు:** N-P-K మోతాదులు, DAP, యూరియా, సేంద్రీయ ఎరువులు, సూక్ష్మ పోషకాలు.\n"
            "• 🦠 **పురుగులు & తెగుళ్ల నివారణ:** పిచికారీ మందుల మోతాదులు (ml/L), సమగ్ర సస్యరక్షణ (IPM).\n"
            "• 💧 **సాగునీటి యాజమాన్యం:** డ్రిప్ ఇరిగేషన్, నీటి తడుల షెడ్యూల్.\n"
            "• 💰 **మండీ ధరలు & దిగుబడి అంచనాలు:** కనీస మద్దతు ధర (MSP), మార్కెట్ విశ్లేషణ.\n"
            "• 🏡 **మీ నమోదైన పొలాల వివరాలు:** మీ భూమికి అనువైన ప్రత్యేక సిఫార్సులు.\n\n"
            "💡 *దయచేసి వ్యవసాయం, పంటలు లేదా ఎరువులకు సంబంధించిన ప్రశ్నను క్రింద అడగండి!*"
        )
    elif lang == 'hi':
        return (
            "❌ **क्षमा करें, मैं गैर-कृषि प्रश्नों का उत्तर नहीं दे सकता।**\n\n"
            "मैं **AgriSmart AI** कृषि विशेषज्ञ हूँ। मैं केवल कृषि, फसलों और खेती से जुड़े प्रश्नों में ही सहायता कर सकता हूँ।\n\n"
            "🌾 **मैं इन विषयों में सहायता कर सकता हूँ:**\n"
            "• 🌾 **फसलें और उन्नत किस्में:** धान, कपास, टमाटर, मिर्च, तरबूज, मक्का, दलहन आदि।\n"
            "• 🧪 **उर्वरक एवं पोषण प्रबंधन:** N-P-K संतुलित मात्रा, यूरिया, डीएपी, जैविक खाद।\n"
            "• 🦠 **कीट एवं रोग नियंत्रण:** अनुशंसित स्प्रे मात्रा और रोकथाम के उपाय।\n"
            "• 💧 **सिंचाई एवं जल प्रबंधन:** ड्रिप सिंचाई और पानी की आवश्यकता।\n"
            "• 💰 **मंडी भाव एवं एमएसपी (MSP):** बाजार मूल्य और पैदावार अनुमान।\n\n"
            "💡 *कृपया खेती या फसलों से संबंधित प्रश्न पूछें!*"
        )
    elif lang == 'ta':
        return (
            "❌ **மன்னிக்கவும், நான் விவசாயம் அல்லாத கேள்விகளுக்கு பதிலளிக்க முடியாது.**\n\n"
            "நான் **AgriSmart AI** விவசாய ஆலோசகர். நான் விவசாயம், பயிர்கள் மற்றும் மண் மேலாண்மை தொடர்பான கேள்விகளுக்கு மட்டுமே பதிலளிக்க முடியும்.\n\n"
            "🌾 **நான் உதவக்கூடிய பகுதிகள்:**\n"
            "• 🌾 **பயிர்கள் மற்றும் சாகுபடி:** நெல், பருத்தி, தக்காளி, மிளகாய், தர்பூசணி, சோளம் போன்றவை.\n"
            "• 🧪 **உர மேலாண்மை:** N-P-K சமச்சீர் உரங்கள், யூரியா, டிஏபி, இயற்கை உரங்கள்.\n"
            "• 🦠 **பூச்சி மற்றும் நோய் கட்டுப்பாடு:** தெளிப்பு மருந்தளவு மற்றும் ஒருங்கிணைந்த பயிர் பாதுகாப்பு.\n"
            "• 💧 **பாசன மேலாண்மை:** சொட்டு நீர் பாசனம் மற்றும் நீர் மேலாண்மை.\n"
            "• 💰 **சந்தை விலை மற்றும் விளைச்சல்:** மண்டி விலை மற்றும் கொள்முதல் விலை (MSP).\n\n"
            "💡 *தயவுசெய்து விவசாயம் அல்லது பயிர்கள் தொடர்பான கேள்விகளைக் கேளுங்கள்!*"
        )
    else:
        return (
            "❌ **I can only assist with agricultural and farming queries.**\n\n"
            "I am **AgriSmart AI**, a dedicated agricultural agronomist and farm advisory assistant. I cannot answer queries about general trivia, people, entertainment, coding, or non-farming topics.\n\n"
            "🌾 **I can assist you with:**\n"
            "• 🌾 **Crop Cultivation & Varieties:** Rice, Cotton, Tomato, Chilli, Watermelon, Maize, Pulses, Sugarcane, etc.\n"
            "• 🧪 **Fertilizer & Soil Nutrition:** Balanced N-P-K dosages, DAP, Urea, micronutrients, and soil pH.\n"
            "• 🦠 **Pest & Disease Control:** Spray schedules, chemical dosages (ml/L), and IPM practices.\n"
            "• 💧 **Irrigation & Water Management:** Drip schedules, critical moisture windows.\n"
            "• 📊 **Harvest Yield & Market Trends:** Mandi prices, MSP support rates, and agro-weather.\n"
            "• 🏡 **Your Farm Profile:** Insights tailored to your registered land parcels.\n\n"
            "💡 *Please ask any question related to crops, soils, fertilizers, pests, or your farm!*"
        )


def get_ai_config() -> Dict[str, Any]:
    """
    Detects configured AI provider and API keys from environment.
    Priority: GEMINI_API_KEY -> OPENAI_API_KEY -> AI_API_KEY.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    generic_key = os.environ.get("AI_API_KEY", "").strip()

    if gemini_key:
        provider = "builtin" if gemini_key in ("builtin", "builtin_agri_intelligence", "demo", "local") else "gemini"
        return {
            "is_configured": True,
            "provider": provider,
            "api_key": gemini_key,
            "model": os.environ.get("GEMINI_MODEL", "gemini-1.5-flash" if provider == "gemini" else "Built-in ICAR Agronomist"),
        }
    elif openai_key:
        return {
            "is_configured": True,
            "provider": "openai",
            "api_key": openai_key,
            "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        }
    elif generic_key:
        provider = os.environ.get("AI_PROVIDER", "gemini").lower()
        return {
            "is_configured": True,
            "provider": provider,
            "api_key": generic_key,
            "model": os.environ.get("AI_MODEL", "gemini-1.5-flash" if provider == "gemini" else "gpt-4o-mini"),
        }
    else:
        return {
            "is_configured": False,
            "provider": None,
            "api_key": None,
            "model": None,
        }


def build_user_agriculture_context(user_id: int) -> str:
    """
    Constructs a structured agricultural context block for the authenticated user.
    Strictly isolated to user_id.
    """
    user = get_user_by_id(user_id)
    user_name = user["name"] if user else "Farmer"

    # 1. User Farms
    farms = get_user_farms(user_id)
    if farms:
        farm_lines = []
        for f in farms:
            crop_str = f"Current Crop: {f['current_crop']}" if f.get("current_crop") else "No active crop recorded"
            farm_lines.append(
                f"  - Farm '{f['farm_name']}': {f['land_area']} acres, {f['soil_type']} soil, "
                f"{f['irrigation_type']} irrigation located in {f['district']}, {f['state']}. ({crop_str})"
            )
        farms_context = "\n".join(farm_lines)
    else:
        farms_context = "  - No registered farm parcels found in profile."

    # 2. Recent Crop Recommendations
    crop_preds = get_user_crop_predictions(user_id, limit=3)
    if crop_preds:
        crop_lines = []
        for cp in crop_preds:
            farm_info = f" for farm '{cp['farm_name']}'" if cp.get("farm_name") else ""
            crop_lines.append(
                f"  - Recommended Crop: {cp['predicted_crop'].title()} (Confidence: {round(cp['confidence']*100, 1)}%){farm_info} "
                f"with Soil N-P-K: {cp['n']}-{cp['p']}-{cp['k']}, pH: {cp['ph']}, Temp: {cp['temperature']}°C, Rainfall: {cp['rainfall']}mm"
            )
        crop_context = "\n".join(crop_lines)
    else:
        crop_context = "  - No recent crop recommendations found."

    # 3. Recent Yield Predictions
    yield_preds = get_user_yield_predictions(user_id, limit=3)
    if yield_preds:
        yield_lines = []
        for yp in yield_preds:
            farm_info = f" on farm '{yp['farm_name']}'" if yp.get("farm_name") else ""
            yield_lines.append(
                f"  - Crop: {yp['crop_type']}{farm_info} ({yp['farm_area']} acres, {yp['soil_type']} soil, {yp['season']} season) "
                f"-> Predicted Harvest: {yp['predicted_yield']} Tons ({yp['yield_per_acre']} tons/acre). "
                f"Inputs used: {yp['fertilizer_used']}t fert, {yp['pesticide_used']}kg pest, {int(yp['water_usage'])}m³ water."
            )
        yield_context = "\n".join(yield_lines)
    else:
        yield_context = "  - No recent harvest yield simulations found."

    # 4. Recent Disease Lookups
    disease_lookups = get_user_disease_lookups(user_id, limit=3)
    if disease_lookups:
        disease_lines = []
        for dl in disease_lookups:
            disease_lines.append(
                f"  - Plant: {dl['plant_name']} | Disease: {dl['disease_name']} (Class: {dl['class_name']})"
            )
        disease_context = "\n".join(disease_lines)
    else:
        disease_context = "  - No recent disease lookups recorded."

    # 5. Global Weather Snapshot (from dataset)
    try:
        w_analyzer = get_weather_analyzer()
        w_stats = w_analyzer.get_summary_statistics()
        w_advisory = w_analyzer.get_agro_advisory(latest_n_days=7)
        weather_context = (
            f"  - Location: {w_stats.get('location', 'Kakinada, Andhra Pradesh')}, 5-Year Dataset.\n"
            f"  - Avg Temp: {w_stats.get('average_temperature_c', 27.2)}°C | Avg Humidity: {w_stats.get('average_humidity_pct', 75.0)}% | Total Rain: {w_stats.get('total_rainfall_mm', 4200)}mm\n"
            f"  - Advisory Status: Spray Suitability: {w_advisory.get('spray_suitability', 'Normal')} | Fungal Risk: {w_advisory.get('fungal_disease_risk', 'Moderate')}"
        )
    except Exception:
        weather_context = "  - Weather analytics summary available via /weather."

    # 6. Global Market Snapshot (from dataset)
    try:
        m_analyzer = get_market_analyzer()
        m_stats = m_analyzer.get_price_statistics()
        m_msp = m_analyzer.get_msp_comparison()
        market_context = (
            f"  - Historical Mandi Bulletin (01-Oct-2026): 25 commodities tracked across 6 groups.\n"
            f"  - Average Market Price: Rs. {int(m_stats.get('average_market_price_rs_quintal', 4896))}/Quintal (Range: Rs. {int(m_stats.get('min_market_price_rs_quintal', 1200))} - {int(m_stats.get('max_market_price_rs_quintal', 13500))})\n"
            f"  - Commodities Trading Above Govt MSP: {m_msp.get('commodities_trading_above_msp', 14)} of {m_msp.get('total_msp_covered_commodities', 19)}"
        )
    except Exception:
        market_context = "  - Mandi market intelligence summary available via /market."

    return f"""AUTHENTICATED FARMER CONTEXT:
Name: {user_name} (User ID: {user_id})

[REGISTERED FARMS]
{farms_context}

[RECENT CROP RECOMMENDATIONS]
{crop_context}

[RECENT HARVEST YIELD PREDICTIONS]
{yield_context}

[RECENT PLANT DISEASE LOOKUPS]
{disease_context}

[REGIONAL AGRO-WEATHER CONTEXT]
{weather_context}

[REGIONAL MANDI MARKET CONTEXT]
{market_context}
"""


def format_system_prompt(user_context: str) -> str:
    """Builds the comprehensive agronomist system prompt with strict domain and language boundaries."""
    return f"""You are AgriSmart AI, an expert agricultural assistant, certified agronomist, and farm advisor.
Your mission is to provide accurate, scientifically sound, actionable, and safety-conscious guidance to farmers in the EXACT language they ask: English if asked in English, Telugu (తెలుగు) if asked in Telugu, Hindi (हिंदी) if asked in Hindi, and Tamil (தமிழ்) if asked in Tamil.

{user_context}

CRITICAL DOMAIN & LANGUAGE PRINCIPLES:
1. STRICT LANGUAGE MATCHING:
   - You MUST reply in the language the user speaks. If the user asks in English, reply entirely in English. If the user asks in Telugu, reply in Telugu. If in Hindi, reply in Hindi. If in Tamil, reply in Tamil.
2. STRICT AGRICULTURAL DOMAIN BOUNDARY:
   - You are EXCLUSIVELY an agricultural and farming assistant.
   - If the user asks about non-agricultural topics (e.g. people/friends, entertainment, movies, coding, sports, general trivia, politics, or unrelated topics), you MUST POLITELY REFUSE in the user's language and state that you only answer questions related to agriculture, farming, crops, soils, fertilizers, pests, irrigation, weather, and mandi prices.
   - Do NOT attempt to answer non-farming queries or invent agricultural analogies for them.
3. User Data Utilization: When the farmer asks about their farms, previous recommendations, yield estimates, or searched diseases, answer accurately using their actual data provided above. If no data exists for a specific query, politely state that no prior record was found in their account.
4. Agriculture Safety First:
   - For chemical fertilizers, pesticides, fungicides, and herbicides: Always advise farmers to check product labels, follow safety data sheets, use protective gear (PPE), and consult local government Krishi Vigyan Kendras (KVK) or agricultural extension officers.
   - Do NOT give extreme, toxic, or unverified chemical cocktail recommendations. Prefer Integrated Pest Management (IPM) combining cultural, biological, and chemical controls.
5. Statistical Transparency:
   - Remind farmers that Crop Recommendation and Yield Prediction outputs are machine learning estimates based on historical datasets rather than commercial guarantees.
   - Note that mandi market data reflects historical bulletin snapshots.
6. Response Style:
   - Structure responses clearly with bullet points, emojis, bold highlights, and actionable takeaways.
   - Keep answers friendly, practical, respectful, and agronomically precise.
"""


def _sanitize_gemini_contents(messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Sanitizes chat history to ensure strictly alternating user and model turns for Gemini API."""
    contents: List[Dict[str, Any]] = []
    
    for msg in messages:
        text = msg.get("message", "").strip()
        if not text:
            continue
        role = "user" if msg.get("role") == "user" else "model"
        
        if contents and contents[-1]["role"] == role:
            contents[-1]["parts"][0]["text"] += f"\n\n{text}"
        else:
            contents.append({"role": role, "parts": [{"text": text}]})

    if contents and contents[0]["role"] != "user":
        contents.insert(0, {"role": "user", "parts": [{"text": "Hello AgriSmart AI."}]})

    if contents and contents[-1]["role"] != "user":
        contents.append({"role": "user", "parts": [{"text": "Please provide agricultural recommendations."}]})

    return contents


def _call_gemini_api(api_key: str, model: str, system_prompt: str, messages: List[Dict[str, str]]) -> str:
    """Calls the Google Gemini REST API."""
    clean_model = model if model.startswith("gemini") else "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{clean_model}:generateContent?key={api_key}"

    sanitized_contents = _sanitize_gemini_contents(messages)
    if not sanitized_contents:
        sanitized_contents = [{"role": "user", "parts": [{"text": "Hello, please assist me with farming advisory."}]}]

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": sanitized_contents,
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1200,
        },
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=12) as response:
        resp_data = json.loads(response.read().decode("utf-8"))
        candidates = resp_data.get("candidates", [])
        if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
            return candidates[0]["content"]["parts"][0].get("text", "")
        raise ValueError("Unexpected response format from Gemini API.")


def _call_openai_api(api_key: str, model: str, system_prompt: str, messages: List[Dict[str, str]]) -> str:
    """Calls the OpenAI REST API."""
    url = "https://api.openai.com/v1/chat/completions"

    formatted_msgs = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        text = msg.get("message", "").strip()
        if text:
            role = "user" if msg.get("role") == "user" else "assistant"
            formatted_msgs.append({"role": role, "content": text})

    payload = {
        "model": model or "gpt-4o-mini",
        "messages": formatted_msgs,
        "temperature": 0.3,
        "max_tokens": 1200,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=12) as response:
        resp_data = json.loads(response.read().decode("utf-8"))
        choices = resp_data.get("choices", [])
        if choices and "message" in choices[0] and "content" in choices[0]["message"]:
            return choices[0]["message"]["content"]
        raise ValueError("Unexpected response format from OpenAI API.")


def _generate_local_agronomist_response(user_id: int, user_message: str) -> str:
    """
    Built-in Expert Agronomist Intelligence Engine.
    Provides precise, context-aware agronomic answers matching the user's active language:
    English -> English, Telugu -> Telugu, Hindi -> Hindi, Tamil -> Tamil.
    """
    msg_lower = user_message.lower().strip()
    lang = detect_user_language(user_message)

    # 0. Strict Domain Validation: If out of agricultural scope, refuse in active language
    if not is_agricultural_query(user_message):
        return _get_out_of_domain_refusal(user_message)

    # 1. Fetch User Context from Database
    farms = get_user_farms(user_id)
    crop_preds = get_user_crop_predictions(user_id, limit=1)
    yield_preds = get_user_yield_predictions(user_id, limit=1)
    disease_lookups = get_user_disease_lookups(user_id, limit=1)

    # 2. Check for User Farm Profile Queries
    if any(k in msg_lower for k in ["my farm", "registered farm", "holding", "నా పొలం", "నా భూమి", "na polam", "na bhoomi", "मेरा खेत", "என் நிலம்", "என் பண்ணை", "en nilam", "en pannai"]):
        if lang == 'ta':
            if farms:
                farm_info = "\n".join([f"• **{f['farm_name']}**: {f['land_area']} ஏக்கர் ({f['soil_type']} மண், {f['irrigation_type']} பாசனம், {f['district']}, {f['state']})" for f in farms])
                return f"🏡 **உங்கள் பதிவு செய்யப்பட்ட நிலங்கள்:**\n\n{farm_info}\n\n💡 உங்கள் நிலத்திற்கு பிரத்யேக பரிந்துரைகளுக்கு **Crop Recommendation** அல்லது **1-Click Farm Advisory** ஐப் பயன்படுத்தவும்."
            else:
                return "🏡 உங்கள் சுயவிவரத்தில் இன்னும் நிலம் பதிவு செய்யப்படவில்லை. டேஷ்போர்டில் **Add Farm** என்பதைக் கிளிக் செய்து உங்கள் நில விவரங்களைச் சேர்க்கவும்."
        elif lang == 'te':
            if farms:
                farm_info = "\n".join([f"• **{f['farm_name']}**: {f['land_area']} ఎకరాలు ({f['soil_type']} నేల, {f['irrigation_type']} విధానం, {f['district']}, {f['state']})" for f in farms])
                return f"🏡 **మీ నమోదైన పొలాల వివరాలు:**\n\n{farm_info}\n\n💡 మీ పొలానికి ప్రత్యేక సిఫార్సుల కొరకు **Crop Recommendation** లేదా **1-Click Farm Advisory** ని ఉపయోగించవచ్చు."
            else:
                return "🏡 మీ ప్రొఫైల్‌లో ఇంకా పొలం నమోదు కాలేదు. డ్యాష్‌బోర్డ్‌లో **Add Farm** పై క్లిక్ చేసి మీ భూమి వివరాలు నమోదు చేసుకోండి."
        elif lang == 'hi':
            if farms:
                farm_info = "\n".join([f"• **{f['farm_name']}**: {f['land_area']} एकड़ ({f['soil_type']} मिट्टी, {f['irrigation_type']} सिंचाई, {f['district']}, {f['state']})" for f in farms])
                return f"🏡 **आपके पंजीकृत खेतों का विवरण:**\n\n{farm_info}\n\n💡 विशेष सलाह के लिए **Crop Recommendation** का उपयोग करें।"
            else:
                return "🏡 आपके खाते में अभी कोई खेत पंजीकृत नहीं है। डैशबोर्ड पर **Add Farm** पर क्लिक करके जोड़ें।"
        else:
            if farms:
                farm_info = "\n".join([f"• **{f['farm_name']}**: {f['land_area']} Acres ({f['soil_type']}, {f['irrigation_type']} system in {f['district']}, {f['state']})" for f in farms])
                return f"🏡 **Your Registered Farm Holdings:**\n\n{farm_info}\n\n💡 You can generate tailor-made advisory for any of these farms from the **Crop Recommendation** module."
            else:
                return "🏡 No registered farm parcel found in your account yet. You can add your land holdings from the **My Farms** section on the dashboard."

    # 3. Check for User's Recommended Crop Query
    if any(k in msg_lower for k in ["recommended crop", "my crop", "what crop was recommended", "నాకు సిఫార్సు చేసిన పంట", "recommendation", "panta sifarusu"]):
        if crop_preds:
            cp = crop_preds[0]
            crop_name = cp['predicted_crop'].title()
            conf = round(cp['confidence'] * 100, 1)
            if lang == 'te':
                return (
                    f"🌾 **మీ తాజా నేల పరీక్ష సిఫార్సు:**\n\n"
                    f"• **సిఫార్సు చేసిన పంట:** **{crop_name}**\n"
                    f"• **AI కాన్ఫిడెన్స్:** **{conf}%**\n"
                    f"• **నేల పరీక్ష విలువలు:** N: {cp['n']} kg/ha, P: {cp['p']} kg/ha, K: {cp['k']} kg/ha, pH: {cp['ph']}\n"
                    f"• **వాతావరణం:** ఉష్ణోగ్రత: {cp['temperature']}°C, వర్షపాతం: {cp['rainfall']} mm\n\n"
                    f"💡 ఈ పంట మీ నేల పోషకాలకు మరియు వాతావరణ పరిస్థితులకు అత్యంత అనుకూలంగా ఉన్నట్లు మోడల్ నిర్ధారించింది."
                )
            elif lang == 'hi':
                return (
                    f"🌾 **आपकी नवीनतम फसल सिफारिश का सारांश:**\n\n"
                    f"• **सिफारिश की गई फसल:** **{crop_name}**\n"
                    f"• **मॉडल का विश्वास:** **{conf}%**\n"
                    f"• **मिट्टी प्रोफ़ाइल:** N: {cp['n']}, P: {cp['p']}, K: {cp['k']} kg/ha, pH: {cp['ph']}\n"
                    f"• **जलवायु सूचकांक:** तापमान: {cp['temperature']}°C, मौसमी वर्षा: {cp['rainfall']} mm"
                )
            elif lang == 'ta':
                return (
                    f"🌾 **உங்கள் பரிந்துரைக்கப்பட்ட பயிர் சுருக்கம்:**\n\n"
                    f"• **பரிந்துரைக்கப்பட்ட பயிர்:** **{crop_name}**\n"
                    f"• **AI துல்லியம்:** **{conf}%**\n"
                    f"• **மண் ஊட்டச்சத்து:** N: {cp['n']}, P: {cp['p']}, K: {cp['k']}, pH: {cp['ph']}"
                )
            else:
                return (
                    f"🌾 **Your Latest Crop Recommendation Summary:**\n\n"
                    f"• **Recommended Crop:** **{crop_name}**\n"
                    f"• **Model Confidence:** **{conf}%**\n"
                    f"• **Tested Soil Profile:** Nitrogen: {cp['n']} kg/ha, Phosphorus: {cp['p']} kg/ha, Potassium: {cp['k']} kg/ha, Soil pH: {cp['ph']}\n"
                    f"• **Climate Match:** Temp: {cp['temperature']}°C, Seasonal Rainfall: {cp['rainfall']} mm\n\n"
                    f"💡 This crop was selected by our Random Forest ML engine because your soil macro-nutrients and local climate indices align with ICAR optimal agronomic growth windows."
                )

    # 4. Check for User's Yield Query
    if any(k in msg_lower for k in ["my yield", "yield prediction", "explain my yield", "నా దిగుబడి", "digubadi", "meri paidawar"]):
        if yield_preds:
            yp = yield_preds[0]
            if lang == 'te':
                return (
                    f"📊 **మీ తాజా దిగుబడి అంచనా:**\n\n"
                    f"• **పంట:** **{yp['crop_type']}** ({yp['farm_area']} ఎకరాలు, {yp['soil_type']})\n"
                    f"• **అంచనా మొత్తం దిగుబడి:** **{yp['predicted_yield']} టన్నులు** ({yp['yield_per_acre']} టన్నులు/ఎకరా)\n"
                    f"• **వాడిన వనరులు:** {yp['fertilizer_used']} టన్నుల ఎరువులు, {yp['pesticide_used']} కేజీల మందులు, {int(yp['water_usage'])} m³ నీరు\n\n"
                    f"💡 సరైన డ్రిప్ ఇరిగేషన్ మరియు సమతుల్య NPK ఎరువుల నిర్వహణ ద్వారా దిగుబడిని మరో 10-15% వరకు పెంచుకోవచ్చు."
                )
            elif lang == 'hi':
                return (
                    f"📊 **आपकी नवीनतम फसल पैदावार का अनुमान:**\n\n"
                    f"• **फसल:** **{yp['crop_type']}** ({yp['farm_area']} एकड़, {yp['soil_type']})\n"
                    f"• **कुल अनुमानित पैदावार:** **{yp['predicted_yield']} टन** ({yp['yield_per_acre']} टन/एकड़)\n"
                    f"• **प्रयुक्त संसाधन:** {yp['fertilizer_used']}t उर्वरक, {yp['pesticide_used']}kg कीटनाशक, {int(yp['water_usage'])} m³ पानी"
                )
            elif lang == 'ta':
                return (
                    f"📊 **உங்கள் சமீபத்திய விளைச்சல் மதிப்பீடு:**\n\n"
                    f"• **பயிர்:** **{yp['crop_type']}** ({yp['farm_area']} ஏக்கர்)\n"
                    f"• **மதிப்பிடப்பட்ட விளைச்சல்:** **{yp['predicted_yield']} டன்**"
                )
            else:
                return (
                    f"📊 **Your Latest Harvest Yield Simulation:**\n\n"
                    f"• **Crop:** **{yp['crop_type']}** on **{yp['farm_area']} Acres** ({yp['soil_type']} soil, {yp['season']} season)\n"
                    f"• **Total Estimated Harvest:** **{yp['predicted_yield']} Metric Tons** ({yp['yield_per_acre']} t/acre)\n"
                    f"• **Inputs Modeled:** {yp['fertilizer_used']}t Fertilizer, {yp['pesticide_used']}kg Crop Protection, {int(yp['water_usage'])} m³ Irrigation Water.\n\n"
                    f"💡 To maximize yield density, ensure split nitrogen top-dressing and maintain critical moisture windows during the flowering and fruit/grain filling stages."
                )

    # 5. Combined Irrigation + Weather Spraying Inquiry (e.g. drip irrigation + chemical spraying in weather)
    if ("irrigation" in msg_lower or "drip" in msg_lower or "సాగునీరు" in msg_lower or "నీరు" in msg_lower or "पासनम" in msg_lower or "सिंचाई" in msg_lower) and \
       ("spray" in msg_lower or "chemical" in msg_lower or "weather" in msg_lower or "పిచికారీ" in msg_lower or "వాతావరణం" in msg_lower or "மழை" in msg_lower):
        if lang == 'te':
            return (
                "💧 **రైతులకు డ్రిప్ ఇరిగేషన్ & వాతావరణ ఆధారిత మందుల పిచికారీ సూచనలు:**\n\n"
                "1. **డ్రిప్ ఇరిగేషన్ సమయాలు:** ఉదయం 6:00 నుండి 9:00 గంటల మధ్య లేదా సాయంత్రం వేళల్లో డ్రిప్ ద్వారా నీరు అందించాలి. తేలికపాటి నేలల్లో రోజుకు లేదా 2 రోజులకు 2-3 గంటల పాటు తడులు ఇవ్వాలి.\n"
                "2. **రసాయన మందుల పిచికారీ విండో:** గాలి వేగం తక్కువగా (<10 km/h) మరియు ఉష్ణోగ్రత 30°C కంటే తక్కువగా ఉన్నప్పుడు (ఉదయం 7 నుండి 10 గంటల మధ్య) మాత్రమే పిచికారీ చేయాలి. మధ్యాహ్నం ఎండలో పిచికారీ చేయరాదు.\n"
                "3. **వర్ష సూచన జాగ్రత్తలు:** రాబోయే 4-6 గంటల్లో వర్షం కురిసే అవకాశం ఉంటే పిచికారీ చేయవద్దు. పొలంలో నీరు నిలవకుండా మురుగు కాల్వలను సిద్ధం చేయండి.\n"
                "4. **సమగ్ర సస్యరక్షణ:** సిఫార్సు చేసిన మోతాదులోనే మందులను కలిపి రక్షణ దుస్తులు (PPE) ధరించి పిచికారీ చేయండి."
            )
        elif lang == 'hi':
            return (
                "💧 **ड्रिप सिंचाई और मौसम आधारित कीटनाशक छिड़काव प्रबंधन:**\n\n"
                "1. **ड्रिप सिंचाई:** सुबह 6:00 से 9:00 बजे के बीच सिंचाई करें। रेतीली व दोमट मिट्टी में हर 1-2 दिन पर 2-3 घंटे ड्रिप चलाएं।\n"
                "2. **छिड़काव का सही समय:** हवा की गति कम होने पर सुबह 7 से 10 बजे के बीच ही कीटनाशक का छिड़काव करें। दोपहर की तेज धूप में छिड़काव से बचें।\n"
                "3. **बारिश की सावधानी:** यदि अगले 4-6 घंटों में बारिश की संभावना हो तो छिड़काव टालें।"
            )
        elif lang == 'ta':
            return (
                "💧 **சொட்டு நீர் பாசனம் மற்றும் வானிலை அடிப்படையிலான தெளிப்பு மேலாண்மை:**\n\n"
                "1. **பாசன நேரம்:** அதிகாலை 6:00 முதல் 9:00 மணிக்குள் சொட்டு நீர் பாசனம் செய்யவும்.\n"
                "2. **தெளிப்பு நேரம்:** காற்று குறைவாக உள்ள காலை 7:00 முதல் 10:00 மணி வரை மருந்துகளைத் தெளிக்கவும்.\n"
                "3. **மழை பாதுகாப்பு:** அடுத்த 4-6 மணி நேரத்தில் மழை பெய்யும் வாய்ப்பு இருந்தால் மருந்து தெளிப்பதைத் தவிர்க்கவும்."
            )
        else:
            return (
                "💧 **Integrated Drip Irrigation & Weather-Calibrated Spraying Strategy:**\n\n"
                "1. **Optimal Drip Irrigation Schedule:** Run drip cycles in early morning hours (6:00 AM - 9:00 AM). In sandy loam soils, deliver 2-3 hour split fertigation cycles every 1-2 days to avoid deep percolation losses.\n"
                "2. **Chemical Spray Window & Temperature Safety:** Spray chemical pesticides/fungicides only when wind velocity is calm (<10 km/h) and ambient temperature is below 30°C (best window: 7:00 AM - 10:00 AM). Never spray under intense midday sun to avoid phytotoxicity and rapid chemical evaporation.\n"
                "3. **Rain & Humidity Precautions:** Postpone foliar spraying if rainfall is forecasted within the next 4-6 hours. Maintain field drainage channels to prevent rootzone hypoxia during monsoon bursts.\n"
                "4. **Protective Measures:** Strictly follow calibrated dosages (ml/L) and wear protective masks/gloves during chemical handling."
            )

    # 6. Watermelon Agronomy (పుచ్చకాయ / Watermelon / Tarbooj / தர்பூசணி)
    if any(k in msg_lower for k in ["watermelon", "water melon", "పుచ్చకాయ", "puchakaya", "puchakayi", "tarbooj", "tarbuz", "தர்பூசணி"]):
        if lang == 'te':
            return (
                "🍉 **పుచ్చకాయ (Watermelon) సమగ్ర సాగు & నేల యాజమాన్యం:**\n\n"
                "1. **అనుకూలమైన నేలలు:** నీరు త్వరగా ఇంకిపోయే తేలికపాటి ఇసుక దుబ్బ నేలలు (Sandy Loam) మరియు ఒండ్రు నేలలు చాలా శ్రేష్టం. నేల pH **6.0 నుండి 7.5** మధ్య ఉండాలి.\n"
                "2. **భూమి తయారీ & మల్చింగ్:** ఎకరానికి **10-12 టన్నుల పశువుల ఎరువు (FYM)** వేసి లోతుగా దున్నాలి. 25-30 మైక్రాన్ల సిల్వర్-బ్లాక్ ప్లాస్టిక్ మల్చింగ్ మరియు డ్రిప్ ఇరిగేషన్ వాడటం వల్ల కలుపు లేకుండా నాణ్యమైన అధిక దిగుబడి (25-35 టన్నులు/ఎకరా) వస్తుంది.\n"
                "3. **ఎరువుల యాజమాన్యం (NPK):** ఎకరానికి 80 kg యూరియా, 50 kg DAP, 60 kg పొటాష్. పూత మరియు కాయ పరిమాణం పెరిగే దశలో 0:52:34 మరియు 0:0:50 ఫెర్టిగేషన్ ఇవ్వడం ద్వారా కాయల్లో తీపి (Brix 11-13) మరియు బరువు పెరుగుతుంది.\n"
                "4. **సస్యరక్షణ:** తామర పురుగులు, పేనుబంక నివారణకు *డయాఫెంథియురాన్ 50% WP* @ 1.0 గ్రా/లీ; బూడిద మరియు ఆకుమచ్చ తెగుళ్లకు *అజాక్సిస్ట్రోబిన్ + డైఫెనోకోనజోల్* @ 1.0 ml/లీ పిచికారీ చేయాలి.\n"
                "5. **నీటి నిర్వహణ:** కాయ కోతకు 7-10 రోజుల ముందు నీటి తడులను తగ్గించాలి (దీనివల్ల కాయలు పగలకుండా నిల్వ సామర్థ్యం పెరుగుతుంది)."
            )
        elif lang == 'hi':
            return (
                "🍉 **तरबूज (Watermelon) की उन्नत खेती और उर्वरक प्रबंधन:**\n\n"
                "1. **उपयुक्त मिट्टी:** अच्छी जल निकासी वाली बलुई दोमट मिट्टी (Sandy Loam), pH **6.0 से 7.5**।\n"
                "2. **मल्चिंग और ड्रिप:** ड्रिप सिंचाई और 25 माइक्रोन सिल्वर-ब्लैक प्लास्टिक मल्चिंग से 30% अधिक पैदावार होती है।\n"
                "3. **उर्वरक प्रबंधन:** फल विकास के समय 0:0:50 (पोटाश) और बोरॉन का प्रयोग मिठास (TSS 11-13 Brix) बढ़ाता है।"
            )
        elif lang == 'ta':
            return (
                "🍉 **தர்பூசணி (Watermelon) சாகுபடி மற்றும் உர மேலாண்மை:**\n\n"
                "1. **மண் தேவைகள்:** நல்ல வடிகால் வசதியுள்ள மணல் கலந்த வண்டல் மண் (Sandy Loam) சிறந்தது, pH **6.0 - 7.5**.\n"
                "2. **உர மேலாண்மை:** ஏக்கருக்கு 10 டன் தொழு உரம், 80 கிலோ யூரியா, 50 கிலோ டிஏபி, 60 கிலோ பொட்டாஷ். காய் வளர்ச்சிக்கு 0:0:50 பொட்டாசியம் சல்பேட் அளிக்கவும்.\n"
                "3. **பூச்சி & நோய் கட்டுப்பாடு:** இலைப்பேன் மற்றும் சாறு உறிஞ்சும் பூச்சிகளுக்கு *பெகாசஸ் (Diafenthiuron)* @ 1.0 கிராம்/லிட்டர் தெளிக்கவும்."
            )
        else:
            return (
                "🍉 **Watermelon Agronomy & Soil Management Guide:**\n\n"
                "1. **Optimal Soil Requirements:** Well-drained, warm **Sandy Loam to Alluvial Loamy soils** rich in organic carbon. Ideal soil pH is **6.0 - 7.5**. Avoid heavy waterlogged clay soils.\n"
                "2. **Land Preparation & Mulching:** Incorporate 10-12 tons/acre FYM. Raised beds (1.5-2.0m width) with Drip lines and 25-30 micron Silver-Black Mulch sheets boost fruit set and sweetness.\n"
                "3. **Nutrient Management (NPK):** Basal application of DAP and Potash; fertigate 19:19:19 during vegetative growth, switch to 13:40:13 at flowering, and apply 0:0:50 (Potassium Sulfate) + Boron during fruit enlargement for uniform sugar density (TSS 11-13 Brix).\n"
                "4. **Crop Protection:** Manage Thrips/Mites with *Spinetoram 11.7% SC* @ 0.9 ml/L or *Diafenthiuron* @ 1.0 g/L. Control Downy/Powdery Mildew with *Azoxystrobin + Difenoconazole* @ 1.0 ml/L.\n"
                "5. **Irrigation Strategy:** Provide consistent moisture through drip cycles; taper off water 7-10 days before harvest to prevent fruit cracking and concentrate sweetness."
            )

    # 7. Tomato Agronomy (టమోటా)
    if any(k in msg_lower for k in ["tomato", "టమోటా", "tamatar", "tamota", "தக்காளி"]):
        if any(k in msg_lower for k in ["soil", "నేల", "మట్టి", "suitable", "mitti", "matti", "மண்"]):
            if lang == 'te':
                return (
                    "🍅 **టమోటా సాగుకు అనుకూలమైన నేలలు & యాజమాన్యం:**\n\n"
                    "1. **అనుకూలమైన నేల రకం:** నీరు నిలవని తేలికపాటి ఇసుక దుబ్బ నేలలు (Sandy Loam), ఎర్ర నేలలు లేదా ఒండ్రు నేలలు (Loamy Soils) చాలా శ్రేష్టం.\n"
                    "2. **నేల pH స్థాయి:** **6.0 నుండి 7.0** (స్వల్ప ఆమ్ల నుండి సమతుల్య pH) అత్యంత అనుకూలం.\n"
                    "3. **భూమి తయారీ:** 2-3 సార్లు లోతుగా దుక్కి దున్ని, ఎకరానికి **10-12 టన్నుల పశువుల ఎరువు (FYM)** లేదా వర్మీకంపోస్ట్ వేసి కలపాలి.\n"
                    "4. **నేల శుద్ధి:** వేరు కుళ్లు, ఎండు తెగులు నివారణకు ఎకరానికి **2.5 కేజీల ట్రైకోడెర్మా విరిడే**ని పశువుల ఎరువుతో కలిపి నేలలో వేయాలి.\n"
                    "5. **జాగ్రత్తలు:** నీరు నిలిచి ఉండే బంకమన్ను నేలలు (Heavy Clay) టమోటాకు మంచివి కావు; ఇవి వేరు కుళ్లుకు దారితీస్తాయి.\n\n"
                    "💡 *డ్రిప్ ఇరిగేషన్ మరియు మల్చింగ్ షీట్ వాడటం వల్ల నాణ్యమైన అధిక దిగుబడి (15-20 టన్నులు/ఎకరా) పొందవచ్చు.*"
                )
            else:
                return (
                    "🍅 **Optimal Soil Requirements for Tomato Crop:**\n\n"
                    "1. **Best Soil Types:** Well-drained, fertile **Sandy Loam to Deep Loamy soils** rich in organic humus. Alluvial and light red soils with good internal aeration are ideal.\n"
                    "2. **Soil pH Range:** Optimal pH is **6.0 to 7.0** (slightly acidic to neutral). Avoid soils with pH > 8.0 or highly saline ground.\n"
                    "3. **Land Preparation:** Deep ploughing followed by 2-3 harrowings. Incorporate **10 to 12 tons/acre of well-decomposed Farm Yard Manure (FYM)** or 3 tons/acre vermicompost.\n"
                    "4. **Biological Soil Treatment:** Mix **2.5 kg/acre of Trichoderma viride** and *Pseudomonas fluorescens* with organic compost to prevent soil-borne Fusarium wilt and damping-off.\n"
                    "5. **Drainage & Aeration:** Ensure adequate drainage. Heavy clay soils with poor water infiltration cause root asphyxiation, blossom end rot, and fungal root rots.\n\n"
                    "💡 *Pro-Tip: Raised bed planting with Drip Irrigation and 25-30 micron silver-black plastic mulching boosts tomato yield by 25-35%.*"
                )
        else:
            if lang == 'te':
                return (
                    "🍅 **టమోటా తెగుళ్లు & పురుగుల నివారణ షెడ్యూల్:**\n\n"
                    "• **కాయ తొలుచు పురుగు (Fruit Borer):** *క్లోరాంట్రానిలిప్రోల్ 18.5% SC (కోరాజెన్)* @ **0.4 ml/లీ** లేదా *ఫ్లూబెండియమైడ్ 39.35% SC (ఫేమ్)* @ **0.3 ml/లీ**.\n"
                    "• **తెల్లదోమ & తామర పురుగులు (Whitefly & Thrips):** *డయాఫెంథియురాన్ 50% WP (పెగాసస్)* @ **1.0 గ్రా/లీ** లేదా *ఎసిటామిప్రిడ్ 20% SP* @ **0.2 గ్రా/లీ**.\n"
                    "• **ఆకుమచ్చ & మాడ తెగులు (Early/Late Blight):** *మాంకోజెబ్ 75% WP* @ **2.5 గ్రా/లీ** లేదా *అజాక్సిస్ట్రోబిన్ + డైఫెనోకోనజోల్* @ **1.0 ml/లీ**.\n"
                    "• **సేంద్రీయ పద్ధతి:** వేప నూనె (10,000 PPM) @ **3.0 ml/లీ** పిచికారీ చేయాలి.\n\n"
                    "⚠️ *ఎల్లప్పుడూ ఉదయం లేదా సాయంత్రం వేళల్లోనే పిచికారీ చేయండి.*"
                )
            else:
                return (
                    "🍅 **Tomato Pest & Disease Spray Schedule:**\n\n"
                    "• **Fruit Borer (Helicoverpa armigera):** Spray *Chlorantraniliprole 18.5% SC (Coragen)* @ **0.4 ml/L** or *Flubendiamide 39.35% SC (Fame)* @ **0.3 ml/L**.\n"
                    "• **Whitefly & Thrips:** Spray *Diafenthiuron 50% WP (Pegasus)* @ **1.0 g/L** or *Acetamiprid 20% SP* @ **0.2 g/L**.\n"
                    "• **Early / Late Blight:** Spray *Mancozeb 75% WP* @ **2.5 g/L** or *Azoxystrobin + Difenoconazole* @ **1.0 ml/L**.\n"
                    "• **Organic Alternative:** Neem Oil (10,000 PPM) @ **3.0 ml/L** at early vegetative stage.\n\n"
                    "⚠️ *Always spray during cool morning or evening hours using protective gear.*"
                )

    # 8. Sugarcane Agronomy (చెరకు / Sugarcane / Ganna / கரும்பு)
    if any(k in msg_lower for k in ["sugarcane", "sugar cane", "చెరకు", "cheraku", "ganna", "கரும்பு", "karumbu"]):
        if lang == 'ta':
            return (
                "🎋 **கரும்பு (Sugarcane) பயிர் பாதுகாப்பு மற்றும் உர மேலாண்மை:**\n\n"
                "1. **உர மேலாண்மை:** ஏக்கருக்கு 150 கிலோ யூரியா, 60 கிலோ டிஏபி, 80 கிலோ பொட்டாஷ் உரங்களை 30, 60, 90 வது நாட்களில் பிரித்து இடவும்.\n"
                "2. **குருத்து துளைப்பான் (Early Shoot Borer):** *குளோரான்ட்ரானிலிப்ரோல் 18.5% SC* @ 0.4 மி.லி/லிட்டர் அல்லது *கார்டாப் ஹைட்ரோகுளோரைடு 4G* குருணைகளை ஏக்கருக்கு 10 கிலோ இடவும்.\n"
                "3. **செவ்வழுகல் நோய் (Red Rot):** நோய் தாக்காத விதைக் கரணைகளை *கார்பன்டசிம்* (1 கிராம்/லிட்டர்) கரைசலில் நனைத்து நடவும்."
            )
        elif lang == 'te':
            return (
                "🎋 **చెరకు సాగు సూచనలు & సస్యరక్షణ:**\n\n"
                "• **నేల:** లోతైన సారవంతమైన ఒండ్రు నేలలు, నల్లరేగడి నేలలు (pH 6.5 - 7.5).\n"
                "• **ఎరువులు:** ఎకరానికి 150 kg యూరియా, 60 kg DAP, 80 kg పొటాష్ (నాటిన 30, 60, 90 రోజులలో దఫాలుగా వేయాలి).\n"
                "• **పీక పురుగు (Early Shoot Borer):** *క్లోరాంట్రానిలిప్రోల్ 18.5% SC* @ 0.4 ml/లీ లేదా *ఫిప్రోనిల్ 0.3% G* గుళికలు @ 10 kg/ఎకరా.\n"
                "• **ఎర్ర కుళ్లు తెగులు (Red Rot):** తెగులు లేని ఆరోగ్యకరమైన విత్తన ముచ్చెలను *కార్బండజిమ్* (1 గ్రా/లీ) ద్రావణంలో నానబెట్టి నాటాలి."
            )
        else:
            return (
                "🎋 **Sugarcane Crop Management & Protection Guide:**\n\n"
                "• **Soil Suitability:** Deep, fertile loams, clay loams, and alluvial soils with neutral pH **6.5 - 7.5**.\n"
                "• **Nutrient Schedule:** Apply NPK 250-100-120 kg/ha in 3 split doses at 30, 60, and 90 Days After Planting (DAP).\n"
                "• **Early Shoot Borer (Chilo infuscatellus):** Apply *Chlorantraniliprole 18.5% SC* @ **0.4 ml/L** or broadcast *Fipronil 0.3% G* @ 10 kg/acre at 30-45 DAP.\n"
                "• **Red Rot Prevention:** Treat seed setts with *Carbendazim 50% WP* @ 1.0 g/L for 15 minutes before furrow planting."
            )

    # 9. Rice / Paddy Agronomy (వరి / நெல் / Dhaan)
    if any(k in msg_lower for k in ["rice", "paddy", "వరి", "vari", "dhaan", "dhan", "நெல்", "nel"]):
        if lang == 'te':
            return (
                "🌾 **వరి సాగు సమగ్ర సూచనలు & ఎరువుల యాజమాన్యం:**\n\n"
                "1. **అనుకూలమైన నేలలు:** నీటిని నిలుపుకునే బంకమన్ను, నల్లరేగడి మరియు ఒండ్రు నేలలు (Clay / Clay Loam), pH **5.5 నుండి 7.0**.\n"
                "2. **ఎరువుల మోతాదు (ఎకరానికి):**\n"
                "   - **నత్రజని (యూరియా):** 80-100 kg (3 దఫాలుగా: దుబ్బు చేసే దశ, పిలకల దశ, చిరుపొట్ట దశ).\n"
                "   - **భాస్వరం (DAP):** 50 kg (ఆఖరి దుక్కిలో బేసల్ డోస్‌గా మాత్రమే వేయాలి).\n"
                "   - **పొటాష్ (MOP):** 30 kg (సగం ఆఖరి దుక్కిలో, సగం చిరుపొట్ట దశలో).\n"
                "   - **జింక్ లోపం నివారణ:** ఎకరానికి **10 kg జింక్ సల్ఫేట్** ఆఖరి దుక్కిలో వేయాలి.\n"
                "3. **కాండం తొలుచు పురుగు (Stem Borer):** *క్లోరాంట్రానిలిప్రోల్ 18.5% SC* @ **0.4 ml/లీ** లేదా *కార్టాప్ హైడ్రోక్లోరైడ్ 4G గుళికలు* @ **8 kg/ఎకరా**.\n"
                "4. **అగ్గితెగులు (Blast):** *ట్రైసైక్లజోల్ 75% WP (బాన్)* @ **0.6 గ్రా/లీ** పిచికారీ చేయాలి."
            )
        else:
            return (
                "🌾 **Rice (Paddy) Agronomic Guide & Nutrient Schedule:**\n\n"
                "1. **Soil Suitability:** Heavy clay, clay loam, and silty soils with high water-holding capacity, pH **5.5 - 7.0**.\n"
                "2. **Nutrient Management (NPK):** Recommended NPK 120-60-40 kg/ha. Apply all P and 50% K as basal; split Nitrogen across basal, active tillering, and panicle initiation.\n"
                "3. **Stem Borer & Leaf Folder:** Spray *Chlorantraniliprole 18.5% SC* @ **0.4 ml/L** or broadcast *Cartap Hydrochloride 4% G* @ **10 kg/acre**.\n"
                "4. **Blast & Sheath Blight:** Spray *Tricyclazole 75% WP* @ **0.6 g/L** or *Hexaconazole 5% SC* @ **2.0 ml/L**."
            )

    # 10. Cotton Agronomy (పత్తి / பருத்தி / Kapas)
    if any(k in msg_lower for k in ["cotton", "పత్తి", "patthi", "kapas", "பருத்தி", "paruthi"]):
        if lang == 'te':
            return (
                "🌾 **పత్తి సాగు సమగ్ర సూచనలు & గులాబీ పురుగు నివారణ:**\n\n"
                "1. **నేల రకం:** లోతైన నల్లరేగడి నేలలు (Black Soils) మరియు లోతైన ఎర్ర నేలలు, pH **6.5 నుండి 8.0**.\n"
                "2. **గులాబీ రంగు పురుగు (Pink Bollworm):** పూత దశలో లింగాకర్షక బుట్టలు (Pheromone traps 8/ఎకరా) అమర్చాలి. తీవ్రత ఉంటే *ఎమామెక్టిన్ బెంజోయేట్ 5% SG* @ **0.5 గ్రా/లీ** లేదా *స్పైనెటోరమ్ 11.7% SC* @ **0.8 ml/లీ** పిచికారీ చేయాలి.\n"
                "3. **రసం పీల్చే పురుగులు (Whitefly/Jassids):** *డయాఫెంథియురాన్ 50% WP (పెగాసస్)* @ **1.0 గ్రా/లీ** లేదా *ఫ్లోనికామిడ్ 50% WG (ఉలాలా)* @ **0.3 గ్రా/లీ**.\n"
                "4. **ఎరువులు:** ఎకరానికి 100 kg యూరియా, 50 kg DAP, 40 kg పొటాష్ సమతుల్యంగా వేయాలి."
            )
        else:
            return (
                "🌾 **Cotton Crop Protection & Management:**\n\n"
                "1. **Soil & Climate:** Deep black cotton soils (Vertisols) or well-drained fertile loams, pH **6.5 - 8.0** with adequate moisture retention.\n"
                "2. **Pink Bollworm Management:** Install 8 pheromone traps/acre. Spray *Emamectin Benzoate 5% SG* @ **0.5 g/L** or *Spinetoram 11.7% SC* @ **0.8 ml/L** upon cross-boll infestation threshold.\n"
                "3. **Sucking Pest Complex:** Spray *Diafenthiuron 50% WP* @ **1.0 g/L** or *Flonicamid 50% WG* @ **0.3 g/L**."
            )

    # 11. Chilli / Mirchi (మిరప / மிளகாய்)
    if any(k in msg_lower for k in ["chilli", "chili", "మిరప", "mirchi", "mirapa", "மிளகாய்"]):
        if lang == 'te':
            return (
                "🌶️ **మిరప సాగు సూచనలు & ముడత తెగులు నివారణ:**\n\n"
                "• **నేల:** నీరు నిలవని ఎర్ర నేలలు, తేలికపాటి నల్లరేగడి నేలలు (pH 6.5 - 7.5).\n"
                "• **పై ముడత / తామర పురుగులు (Thrips):** *స్పైనెటోరమ్ 11.7% SC* @ **0.9 ml/లీ** లేదా *ఫిప్రోనిల్ 5% SC* @ **2.0 ml/లీ**.\n"
                "• **కింది ముడత / నల్లి (Mites):** *డయాఫెంథియురాన్ 50% WP* @ **1.0 గ్రా/లీ** లేదా *అబామెక్టిన్ 1.9% EC* @ **0.5 ml/లీ**.\n"
                "• **కొమ్మ ఎండు తెగులు & కాయ కుళ్లు (Dieback & Fruit Rot):** *అజాక్సిస్ట్రోబిన్ + డైఫెనోకోనజోల్* @ **1.0 ml/లీ** లేదా *కాపర్ ఆక్సిక్లోరైడ్* @ **3.0 గ్రా/లీ**."
            )
        else:
            return (
                "🌶️ **Chilli (Mirchi) Crop Management & Protection:**\n\n"
                "• **Soil:** Well-drained light loamy, sandy loam, or medium black soils with pH **6.5 - 7.5**.\n"
                "• **Thrips & Upward Leaf Curl:** Spray *Spinetoram 11.7% SC* @ **0.9 ml/L** or *Fipronil 5% SC* @ **2.0 ml/L**.\n"
                "• **Mites & Downward Leaf Curl:** Spray *Diafenthiuron 50% WP* @ **1.0 g/L** or *Abamectin 1.9% EC* @ **0.5 ml/L**.\n"
                "• **Die-back & Anthracnose:** Spray *Azoxystrobin + Difenoconazole* @ **1.0 ml/L** or *Copper Oxychloride* @ **3.0 g/L**."
            )

    # 12. Maize / Corn (మొక్కజొన్న / சோளம்)
    if any(k in msg_lower for k in ["maize", "corn", "మొక్కజొన్న", "mokkajonna", "makka", "சோளம்"]):
        if lang == 'te':
            return (
                "🌽 **మొక్కజొన్న సాగు & కత్తెర పురుగు నివారణ:**\n\n"
                "• **నేల:** సారవంతమైన ఎర్ర నేలలు, ఒండ్రు నేలలు (pH 6.0 - 7.5).\n"
                "• **కత్తెర పురుగు (Fall Armyworm):** పంట ప్రారంభ దశలోనే ఆకుల సుడులలో *క్లోరాంట్రానిలిప్రోల్ 18.5% SC* @ **0.4 ml/లీ** లేదా *ఎమామెక్టిన్ బెంజోయేట్ 5% SG* @ **0.5 గ్రా/లీ** ఉదయాన్నే పిచికారీ చేయాలి.\n"
                "• **ఎరువుల మోతాదు:** ఎకరానికి 80 kg యూరియా, 40 kg DAP, 30 kg పొటాష్."
            )
        else:
            return (
                "🌽 **Maize (Corn) Agronomy Guide:**\n\n"
                "• **Soil:** Deep, fertile, well-drained loam or sandy loam with neutral pH **6.0 - 7.5**.\n"
                "• **Fall Armyworm (Spodoptera frugiperda):** Spray *Chlorantraniliprole 18.5% SC* @ **0.4 ml/L** or *Emamectin Benzoate 5% SG* @ **0.5 g/L** directly into leaf whorls in early mornings.\n"
                "• **Fertilizer:** NPK 120-60-50 kg/ha with Zinc Sulfate @ 25 kg/ha basal."
            )

    # 13. Groundnut & Pulses (వేరుశనగ / நிலக்கடலை)
    if any(k in msg_lower for k in ["groundnut", "peanut", "వేరుశనగ", "verusanaga", "moong", "urad", "minumu", "pesara", "dal", "நிலக்கடலை"]):
        if lang == 'te':
            return (
                "🥜 **వేరుశనగ & పప్పుధాన్యాల సాగు సూచనలు:**\n\n"
                "• **అనుకూలమైన నేలలు:** ఇసుకతో కూడిన తేలికపాటి ఎర్ర నేలలు (Sandy Loam), pH 6.0 - 7.0.\n"
                "• **విత్తన శుద్ధి:** కిలో విత్తనానికి **3 గ్రాముల మాంకోజెబ్** లేదా **ట్రైకోడెర్మా విరిడే 10 గ్రాములు** మరియు రైజోబియం కల్చర్ కలపాలి.\n"
                "• **జిప్సం వాడకం:** వేరుశనగలో కాయ బాగా ఊరడానికి (ఊడలు దిగే దశలో 40-45 రోజులకు) ఎకరానికి **200 kg జిప్సం** వేయాలి.\n"
                "• **తిక్కా ఆకుమచ్చ తెగులు:** *కార్బండజిమ్ + మాంకోజెబ్ (సాఫ్)* @ **2.0 గ్రా/లీ** పిచికారీ చేయాలి."
            )
        else:
            return (
                "🥜 **Groundnut (Peanut) & Legume Agronomy:**\n\n"
                "• **Soil Suitability:** Light sandy loams with good drainage, pH **6.0 - 7.0**.\n"
                "• **Seed Treatment:** Treat seeds with *Trichoderma viride* @ 10 g/kg seed + *Rhizobium* culture for root nodulation.\n"
                "• **Gypsum Application:** Apply **200 kg/acre Gypsum** at pegging stage (40-45 DAS) for calcium-rich shell hardening and pod filling.\n"
                "• **Tikka Leaf Spot:** Spray *Carbendazim + Mancozeb (Saaf)* @ **2.0 g/L**."
            )

    # 14. Fertilizers / NPK / Soil Nutrition (ఎరువులు / உரம் / खाद)
    if any(k in msg_lower for k in ["fertilizer", "fertiliser", "npk", "urea", "dap", "potash", "ఎరువులు", "eruvulu", "khad", "khaad", "యూరియా", "రసాయన ఎరువులు", "உரம்", "உரங்கள்"]):
        if lang == 'te':
            return (
                "🌱 **సమగ్ర పోషక యాజమాన్యం & ఎరువుల సూచనలు (NPK):**\n\n"
                "1. **నత్రజని (Nitrogen / Urea):** ఆకుల పెరుగుదలకు, పచ్చదనానికి ఉపయోగపడుతుంది. ఎల్లప్పుడూ 2-3 దఫాలుగా సమతుల్యంగా వేయాలి.\n"
                "2. **భాస్వరం (Phosphorus / DAP / SSP):** వేర్లు బలంగా నాటుకోవడానికి, పూత రావడానికి సహాయపడుతుంది. ఆఖరి దుక్కిలోనే వేయాలి.\n"
                "3. **పొటాష్ (Potassium / MOP):** రోగ నిరోధక శక్తికి, గింజ/కాయ బరువు, నాణ్యత మరియు నిగారింపునకు అవసరం.\n"
                "4. **సేంద్రీయ పోషకాలు:** ఎకరానికి 5-10 టన్నుల పశువుల ఎరువు, 2 టన్నుల వర్మీకంపోస్ట్ మరియు జీవామృతం వాడటం వల్ల నేల సారం శాశ్వతంగా పెరుగుతుంది.\n\n"
                "💡 *నేల పరీక్ష (Soil Test) ఆధారంగా ఎరువులు వేస్తే ఖర్చు 30% తగ్గుతుంది, దిగుబడి పెరుగుతుంది.*"
            )
        else:
            return (
                "🌱 **Balanced N-P-K & Integrated Nutrient Management:**\n\n"
                "1. **Nitrogen (Urea 46% N):** Drives vegetative shoot expansion and chlorophyll synthesis. Apply in 2-3 split top-dressings.\n"
                "2. **Phosphorus (DAP / SSP):** Stimulates root architecture and floral initiation. Apply 100% as basal during land preparation.\n"
                "3. **Potassium (Muriate of Potash - MOP 60% K2O):** Regulates stomatal conductance, strengthens stem resistance, and enhances grain density.\n"
                "4. **Secondary & Micronutrients:** Apply Zinc Sulfate (25 kg/ha) and Boron (5 kg/ha) to correct hidden hunger.\n"
                "5. **Organic Foundation:** Incorporate 5-10 tons/acre well-rotted FYM or Vermicompost before sowing."
            )

    # 15. Irrigation / Water Questions (సాగునీరు / பாசனம்)
    if any(k in msg_lower for k in ["irrigation", "water", "drip", "sprinkler", "సాగునీరు", "నీటి పారుదల", "నీరు", "neeru", "sinchai", "பாசனம்"]):
        if lang == 'te':
            return (
                "💧 **రైతు భూమికి సాగునీటి నిర్వహణ సూచనలు:**\n\n"
                "1. **డ్రిప్ ఇరిగేషన్ (బిందు సేద్యం):** నేల రకాన్ని బట్టి ప్రతి **1 నుండి 2 రోజులకు** ఒకసారి 2-3 గంటల పాటు నీరు అందించాలి (నీటి పొదుపు 40-50%).\n"
                "2. **కాల్వ / బోరు నీరు (Flood Irrigation):** ప్రతి **5 నుండి 7 రోజులకు** ఒక తడి ఇవ్వాలి.\n"
                "3. **కీలక దశలు:** పూత దశ (Flowering), కాయ లేదా గింజ పాలు పోసుకునే దశలో (Grain Filling) నేలలో ఎట్టి పరిస్థితుల్లో తేమ తగ్గకూడదు.\n"
                "4. **వేసవి జాగ్రత్తలు:** బాష్పీభవనాన్ని అరికట్టడానికి సేంద్రీయ వ్యర్థాలు లేదా ప్లాస్టిక్ మల్చింగ్ వాడండి."
            )
        else:
            return (
                "💧 **Farm Land Irrigation & Water Management Principles:**\n\n"
                "1. **Drip Irrigation:** Run cycles every **1 to 2 days** for 2-3 hours depending on canopy evapotranspiration (saves 40-50% water with 90% application efficiency).\n"
                "2. **Flood / Surface Systems:** Water every **5 to 7 days** ensuring uniform furrow grading to prevent rootzone hypoxia.\n"
                "3. **Critical Growth Stages:** Never stress moisture during flowering, fruit set, and grain filling stages.\n"
                "4. **Soil Moisture Check:** Sandy soils require frequent light waterings, while clay soils need deeper, less frequent irrigations."
            )

    # 16. Mandi Market / Price Questions
    if any(k in msg_lower for k in ["market", "mandi", "price", "msp", "ధర", "మార్కెట్", "dhara", "bhaav", "rate", "விலை", "சந்தை"]):
        try:
            ma = get_market_analyzer()
            alerts = ma.get_high_price_alerts()
            top_msg = ", ".join([f"{a['commodity']} (₹{int(a['price'])}/Qtl)" for a in alerts[:3]])
        except Exception:
            top_msg = "Cotton, Chilli, Tomato, Sugarcane"

        if lang == 'te':
            return (
                f"💰 **తాజా మండీ మార్కెట్ విశ్లేషణ & మద్దతు ధరలు (MSP):**\n\n"
                f"• ప్రస్తుతం మార్కెట్లో ప్రభుత్వ మద్దతు ధర (MSP) కంటే అధిక ధర పలుకుతున్న పంటలు: **{top_msg}**.\n"
                f"• మండీలలో గరిష్ట ధర పొందడానికి పంటను నాణ్యత ఆధారంగా గ్రేడింగ్ చేసి, తేమ శాతాన్ని 12% లోపు ఉండేలా చూసుకోండి.\n"
                f"• పూర్తి వివరాలు మరియు జిల్లాల వారీ ధరల కొరకు డ్యాష్‌బోర్డ్‌లోని **Mandi Market Dashboard** ను చూడండి."
            )
        else:
            return (
                f"💰 **Live Mandi Market Intelligence:**\n\n"
                f"• **High Value Commodities Trading Above MSP:** **{top_msg}**.\n"
                f"• **Selling Recommendation:** Ensure moisture standardisation (<12% for grains, <8% for pulses) before transporting to Mandi to avoid grade deductions.\n"
                f"• Explore commodity-wise trends and arrivals via the **Mandi Market Dashboard**."
            )

    # 17. Weather & Climate Questions
    if any(k in msg_lower for k in ["weather", "climate", "rain", "temperature", "వాతావరణం", "వర్షం", "varsham", "mausam", "வானிலை"]):
        try:
            wa = get_weather_analyzer()
            advisory = wa.get_agro_advisory(latest_n_days=7)
            spray_status = advisory.get("spray_suitability", "Normal")
            fungal_risk = advisory.get("fungal_disease_risk", "Moderate")
        except Exception:
            spray_status = "Suitable for morning spraying"
            fungal_risk = "Moderate"

        if lang == 'te':
            return (
                f"🌦️ **వ్యవసాయ వాతావరణ సలహా:**\n\n"
                f"• **మందుల పిచికారీ అనుకూలత:** **{spray_status}**\n"
                f"• **శిలీంద్ర తెగుళ్ల ముప్పు:** **{fungal_risk}**\n"
                f"• **రైతులకు సూచన:** గాలులు తీవ్రంగా ఉన్నప్పుడు లేదా వర్ష సూచన ఉన్నప్పుడు పురుగు మందులు పిచికారీ చేయవద్దు. ఎల్లప్పుడూ ఉదయం 7 నుండి 10 గంటల మధ్య లేదా సాయంత్రం వేళల్లో పిచికారీ చేయండి."
            )
        else:
            return (
                f"🌦️ **Agro-Weather Advisory:**\n\n"
                f"• **Chemical Spray Window:** **{spray_status}**\n"
                f"• **Fungal Pathology Risk:** **{fungal_risk}**\n"
                f"• **Actionable Advice:** Avoid spraying during high wind velocity or imminent rain forecast. Maintain proper field drainage after rainfall events to protect root health."
            )

    # 18. Greetings, Help, or General Assistant Questions
    if any(k in msg_lower for k in ["hi", "hello", "hey", "namaste", "నమస్తే", "హలో", "help", "who are you", "correct work", "ela unnav", "வணக்கம்", "नमस्ते"]):
        if lang == 'te':
            return (
                "🌾 **నమస్తే! నేను మీ AgriSmart AI వ్యవసాయ నిపుణుడిని (Agronomist AI).**\n\n"
                "నేను సంపూర్ణంగా సిద్ధంగా ఉన్నాను! మీ పొలానికి సంబంధించిన ఎలాంటి ప్రశ్నలనైనా నన్ను అడగవచ్చు:\n\n"
                "• 🌾 **పంటలు & సాగు పద్ధతులు** (వరి, పత్తి, టమోటా, మిరప, పుచ్చకాయ, మొక్కజొన్న, వేరుశనగ, మొదలైనవి)\n"
                "• 🧪 **ఎరువుల మోతాదు (NPK, యూరియా, DAP, జింక్, సేంద్రీయ ఎరువులు)**\n"
                "• 🦠 **తెగుళ్లు & పురుగు మందుల పిచికారీ షెడ్యూల్**\n"
                "• 🏡 **మీ నమోదైన పొలాలు & నేల పరీక్ష సిఫార్సుల విశ్లేషణ**\n"
                "• 💰 **మండీ మార్కెట్ ధరలు & కనీస మద్దతు ధర (MSP)**\n\n"
                "💡 *మీరు ఏ పంట లేదా సమస్య గురించి తెలుసుకోవాలనుకుంటున్నారో క్రింద టైప్ చేయండి!*"
            )
        elif lang == 'hi':
            return (
                "🌾 **नमस्ते! मैं आपका AgriSmart AI कृषि विशेषज्ञ हूँ।**\n\n"
                "मैं आपकी सहायता के लिए तैयार हूँ। आप मुझसे पूछ सकते हैं:\n\n"
                "• 🌾 **फसल प्रबंधन और उन्नत किस्में** (धान, कपास, टमाटर, मिर्च, तरबूज, मक्का)\n"
                "• 🧪 **खाद और उर्वरक मात्रा (NPK, यूरिया, डीएपी)**\n"
                "• 🦠 **कीट एवं रोग नियंत्रण और स्प्रे शेड्यूल**\n"
                "• 💰 **मंडी भाव एवं एमएसपी (MSP) रुझान**\n\n"
                "💡 *अपनी फसल या खेत से संबंधित सवाल नीचे लिखें!*"
            )
        elif lang == 'ta':
            return (
                "🌾 **வணக்கம்! நான் உங்கள் AgriSmart AI விவசாய ஆலோசகர்.**\n\n"
                "நான் உங்களுக்கு உதவ தயாராக உள்ளேன். நீங்கள் கேட்கலாம்:\n\n"
                "• 🌾 **பயிர்கள் மற்றும் சாகுபடி நுட்பங்கள்** (நெல், பருத்தி, தக்காளி, மிளகாய், தர்பூசணி, கரும்பு)\n"
                "• 🧪 **உர மேலாண்மை (NPK, யூரியா, டிஏபி, இயற்கை உரங்கள்)**\n"
                "• 🦠 **பூச்சி மற்றும் நோய் கட்டுப்பாடு (தெளிப்பு மருந்துகள்)**\n"
                "• 💰 **மண்டி சந்தை விலைகள் மற்றும் விளைச்சல் ஆலோசனை**\n\n"
                "💡 *உங்கள் விவசாயக் கேள்விகளை கீழே பதிவிடுங்கள்!*"
            )
        else:
            return (
                "🌾 **Namaste! I am your AgriSmart AI Agronomist & Farm Advisor.**\n\n"
                "I am online and ready to assist you with actionable agricultural intelligence:\n\n"
                "• 🌾 **Crop Science & Soil Care:** Optimal soil types, sowing, pH balancing, and climate suitability.\n"
                "• 🧪 **Fertilizer & Nutrition Plans:** Scientifically calculated N-P-K dosages, micronutrients, and organic manures.\n"
                "• 🦠 **Pest & Disease Management:** IPM guidelines, chemical spray dosages (ml/L), and biological controls.\n"
                "• 🏡 **Personalized Farm Analytics:** Contextual advisory tailored to your registered land parcels.\n"
                "• 💰 **Market & Weather Intelligence:** Mandi price trends, MSP benchmarks, and spray timing advisories.\n\n"
                "💡 *Feel free to type your question above or click one of the suggestion chips!*"
            )

    # 19. General Valid Agricultural Query Response
    if lang == 'te':
        return (
            f"🌾 **AgriSmart AI వ్యవసాయ నిపుణుడి సమాధానం:**\n\n"
            f"మీరు అడిగిన వ్యవసాయ అంశం: *\"{user_message}\"*\n\n"
            f"1. **నేల & పోషకాల నిర్వహణ:** పంటకు అవసరమైన నత్రజని (N), భాస్వరం (P), పొటాష్ (K) లను నేల పరీక్ష ఆధారంగా సమతుల్యంగా వేయండి. ఎకరానికి 5-10 టన్నుల పశువుల ఎరువు నేల సారాన్ని పెంచుతుంది.\n"
            f"2. **తెగుళ్ల నివారణ (IPM):** పురుగులు లేదా తెగుళ్లు కనిపించినప్పుడు ముందుగా జీవ నియంత్రణ లేదా వేప నూనె వాడండి; తీవ్రత ఉంటేనే సరైన రసాయన మందును సిఫార్సు చేసిన మోతాదులోనే పిచికారీ చేయండి.\n"
            f"3. **నీటి యాజమాన్యం:** పూత మరియు కాయ దశలలో తేమ తగ్గకుండా డ్రిప్ లేదా కాల్వ ద్వారా సక్రమంగా నీరు అందించండి.\n\n"
            f"💡 *మీరు ఏ పంట గురించి అడుగుతున్నారో (ఉదా: టమోటా, వరి, పత్తి, మిరప, పుచ్చకాయ) వివరంగా అడిగితే మరింత ఖచ్చితమైన సమాచారం ఇస్తాను.*"
        )
    elif lang == 'hi':
        return (
            f"🌾 **AgriSmart AI कृषि विशेषज्ञ सलाह:**\n\n"
            f"आपके कृषि प्रश्न: *\"{user_message}\"* के संदर्भ में:\n\n"
            f"1. **संतुलित पोषण (NPK):** मिट्टी परीक्षण के आधार पर यूरिया, डीएपी और पोटाश का उचित प्रयोग करें।\n"
            f"2. **कीट एवं रोग प्रबंधन:** कीटनाशकों का छिड़काव सुबह या शाम के समय अनुशंसित मात्रा में ही करें।\n"
            f"3. **सिंचाई प्रबंधन:** फूल आने और दाना भरने की अवस्था में नमी बनाए रखें।\n\n"
            f"💡 *अपनी विशिष्ट फसल (जैसे टमाटर, धान, कपास, तरबूज) का नाम लिखकर अधिक जानकारी पाएं।*"
        )
    elif lang == 'ta':
        return (
            f"🌾 **AgriSmart AI விவசாய ஆலோசனை:**\n\n"
            f"உங்கள் விவசாயக் கேள்வி: *\"{user_message}\"* பற்றிய விவரங்கள்:\n\n"
            f"1. **மண் மற்றும் ஊட்டச்சத்து மேலாண்மை:** மண் பரிசோதனை அடிப்படையில் N-P-K சமச்சீர் உரங்களை இடவும். தொழு உரம் மண் வளத்தை மேம்படுத்தும்.\n"
            f"2. **பயிர் பாதுகாப்பு (IPM):** பூச்சி மற்றும் நோய் தாக்குதலை ஆரம்ப நிலையிலேயே கட்டுப்படுத்த இயற்கை அல்லது பரிந்துரைக்கப்பட்ட தெளிப்பு மருந்துகளைப் பயன்படுத்தவும்.\n"
            f"3. **பாசன மேலாண்மை:** பூக்கும் மற்றும் காய் பிடிக்கும் பருவங்களில் சீரான நீர் பாசனம் அளிக்கவும்.\n\n"
            f"💡 *உங்கள் குறிப்பிட்ட பயிர் பற்றிய கேள்விகளைத் தொடர்ந்து கேட்கலாம்.*"
        )
    else:
        return (
            f"🌾 **AgriSmart Agronomist AI Guidance:**\n\n"
            f"Regarding your agricultural inquiry on *\"{user_message}\"*:\n\n"
            f"1. **Soil & Nutrient Care:** Ensure balanced N-P-K nutrition based on laboratory soil tests. Supplement with organic compost (5-10 tons/acre FYM) to boost microbial biomass.\n"
            f"2. **Targeted Crop Protection:** Practice Integrated Pest Management (IPM). Rotate chemical active ingredients and adhere strictly to recommended concentrations.\n"
            f"3. **Water Efficiency:** Transition to micro-irrigation (Drip/Sprinkler) to optimize water usage and fertigation uptake.\n\n"
            f"💡 *Feel free to ask specifically about any crop (e.g. Tomato, Rice, Cotton, Maize, Chilli, Watermelon), fertilizer dosages, pesticide sprays, or your registered land parcels!*"
        )


def generate_assistant_response(user_id: int, user_message: str) -> Dict[str, Any]:
    """
    Main entry point for AI Agriculture Assistant.
    Validates message, logs user message, queries AI provider with user context,
    logs assistant reply, and returns structured result in the user's active language.
    """
    user_msg_clean = user_message.strip()
    if not user_msg_clean:
        return {
            "success": False,
            "status": "empty_message",
            "message": "Please enter a valid message or question.",
            "is_configured": True,
        }

    # 1. Check AI Provider Configuration
    config = get_ai_config()
    if not config["is_configured"]:
        return {
            "success": False,
            "status": "not_configured",
            "message": UNCONFIGURED_MESSAGE,
            "is_configured": False,
        }

    # 2. Save user message to database
    save_assistant_message(user_id=user_id, role="user", message=user_msg_clean)

    # 3. Domain Validation: If user query is out-of-domain, reply immediately with localized refusal
    if not is_agricultural_query(user_msg_clean):
        refusal_msg = _get_out_of_domain_refusal(user_msg_clean)
        save_assistant_message(user_id=user_id, role="assistant", message=refusal_msg)
        return {
            "success": True,
            "status": "success",
            "message": refusal_msg,
            "is_configured": True,
        }

    # 4. Retrieve recent conversation history (last 10 messages)
    history = get_user_assistant_messages(user_id=user_id, limit=10)

    # 5. Build user context & system prompt
    user_context = build_user_agriculture_context(user_id)
    system_prompt = format_system_prompt(user_context)

    # 6. Invoke Built-in Local Engine if provider is builtin or key is demo/builtin
    api_key = config.get("api_key", "")
    if config["provider"] == "builtin" or api_key in ("builtin", "builtin_agri_intelligence", "demo", "local"):
        ai_reply = _generate_local_agronomist_response(user_id=user_id, user_message=user_msg_clean)
        save_assistant_message(user_id=user_id, role="assistant", message=ai_reply)
        return {
            "success": True,
            "status": "success",
            "message": ai_reply,
            "is_configured": True,
        }

    # 7. Invoke Cloud LLM API with graceful fallback to Built-in Agronomist
    try:
        if config["provider"] == "gemini":
            ai_reply = _call_gemini_api(
                api_key=config["api_key"],
                model=config["model"],
                system_prompt=system_prompt,
                messages=history,
            )
        elif config["provider"] == "openai":
            ai_reply = _call_openai_api(
                api_key=config["api_key"],
                model=config["model"],
                system_prompt=system_prompt,
                messages=history,
            )
        else:
            ai_reply = _call_gemini_api(
                api_key=config["api_key"],
                model=config["model"],
                system_prompt=system_prompt,
                messages=history,
            )

        ai_reply = (ai_reply or "").strip()
        if not ai_reply:
            ai_reply = _generate_local_agronomist_response(user_id=user_id, user_message=user_msg_clean)

        # Save assistant response to database
        save_assistant_message(user_id=user_id, role="assistant", message=ai_reply)

        return {
            "success": True,
            "status": "success",
            "message": ai_reply,
            "is_configured": True,
        }

    except Exception:
        # Seamless fallback to Built-in Agronomist Engine on API/network errors
        ai_reply = _generate_local_agronomist_response(user_id=user_id, user_message=user_msg_clean)
        save_assistant_message(user_id=user_id, role="assistant", message=ai_reply)
        return {
            "success": True,
            "status": "success",
            "message": ai_reply,
            "is_configured": True,
        }
