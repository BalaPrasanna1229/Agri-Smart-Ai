/**
 * Agri Smart AI - Global Frontend & Multi-Language Translation Engine
 * Supports: English (en), Telugu (te), Hindi (hi)
 * 100% Pure Separation: English only in English mode, Telugu only in Telugu mode.
 */

const UI_TRANSLATIONS = {
    en: {
        menu_core: "Core Workspace",
        menu_dashboard: "Dashboard",
        menu_farms: "My Farms",
        menu_notif: "Price Alerts",
        menu_history: "Activity History",
        menu_modules: "Active AI Modules",
        menu_crop: "Smart Farm Advisory (360° AI)",
        menu_yield: "Yield Prediction",
        menu_disease: "Disease Detection",
        menu_weather: "Weather Analytics",
        menu_market: "Market Dashboard",
        menu_assistant: "AI Assistant",
        user_role: "Farmer / Agronomist",
        btn_new_pred: "New Advisory",
        btn_add_farm: "Add Farm",
        btn_print: "Print Advisory",
        btn_export: "Export CSV",
        btn_mark_read: "Mark All Read",
        notif_header: "Price Alerts & Advisories",
        notif_title: "Farmer Notification Center",
        notif_subtitle: "Stay updated with profitable mandi selling windows and crop health precautions",
        notif_high_price_title: "High Market Price Alerts",
        notif_history_title: "In-App Notifications History",
        mark_all_read: "Mark All as Read",
        view_market: "View Live Mandi",
        view_details: "View Details →",
        market_details: "Market Details →",
        mark_read_single: "✓ Mark Read",
        pillar_crop: "Crop Recommendation",
        pillar_yield: "Harvest Yield Forecast",
        pillar_disease: "Disease Precautions",
        pillar_market: "Mandi Market Economics",
        high_price_banner_title: "HIGH MARKET PRICE ALERT",
        high_price_opp: "High Mandi Price Opportunities",
        open_notif_hub: "Open Full Notification Hub →",
        no_notifications: "No recent notifications.",
        top_match: "Top Match",
        optimal_crop_title: "1. Optimal Recommended Crop",
        model_confidence: "Model Confidence",
        mandi_rate: "Mandi Rate",
        est_yield: "Est. Yield",
        registered_farm: "Registered Farm",
        yield_per_acre: "Yield Per Acre",
        farm_area: "Farm Area",
        projected_gross_rev: "Projected Gross Farm Revenue",
        trading_tip: "Trading Tip",
        symptoms_label: "Disease Symptoms",
        organic_label: "Organic & Bio-Control Remedies",
        chemical_label: "Chemical Controls & Exact Dosage",
        preventive_label: "Preventive Cultural Care & Farm Practices",
        view_spray_below: "View Step-by-Step Spray Dosages Below ↓",
        disease_precautions_title: "Disease Identification & Step-by-Step Precautions",
        tested_params_title: "Tested Soil & Environmental Parameters",
        soil_param: "Parameter",
        soil_value: "Tested Value",
        soil_status: "Agronomic Status",
        test_another: "🌱 Test Another Sample",
        ask_ai: "🤖 Ask AI Agronomist",
        view_history: "📜 View History Logs",
        preset_rice: "🍚 Rice Preset",
        preset_cotton: "🌾 Cotton Preset",
        preset_chana: "🌱 Gram / Chana",
        preset_apple: "🍎 Apple Preset",
        soil_section_1: "1. Soil Chemical Properties",
        soil_section_2: "2. Environmental & Climate Parameters",
        soil_section_3: "3. Farm Parcel & Harvest Parameters",
        btn_submit_advisory: "🚀 Generate 360° Comprehensive Farm Advisory →",
        mandi_bulletin_title: "HISTORICAL MANDI MARKET BULLETIN",
        search_crop_label: "Search Commodity / Crop",
        commodity_category_label: "Commodity Category",
        sort_order_label: "Sort Order",
        est_harvest_rev: "Estimated Harvest Revenue",
        calc_title: "Farmer Mandi Revenue & Selling Advisory Calculator",
        select_harvested_crop: "Select Your Harvested Crop:",
        quantity_label: "Quantity:",
        unit_label: "Unit:",
        all_commodity_groups: "-- All Commodity Groups --",
        highest_val_label: "Average Market Price (Rs./Quintal) • 25 Commodities Tracked",
        top_gainer_label: "Top 3-Day Price Gainer",
        top_arrival_label: "Largest Mandi Arrival Volume",
        best_margin_label: "Best Margin Over Govt MSP",
        live_mandi_highs: "Live Highs",
        all_alerts_btn: "🔔 All Alerts",
        smart_farm_summary: "Smart Farm Activity Summary",
        latest_crop_rec: "Latest Crop Recommendation",
        theme_picker_title: "Select Interface Theme",
        theme_auto_saved: "Auto-saved",
        theme_emerald: "Emerald Nature",
        theme_emerald_sub: "Lush green & daylight freshness",
        theme_midnight: "Midnight Agro (Dark)",
        theme_midnight_sub: "OLED dark & glowing neon accents",
        theme_golden: "Golden Harvest",
        theme_golden_sub: "Warm amber & sunlit wheat tones",
        theme_monsoon: "Monsoon Ocean",
        theme_monsoon_sub: "Cool rain breeze & azure skies",
        theme_sage: "Forest Sage",
        theme_sage_sub: "Organic botanical & earthy moss",
    },
    te: {
        menu_core: "ప్రధాన విభాగాలు",
        menu_dashboard: "డాష్‌బోర్డ్",
        menu_farms: "నా పొలాలు",
        menu_notif: "ధరల అలర్ట్‌లు",
        menu_history: "కార్యకలాపాల చరిత్ర",
        menu_modules: "క్రియాశీల AI విభాగాలు",
        menu_crop: "రైతు సమగ్ర వ్యవసాయ సలహా (360° AI)",
        menu_yield: "దిగుబడి అంచనా",
        menu_disease: "వ్యాధి నిర్ధారణ",
        menu_weather: "వాతావరణ విశ్లేషణ",
        menu_market: "మార్కెట్ ధరలు",
        menu_assistant: "AI సహాయకుడు",
        user_role: "రైతు / వ్యవసాయదారుడు",
        btn_new_pred: "కొత్త సిఫార్సు",
        btn_add_farm: "పొలం చేర్చండి",
        btn_print: "ప్రింట్ చేయండి",
        btn_export: "CSV డౌన్‌లోడ్",
        btn_mark_read: "అన్నీ చదివినట్లు గుర్తించు",
        notif_header: "ధరల అలర్ట్‌లు & సలహాలు",
        notif_title: "రైతు నోటిఫికేషన్ కేంద్రం",
        notif_subtitle: "లాభసాటి మార్కెట్ అమ్మకాల అవకాశాలు మరియు పంట తెగుళ్ల నివారణ సమాచారం",
        notif_high_price_title: "అధిక మార్కెట్ ధరల హెచ్చరికలు",
        notif_history_title: "నోటిఫికేషన్ల చరిత్ర",
        mark_all_read: "అన్నీ చదివినట్లు గుర్తించు",
        view_market: "మార్కెట్ ధరలు చూడండి",
        view_details: "వివరాలు చూడండి →",
        market_details: "మార్కెట్ వివరాలు →",
        mark_read_single: "✓ చదివినట్లు గుర్తించు",
        pillar_crop: "పంట సిఫార్సు",
        pillar_yield: "దిగుబడి అంచనా",
        pillar_disease: "తెగుళ్లు & నివారణ చర్యలు",
        pillar_market: "మార్కెట్ ధరలు & విక్రయ సూచనలు",
        high_price_banner_title: "అధిక మార్కెట్ ధరల హెచ్చరిక",
        high_price_opp: "అధిక మండీ ధరల అవకాశాలు",
        open_notif_hub: "నోటిఫికేషన్ కేంద్రానికి వెళ్లండి →",
        no_notifications: "ఎటువంటి తాజా నోటిఫికేషన్లు లేవు.",
        top_match: "ఉత్తమ సిఫార్సు",
        optimal_crop_title: "1. సిఫార్సు చేయబడిన అనుకూల పంట",
        model_confidence: "మోడల్ ఖచ్చితత్వం",
        mandi_rate: "మండీ ధర",
        est_yield: "అంచనా దిగుబడి",
        registered_farm: "నమోదైన పొలం",
        yield_per_acre: "ఎకరాకు దిగుబడి",
        farm_area: "పొలం విస్తీర్ణం",
        projected_gross_rev: "అంచనా మొత్తం ఆదాయం",
        trading_tip: "విక్రయ సూచన",
        symptoms_label: "తెగులు లక్షణాలు",
        organic_label: "సేంద్రీయ నివారణ చర్యలు",
        chemical_label: "రసాయన నివారణ & ఖచ్చితమైన మోతాదు",
        preventive_label: "ముందస్తు సాగు జాగ్రత్తలు",
        view_spray_below: "వివరణాత్మక మందుల మోతాదు కింద చూడండి ↓",
        disease_precautions_title: "పంట తెగుళ్ల గుర్తింపు & నివారణ చర్యలు",
        tested_params_title: "పరీక్షించిన నేల & వాతావరణ వివరాలు",
        soil_param: "వివరము",
        soil_value: "పరీక్షించిన విలువ",
        soil_status: "వ్యవసాయ స్థితి",
        test_another: "🌱 మరో నమూనాను పరీక్షించండి",
        ask_ai: "🤖 AI వ్యవసాయ నిపుణుడిని అడగండి",
        view_history: "📜 చరిత్రను చూడండి",
        preset_rice: "🍚 వరి ప్రీసెట్",
        preset_cotton: "🌾 పత్తి ప్రీసెట్",
        preset_chana: "🌱 శనగ ప్రీసెట్",
        preset_apple: "🍎 యాపిల్ ప్రీసెట్",
        soil_section_1: "1. నేల పోషకాలు & pH వివరాలు",
        soil_section_2: "2. వాతావరణ పరిస్థితులు",
        soil_section_3: "3. పొలం విస్తీర్ణం & దిగుబడి వివరాలు",
        btn_submit_advisory: "🚀 పూర్తి సమగ్ర వ్యవసాయ నివేదికను రూపొందించండి →",
        mandi_bulletin_title: "మండీ మార్కెట్ ధరల సమాచారం",
        search_crop_label: "పంట పేరు ద్వారా వెతకండి",
        commodity_category_label: "పంట విభాగం",
        sort_order_label: "క్రమబద్ధీకరణ",
        est_harvest_rev: "అంచనా ఆదాయం",
        calc_title: "రైతు ఆదాయం & విక్రయ సలహా కాలిక్యులేటర్",
        select_harvested_crop: "మీ పంటను ఎంచుకోండి:",
        quantity_label: "పరిమాణం:",
        unit_label: "యూనిట్:",
        all_commodity_groups: "-- అన్ని పంట విభాగాలు --",
        highest_val_label: "సగటు మార్కెట్ ధర (రూ./క్వింటాల్) • 25 పంటల సమాచారం",
        top_gainer_label: "గరిష్టంగా ధర పెరిగిన పంట",
        top_arrival_label: "అత్యధిక మండీ రాకల పరిమాణం",
        best_margin_label: "ప్రభుత్వ మద్దతు ధర (MSP) కంటే ఎక్కువ లాభం",
        live_mandi_highs: "అధిక ధరలు",
        all_alerts_btn: "🔔 అన్ని అలర్ట్‌లు",
        smart_farm_summary: "వ్యవసాయ కార్యకలాపాల సారాంశం",
        latest_crop_rec: "తాజా పంట సిఫార్సు",
        theme_picker_title: "ఇంటర్‌ఫేస్ థీమ్‌ను ఎంచుకోండి",
        theme_auto_saved: "ఆటో-సేవ్ అయింది",
        theme_emerald: "పచ్చని పైరు (ఎమరాల్డ్)",
        theme_emerald_sub: "తాజా పచ్చదనం & ప్రకాశవంతమైన వెలుగు",
        theme_midnight: "మిడ్‌నైట్ డార్క్ మోడ్",
        theme_midnight_sub: "కంటికి హాయినిచ్చే డార్క్ మోడ్",
        theme_golden: "బంగారు పంట (గోల్డెన్)",
        theme_golden_sub: "బంగారు రంగు ధాన్యపు కాంతులు",
        theme_monsoon: "వర్షాకాలం (బ్లూ)",
        theme_monsoon_sub: "చల్లని వర్షపు గాలులు & నీలాకాశం",
        theme_sage: "దట్టమైన అడవి (సేజ్)",
        theme_sage_sub: "సహజమైన సేంద్రీయ వన రంగులు",
    },
    hi: {
        menu_core: "मुख्य कार्यक्षेत्र",
        menu_dashboard: "डैशबोर्ड",
        menu_farms: "मेरे खेत",
        menu_notif: "भाव अलर्ट",
        menu_history: "गतिविधि इतिहास",
        menu_modules: "सक्रिय AI मॉड्यूल",
        menu_crop: "किसान समग्र कृषि सलाहकार (360° AI)",
        menu_yield: "उपज अनुमान",
        menu_disease: "रोग निदान",
        menu_weather: "मौसम विश्लेषण",
        menu_market: "मंडी भाव",
        menu_assistant: "AI सहायक",
        user_role: "किसान / कृषि विशेषज्ञ",
        btn_new_pred: "नई सिफारिश",
        btn_add_farm: "खेत जोड़ें",
        btn_print: "प्रिंट करें",
        btn_export: "CSV डाउनलोड",
        btn_mark_read: "सभी पढ़ा हुआ चिह्नित करें",
        notif_header: "मंडी भाव अलर्ट व सलाह",
        notif_title: "किसान सूचना केंद्र",
        notif_subtitle: "लाभकारी मंडी बिक्री अवसर और फसल सुरक्षा सलाह",
        notif_high_price_title: "उच्च मंडी भाव अलर्ट",
        notif_history_title: "सूचना इतिहास",
        mark_all_read: "सभी पढ़ा हुआ चिह्नित करें",
        view_market: "लाइव मंडी भाव देखें",
        view_details: "विवरण देखें →",
        market_details: "मंडी विवरण →",
        mark_read_single: "✓ पढ़ा हुआ चिह्नित करें",
        pillar_crop: "फसल सिफारिश",
        pillar_yield: "उपज अनुमान",
        pillar_disease: "रोग निदान व रोकथाम",
        pillar_market: "मंडी भाव व बिक्री सलाह",
        high_price_banner_title: "उच्च मंडी भाव अलर्ट",
        high_price_opp: "उच्च मंडी भाव के अवसर",
        open_notif_hub: "पूरा सूचना केंद्र खोलें →",
        no_notifications: "कोई नई सूचना नहीं है।",
        top_match: "सर्वश्रेष्ठ मेल",
        optimal_crop_title: "1. अनुशंसित उपयुक्त फसल",
        model_confidence: "मॉडल सटीकता",
        mandi_rate: "मंडी भाव",
        est_yield: "अनुमानित उपज",
        registered_farm: "पंजीकृत खेत",
        yield_per_acre: "प्रति एकड़ उपज",
        farm_area: "खेत का क्षेत्रफल",
        projected_gross_rev: "अनुमानित कुल आमदनी",
        trading_tip: "बिक्री सलाह",
        symptoms_label: "रोग के लक्षण",
        organic_label: "जैविक रोकथाम उपाय",
        chemical_label: "रासायनिक रोकथाम व सटीक मात्रा",
        preventive_label: "अग्रिम सुरक्षा व कृषि प्रबंधन",
        view_spray_below: "विस्तृत छिड़काव मात्रा नीचे देखें ↓",
        disease_precautions_title: "फसल रोग पहचान व रोकथाम के उपाय",
        tested_params_title: "परीक्षण किए गए मिट्टी व जलवायु पैरामीटर",
        soil_param: "पैरामीटर",
        soil_value: "परीक्षण मान",
        soil_status: "कृषि स्थिति",
        test_another: "🌱 दूसरा नमूना जांचें",
        ask_ai: "🤖 AI कृषि विशेषज्ञ से पूछें",
        view_history: "📜 इतिहास देखें",
        preset_rice: "🍚 धान प्रीसेट",
        preset_cotton: "🌾 कपास प्रीसेट",
        preset_chana: "🌱 चना प्रीसेट",
        preset_apple: "🍎 सेब प्रीसेट",
        soil_section_1: "1. मिट्टी के रासायनिक गुण व pH",
        soil_section_2: "2. पर्यावरणीय व जलवायु पैरामीटर",
        soil_section_3: "3. खेत का क्षेत्रफल व उपज विवरण",
        btn_submit_advisory: "🚀 संपूर्ण कृषि सलाह रिपोर्ट तैयार करें →",
        mandi_bulletin_title: "मंडी बाजार भाव बुलेटिन",
        search_crop_label: "फसल का नाम खोजें",
        commodity_category_label: "फसल श्रेणी",
        sort_order_label: "क्रमबद्ध करें",
        est_harvest_rev: "अनुमानित आमदनी",
        calc_title: "किसान आमदनी व बिक्री सलाह कैलकुलेटर",
        select_harvested_crop: "अपनी फसल चुनें:",
        quantity_label: "मात्रा:",
        unit_label: "इकाई:",
        all_commodity_groups: "-- सभी फसल श्रेणियां --",
        highest_val_label: "औसत बाजार भाव (रु./क्विंटल) • 25 फसलों की जानकारी",
        top_gainer_label: "शीर्ष 3-दिवसीय भाव वृद्धि",
        top_arrival_label: "सर्वाधिक मंडी आवक मात्रा",
        best_margin_label: "सरकारी समर्थन मूल्य (MSP) से अधिक लाभ",
        live_mandi_highs: "उच्च भाव",
        all_alerts_btn: "🔔 सभी अलर्ट",
        smart_farm_summary: "कृषि गतिविधि सारांश",
        latest_crop_rec: "नवीनतम फसल सिफारिश",
        theme_picker_title: "इंटरफ़ेस थीम चुनें",
        theme_auto_saved: "स्वचालित सहेजा गया",
        theme_emerald: "एमराल्ड प्रकृति",
        theme_emerald_sub: "ताज़ा हरियाली और दिन का उजाला",
        theme_midnight: "मिडनाइट डार्क",
        theme_midnight_sub: "ओएलईडी डार्क और नियॉन चमक",
        theme_golden: "सुनहरी फसल",
        theme_golden_sub: "सुनहरा रंग और धूप की चमक",
        theme_monsoon: "मानसून ओशन",
        theme_monsoon_sub: "शीतल मानसूनी हवा और नीला आसमान",
        theme_sage: "सघन वन (सेज)",
        theme_sage_sub: "प्राकृतिक वानस्पतिक रंग",
    },
    ta: {
        menu_core: "முதன்மைப் பணியிடம்",
        menu_dashboard: "முகப்புப் பலகை",
        menu_farms: "என் நிலங்கள்",
        menu_notif: "விலை எச்சரிக்கைகள்",
        menu_history: "செயல்பாட்டு வரலாறு",
        menu_modules: "AI தொகுதிகள்",
        menu_crop: "ஒருங்கிணைந்த பயிர் ஆலோசனை (360° AI)",
        menu_yield: "மகசூல் கணிப்பு",
        menu_disease: "நோய் கண்டறிதல்",
        menu_weather: "வானிலை பகுப்பாய்வு",
        menu_market: "சந்தை விலை நிலவரம்",
        menu_assistant: "AI வேளாண் உதவியாளர்",
        user_role: "விவசாயி / வேளாண் நிபுணர்",
        btn_new_pred: "புதிய ஆலோசனை",
        btn_add_farm: "நிலம் சேர்க்க",
        btn_print: "அச்சிடுக",
        btn_export: "CSV பதிவிறக்கம்",
        btn_mark_read: "அனைத்தும் படித்ததாகக் குறிக்கவும்",
        notif_header: "விலை எச்சரிக்கைகள் & ஆலோசனைகள்",
        notif_title: "விவசாயி தகவல் மையம்",
        notif_subtitle: "சந்தை விற்பனை வாய்ப்புகள் மற்றும் பயிர் பாதுகாப்பு எச்சரிக்கைகள்",
        notif_high_price_title: "உயர் சந்தை விலை எச்சரிக்கைகள்",
        notif_history_title: "அறிவிப்பு வரலாறு",
        mark_all_read: "அனைத்தும் படித்ததாகக் குறிக்கவும்",
        view_market: "சந்தை விலைகளைக் காண்க",
        view_details: "விவரங்களைக் காண்க →",
        market_details: "சந்தை விவரங்கள் →",
        mark_read_single: "✓ படித்ததாகக் குறிக்க",
        pillar_crop: "பயிர் பரிந்துரை",
        pillar_yield: "மகசூல் கணிப்பு",
        pillar_disease: "நோய் தடுப்பு முறைகள்",
        pillar_market: "சந்தை பொருளாதாரம்",
        high_price_banner_title: "உயர் சந்தை விலை எச்சரிக்கை",
        high_price_opp: "அதிக லாபகரமான சந்தை வாய்ப்புகள்",
        open_notif_hub: "முழு தகவல் மையத்தைத் திறக்கவும் →",
        no_notifications: "சமீபத்திய அறிவிப்புகள் எதுவும் இல்லை.",
        top_match: "சிறந்த பொருத்தம்",
        optimal_crop_title: "1. பரிந்துரைக்கப்படும் உகந்த பயிர்",
        model_confidence: "AI துல்லியம்",
        mandi_rate: "சந்தை விலை",
        est_yield: "எதிர்பார்க்கப்படும் மகசூல்",
        registered_farm: "பதிவு செய்யப்பட்ட நிலம்",
        yield_per_acre: "ஏக்கருக்கு மகசூல்",
        farm_area: "நிலப் பரப்பளவு",
        projected_gross_rev: "மதிப்பிடப்பட்ட மொத்த வருமானம்",
        trading_tip: "விற்பனை ஆலோசனை",
        symptoms_label: "நோய் அறிகுறிகள்",
        organic_label: "இயற்கை & உயிரியல் கட்டுப்பாடு",
        chemical_label: "இரசாயன மருந்துகள் & துல்லிய அளவு",
        preventive_label: "முன்னெச்சரிக்கை சாகுபடி முறைகள்",
        view_spray_below: "கீழே தெளிப்பு மருந்து அளவுகளைக் காண்க ↓",
        disease_precautions_title: "பயிர் நோய் கண்டறிதல் & தடுப்பு நடவடிக்கைகள்",
        tested_params_title: "பரிசோதிக்கப்பட்ட மண் & வானிலை அளவுகள்",
        soil_param: "அளவுரு",
        soil_value: "பரிசோதனை மதிப்பு",
        soil_status: "வேளாண் நிலை",
        test_another: "🌱 மற்றொரு மாதிரியை சோதிக்க",
        ask_ai: "🤖 AI வேளாண் வல்லுநரிடம் கேளுங்கள்",
        view_history: "📜 வரலாற்றைக் காண்க",
        preset_rice: "🍚 நெல் மாதிரி",
        preset_cotton: "🌾 பருத்தி மாதிரி",
        preset_chana: "🌱 கொண்டைக்கடலை",
        preset_apple: "🍎 ஆப்பிள் மாதிரி",
        soil_section_1: "1. மண் வேதியியல் & pH விவரங்கள்",
        soil_section_2: "2. சுற்றுச்சூழல் & காலநிலை அளவுகள்",
        soil_section_3: "3. நிலம் & மகசூல் அளவுருக்கள்",
        btn_submit_advisory: "🚀 360° முழுமையான வேளாண் அறிக்கையைப் பெறுக →",
        mandi_bulletin_title: "சந்தை விலை அறிக்கை",
        search_crop_label: "பயிர் பெயரைத் தேடவும்",
        commodity_category_label: "பயிர் வகை",
        sort_order_label: "வரிசைப்படுத்து",
        est_harvest_rev: "மதிப்பிடப்பட்ட வருமானம்",
        calc_title: "விவசாயி வருமானக் கணக்கீட்டுப் பலகை",
        select_harvested_crop: "உங்கள் பயிரைத் தேர்ந்தெடுக்கவும்:",
        quantity_label: "அளவு:",
        unit_label: "அலகு:",
        all_commodity_groups: "-- அனைத்து பயிர் வகைகள் --",
        highest_val_label: "சராசரி சந்தை விலை (ரூ./குவிண்டால்) • 25 பயிர்கள்",
        top_gainer_label: "அதிக விலை உயர்ந்த பயிர்",
        top_arrival_label: "அதிக சந்தை வரத்து அளவு",
        best_margin_label: "அரசு ஆதரவு விலையை (MSP) விட கூடுதல் லாபம்",
        live_mandi_highs: "நேரலை உயர் விலைகள்",
        all_alerts_btn: "🔔 அனைத்து எச்சரிக்கைகளும்",
        smart_farm_summary: "பண்ணை செயல்பாட்டுச் சுருக்கம்",
        latest_crop_rec: "சமீபத்திய பயிர் பரிந்துரை",
        theme_picker_title: "வடிவமைப்பைத் தேர்வு செய்க",
        theme_auto_saved: "தானாகச் சேமிக்கப்பட்டது",
        theme_emerald: "பசுமை இயற்கை (எமரால்டு)",
        theme_emerald_sub: "பசுமையான இயற்கை மற்றும் பகல் வெளிச்சம்",
        theme_midnight: "மிட்நைட் டார்க் மோட்",
        theme_midnight_sub: "கண்களுக்கு இதமான டார்க் மோட்",
        theme_golden: "தங்க அறுவடை (கோல்டன்)",
        theme_golden_sub: "சூரிய ஒளி தங்க நிற தானியங்கள்",
        theme_monsoon: "பருவமழை (ப்ளூ)",
        theme_monsoon_sub: "குளிர்ந்த மழை மற்றும் நீல வானம்",
        theme_sage: "காட்டு பசுமை (சேஜ்)",
        theme_sage_sub: "இயற்கை தாவர வண்ணங்கள்",
    }
};

let currentGlobalLang = localStorage.getItem('agri_lang') || 'en';
let currentAppTheme = localStorage.getItem('agri_theme') || 'emerald';

const THEME_META = {
    emerald: { name_en: "Emerald Nature", name_te: "పచ్చని పైరు", name_hi: "एमराल्ड प्रकृति", name_ta: "பசுமை இயற்கை", icon: "🌿", isDark: false },
    midnight: { name_en: "Midnight Dark", name_te: "మిడ్‌నైట్ డార్క్", name_hi: "मिडनाइट डार्क", name_ta: "மிட்நைட் டார்க்", icon: "🌙", isDark: true },
    golden: { name_en: "Golden Harvest", name_te: "బంగారు పంట", name_hi: "सुनहरी फसल", name_ta: "தங்க அறுவடை", icon: "🌾", isDark: false },
    monsoon: { name_en: "Monsoon Ocean", name_te: "వర్షాకాలం", name_hi: "मानसून ओशन", name_ta: "பருவமழை", icon: "🌊", isDark: false },
    sage: { name_en: "Forest Sage", name_te: "దట్టమైన అడవి", name_hi: "सघन वन", name_ta: "காட்டு பசுமை", icon: "🍃", isDark: false }
};

/* =========================================================
   Theme Switcher Engine
   ========================================================= */
function setAppTheme(themeName) {
    if (!THEME_META[themeName]) {
        themeName = 'emerald';
    }
    currentAppTheme = themeName;
    localStorage.setItem('agri_theme', themeName);
    document.documentElement.setAttribute('data-theme', themeName);

    const meta = THEME_META[themeName];
    const localizedName = currentGlobalLang === 'te' ? meta.name_te : (currentGlobalLang === 'hi' ? meta.name_hi : meta.name_en);

    // Update Header Trigger Display
    const headerName = document.getElementById('themePickerCurrentName');
    const headerIcon = document.getElementById('themePickerCurrentIcon');
    if (headerName) headerName.textContent = localizedName;
    if (headerIcon) headerIcon.textContent = meta.icon;

    // Update Guest Header Trigger if present
    const guestName = document.getElementById('guestThemePickerName');
    const guestIcon = document.getElementById('guestThemePickerIcon');
    if (guestName) guestName.textContent = localizedName;
    if (guestIcon) guestIcon.textContent = meta.icon;

    // Update Quick Dark Toggle Button Icon
    const quickDarkIcon = document.getElementById('quickDarkIcon');
    const guestQuickDarkIcon = document.getElementById('guestQuickDarkIcon');
    const darkToggleIcon = meta.isDark ? '☀️' : '🌙';
    if (quickDarkIcon) quickDarkIcon.textContent = darkToggleIcon;
    if (guestQuickDarkIcon) guestQuickDarkIcon.textContent = darkToggleIcon;

    // Update active highlight on theme buttons
    document.querySelectorAll('.theme-option-btn').forEach(btn => {
        if (btn.getAttribute('data-theme-val') === themeName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Close Dropdowns
    const menu = document.getElementById('themeDropdownMenu');
    if (menu) menu.style.display = 'none';
    const guestMenu = document.getElementById('guestThemeDropdownMenu');
    if (guestMenu) guestMenu.style.display = 'none';

    // Dispatch theme event
    document.dispatchEvent(new CustomEvent('agri:themeChanged', { detail: { theme: themeName } }));
}

function toggleThemeDropdown() {
    const menu = document.getElementById('themeDropdownMenu') || document.getElementById('guestThemeDropdownMenu');
    if (!menu) return;
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

function toggleQuickDarkMode() {
    if (currentAppTheme === 'midnight') {
        setAppTheme('emerald');
    } else {
        setAppTheme('midnight');
    }
}

// Close dropdowns on outside click or escape key
document.addEventListener('click', (e) => {
    // Theme Dropdown Outside Click
    const themeWrapper = document.querySelector('.theme-dropdown-wrapper');
    const themeMenu = document.getElementById('themeDropdownMenu');
    const guestThemeMenu = document.getElementById('guestThemeDropdownMenu');
    if (themeWrapper && !themeWrapper.contains(e.target)) {
        if (themeMenu) themeMenu.style.display = 'none';
        if (guestThemeMenu) guestThemeMenu.style.display = 'none';
    }

    // Notification Dropdown Outside Click
    const notifWrapper = document.querySelector('.notif-dropdown-wrapper');
    const notifMenu = document.getElementById('notifDropdownMenu');
    if (notifWrapper && notifMenu && !notifWrapper.contains(e.target)) {
        notifMenu.style.display = 'none';
    }
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const themeMenu = document.getElementById('themeDropdownMenu');
        const guestThemeMenu = document.getElementById('guestThemeDropdownMenu');
        const notifMenu = document.getElementById('notifDropdownMenu');
        if (themeMenu) themeMenu.style.display = 'none';
        if (guestThemeMenu) guestThemeMenu.style.display = 'none';
        if (notifMenu) notifMenu.style.display = 'none';
    }
});

function toggleNotificationDropdown() {
    const menu = document.getElementById('notifDropdownMenu');
    if (!menu) return;
    if (menu.style.display === 'none' || menu.style.display === '') {
        menu.style.display = 'block';
    } else {
        menu.style.display = 'none';
    }
}

/* =========================================================
   Language Switcher Engine
   ========================================================= */
function setGlobalLanguage(lang) {
    if (!['en', 'te', 'hi', 'ta'].includes(lang)) {
        lang = 'en';
    }
    currentGlobalLang = lang;
    localStorage.setItem('agri_lang', lang);
    document.documentElement.lang = lang;

    // 1. Update Header Language Selector Buttons
    ['en', 'te', 'hi', 'ta'].forEach(l => {
        const btn = document.getElementById('globalLang' + l.charAt(0).toUpperCase() + l.slice(1));
        if (btn) {
            if (l === lang) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        }

        // Auth page buttons
        const authBtn = document.getElementById('authLang' + l.charAt(0).toUpperCase() + l.slice(1));
        if (authBtn) {
            if (l === lang) {
                authBtn.classList.add('active');
            } else {
                authBtn.classList.remove('active');
            }
        }

        // Also sync any in-page lang pills (e.g. disease page)
        const pillBtn = document.getElementById('btnLang' + l.charAt(0).toUpperCase() + l.slice(1));
        if (pillBtn) {
            if (l === lang) {
                pillBtn.classList.add('active');
            } else {
                pillBtn.classList.remove('active');
            }
        }
    });

    // 2. Translate all [data-i18n] elements
    const translations = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            el.textContent = translations[key];
        }
    });

    // 3. Translate all .lang-text elements (with data-en, data-te, data-hi, data-ta)
    document.querySelectorAll('.lang-text').forEach(el => {
        const text = el.getAttribute('data-' + lang);
        if (text) {
            el.textContent = text;
        }
    });

    // 4. Translate option elements that have data-en, data-te, data-hi, data-ta
    document.querySelectorAll('option[data-' + lang + ']').forEach(opt => {
        const text = opt.getAttribute('data-' + lang);
        if (text) {
            opt.textContent = text;
        }
    });

    // 5. Translate input placeholders that have data-en-placeholder, data-te-placeholder, data-ta-placeholder
    document.querySelectorAll('[data-' + lang + '-placeholder]').forEach(input => {
        const ph = input.getAttribute('data-' + lang + '-placeholder');
        if (ph) {
            input.placeholder = ph;
        }
    });

    // 6. Refresh Theme Button text
    const meta = THEME_META[currentAppTheme] || THEME_META.emerald;
    const localizedName = lang === 'ta' ? meta.name_ta : (lang === 'te' ? meta.name_te : (lang === 'hi' ? meta.name_hi : meta.name_en));
    const headerName = document.getElementById('themePickerCurrentName');
    if (headerName) headerName.textContent = localizedName;
    const guestName = document.getElementById('guestThemePickerName');
    if (guestName) guestName.textContent = localizedName;

    // 7. Trigger custom event for special modules
    document.dispatchEvent(new CustomEvent('agri:languageChanged', { detail: { lang } }));

    // 8. Page-specific hooks if available
    if (typeof switchGlobalLanguage === 'function' && switchGlobalLanguage !== setGlobalLanguage) {
        try {
            switchGlobalLanguage(lang);
        } catch (e) {
            console.debug('Local sync hook:', e);
        }
    }
}

