"""
Database Module for Agri Smart AI
Handles SQLite database initialization, connection pooling, and schema management.
"""

import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from werkzeug.security import generate_password_hash, check_password_hash

# Default DB Path inside database/ folder
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.environ.get("AGRI_DB_PATH", str(BASE_DIR / "database" / "agri_smart.db")))


def get_db_connection() -> sqlite3.Connection:
    """Creates a database connection with dictionary-like row access."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_file: Optional[Path] = None) -> None:
    """
    Initializes database schema and tables if they do not exist.
    """
    target_path = db_file or DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(target_path))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        phone TEXT,
        sms_alerts_enabled INTEGER DEFAULT 1,
        whatsapp_alerts_enabled INTEGER DEFAULT 1,
        preferred_channel TEXT DEFAULT 'sms',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Try adding new user columns if table was created in older schema
    for col_def in [
        "phone TEXT",
        "sms_alerts_enabled INTEGER DEFAULT 1",
        "whatsapp_alerts_enabled INTEGER DEFAULT 1",
        "preferred_channel TEXT DEFAULT 'sms'",
    ]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {col_def};")
        except Exception:
            pass

    # 2. Farms Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        farm_name TEXT NOT NULL,
        location TEXT NOT NULL,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        soil_type TEXT NOT NULL,
        land_area REAL NOT NULL,
        irrigation_type TEXT NOT NULL,
        previous_crop TEXT,
        current_crop TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 3. Crop Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        farm_id INTEGER,
        n REAL NOT NULL,
        p REAL NOT NULL,
        k REAL NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        ph REAL NOT NULL,
        rainfall REAL NOT NULL,
        predicted_crop TEXT NOT NULL,
        confidence REAL NOT NULL,
        top_recommendations_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE SET NULL
    );
    """)

    # 4. Disease Lookups Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_lookups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        class_name TEXT NOT NULL,
        disease_name TEXT NOT NULL,
        plant_name TEXT NOT NULL,
        lookup_type TEXT DEFAULT 'manual_search',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 5. Yield Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS yield_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        farm_id INTEGER,
        crop_type TEXT NOT NULL,
        farm_area REAL NOT NULL,
        soil_type TEXT NOT NULL,
        irrigation_type TEXT NOT NULL,
        season TEXT NOT NULL,
        fertilizer_used REAL NOT NULL,
        pesticide_used REAL NOT NULL,
        water_usage REAL NOT NULL,
        predicted_yield REAL NOT NULL,
        yield_per_acre REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE SET NULL
    );
    """)

    # 6. Assistant Messages Table (Phase 6)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assistant_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 7. Notifications Table (High Price Alerts & Disease Advisories)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        title_te TEXT,
        title_ta TEXT,
        message TEXT NOT NULL,
        message_te TEXT,
        message_ta TEXT,
        category TEXT DEFAULT 'market_price',
        action_url TEXT,
        badge_type TEXT DEFAULT 'high_price',
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Try adding title_ta / message_ta if table was created in older schema
    try:
        cursor.execute("ALTER TABLE notifications ADD COLUMN title_ta TEXT;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE notifications ADD COLUMN message_ta TEXT;")
    except Exception:
        pass

    # 8. Custom Crop Price Alerts & Real-Time Fluctuation Watchlist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_price_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        crop_name TEXT NOT NULL,
        alert_type TEXT DEFAULT 'both',
        target_high_price REAL,
        target_low_price REAL,
        trigger_percentage REAL DEFAULT 5.0,
        is_active INTEGER DEFAULT 1,
        last_price REAL,
        last_alert_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # 9. SMS & WhatsApp Message Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sms_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        recipient_phone TEXT NOT NULL,
        channel TEXT DEFAULT 'sms',
        crop_name TEXT NOT NULL,
        market_price REAL NOT NULL,
        msp_price REAL,
        price_change_pct REAL,
        message_text TEXT NOT NULL,
        message_text_te TEXT,
        message_text_hi TEXT,
        status TEXT DEFAULT 'sent',
        provider TEXT DEFAULT 'simulation',
        external_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()



# ==========================================
# USER OPERATIONS
# ==========================================

def create_user(name: str, username: str, email: str, password: str, phone: Optional[str] = None) -> Dict[str, Any]:
    """Hashes password and registers a new user with optional mobile number."""
    name = name.strip()
    username = username.strip().lower()
    email = email.strip().lower()
    phone = phone.strip() if phone else None

    if not name or not username or not email or not password:
        raise ValueError("All registration fields are required.")

    password_hash = generate_password_hash(password)
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (name, username, email, password_hash, phone)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, username, email, password_hash, phone),
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"id": user_id, "name": name, "username": username, "email": email, "phone": phone}
    except sqlite3.IntegrityError as e:
        err_msg = str(e).lower()
        if "username" in err_msg:
            raise ValueError("Username is already taken. Please choose another.")
        elif "email" in err_msg:
            raise ValueError("Email address is already registered. Please login.")
        else:
            raise ValueError("User with these credentials already exists.")
    finally:
        conn.close()


def authenticate_user(login_id: str, password: str) -> Optional[Dict[str, Any]]:
    """Validates user by email/username and password. Returns user dict or None."""
    login_id = login_id.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?
        """,
        (login_id, login_id),
    )
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row["password_hash"], password):
        return {
            "id": row["id"],
            "name": row["name"],
            "username": row["username"],
            "email": row["email"],
            "phone": row["phone"] if "phone" in row.keys() else None,
            "sms_alerts_enabled": row["sms_alerts_enabled"] if "sms_alerts_enabled" in row.keys() else 1,
            "whatsapp_alerts_enabled": row["whatsapp_alerts_enabled"] if "whatsapp_alerts_enabled" in row.keys() else 1,
            "preferred_channel": row["preferred_channel"] if "preferred_channel" in row.keys() else "sms",
            "created_at": row["created_at"],
        }
    return None


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves user profile by ID including phone number and alert preferences."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, name, username, email, phone, sms_alerts_enabled, whatsapp_alerts_enabled, preferred_channel, created_at 
        FROM users WHERE id = ?
        """, 
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    if "phone" not in d or d["phone"] is None:
        d["phone"] = ""
    if "sms_alerts_enabled" not in d or d["sms_alerts_enabled"] is None:
        d["sms_alerts_enabled"] = 1
    if "whatsapp_alerts_enabled" not in d or d["whatsapp_alerts_enabled"] is None:
        d["whatsapp_alerts_enabled"] = 1
    if "preferred_channel" not in d or not d["preferred_channel"]:
        d["preferred_channel"] = "sms"
    return d


def update_user_phone_and_alert_settings(
    user_id: int,
    phone: Optional[str] = None,
    sms_alerts_enabled: bool = True,
    whatsapp_alerts_enabled: bool = True,
    preferred_channel: str = "sms",
) -> bool:
    """Updates user phone number and SMS/WhatsApp alert notification preferences."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cleaned_phone = phone.strip() if phone and phone.strip() else None
    cursor.execute(
        """
        UPDATE users 
        SET phone = ?, sms_alerts_enabled = ?, whatsapp_alerts_enabled = ?, preferred_channel = ?
        WHERE id = ?
        """,
        (cleaned_phone, 1 if sms_alerts_enabled else 0, 1 if whatsapp_alerts_enabled else 0, (preferred_channel or "sms").strip().lower(), user_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def clear_user_phone_alerts(user_id: int) -> bool:
    """Permanently clears the registered phone number and disables phone alerts for user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users 
        SET phone = NULL, sms_alerts_enabled = 0, whatsapp_alerts_enabled = 0
        WHERE id = ?
        """,
        (user_id,),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated



def update_user_profile(
    user_id: int,
    name: str,
    email: str,
    phone: Optional[str] = None,
) -> bool:
    """Updates basic profile info (name, email, phone)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE users 
        SET name = ?, email = ?, phone = ?
        WHERE id = ?
        """,
        (name.strip(), email.strip().lower(), phone.strip() if phone else None, user_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


# ==========================================
# SMS & WHATSAPP MESSAGE LOGGING
# ==========================================

def log_sent_message(
    user_id: int,
    recipient_phone: str,
    channel: str,
    crop_name: str,
    market_price: float,
    msp_price: Optional[float] = None,
    price_change_pct: Optional[float] = None,
    message_text: str = "",
    message_text_te: Optional[str] = None,
    message_text_hi: Optional[str] = None,
    status: str = "sent",
    provider: str = "simulation",
    external_id: Optional[str] = None,
) -> int:
    """Logs sent SMS / WhatsApp alert message."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO sms_logs (
            user_id, recipient_phone, channel, crop_name, market_price,
            msp_price, price_change_pct, message_text, message_text_te, message_text_hi,
            status, provider, external_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            recipient_phone.strip(),
            channel.strip().lower(),
            crop_name.strip(),
            float(market_price),
            float(msp_price) if msp_price is not None else None,
            float(price_change_pct) if price_change_pct is not None else None,
            message_text.strip(),
            message_text_te.strip() if message_text_te else None,
            message_text_hi.strip() if message_text_hi else None,
            status.strip().lower(),
            provider.strip(),
            external_id,
        ),
    )
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id


def get_user_message_logs(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves all sent SMS & WhatsApp message logs for a user, newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM sms_logs
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==========================================
# FARM OPERATIONS (USER-ISOLATED)
# ==========================================

def add_farm(
    user_id: int,
    farm_name: str,
    location: str,
    state: str,
    district: str,
    soil_type: str,
    land_area: float,
    irrigation_type: str,
    previous_crop: Optional[str] = None,
    current_crop: Optional[str] = None,
    description: Optional[str] = None,
) -> int:
    """Inserts a new farm belonging to a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO farms (
            user_id, farm_name, location, state, district, soil_type,
            land_area, irrigation_type, previous_crop, current_crop, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            farm_name.strip(),
            location.strip(),
            state.strip(),
            district.strip(),
            soil_type.strip(),
            float(land_area),
            irrigation_type.strip(),
            previous_crop.strip() if previous_crop else "",
            current_crop.strip() if current_crop else "",
            description.strip() if description else "",
        ),
    )
    conn.commit()
    farm_id = cursor.lastrowid
    conn.close()
    return farm_id


def get_user_farms(user_id: int) -> List[Dict[str, Any]]:
    """Fetches all farms owned by the given user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM farms WHERE user_id = ? ORDER BY created_at DESC", (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_farm_by_id(farm_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches a specific farm with strict user ownership verification."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM farms WHERE id = ? AND user_id = ?", (farm_id, user_id)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_farm(
    farm_id: int,
    user_id: int,
    farm_name: str,
    location: str,
    state: str,
    district: str,
    soil_type: str,
    land_area: float,
    irrigation_type: str,
    previous_crop: Optional[str] = None,
    current_crop: Optional[str] = None,
    description: Optional[str] = None,
) -> bool:
    """Updates farm details only if owned by the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE farms SET
            farm_name = ?, location = ?, state = ?, district = ?, soil_type = ?,
            land_area = ?, irrigation_type = ?, previous_crop = ?, current_crop = ?, description = ?
        WHERE id = ? AND user_id = ?
        """,
        (
            farm_name.strip(),
            location.strip(),
            state.strip(),
            district.strip(),
            soil_type.strip(),
            float(land_area),
            irrigation_type.strip(),
            previous_crop.strip() if previous_crop else "",
            current_crop.strip() if current_crop else "",
            description.strip() if description else "",
            farm_id,
            user_id,
        ),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_farm(farm_id: int, user_id: int) -> bool:
    """Deletes farm record only if owned by the user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM farms WHERE id = ? AND user_id = ?", (farm_id, user_id))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


# ==========================================
# CROP PREDICTION HISTORY (USER-ISOLATED)
# ==========================================

def save_crop_prediction(
    user_id: int,
    farm_id: Optional[int],
    n: float,
    p: float,
    k: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float,
    predicted_crop: str,
    confidence: float,
    top_recommendations_json: str,
) -> int:
    """Saves crop recommendation query and result for user history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO crop_predictions (
            user_id, farm_id, n, p, k, temperature, humidity, ph, rainfall,
            predicted_crop, confidence, top_recommendations_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            farm_id if farm_id else None,
            float(n),
            float(p),
            float(k),
            float(temperature),
            float(humidity),
            float(ph),
            float(rainfall),
            predicted_crop,
            float(confidence),
            top_recommendations_json,
        ),
    )
    conn.commit()
    pred_id = cursor.lastrowid
    conn.close()
    return pred_id


DB_CROP_NAMES = {
    "rice": {"en": "Rice", "te": "వరి", "hi": "धान"},
    "paddy": {"en": "Paddy", "te": "వరి", "hi": "धान"},
    "maize": {"en": "Maize", "te": "మొక్కజొన్న", "hi": "मक्का"},
    "chickpea": {"en": "Chickpea", "te": "శనగలు", "hi": "चना"},
    "kidneybeans": {"en": "Kidney Beans", "te": "రాజ్మా", "hi": "राजमा"},
    "pigeonpeas": {"en": "Pigeon Peas (Tur)", "te": "కందులు", "hi": "अरहर"},
    "mothbeans": {"en": "Moth Beans", "te": "మొత్ బీన్స్", "hi": "मोठ"},
    "mungbean": {"en": "Green Gram (Mung)", "te": "పెసలు", "hi": "मूंग"},
    "blackgram": {"en": "Black Gram (Urad)", "te": "మినుములు", "hi": "उड़द"},
    "lentil": {"en": "Lentil", "te": "మసూర్ పప్పు", "hi": "मसूर"},
    "pomegranate": {"en": "Pomegranate", "te": "దానిమ్మ", "hi": "अनार"},
    "banana": {"en": "Banana", "te": "అరటి", "hi": "केला"},
    "mango": {"en": "Mango", "te": "మామిడి", "hi": "आम"},
    "grapes": {"en": "Grapes", "te": "ద్రాక్ష", "hi": "अंगूर"},
    "watermelon": {"en": "Watermelon", "te": "పుచ్చకాయ", "hi": "तरबूज"},
    "muskmelon": {"en": "Muskmelon", "te": "ఖర్బూజ", "hi": "खरबूजा"},
    "apple": {"en": "Apple", "te": "యాపిల్", "hi": "सेब"},
    "orange": {"en": "Orange", "te": "నారింజ", "hi": "संतरा"},
    "papaya": {"en": "Papaya", "te": "బొప్పాయి", "hi": "पपीता"},
    "coconut": {"en": "Coconut", "te": "కొబ్బరి", "hi": "नारियल"},
    "cotton": {"en": "Cotton", "te": "పత్తి", "hi": "कपास"},
    "jute": {"en": "Jute", "te": "జనపనార", "hi": "पटसन"},
    "coffee": {"en": "Coffee", "te": "కాఫీ", "hi": "कॉफी"},
}

DB_SEASON_NAMES = {
    "Kharif": {"en": "Kharif", "te": "ఖరీఫ్ (వానాకాలం)", "hi": "खरीफ"},
    "Rabi": {"en": "Rabi", "te": "రబీ (యాసంగి)", "hi": "रबी"},
    "Zaid": {"en": "Zaid", "te": "జైద్ (వేసవి)", "hi": "जायद"},
    "Whole Year": {"en": "Whole Year", "te": "ఏడాది పొడవునా", "hi": "पूरे साल"},
    "Summer": {"en": "Summer", "te": "వేసవి", "hi": "गर्मी"},
    "Winter": {"en": "Winter", "te": "శీతాకాలం", "hi": "सर्दी"},
}

DB_SOIL_NAMES = {
    "Clay": {"en": "Clay", "te": "జిగురు నేల", "hi": "चिकनी मिट्टी"},
    "Sandy": {"en": "Sandy", "te": "ఇసుక నేల", "hi": "बलुई मिट्टी"},
    "Loamy": {"en": "Loamy", "te": "ఒండ్రు నేల", "hi": "दोमट मिट्टी"},
    "Black": {"en": "Black", "te": "నల్లరేగడి నేల", "hi": "काली मिट्टी"},
    "Red": {"en": "Red", "te": "ఎర్ర నేల", "hi": "लाल मिट्टी"},
    "Alluvial": {"en": "Alluvial", "te": "వరి ఒండ్రు నేల", "hi": "जलोढ़ मिट्टी"},
}

DB_PLANT_NAMES = {
    "Tomato": {"en": "Tomato", "te": "టమోటా", "hi": "टमाटर"},
    "Potato": {"en": "Potato", "te": "బంగాళాదుంప", "hi": "आलू"},
    "Corn_(maize)": {"en": "Corn (Maize)", "te": "మొక్కజొన్న", "hi": "मक्का"},
    "Grape": {"en": "Grape", "te": "ద్రాక్ష", "hi": "अंगूर"},
    "Apple": {"en": "Apple", "te": "యాపిల్", "hi": "सेब"},
    "Pepper,_bell": {"en": "Bell Pepper (Chili)", "te": "క్యాప్సికం / మిరప", "hi": "शिमला मिर्च / मिर्च"},
    "Strawberry": {"en": "Strawberry", "te": "స్ట్రాబెర్రీ", "hi": "स्ट्रॉबेरी"},
    "Peach": {"en": "Peach", "te": "పీచ్", "hi": "आड़ू"},
    "Orange": {"en": "Orange (Citrus)", "te": "బత్తాయి / నారింజ", "hi": "संतरा / नींबू"},
    "Squash": {"en": "Squash / Gourd", "te": "గుమ్మడి / సొరకాయ", "hi": "कद्दू / लौकी"},
    "Soybean": {"en": "Soybean", "te": "సోయాబీన్", "hi": "सोयाबीन"},
    "Blueberry": {"en": "Blueberry", "te": "బ్లూబెర్రీ", "hi": "ब्लूबेरी"},
    "Raspberry": {"en": "Raspberry", "te": "రాస్ప్‌బెర్రీ", "hi": "रसभरी"},
    "Cherry_(including_sour)": {"en": "Cherry", "te": "చెర్రీ", "hi": "चेरी"},
}

DB_DISEASE_NAMES = {
    "Bacterial spot": {"en": "Bacterial Spot", "te": "బాక్టీరియల్ మచ్చల తెగులు", "hi": "जीवाणु धब्बा रोग"},
    "Early blight": {"en": "Early Blight", "te": "ముందస్తు ఆకుమచ్చ తెగులు", "hi": "अगेती झुलसा"},
    "Late blight": {"en": "Late Blight", "te": "ఆలస్యపు ఆకుమచ్చ తెగులు", "hi": "पछेती झुलसा"},
    "Leaf Mold": {"en": "Leaf Mold", "te": "బూజు తెగులు", "hi": "पत्ती का फफूंद रोग"},
    "Septoria leaf spot": {"en": "Septoria Leaf Spot", "te": "సెప్టోరియా ఆకుమచ్చ తెగులు", "hi": "सेप्टोरिया पत्ती धब्बा"},
    "Spider mites Two-spotted spider mite": {"en": "Spider Mites", "te": "ఎర్ర నల్లి / బూడిద పురుగు", "hi": "मकड़ी कीट"},
    "Target Spot": {"en": "Target Spot", "te": "లక్ష్య ఆకుమచ్చ తెగులు", "hi": "टारगेट स्पॉट"},
    "Yellow Leaf Curl Virus": {"en": "Yellow Leaf Curl Virus", "te": "ఆకు ముడత వైరస్", "hi": "पीला पत्ता मरोड़ वायरस"},
    "mosaic virus": {"en": "Mosaic Virus", "te": "మొజాయిక్ వైరస్ తెగులు", "hi": "मोज़ेक वायरस"},
    "healthy": {"en": "Healthy Crop (No Disease)", "te": "ఆరోగ్యకరమైన పంట (వ్యాధి లేదు)", "hi": "स्वस्थ फसल (कोई रोग नहीं)"},
    "Common rust": {"en": "Common Rust", "te": "తుప్పు తెగులు", "hi": "रतुआ / जंग रोग"},
    "Northern Leaf Blight": {"en": "Northern Leaf Blight", "te": "ఉత్తరాది ఆకు ఎండ తెగులు", "hi": "उत्तरी पत्ता झुलसा"},
    "Black rot": {"en": "Black Rot", "te": "నల్ల కుళ్లు తెగులు", "hi": "काला सड़न रोग"},
    "Esca (Black Measles)": {"en": "Esca (Black Measles)", "te": "ఎస్కా (నల్ల మచ్చల తెగులు)", "hi": "एस्का (काला चेचक)"},
    "Leaf blight (Isariopsis Leaf Spot)": {"en": "Leaf Blight", "te": "ఆకు ఎండు తెగులు", "hi": "पत्ती झुलसा"},
    "Apple scab": {"en": "Apple Scab", "te": "యాపిల్ గజ్జి తెగులు", "hi": "सेब का स्कैब रोग"},
    "Cedar apple rust": {"en": "Cedar Apple Rust", "te": "సీడార్ యాపిల్ తుప్పు తెగులు", "hi": "देवदार सेब रतुआ"},
    "Powdery mildew": {"en": "Powdery Mildew", "te": "బూడిద తెగులు", "hi": "चूर्णिल आसिता (सफेद फफूंद)"},
}


def get_user_crop_predictions(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves prediction history for the current user joined with optional farm name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT cp.*, f.farm_name
        FROM crop_predictions cp
        LEFT JOIN farms f ON cp.farm_id = f.id
        WHERE cp.user_id = ?
        ORDER BY cp.created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        c_key = str(d.get("predicted_crop", "")).lower().strip()
        t_info = DB_CROP_NAMES.get(c_key, {})
        d["predicted_crop_en"] = t_info.get("en", d.get("predicted_crop", "").capitalize())
        d["predicted_crop_te"] = t_info.get("te", d.get("predicted_crop", ""))
        d["predicted_crop_hi"] = t_info.get("hi", d.get("predicted_crop", ""))
        results.append(d)
    return results


def get_user_dashboard_stats(user_id: int) -> Dict[str, Any]:
    """Gathers aggregate counts for user's dashboard view."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Farms count and total acreage
    cursor.execute(
        "SELECT COUNT(*) as farm_count, COALESCE(SUM(land_area), 0) as total_area FROM farms WHERE user_id = ?",
        (user_id,),
    )
    farm_row = cursor.fetchone()
    
    # Crop Predictions count
    cursor.execute(
        "SELECT COUNT(*) as pred_count FROM crop_predictions WHERE user_id = ?",
        (user_id,),
    )
    pred_row = cursor.fetchone()

    # Disease lookups count
    cursor.execute(
        "SELECT COUNT(*) as disease_count FROM disease_lookups WHERE user_id = ?",
        (user_id,),
    )
    disease_row = cursor.fetchone()

    # Yield Predictions count
    cursor.execute(
        "SELECT COUNT(*) as yield_count FROM yield_predictions WHERE user_id = ?",
        (user_id,),
    )
    yield_row = cursor.fetchone()
    
    conn.close()
    return {
        "farm_count": farm_row["farm_count"] if farm_row else 0,
        "total_area_acres": round(farm_row["total_area"], 1) if farm_row else 0.0,
        "prediction_count": pred_row["pred_count"] if pred_row else 0,
        "disease_lookup_count": disease_row["disease_count"] if disease_row else 0,
        "yield_prediction_count": yield_row["yield_count"] if yield_row else 0,
    }


# ==========================================
# DISEASE LOOKUP LOGGING (USER-ISOLATED)
# ==========================================

def save_disease_lookup(
    user_id: int,
    class_name: str,
    disease_name: str,
    plant_name: str,
    lookup_type: str = "manual_search",
) -> int:
    """Logs disease lookup for current user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO disease_lookups (user_id, class_name, disease_name, plant_name, lookup_type)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, class_name.strip(), disease_name.strip(), plant_name.strip(), lookup_type.strip()),
    )
    conn.commit()
    lookup_id = cursor.lastrowid
    conn.close()
    return lookup_id


def get_user_disease_lookups(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches disease lookup history for user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM disease_lookups
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        p_name = d.get("plant_name", "")
        d_name = d.get("disease_name", "")
        d["plant_name_en"] = DB_PLANT_NAMES.get(p_name, {}).get("en", p_name)
        d["plant_name_te"] = DB_PLANT_NAMES.get(p_name, {}).get("te", p_name)
        d["plant_name_hi"] = DB_PLANT_NAMES.get(p_name, {}).get("hi", p_name)
        d["disease_name_en"] = DB_DISEASE_NAMES.get(d_name, {}).get("en", d_name)
        d["disease_name_te"] = DB_DISEASE_NAMES.get(d_name, {}).get("te", d_name)
        d["disease_name_hi"] = DB_DISEASE_NAMES.get(d_name, {}).get("hi", d_name)
        results.append(d)
    return results


# ==========================================
# YIELD PREDICTION LOGGING (USER-ISOLATED)
# ==========================================

def save_yield_prediction(
    user_id: int,
    farm_id: Optional[int],
    crop_type: str,
    farm_area: float,
    soil_type: str,
    irrigation_type: str,
    season: str,
    fertilizer_used: float,
    pesticide_used: float,
    water_usage: float,
    predicted_yield: float,
    yield_per_acre: float,
) -> int:
    """Saves farm crop yield prediction query and result for user history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO yield_predictions (
            user_id, farm_id, crop_type, farm_area, soil_type, irrigation_type,
            season, fertilizer_used, pesticide_used, water_usage, predicted_yield, yield_per_acre
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            farm_id if farm_id else None,
            crop_type.strip(),
            float(farm_area),
            soil_type.strip(),
            irrigation_type.strip(),
            season.strip(),
            float(fertilizer_used),
            float(pesticide_used),
            float(water_usage),
            float(predicted_yield),
            float(yield_per_acre),
        ),
    )
    conn.commit()
    yield_id = cursor.lastrowid
    conn.close()
    return yield_id


def get_user_yield_predictions(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves yield prediction history for current user joined with optional farm name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT yp.*, f.farm_name
        FROM yield_predictions yp
        LEFT JOIN farms f ON yp.farm_id = f.id
        WHERE yp.user_id = ?
        ORDER BY yp.created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        c_key = str(d.get("crop_type", "")).lower().strip()
        t_info = DB_CROP_NAMES.get(c_key, {})
        d["crop_type_en"] = t_info.get("en", d.get("crop_type", "").capitalize())
        d["crop_type_te"] = t_info.get("te", d.get("crop_type", ""))
        d["crop_type_hi"] = t_info.get("hi", d.get("crop_type", ""))
        
        s_val = d.get("season", "")
        d["season_en"] = DB_SEASON_NAMES.get(s_val, {}).get("en", s_val)
        d["season_te"] = DB_SEASON_NAMES.get(s_val, {}).get("te", s_val)
        d["season_hi"] = DB_SEASON_NAMES.get(s_val, {}).get("hi", s_val)
        
        soil_val = d.get("soil_type", "")
        d["soil_type_en"] = DB_SOIL_NAMES.get(soil_val, {}).get("en", soil_val)
        d["soil_type_te"] = DB_SOIL_NAMES.get(soil_val, {}).get("te", soil_val)
        d["soil_type_hi"] = DB_SOIL_NAMES.get(soil_val, {}).get("hi", soil_val)
        results.append(d)
    return results


# ==========================================
# ASSISTANT CHAT LOGGING (USER-ISOLATED)
# ==========================================

def save_assistant_message(user_id: int, role: str, message: str) -> int:
    """Saves user or assistant chat message for current user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO assistant_messages (user_id, role, message)
        VALUES (?, ?, ?)
        """,
        (user_id, role.strip(), message.strip()),
    )
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()
    return msg_id


def get_user_assistant_messages(user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves chat message history for current user ordered chronologically."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM (
            SELECT * FROM assistant_messages
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ) ORDER BY created_at ASC
        """,
        (user_id, limit),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def clear_user_assistant_messages(user_id: int) -> bool:
    """Deletes all assistant messages for current user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assistant_messages WHERE user_id = ?", (user_id,))
    conn.commit()
    cleared = cursor.rowcount >= 0
    conn.close()
    return cleared


def get_user_smart_summary(user_id: int) -> Dict[str, Any]:
    """
    Gathers latest user records across all modules for smart dashboard summary.
    Enriched with clean multilingual fields for pure language switching.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Latest Crop Prediction
    cursor.execute(
        """
        SELECT cp.*, f.farm_name
        FROM crop_predictions cp
        LEFT JOIN farms f ON cp.farm_id = f.id
        WHERE cp.user_id = ?
        ORDER BY cp.created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    crop_row = cursor.fetchone()

    # Latest Yield Prediction
    cursor.execute(
        """
        SELECT yp.*, f.farm_name
        FROM yield_predictions yp
        LEFT JOIN farms f ON yp.farm_id = f.id
        WHERE yp.user_id = ?
        ORDER BY yp.created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    yield_row = cursor.fetchone()

    # Latest Disease Lookup
    cursor.execute(
        """
        SELECT * FROM disease_lookups
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    disease_row = cursor.fetchone()

    # Chat message count
    cursor.execute(
        "SELECT COUNT(*) as msg_count FROM assistant_messages WHERE user_id = ?",
        (user_id,),
    )
    msg_row = cursor.fetchone()

    conn.close()

    crop_dict = dict(crop_row) if crop_row else None
    if crop_dict:
        c_key = str(crop_dict.get("predicted_crop", "")).lower().strip()
        t_info = DB_CROP_NAMES.get(c_key, {})
        crop_dict["predicted_crop_en"] = t_info.get("en", crop_dict.get("predicted_crop", "").capitalize())
        crop_dict["predicted_crop_te"] = t_info.get("te", crop_dict.get("predicted_crop", ""))
        crop_dict["predicted_crop_hi"] = t_info.get("hi", crop_dict.get("predicted_crop", ""))

    yield_dict = dict(yield_row) if yield_row else None
    if yield_dict:
        c_key = str(yield_dict.get("crop_type", "")).lower().strip()
        t_info = DB_CROP_NAMES.get(c_key, {})
        yield_dict["crop_type_en"] = t_info.get("en", yield_dict.get("crop_type", "").capitalize())
        yield_dict["crop_type_te"] = t_info.get("te", yield_dict.get("crop_type", ""))
        yield_dict["crop_type_hi"] = t_info.get("hi", yield_dict.get("crop_type", ""))

        s_val = yield_dict.get("season", "")
        yield_dict["season_en"] = DB_SEASON_NAMES.get(s_val, {}).get("en", s_val)
        yield_dict["season_te"] = DB_SEASON_NAMES.get(s_val, {}).get("te", s_val)
        yield_dict["season_hi"] = DB_SEASON_NAMES.get(s_val, {}).get("hi", s_val)

        soil_val = yield_dict.get("soil_type", "")
        yield_dict["soil_type_en"] = DB_SOIL_NAMES.get(soil_val, {}).get("en", soil_val)
        yield_dict["soil_type_te"] = DB_SOIL_NAMES.get(soil_val, {}).get("te", soil_val)
        yield_dict["soil_type_hi"] = DB_SOIL_NAMES.get(soil_val, {}).get("hi", soil_val)

    disease_dict = dict(disease_row) if disease_row else None
    if disease_dict:
        p_name = disease_dict.get("plant_name", "")
        d_name = disease_dict.get("disease_name", "")
        disease_dict["plant_name_en"] = DB_PLANT_NAMES.get(p_name, {}).get("en", p_name)
        disease_dict["plant_name_te"] = DB_PLANT_NAMES.get(p_name, {}).get("te", p_name)
        disease_dict["plant_name_hi"] = DB_PLANT_NAMES.get(p_name, {}).get("hi", p_name)
        disease_dict["disease_name_en"] = DB_DISEASE_NAMES.get(d_name, {}).get("en", d_name)
        disease_dict["disease_name_te"] = DB_DISEASE_NAMES.get(d_name, {}).get("te", d_name)
        disease_dict["disease_name_hi"] = DB_DISEASE_NAMES.get(d_name, {}).get("hi", d_name)

    return {
        "latest_crop": crop_dict,
        "latest_yield": yield_dict,
        "latest_disease": disease_dict,
        "assistant_message_count": msg_row["msg_count"] if msg_row else 0,
    }


# ==========================================
# NOTIFICATIONS (HIGH PRICE ALERTS & ADVISORIES)
# ==========================================

def create_user_notification(
    user_id: int,
    title: str,
    message: str,
    title_te: Optional[str] = None,
    message_te: Optional[str] = None,
    title_ta: Optional[str] = None,
    message_ta: Optional[str] = None,
    category: str = "market_price",
    action_url: Optional[str] = None,
    badge_type: str = "high_price",
) -> int:
    """Creates an in-app alert notification for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO notifications (user_id, title, title_te, title_ta, message, message_te, message_ta, category, action_url, badge_type, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """,
        (user_id, title.strip(), title_te, title_ta, message.strip(), message_te, message_ta, category, action_url, badge_type),
    )
    conn.commit()
    notif_id = cursor.lastrowid
    conn.close()
    return notif_id


def get_user_notifications(user_id: int, limit: int = 20, unread_only: bool = False) -> List[Dict[str, Any]]:
    """Retrieves notifications for a user, sorted latest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if unread_only:
        cursor.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = ? AND is_read = 0
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
    else:
        cursor.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_unread_notification_count(user_id: int) -> int:
    """Returns the count of unread notifications for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) as unread_count FROM notifications
        WHERE user_id = ? AND is_read = 0
        """,
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()
    return int(row["unread_count"]) if row else 0


def mark_notification_read(notif_id: int, user_id: int) -> bool:
    """Marks a single notification as read."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE notifications SET is_read = 1
        WHERE id = ? AND user_id = ?
        """,
        (notif_id, user_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def mark_all_notifications_read(user_id: int) -> bool:
    """Marks all unread notifications for a user as read."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE notifications SET is_read = 1
        WHERE user_id = ? AND is_read = 0
        """,
        (user_id,),
    )
    conn.commit()
    updated = cursor.rowcount >= 0
    conn.close()
    return updated


def delete_notification(notif_id: int, user_id: int) -> bool:
    """Deletes a notification record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM notifications
        WHERE id = ? AND user_id = ?
        """,
        (notif_id, user_id),
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


# ==========================================
# CUSTOM CROP PRICE WATCH & FLUCTUATION ALERTS
# ==========================================

def add_crop_price_alert(
    user_id: int,
    crop_name: str,
    alert_type: str = "both",
    target_high_price: Optional[float] = None,
    target_low_price: Optional[float] = None,
    trigger_percentage: float = 5.0,
    last_price: Optional[float] = None,
) -> int:
    """Creates or updates a custom crop price watch trigger for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO crop_price_alerts (user_id, crop_name, alert_type, target_high_price, target_low_price, trigger_percentage, is_active, last_price)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?)
        """,
        (user_id, crop_name.strip(), alert_type, target_high_price, target_low_price, trigger_percentage, last_price),
    )
    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()
    return alert_id


def get_user_crop_price_alerts(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all active and inactive price watch alerts set by user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM crop_price_alerts
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_crop_price_alert(alert_id: int, user_id: int) -> bool:
    """Deletes a custom crop price alert rule."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM crop_price_alerts
        WHERE id = ? AND user_id = ?
        """,
        (alert_id, user_id),
    )
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def toggle_crop_price_alert(alert_id: int, user_id: int, is_active: bool) -> bool:
    """Toggles active state of a crop price alert."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE crop_price_alerts SET is_active = ?
        WHERE id = ? AND user_id = ?
        """,
        (1 if is_active else 0, alert_id, user_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated





