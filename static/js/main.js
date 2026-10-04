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
    }
};

let currentGlobalLang = localStorage.getItem('agri_lang') || 'en';
let currentAppTheme = localStorage.getItem('agri_theme') || 'emerald';

const THEME_META = {
    emerald: { name_en: "Emerald Nature", name_te: "పచ్చని పైరు", name_hi: "एमराल्ड प्रकृति", icon: "🌿", isDark: false },
    midnight: { name_en: "Midnight Dark", name_te: "మిడ్‌నైట్ డార్క్", name_hi: "मिडनाइट डार्क", icon: "🌙", isDark: true },
    golden: { name_en: "Golden Harvest", name_te: "బంగారు పంట", name_hi: "सुनहरी फसल", icon: "🌾", isDark: false },
    monsoon: { name_en: "Monsoon Ocean", name_te: "వర్షాకాలం", name_hi: "मानसून ओशन", icon: "🌊", isDark: false },
    sage: { name_en: "Forest Sage", name_te: "దట్టమైన అడవి", name_hi: "सघन वन", icon: "🍃", isDark: false }
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
    if (!['en', 'te', 'hi'].includes(lang)) {
        lang = 'en';
    }
    currentGlobalLang = lang;
    localStorage.setItem('agri_lang', lang);
    document.documentElement.lang = lang;

    // 1. Update Header Language Selector Buttons
    ['en', 'te', 'hi'].forEach(l => {
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

    // 3. Translate all .lang-text elements (with data-en, data-te, data-hi)
    document.querySelectorAll('.lang-text').forEach(el => {
        const text = el.getAttribute('data-' + lang);
        if (text) {
            el.textContent = text;
        }
    });

    // 4. Translate option elements that have data-en, data-te, data-hi
    document.querySelectorAll('option[data-' + lang + ']').forEach(opt => {
        const text = opt.getAttribute('data-' + lang);
        if (text) {
            opt.textContent = text;
        }
    });

    // 5. Translate input placeholders that have data-en-placeholder, data-te-placeholder
    document.querySelectorAll('[data-' + lang + '-placeholder]').forEach(input => {
        const ph = input.getAttribute('data-' + lang + '-placeholder');
        if (ph) {
            input.placeholder = ph;
        }
    });

    // 6. Refresh Theme Button text
    const meta = THEME_META[currentAppTheme] || THEME_META.emerald;
    const localizedName = lang === 'te' ? meta.name_te : (lang === 'hi' ? meta.name_hi : meta.name_en);
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

document.addEventListener('DOMContentLoaded', () => {
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
            const confirmMsg = currentGlobalLang === 'te' 
                ? `మీరు "${farmName}" పొలాన్ని తొలగించాలనుకుంటున్నారా?` 
                : (currentGlobalLang === 'hi' ? `क्या आप "${farmName}" को हटाना चाहते हैं?` : `Are you sure you want to delete "${farmName}"?`);
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });
});
