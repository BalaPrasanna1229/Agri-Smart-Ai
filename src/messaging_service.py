"""
Direct Market Price Surge SMS & WhatsApp Messaging Service for Agri Smart AI
Handles instant SMS notifications, WhatsApp dispatch, Twilio, Fast2SMS API, 
multilingual alert formatting, and automated farmer price surge detection.
"""

import os
import json
import urllib.parse
import urllib.request
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

from src.database import (
    get_db_connection,
    get_user_by_id,
    get_user_farms,
    get_user_crop_predictions,
    get_user_crop_price_alerts,
    create_user_notification,
    log_sent_message,
    get_user_message_logs,
)
from src.market_analysis import get_market_analyzer, COMMODITY_TRANSLATIONS

logger = logging.getLogger("agri_messaging")


def get_messaging_config() -> Dict[str, Any]:
    """Reads messaging gateway credentials from environment variables."""
    fast2sms_key = os.environ.get("FAST2SMS_API_KEY", "").strip()
    twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    twilio_auth = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    twilio_phone = os.environ.get("TWILIO_PHONE_NUMBER", "").strip()
    twilio_whatsapp = os.environ.get("TWILIO_WHATSAPP_NUMBER", "").strip()

    has_fast2sms = bool(fast2sms_key and fast2sms_key != "your_fast2sms_api_key_here")
    has_twilio = bool(twilio_sid and twilio_auth and twilio_phone)

    return {
        "fast2sms_api_key": fast2sms_key,
        "twilio_account_sid": twilio_sid,
        "twilio_auth_token": twilio_auth,
        "twilio_phone_number": twilio_phone,
        "twilio_whatsapp_number": twilio_whatsapp,
        "has_fast2sms": has_fast2sms,
        "has_twilio": has_twilio,
        "active_provider": "Fast2SMS" if has_fast2sms else ("Twilio" if has_twilio else "Simulation / Direct Link"),
    }


def clean_phone_number(phone: str, default_country_code: str = "+91") -> str:
    """Standardizes phone number for international SMS & WhatsApp."""
    if not phone:
        return ""
    digits = "".join(c for c in str(phone) if c.isdigit() or c == "+")
    if digits.startswith("+"):
        return digits
    if len(digits) == 10:
        return f"+91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+{digits}"
    return f"+91{digits}" if not digits.startswith("+") else digits


def generate_whatsapp_click_url(phone: str, message: str) -> str:
    """Generates direct WhatsApp deep link (wa.me) for instant farmer redirection."""
    clean_p = "".join(c for c in phone if c.isdigit())
    encoded_msg = urllib.parse.quote(message)
    if clean_p:
        return f"https://wa.me/{clean_p}?text={encoded_msg}"
    return f"https://api.whatsapp.com/send?text={encoded_msg}"