// Global Alias for pages using switchGlobalLanguage
window.switchGlobalLanguage = setGlobalLanguage;

/* ==========================================================================
   AGRI SMART AI - MULTILINGUAL AUDIO & VOICE SPEAKER ENGINE
   ========================================================================== */
const AgriSpeaker = {
    synth: typeof window !== 'undefined' ? window.speechSynthesis : null,
    currentUtterance: null,
    activeButton: null,
    isSpeaking: false,
    isPaused: false,
    voices: [],
    keepAliveInterval: null,
    
    init() {
        if (!this.synth) return;
        this.loadVoices();
        if (typeof speechSynthesis !== 'undefined' && speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = () => this.loadVoices();
        }
        
        // Delegated click listener for general page speaker buttons (excluding chat-msg-speaker-btn which has dedicated handler)
        document.addEventListener('click', (e) => {
            const btn = e.target.closest('.agri-speaker-btn, .agri-speak-btn');
            if (!btn) return;
            e.preventDefault();
            this.handleButtonClick(btn);
        });
    },

    loadVoices() {
        if (!this.synth) return;
        try {
            this.voices = this.synth.getVoices() || [];
        } catch (e) {
            this.voices = [];
        }
    },

    detectTextLanguage(text) {
        if (!text) return currentGlobalLang || 'en';
        if (/[\u0C00-\u0C7F]/.test(text)) return 'te'; // Telugu
        if (/[\u0B80-\u0BFF]/.test(text)) return 'ta'; // Tamil
        if (/[\u0900-\u097F]/.test(text)) return 'hi'; // Hindi
        return currentGlobalLang || localStorage.getItem('agri_lang') || 'en';
    },

    cleanTextForSpeech(raw) {
        if (!raw) return '';
        let txt = String(raw);
        // Strip HTML tags
        txt = txt.replace(/<[^>]*>/g, ' ');
        // Strip markdown bold, italics, headers, code blocks
        txt = txt.replace(/[\*_~`#]/g, ' ');
        // Convert list bullets and numbering
        txt = txt.replace(/^[\s•\-\*]+/gm, ' ');
        // Strip emojis
        txt = txt.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF])/g, ' ');
        // Natural speech replacements
        txt = txt.replace(/₹/g, ' Rupees ');
        txt = txt.replace(/kg\/ha/gi, ' kilograms per hectare ');
        txt = txt.replace(/t\/acre/gi, ' tons per acre ');
        txt = txt.replace(/ml\/L/gi, ' milliliters per liter ');
        txt = txt.replace(/°C/gi, ' degrees Celsius ');
        txt = txt.replace(/\bNPK\b/g, 'N P K');
        txt = txt.replace(/\bpH\b/g, 'p H');
        txt = txt.replace(/\bMSP\b/g, 'M S P');
        txt = txt.replace(/\bIPM\b/g, 'I P M');
        txt = txt.replace(/\bFYM\b/g, 'F Y M');
        txt = txt.replace(/\bDAP\b/g, 'D A P');
        txt = txt.replace(/\bMOP\b/g, 'M O P');
        // Normalize whitespace
        txt = txt.replace(/\s+/g, ' ').trim();
        return txt;
    },

    getVoiceForLanguage(lang) {
        if (!this.voices || !this.voices.length) this.loadVoices();
        const codeMap = {
            ta: ['ta-IN', 'ta_IN', 'ta', 'Tamil'],
            te: ['te-IN', 'te_IN', 'te', 'Telugu'],
            hi: ['hi-IN', 'hi_IN', 'hi', 'Hindi'],
            en: ['en-IN', 'en-US', 'en-GB', 'en', 'English']
        };
        const targets = codeMap[lang] || codeMap.en;
        for (const t of targets) {
            const found = this.voices.find(v => 
                (v.lang && v.lang.toLowerCase().replace('_', '-').includes(t.toLowerCase())) || 
                (v.name && v.name.toLowerCase().includes(t.toLowerCase()))
            );
            if (found) return found;
        }
        return this.voices[0] || null;
    },

    speak(text, buttonEl = null, lang = null, title = null) {
        if (!this.synth) {
            alert('Voice speech narration is not supported on your browser.');
            return;
        }

        this.stop();

        const cleaned = this.cleanTextForSpeech(text);
        if (!cleaned) return;

        // Auto-detect language if not passed
        const activeLang = lang || this.detectTextLanguage(cleaned);

        // Resume engine in case browser suspended audio context
        if (this.synth.paused) {
            this.synth.resume();
        }

        const utterance = new SpeechSynthesisUtterance(cleaned);
        this.currentUtterance = utterance;

        // Language tag
        const langCode = activeLang === 'ta' ? 'ta-IN' : (activeLang === 'te' ? 'te-IN' : (activeLang === 'hi' ? 'hi-IN' : 'en-IN'));
        utterance.lang = langCode;

        // Assign matched native voice
        const matchedVoice = this.getVoiceForLanguage(activeLang);
        if (matchedVoice) {
            utterance.voice = matchedVoice;
        }

        utterance.rate = activeLang === 'en' ? 0.95 : 0.88;
        utterance.pitch = 1.0;

        // Update button UI
        if (buttonEl) {
            this.activeButton = buttonEl;
            buttonEl.classList.add('is-speaking');
            const icon = buttonEl.querySelector('.speaker-icon');
            if (icon) icon.textContent = '⏹️';
        }

        // Show Audio Bar HUD
        const displayTitle = title || (activeLang === 'ta' ? 'வேளாண் குரல் வாசிப்பு' : (activeLang === 'te' ? 'వ్యవసాయ ఆడియో సలహా' : (activeLang === 'hi' ? 'कृषि ऑडियो परामर्श' : 'Agri Voice Narration')));
        this.showAudioBar(displayTitle, cleaned, activeLang);

        utterance.onstart = () => {
            this.isSpeaking = true;
            this.isPaused = false;
            // Chrome keep-alive heartbeat
            if (this.keepAliveInterval) clearInterval(this.keepAliveInterval);
            this.keepAliveInterval = setInterval(() => {
                if (this.isSpeaking && !this.isPaused && this.synth && this.synth.speaking) {
                    this.synth.pause();
                    this.synth.resume();
                }
            }, 10000);
        };

        utterance.onend = () => {
            this.handlePlaybackEnd();
        };

        utterance.onerror = (e) => {
            console.warn('[AgriSpeaker] TTS playback error/interrupted:', e);
            this.handlePlaybackEnd();
        };

        // Small timeout for browser audio engine stabilization
        setTimeout(() => {
            try {
                this.synth.speak(utterance);
            } catch (err) {
                console.error('[AgriSpeaker] Speech dispatch failed:', err);
                this.handlePlaybackEnd();
            }
        }, 50);
    },

    stop() {
        if (this.keepAliveInterval) {
            clearInterval(this.keepAliveInterval);
            this.keepAliveInterval = null;
        }
        if (!this.synth) return;
        try {
            this.synth.cancel();
        } catch (e) {}
        this.handlePlaybackEnd();
    },

    pause() {
        if (!this.synth || !this.isSpeaking) return;
        if (this.isPaused) {
            this.synth.resume();
            this.isPaused = false;
            const playBtn = document.getElementById('agriAudioPlayPauseBtn');
            if (playBtn) playBtn.textContent = '⏸️';
        } else {
            this.synth.pause();
            this.isPaused = true;
            const playBtn = document.getElementById('agriAudioPlayPauseBtn');
            if (playBtn) playBtn.textContent = '▶️';
        }
    },

    handlePlaybackEnd() {
        if (this.keepAliveInterval) {
            clearInterval(this.keepAliveInterval);
            this.keepAliveInterval = null;
        }
        this.isSpeaking = false;
        this.isPaused = false;
        this.currentUtterance = null;
        if (this.activeButton) {
            this.activeButton.classList.remove('is-speaking');
            const icon = this.activeButton.querySelector('.speaker-icon');
            if (icon) icon.textContent = '🔊';
            this.activeButton = null;
        }
        this.hideAudioBar();
    },

    showAudioBar(title, textPreview, lang) {
        const bar = document.getElementById('agriGlobalAudioBar');
        if (!bar) return;
        const titleEl = document.getElementById('agriAudioTitle');
        const subEl = document.getElementById('agriAudioSub');
        const langChip = document.getElementById('agriAudioLangChip');
        if (titleEl) titleEl.textContent = title;
        if (subEl) subEl.textContent = textPreview;
        if (langChip) langChip.textContent = (lang || 'EN').toUpperCase();
        bar.style.display = 'flex';
    },

    hideAudioBar() {
        const bar = document.getElementById('agriGlobalAudioBar');
        if (bar) bar.style.display = 'none';
    },

    handleButtonClick(btn) {
        if (btn.classList.contains('is-speaking')) {
            this.stop();
            return;
        }

        const activeLang = currentGlobalLang || localStorage.getItem('agri_lang') || 'en';
        let textToSpeak = '';

        // Priority 1: Multi-language data attributes data-speak-ta, te, hi, en
        if (btn.getAttribute(`data-speak-${activeLang}`)) {
            textToSpeak = btn.getAttribute(`data-speak-${activeLang}`);
        } else if (btn.getAttribute('data-speak-text')) {
            textToSpeak = btn.getAttribute('data-speak-text');
        } else if (btn.getAttribute('data-speak-target')) {
            const targetEl = document.querySelector(btn.getAttribute('data-speak-target'));
            if (targetEl) {
                const langEl = targetEl.querySelector('.lang-text');
                if (langEl && langEl.getAttribute(`data-${activeLang}`)) {
                    textToSpeak = langEl.getAttribute(`data-${activeLang}`);
                } else {
                    textToSpeak = targetEl.innerText || targetEl.textContent;
                }
            }
        } else {
            const parentCard = btn.closest('.card, .slide-content, .msg-bubble, .advisory-card, .chat-ai-bubble');
            if (parentCard) {
                textToSpeak = parentCard.innerText;
            }
        }

        const title = btn.getAttribute('data-speak-title') || 'Farm Advisory';
        if (textToSpeak) {
            this.speak(textToSpeak, btn, activeLang, title);
        }
    }
};

window.AgriSpeaker = AgriSpeaker;

// Farm Name Quick Selector helper
function setFarmName(nameEn, nameTe, nameHi, nameTa, targetId = 'farm_name') {
    const input = document.getElementById(targetId) || document.querySelector('input[name="farm_name"]');
    if (!input) return;
    
    let chosen = nameEn;
    if (currentGlobalLang === 'te' && nameTe) chosen = nameTe;
    else if (currentGlobalLang === 'hi' && nameHi) chosen = nameHi;
    else if (currentGlobalLang === 'ta' && nameTa) chosen = nameTa;
    
    input.value = chosen;
    input.focus();
}
window.setFarmName = setFarmName;


// ==========================================
// COMPREHENSIVE INDIAN STATES & DISTRICTS CATALOG
// ==========================================
const INDIA_STATE_DISTRICTS = {
    "Andhra Pradesh": [
        "Alluri Sitharama Raju", "Anakapalli", "Ananthapuramu", "Annamayya", "Bapatla", 
        "Chittoor", "Dr. B.R. Ambedkar Konaseema", "East Godavari", "Eluru", "Guntur", 
        "Kakinada", "Krishna", "Kurnool", "Nandyal", "NTR", "Palnadu", 
        "Parvathipuram Manyam", "Prakasam", "Sri Potti Sriramulu Nellore", "Sri Sathya Sai", 
        "Srikakulam", "Tirupati", "Visakhapatnam", "Vizianagaram", "West Godavari", "YSR Kadapa"
    ],
    "Telangana": [
        "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial", 
        "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy", "Karimnagar", 
        "Khammam", "Kumuram Bheem Asifabad", "Mahabubabad", "Mahabubnagar", "Mancherial", 
        "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda", 
        "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", 
        "Ranga Reddy", "Sangareddy", "Siddipet", "Suryapet", "Vikarabad", 
        "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri"
    ],
    "Tamil Nadu": [
        "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", 
        "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram", 
        "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai", 
        "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai", 
        "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", 
        "Thanjavur", "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", 
        "Tirupathur", "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", 
        "Vellore", "Viluppuram", "Virudhunagar"
    ],
    "Karnataka": [
        "Bagalkot", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban", 
        "Bidar", "Chamarajanagar", "Chikkaballapur", "Chikkamagaluru", "Chitradurga", 
        "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag", "Hassan", 
        "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal", 
        "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga", 
        "Tumakuru", "Udupi", "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir"
    ],
    "Maharashtra": [
        "Ahmednagar", "Akola", "Amravati", "Chhatrapati Sambhajinagar", "Beed", 
        "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", 
        "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", 
        "Latur", "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded", 
        "Nandurbar", "Nashik", "Dharashiv", "Palghar", "Parbhani", 
        "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara", 
        "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal"
    ],
    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", 
        "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar", 
        "Kapurthala", "Ludhiana", "Malerkotla", "Mansa", "Moga", 
        "Pathankot", "Patiala", "Rupnagar", "Sahibzada Ajit Singh Nagar", "Sangrur", 
        "Shahid Bhagat Singh Nagar", "Sri Muktsar Sahib", "Tarn Taran"
    ],
    "Uttar Pradesh": [
        "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", 
        "Auraiya", "Ayodhya", "Azamgarh", "Baghpat", "Bahraich", 
        "Ballia", "Balrampur", "Banda", "Barabanki", "Bareilly", 
        "Basti", "Bhadohi", "Bijnor", "Budaun", "Bulandshahr", 
        "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah", 
        "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar", "Ghaziabad", 
        "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur", 
        "Hardoi", "Hathras", "Jalaun", "Jaunpur", "Jhansi", 
        "Kannauj", "Kanpur Dehat", "Kanpur Nagar", "Kasganj", "Kaushambi", 
        "Kheri", "Kushinagar", "Lalitpur", "Lucknow", "Maharajganj", 
        "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut", 
        "Mirzapur", "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh", 
        "Prayagraj", "Raebareli", "Rampur", "Saharanpur", "Sambhal", 
        "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shravasti", "Siddharthnagar", 
        "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi"
    ],
    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", 
        "Bharuch", "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", 
        "Dang", "Devbhoomi Dwarka", "Gandhinagar", "Gir Somnath", "Jamnagar", 
        "Junagadh", "Kheda", "Kutch", "Mahisagar", "Mehsana", 
        "Morbi", "Narmada", "Navsari", "Panchmahal", "Patan", 
        "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar", 
        "Tapi", "Vadodara", "Valsad"
    ],
    "Madhya Pradesh": [
        "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", 
        "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", 
        "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", 
        "Dhar", "Dindori", "Guna", "Gwalior", "Harda", 
        "Indore", "Jabalpur", "Jhabua", "Katni", "Khandwa", 
        "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur", 
        "Neemuch", "Niwari", "Narmadapuram", "Panna", "Raisen", 
        "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", 
        "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", 
        "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", 
        "Umaria", "Vidisha"
    ],
    "Rajasthan": [
        "Ajmer", "Alwar", "Anupgarh", "Balotra", "Banswara", 
        "Baran", "Barmer", "Beawar", "Bharatpur", "Bhilwara", 
        "Bikaner", "Bundi", "Chittorgarh", "Churu", "Dausa", 
        "Deeg", "Dholpur", "Didwana-Kuchaman", "Dudu", "Dungarpur", 
        "Ganganagar", "Gangapur City", "Hanumangarh", "Jaipur", "Jaipur Rural", 
        "Jaisalmer", "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur", 
        "Jodhpur Rural", "Karauli", "Kekri", "Khairthal-Tijara", "Kota", 
        "Kotputli-Behror", "Nagaur", "Neem Ka Thana", "Pali", "Phalodi", 
        "Pratapgarh", "Rajsamand", "Salumber", "Sanchore", "Sawai Madhopur", 
        "Shahpura", "Sikar", "Sirohi", "Tonk", "Udaipur"
    ],
    "Kerala": [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", 
        "Kollam", "Kottayam", "Kozhikode", "Malappuram", "Palakkad", 
        "Pathanamthitta", "Thiruvananthapuram", "Thrissur", "Wayanad"
    ],
    "West Bengal": [
        "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur", 
        "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram", 
        "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia", 
        "North 24 Parganas", "Paschim Bardhaman", "Paschim Medinipur", "Purba Bardhaman", "Purba Medinipur", 
        "Purulia", "South 24 Parganas", "Uttar Dinajpur"
    ],
    "Odisha": [
        "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", 
        "Boudh", "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", 
        "Ganjam", "Jagatsinghpur", "Jajpur", "Jharsuguda", "Kalahandi", 
        "Kandhamal", "Kendrapara", "Kendujhar", "Khordha", "Koraput", 
        "Malkangiri", "Mayurbhanj", "Nabarangpur", "Nayagarh", "Nuapada", 
        "Puri", "Rayagada", "Sambalpur", "Subarnapur", "Sundergarh"
    ],
    "Bihar": [
        "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", 
        "Bhagalpur", "Bhojpur", "Buxar", "Darbhanga", "East Champaran", 
        "Gaya", "Gopalganj", "Jamui", "Jehanabad", "Kaimur", 
        "Katihar", "Khagaria", "Kishanganj", "Lakhisarai", "Madhepura", 
        "Madhubani", "Munger", "Muzaffarpur", "Nalanda", "Nawada", 
        "Patna", "Purnia", "Rohtas", "Saharsa", "Samastipur", 
        "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan", 
        "Supaul", "Vaishali", "West Champaran"
    ],
    "Haryana": [
        "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", 
        "Gurugram", "Hisar", "Jhajjar", "Jind", "Kaithal", 
        "Karnal", "Kurukshetra", "Mahendragarh", "Nuh", "Palwal", 
        "Panchkula", "Panipat", "Rewari", "Rohtak", "Sirsa", 
        "Sonipat", "Yamunanagar"
    ],
    "Assam": [
        "Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", 
        "Charaideo", "Chirang", "Darrang", "Dhemaji", "Dhubri", 
        "Dibrugarh", "Dima Hasao", "Goalpara", "Golaghat", "Hailakandi", 
        "Hojai", "Jorhat", "Kamrup", "Kamrup Metropolitan", "Karbi Anglong", 
        "Karimganj", "Kokrajhar", "Lakhimpur", "Majuli", "Morigaon", 
        "Nagaon", "Nalbari", "Sivasagar", "Sonitpur", "South Salmara-Mankachar", 
        "Tinsukia", "Udalguri", "West Karbi Anglong"
    ],
    "Chhattisgarh": [
        "Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", 
        "Bijapur", "Bilaspur", "Dantewada", "Dhamtari", "Durg", 
        "Gariaband", "Gaurela-Pendra-Marwahi", "Janjgir-Champa", "Jashpur", "Kabirdham", 
        "Kanker", "Khairagarh-Chhuikhadan-Gandai", "Kondagaon", "Korba", "Koriya", 
        "Mahasamund", "Manendragarh-Chirmiri-Bharatpur", "Mohla-Manpur-Ambagarh Chowki", "Mungeli", "Narayanpur", 
        "Raigarh", "Raipur", "Rajnandgaon", "Sarangarh-Bilaigarh", "Sakti", 
        "Sukma", "Surajpur", "Surguja"
    ],
    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", 
        "East Singhbhum", "Garhwa", "Giridih", "Godda", "Gumla", 
        "Hazaribagh", "Jamtara", "Khunti", "Koderma", "Latehar", 
        "Lohardaga", "Pakur", "Palamu", "Ramgarh", "Ranchi", 
        "Sahebganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum"
    ],
    "Uttarakhand": [
        "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", 
        "Haridwar", "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag", 
        "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi"
    ],
    "Himachal Pradesh": [
        "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", 
        "Kullu", "Lahaul and Spiti", "Mandi", "Shimla", "Sirmaur", 
        "Solan", "Una"
    ],
    "Jammu & Kashmir": [
        "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda", 
        "Ganderbal", "Jammu", "Kathua", "Kishtwar", "Kulgam", 
        "Kupwara", "Poonch", "Pulwama", "Rajouri", "Ramban", 
        "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur"
    ],
    "Goa": [
        "North Goa", "South Goa"
    ],
    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala", 
        "South Tripura", "Unakoti", "West Tripura"
    ],
    "Meghalaya": [
        "East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "North Garo Hills", 
        "Ri Bhoi", "South Garo Hills", "South West Garo Hills", "South West Khasi Hills", 
        "West Garo Hills", "West Jaintia Hills", "West Khasi Hills", "Eastern West Khasi Hills"
    ],
    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West", 
        "Jiribam", "Kakching", "Kamjong", "Kangpokpi", "Noney", 
        "Pherzawl", "Senapati", "Tamenglong", "Tengnoupal", "Thoubal", "Ukhrul"
    ],
    "Nagaland": [
        "Chumoukedima", "Dimapur", "Kiphire", "Kohima", "Longleng", 
        "Mokokchung", "Mon", "Niuland", "Noklak", "Peren", 
        "Phek", "Shamator", "Tseminyu", "Tuensang", "Wokha", "Zunheboto"
    ],
    "Mizoram": [
        "Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Kolasib", 
        "Lawngtlai", "Lunglei", "Mamit", "Saitual", "Serchhip", "Siaha"
    ],
    "Arunachal Pradesh": [
        "Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang", 
        "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", 
        "Longding", "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai", 
        "Pakke Kessang", "Papum Pare", "Shi Yomi", "Siang", "Tawang", 
        "Tirap", "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang", "Itanagar"
    ],
    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng"
    ],
    "Delhi": [
        "Central Delhi", "East Delhi", "New Delhi", "North Delhi", "North East Delhi", 
        "North West Delhi", "Shahdara", "South Delhi", "South East Delhi", "South West Delhi", "West Delhi"
    ],
    "Puducherry": [
        "Karaikal", "Mahe", "Puducherry", "Yanam"
    ],
    "Andaman & Nicobar": [
        "Nicobar", "North and Middle Andaman", "South Andaman"
    ],
    "Ladakh": [
        "Kargil", "Leh"
    ],
    "Chandigarh": [
        "Chandigarh"
    ]
};

function initDynamicStateDistrictSelector() {
    const stateSelects = document.querySelectorAll('select.state-select, select#state, select[name="state"]');
    stateSelects.forEach(stateEl => {
        const form = stateEl.closest('form') || document;
        const districtEl = form.querySelector('select.district-select, select#district, select[name="district"]');
        if (!districtEl) return;

        const customInput = form.querySelector('#custom_district, input[name="custom_district"]');

        // Populate State dropdown if options <= 1
        if (stateEl.options.length <= 1) {
            const statesList = Object.keys(INDIA_STATE_DISTRICTS).sort();
            statesList.forEach(st => {
                const opt = document.createElement('option');
                opt.value = st;
                opt.textContent = st;
                stateEl.appendChild(opt);
            });
        }

        const initialSelectedState = stateEl.getAttribute('data-selected-state') || stateEl.value || 'Andhra Pradesh';
        const initialSelectedDistrict = districtEl.getAttribute('data-selected-district') || districtEl.value || '';

        function updateDistricts(selectedState, preselectDistrict) {
            const currentVal = (preselectDistrict !== undefined && preselectDistrict !== '') ? preselectDistrict : districtEl.value;
            districtEl.innerHTML = '';
            
            const placeholder = document.createElement('option');
            placeholder.value = '';
            placeholder.textContent = currentGlobalLang === 'te' ? '-- జిల్లాను ఎంచుకోండి --' : 
                                      (currentGlobalLang === 'hi' ? '-- जिला चुनें --' : 
                                      (currentGlobalLang === 'ta' ? '-- மாவட்டத்தைத் தேர்ந்தெடுக்கவும் --' : '-- Select District --'));
            districtEl.appendChild(placeholder);

            const districts = INDIA_STATE_DISTRICTS[selectedState] || [];
            let districtFound = false;

            districts.forEach(dist => {
                const opt = document.createElement('option');
                opt.value = dist;
                opt.textContent = dist;
                if (currentVal && dist.toLowerCase() === currentVal.toLowerCase()) {
                    opt.selected = true;
                    districtFound = true;
                }
                districtEl.appendChild(opt);
            });

            // Add Custom option
            const customOpt = document.createElement('option');
            customOpt.value = '__custom__';
            customOpt.textContent = currentGlobalLang === 'te' ? '➕ ఇతర / వేరే జిల్లా నమోదు...' : 
                                   (currentGlobalLang === 'hi' ? '➕ अन्य / कस्टम जिला दर्ज करें...' : 
                                   (currentGlobalLang === 'ta' ? '➕ பிற / தனிப்பயன் மாவட்டம்...' : '➕ Other / Enter Custom District...'));
            districtEl.appendChild(customOpt);

            if (currentVal && !districtFound && currentVal !== '' && currentVal !== '__custom__') {
                customOpt.selected = true;
                if (customInput) {
                    customInput.style.display = 'block';
                    customInput.value = currentVal;
                    customInput.required = true;
                }
            } else if (currentVal === '__custom__') {
                customOpt.selected = true;
                if (customInput) {
                    customInput.style.display = 'block';
                    customInput.required = true;
                }
            } else {
                if (customInput) {
                    customInput.style.display = 'none';
                    customInput.required = false;
                }
            }
        }

        // Set initial selected state in element
        if (initialSelectedState) {
            for (let i = 0; i < stateEl.options.length; i++) {
                if (stateEl.options[i].value.toLowerCase() === initialSelectedState.toLowerCase()) {
                    stateEl.selectedIndex = i;
                    break;
                }
            }
        }

        // Populate initial districts
        updateDistricts(stateEl.value || initialSelectedState, initialSelectedDistrict);

        // Event listener for state change
        stateEl.addEventListener('change', () => {
            updateDistricts(stateEl.value, '');
        });

        // Event listener for district change
        districtEl.addEventListener('change', () => {
            if (districtEl.value === '__custom__') {
                if (customInput) {
                    customInput.style.display = 'block';
                    customInput.focus();
                    customInput.required = true;
                }
            } else {
                if (customInput) {
                    customInput.style.display = 'none';
                    customInput.required = false;
                }
            }
        });
    });
}

window.initDynamicStateDistrictSelector = initDynamicStateDistrictSelector;


document.addEventListener('DOMContentLoaded', () => {
    // Initialize AgriSpeaker
    AgriSpeaker.init();

    // Initialize Dynamic State & District Dropdowns
    initDynamicStateDistrictSelector();

    // Apply saved theme and language preferences
    setAppTheme(currentAppTheme);
    setGlobalLanguage(currentGlobalLang);

    // Auto-dismiss alerts after 6 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 6000);
    });

    // Mobile sidebar toggle (if toggle button exists)
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('mobile-open');
        });
    }

    // Delete farm confirmation modal / prompt
    const deleteBtns = document.querySelectorAll('.confirm-delete');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const farmName = btn.getAttribute('data-farm-name') || 'this farm';
            const confirmMsg = currentGlobalLang === 'ta'
                ? `நீங்கள் "${farmName}" நிலத்தை நீக்க விரும்புகிறீர்களா?`
                : (currentGlobalLang === 'te'
                    ? `మీరు "${farmName}" పొలాన్ని తొలగించాలనుకుంటున్నారా?` 
                    : (currentGlobalLang === 'hi' ? `क्या आप "${farmName}" को हटाना चाहते हैं?` : `Are you sure you want to delete "${farmName}"?`));
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });
});