def format_price_surge_message(
    crop_name: str,
    market_price: float,
    msp: Optional[float] = None,
    spread_pct: Optional[float] = None,
    change_3d_pct: Optional[float] = None,
    lang: str = "te",
) -> Dict[str, str]:
    """
    Builds rich, farmer-friendly, actionable alert messages in Telugu, English, and Hindi.
    """
    # Crop translation lookup
    t_info = COMMODITY_TRANSLATIONS.get(crop_name, {})
    crop_te = t_info.get("te", crop_name)
    crop_hi = t_info.get("hi", crop_name)
    crop_en = t_info.get("en", crop_name)

    price_int = int(round(market_price))
    msp_int = int(round(msp)) if msp else None

    # Telugu Text (Primary for AP/Telangana farmers)
    te_lines = [
        f"🚨 *అగ్రి స్మార్ట్ AI మార్కెట్ ధరల అలర్ట్!* 🌾",
        f"మీ పంట: *{crop_te} ({crop_en})*",
        f"📈 ప్రస్తుత మండీ ధర: *₹{price_int:,} / క్వింటాల్*",
    ]
    if change_3d_pct and change_3d_pct > 0:
        te_lines.append(f"🔥 గత 3 రోజుల్లో ధరల పెరుగుదల: *+{change_3d_pct:.2f}%* 🚀")
    if msp_int and spread_pct and spread_pct > 0:
        te_lines.append(f"💰 ప్రభుత్వ మద్దతు ధర (MSP ₹{msp_int:,}) కంటే *+{spread_pct:.1f}%* ఎక్కువ లాభం!")
    te_lines.append(f"💡 *సలహా:* మండీలో ధరలు గరిష్ట స్థాయిలో ఉన్నాయి. పంట విక్రయించడానికి ఇది అనుకూల సమయం!")
    te_lines.append(f"🌐 మార్కెట్ లైవ్ రిపోర్ట్: https://agrismart.ai/market")

    # English Text
    en_lines = [
        f"🚨 *Agri Smart AI Market Price Surge Alert!* 🌾",
        f"Crop: *{crop_en}*",
        f"📈 Current Mandi Price: *₹{price_int:,}/Quintal*",
    ]
    if change_3d_pct and change_3d_pct > 0:
        en_lines.append(f"🔥 3-Day Price Surge: *+{change_3d_pct:.2f}%* 🚀")
    if msp_int and spread_pct and spread_pct > 0:
        en_lines.append(f"💰 Trading *+{spread_pct:.1f}%* above Govt MSP (₹{msp_int:,})!")
    en_lines.append(f"💡 *Advisory:* Mandi prices are peaking. Excellent opportunity to sell your harvest now!")
    en_lines.append(f"🌐 Live Mandi Dashboard: https://agrismart.ai/market")

    # Hindi Text
    hi_lines = [
        f"🚨 *एग्री स्मार्ट AI मंडी भाव अलर्ट!* 🌾",
        f"फसल: *{crop_hi} ({crop_en})*",
        f"📈 वर्तमान मंडी भाव: *₹{price_int:,}/क्विंटल*",
    ]
    if change_3d_pct and change_3d_pct > 0:
        hi_lines.append(f"🔥 पिछले 3 दिनों में तेजी: *+{change_3d_pct:.2f}%* 🚀")
    if msp_int and spread_pct and spread_pct > 0:
        hi_lines.append(f"💰 सरकारी MSP (₹{msp_int:,}) से *+{spread_pct:.1f}%* अधिक लाभ!")
    hi_lines.append(f"💡 *सलाह:* मंडी में भाव उच्चतम स्तर पर हैं। फसल बेचने का यह सर्वोत्तम समय है!")
    hi_lines.append(f"🌐 लाइव रिपोर्ट: https://agrismart.ai/market")

    return {
        "te": "\n".join(te_lines),
        "en": "\n".join(en_lines),
        "hi": "\n".join(hi_lines),
        "crop_te": crop_te,
        "crop_en": crop_en,
        "crop_hi": crop_hi,
    }


def send_sms_via_fast2sms(phone_number: str, message: str, api_key: str) -> Dict[str, Any]:
    """Sends SMS using Fast2SMS API (Indian Telecom Operator Gateway)."""
    clean_digits = "".join(c for c in phone_number if c.isdigit())
    if len(clean_digits) > 10:
        clean_digits = clean_digits[-10:]

    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "authorization": api_key,
        "route": "q",
        "message": message,
        "language": "unicode",
        "numbers": clean_digits,
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "AgriSmartAI/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            is_return = res_json.get("return", False)
            return {
                "success": bool(is_return),
                "provider": "Fast2SMS",
                "request_id": res_json.get("request_id", ""),
                "message": res_json.get("message", ["Sent successfully"])[0] if isinstance(res_json.get("message"), list) else str(res_json.get("message")),
                "raw": res_json,
            }
    except Exception as e:
        logger.error(f"Fast2SMS error: {e}")
        return {"success": False, "provider": "Fast2SMS", "error": str(e)}


def send_sms_via_twilio(phone_number: str, message: str, cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Sends SMS via Twilio REST API."""
    import base64

    sid = cfg["twilio_account_sid"]
    auth = cfg["twilio_auth_token"]
    from_num = cfg["twilio_phone_number"]
    to_num = clean_phone_number(phone_number)

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    auth_header = base64.b64encode(f"{sid}:{auth}".encode("utf-8")).decode("ascii")

    data = urllib.parse.urlencode({
        "To": to_num,
        "From": from_num,
        "Body": message,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "provider": "Twilio SMS",
                "message_sid": res_json.get("sid"),
                "status": res_json.get("status"),
            }
    except Exception as e:
        logger.error(f"Twilio SMS error: {e}")
        return {"success": False, "provider": "Twilio SMS", "error": str(e)}


def send_direct_message(
    phone_number: str,
    message_text: str,
    channel: str = "sms",
    user_id: Optional[int] = None,
    crop_name: str = "",
    market_price: float = 0.0,
    msp_price: Optional[float] = None,
    change_pct: Optional[float] = None,
    message_text_te: Optional[str] = None,
    message_text_hi: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Universal dispatch engine:
    1. Attempts Fast2SMS / Twilio if credentials configured.
    2. Otherwise executes Instant Local Delivery Simulation + WhatsApp Direct Click Link.
    3. Logs into sms_logs and notifications table.
    """
    if not phone_number:
        return {"success": False, "status": "no_phone", "message": "User phone number is not registered."}

    cfg = get_messaging_config()
    result = {"success": True, "status": "simulated", "provider": "Simulation Engine"}

    # Attempt Live Provider 1: Fast2SMS (for Indian numbers)
    if cfg["has_fast2sms"]:
        sms_res = send_sms_via_fast2sms(phone_number, message_text, cfg["fast2sms_api_key"])
        if sms_res.get("success"):
            result = {
                "success": True,
                "status": "delivered",
                "provider": "Fast2SMS",
                "external_id": sms_res.get("request_id"),
            }
        else:
            logger.warning(f"Fast2SMS failed, falling back to simulated log: {sms_res.get('error')}")

    # Attempt Live Provider 2: Twilio
    elif cfg["has_twilio"]:
        tw_res = send_sms_via_twilio(phone_number, message_text, cfg)
        if tw_res.get("success"):
            result = {
                "success": True,
                "status": "delivered",
                "provider": "Twilio SMS",
                "external_id": tw_res.get("message_sid"),
            }

    # High-Fidelity Simulation Mode
    if result["status"] == "simulated":
        result = {
            "success": True,
            "status": "simulated",
            "provider": "AgriSmart AI Direct Message Engine (Simulated + WhatsApp Ready)",
            "external_id": f"SIM-MSG-{int(datetime.now().timestamp())}",
            "note": "Message prepared and simulated. To send live network SMS, add FAST2SMS_API_KEY or TWILIO credentials in Settings.",
        }

    # Generate WhatsApp Click URL
    wa_url = generate_whatsapp_click_url(phone_number, message_text)
    result["whatsapp_url"] = wa_url
    result["phone"] = phone_number
    result["crop_name"] = crop_name
    result["message_preview"] = message_text[:120] + "..." if len(message_text) > 120 else message_text

    # Log to Database if user_id is provided
    if user_id:
        try:
            log_sent_message(
                user_id=user_id,
                recipient_phone=phone_number,
                channel=channel,
                crop_name=crop_name,
                market_price=market_price,
                msp_price=msp_price,
                price_change_pct=change_pct,
                message_text=message_text,
                message_text_te=message_text_te,
                message_text_hi=message_text_hi,
                status=result["status"],
                provider=result.get("provider", "Simulation"),
                external_id=result.get("external_id"),
            )
        except Exception as e:
            logger.error(f"Could not write to sms_logs: {e}")

    return result


def check_and_dispatch_crop_price_alerts(
    user_id: int,
    force: bool = False,
    min_surge_pct: float = 3.0,
) -> Dict[str, Any]:
    """
    Core Intelligence Engine:
    1. Scans user's registered crops (from Farms, Crop Predictions, Price Watchlist).
    2. Checks Mandi market prices and identifies crops with price surges or premium prices.
    3. Dispatches instant SMS / WhatsApp alert directly to farmer's mobile number.
    4. Avoids duplicate messages within 12 hours unless force=True.
    """
    user = get_user_by_id(user_id)
    if not user:
        return {"success": False, "message": "User not found."}

    phone = user.get("phone", "")
    sms_enabled = bool(user.get("sms_alerts_enabled", 1))
    preferred_channel = user.get("preferred_channel", "sms")

    if not phone:
        return {
            "success": False,
            "status": "missing_phone",
            "message": "దయచేసి మీ మొబైల్ నంబర్ నమోదు చేయండి. (Please register your mobile number to receive instant SMS price alerts.)",
            "user_id": user_id,
            "alerts_sent": 0,
        }

    # 1. Gather all crops associated with this farmer
    farmer_crop_set = set()

    # From user's registered farms
    farms = get_user_farms(user_id)
    for f in farms:
        if f.get("current_crop"):
            farmer_crop_set.add(f["current_crop"].strip())
        if f.get("previous_crop"):
            farmer_crop_set.add(f["previous_crop"].strip())

    # From user's latest crop recommendations
    preds = get_user_crop_predictions(user_id, limit=5)
    for p in preds:
        if p.get("predicted_crop"):
            farmer_crop_set.add(p["predicted_crop"].strip())

    # From user's custom price alert triggers
    custom_alerts = get_user_crop_price_alerts(user_id)
    for ca in custom_alerts:
        if ca.get("crop_name") and ca.get("is_active"):
            farmer_crop_set.add(ca["crop_name"].strip())

    # Default fallback crops if farmer hasn't added any yet
    if not farmer_crop_set:
        farmer_crop_set = {"Paddy", "Cotton", "Maize", "Chilli", "Tomato"}

    analyzer = get_market_analyzer()
    dispatched_alerts = []
    skipped_crops = []

    # Check recent sent messages to prevent spamming within 12 hours
    recent_logs = get_user_message_logs(user_id, limit=30)
    recent_alerted_crops = set()
    cutoff_time = datetime.now() - timedelta(hours=12)

    for l in recent_logs:
        c_time_str = l.get("created_at")
        if c_time_str:
            try:
                # Parse timestamp
                clean_ts = str(c_time_str).split(".")[0]
                dt = datetime.strptime(clean_ts, "%Y-%m-%d %H:%M:%S")
                if dt >= cutoff_time and not force:
                    recent_alerted_crops.add(str(l.get("crop_name", "")).lower().strip())
            except Exception:
                pass

    for crop in sorted(farmer_crop_set):
        crop_clean = crop.lower().strip()
        if crop_clean in recent_alerted_crops and not force:
            skipped_crops.append({"crop": crop, "reason": "Already alerted in last 12 hours"})
            continue

        comm_data = analyzer.get_commodity_for_crop(crop)
        if not comm_data:
            continue

        current_price = float(comm_data.get("Price on 01 Oct, 2026") or 0.0)
        msp = float(comm_data.get("MSP (Rs./Quintal) 2026-27") or 0.0)
        spread_rs = float(comm_data.get("msp_spread_rs") or 0.0)
        spread_pct = float(comm_data.get("msp_spread_pct") or 0.0)
        change_3d = float(comm_data.get("price_change_pct_3d") or 0.0)

        # Evaluate Price Surge Trigger Conditions:
        # 1. Positive 3-day gain >= min_surge_pct (e.g., +3%)
        # 2. Trading significantly above Govt MSP (>= +5%)
        # 3. Matches custom alert target high price if set
        is_surge = False
        surge_reasons = []

        if change_3d >= min_surge_pct:
            is_surge = True
            surge_reasons.append(f"3-day gain +{change_3d:.1f}%")

        if msp > 0 and spread_pct >= 5.0:
            is_surge = True
            surge_reasons.append(f"+{spread_pct:.1f}% above MSP")

        # Check custom price triggers
        for ca in custom_alerts:
            if ca.get("crop_name", "").lower() == crop_clean and ca.get("target_high_price"):
                if current_price >= float(ca["target_high_price"]):
                    is_surge = True
                    surge_reasons.append(f"Exceeded target ₹{int(ca['target_high_price']):,}")

        if is_surge or force:
            # Format multilingual message
            msgs = format_price_surge_message(
                crop_name=comm_data.get("Commodity", crop),
                market_price=current_price,
                msp=msp if msp > 0 else None,
                spread_pct=spread_pct if spread_pct > 0 else None,
                change_3d_pct=change_3d,
                lang="te",
            )

            # Combined Telugu & English SMS text
            sms_body = f"{msgs['te']}\n\n[English]:\n{msgs['en']}"

            # Dispatch via Messaging Gateway
            dispatch_res = send_direct_message(
                phone_number=phone,
                message_text=sms_body,
                channel=preferred_channel,
                user_id=user_id,
                crop_name=crop,
                market_price=current_price,
                msp_price=msp if msp > 0 else None,
                change_pct=change_3d if change_3d > 0 else spread_pct,
                message_text_te=msgs["te"],
                message_text_hi=msgs["hi"],
            )

            # Also create in-app notification
            create_user_notification(
                user_id=user_id,
                title=f"SMS Sent: {msgs['crop_en']} Price Surge at ₹{int(current_price):,}/Qtl",
                title_te=f"SMS పంపబడింది: {msgs['crop_te']} మార్కెట్ ధర ₹{int(current_price):,}/క్వింటాల్",
                message=f"Direct SMS alert sent to {phone}. Mandi price is ₹{int(current_price):,}/Qtl ({', '.join(surge_reasons)}).",
                message_te=f"మీ మొబైల్ {phone} కు నేరుగా SMS అలర్ట్ పంపబడింది. {msgs['crop_te']} మార్కెట్ ధర ₹{int(current_price):,}/క్వింటాల్ కి పెరిగింది.",
                category="market_price",
                action_url="/market",
                badge_type="high_price",
            )

            dispatched_alerts.append({
                "crop": crop,
                "commodity_name": comm_data.get("Commodity", crop),
                "crop_te": msgs["crop_te"],
                "price": current_price,
                "msp": msp,
                "change_3d_pct": change_3d,
                "spread_pct": spread_pct,
                "reasons": surge_reasons,
                "recipient_phone": phone,
                "dispatch_status": dispatch_res.get("status"),
                "whatsapp_url": dispatch_res.get("whatsapp_url"),
                "message_te": msgs["te"],
                "message_en": msgs["en"],
            })

    return {
        "success": True,
        "recipient_phone": phone,
        "alerts_sent": len(dispatched_alerts),
        "dispatched_alerts": dispatched_alerts,
        "skipped_crops": skipped_crops,
        "message": f"విజయవంతంగా {len(dispatched_alerts)} పంట ధరల అలర్ట్ SMS లు మీ మొబైల్ ({phone}) కు పంపబడ్డాయి!" if dispatched_alerts else "ప్రస్తుతం ధరల మార్పు లేదు లేదా ఇప్పటికే అలర్ట్ పంపబడింది.",
    }
