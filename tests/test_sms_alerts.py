"""
Test Suite for Direct Mobile SMS & WhatsApp Price Surge Alert System
Tests phone storage, SMS/WhatsApp formatting, automated market price surge detection,
logging, and Flask API endpoints.
"""

import unittest
import json
import uuid
from pathlib import Path

from app import app
from src.database import (
    init_db,
    get_db_connection,
    create_user,
    get_user_by_id,
    update_user_phone_and_alert_settings,
    add_farm,
    log_sent_message,
    get_user_message_logs,
)
from src.messaging_service import (
    clean_phone_number,
    format_price_surge_message,
    check_and_dispatch_crop_price_alerts,
    send_direct_message,
    get_messaging_config,
)


class TestDirectSMSPriceAlerts(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        init_db()

    def test_01_clean_phone_number(self):
        """Validates phone number parsing for international SMS."""
        self.assertEqual(clean_phone_number("9876543210"), "+919876543210")
        self.assertEqual(clean_phone_number("+919876543210"), "+919876543210")
        self.assertEqual(clean_phone_number("919876543210"), "+919876543210")

    def test_02_format_price_surge_message_multilingual(self):
        """Verifies Telugu, English, and Hindi SMS formatting."""
        msgs = format_price_surge_message(
            crop_name="Paddy(Common)",
            market_price=3317.0,
            msp=2441.0,
            spread_pct=35.9,
            change_3d_pct=4.2,
            lang="te",
        )
        self.assertIn("అగ్రి స్మార్ట్ AI", msgs["te"])
        self.assertIn("3,317", msgs["te"])
        self.assertIn("వరి", msgs["te"])
        self.assertIn("Agri Smart AI", msgs["en"])
        self.assertIn("3,317", msgs["en"])
        self.assertIn("Paddy", msgs["en"])
        self.assertIn("मंडी भाव अलर्ट", msgs["hi"])

    def test_03_user_phone_storage_and_settings(self):
        """Tests user creation with phone number and setting updates."""
        uid = uuid.uuid4().hex[:6]
        user = create_user(
            name="Sita Ram",
            username=f"sitaram_{uid}",
            email=f"sitaram_{uid}@example.com",
            password="password123",
            phone="+919876543210",
        )
        user_id = user["id"]
        fetched = get_user_by_id(user_id)
        self.assertEqual(fetched["phone"], "+919876543210")
        self.assertEqual(fetched["sms_alerts_enabled"], 1)

        # Update settings
        update_user_phone_and_alert_settings(
            user_id=user_id,
            phone="+919123456789",
            sms_alerts_enabled=True,
            whatsapp_alerts_enabled=True,
            preferred_channel="whatsapp",
        )
        updated = get_user_by_id(user_id)
        self.assertEqual(updated["phone"], "+919123456789")
        self.assertEqual(updated["preferred_channel"], "whatsapp")

    def test_04_sms_logging_and_retrieval(self):
        """Tests logging dispatched SMS and retrieving history."""
        uid = uuid.uuid4().hex[:6]
        user = create_user(
            name="Venkat Rao",
            username=f"venkat_{uid}",
            email=f"venkat_{uid}@example.com",
            password="password123",
            phone="+919988776655",
        )
        user_id = user["id"]

        log_id = log_sent_message(
            user_id=user_id,
            recipient_phone="+919988776655",
            channel="sms",
            crop_name="Cotton",
            market_price=7850.0,
            msp_price=7122.0,
            price_change_pct=8.5,
            message_text="Cotton price surge test message",
            message_text_te="పత్తి ధర పెరిగింది",
            status="delivered",
            provider="Fast2SMS",
            external_id="MSG-12345",
        )
        self.assertGreater(log_id, 0)

        logs = get_user_message_logs(user_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]["crop_name"], "Cotton")
        self.assertEqual(logs[0]["market_price"], 7850.0)
        self.assertEqual(logs[0]["status"], "delivered")

    def test_05_check_and_dispatch_crop_price_alerts_flow(self):
        """Tests end-to-end automated price surge detection and dispatch."""
        uid = uuid.uuid4().hex[:6]
        user = create_user(
            name="Naveen Reddy",
            username=f"naveen_{uid}",
            email=f"naveen_{uid}@example.com",
            password="password123",
            phone="+919848012345",
        )
        user_id = user["id"]

        # Register farm with Paddy (which trades +35.9% above MSP)
        add_farm(
            user_id=user_id,
            farm_name="Naveen Paddy Field",
            location="Tenali",
            state="Andhra Pradesh",
            district="Guntur",
            soil_type="Clay Loam",
            land_area=8.0,
            irrigation_type="Canal",
            current_crop="Paddy",
        )

        dispatch_result = check_and_dispatch_crop_price_alerts(user_id=user_id, force=True)
        self.assertTrue(dispatch_result["success"])
        self.assertGreater(dispatch_result["alerts_sent"], 0)
        self.assertEqual(dispatch_result["recipient_phone"], "+919848012345")

        # Verify message log was recorded
        logs = get_user_message_logs(user_id)
        self.assertGreater(len(logs), 0)

    def test_06_flask_alert_api(self):
        """Tests Flask AJAX SMS dispatch endpoint."""
        uid = uuid.uuid4().hex[:6]
        with self.client as c:
            # Register user
            reg_res = c.post("/register", data={
                "name": "Bala Prasanna",
                "username": f"balaprasanna_{uid}",
                "email": f"bala_{uid}@example.com",
                "phone": "+919876543210",
                "password": "password123",
                "confirm_password": "password123",
                "farm_name": "Main Farm",
                "land_area": "10",
                "district": "Guntur",
                "state": "Andhra Pradesh",
                "soil_type": "Black Soil",
                "irrigation_type": "Drip Irrigation",
                "current_crop": "Cotton",
            }, follow_redirects=True)
            self.assertEqual(reg_res.status_code, 200)

            # Login
            login_res = c.post("/login", data={
                "login_id": f"balaprasanna_{uid}",
                "password": "password123",
            }, follow_redirects=True)
            self.assertEqual(login_res.status_code, 200)


            # Test AJAX dispatch API
            api_res = c.post("/api/alerts/dispatch-crop-sms?force=1", headers={
                "X-Requested-With": "XMLHttpRequest",
            })
            self.assertEqual(api_res.status_code, 200)
            data = json.loads(api_res.data.decode("utf-8"))
            self.assertTrue(data["success"])
            self.assertGreater(data["alerts_sent"], 0)

            # Test single crop SMS API
            single_res = c.post("/api/alerts/send-single-crop-sms", json={
                "crop_name": "Cotton",
            }, headers={
                "X-Requested-With": "XMLHttpRequest",
            })
            self.assertEqual(single_res.status_code, 200)
            single_data = json.loads(single_res.data.decode("utf-8"))
            self.assertTrue(single_data["success"])
            self.assertEqual(single_data["crop_name"], "Cotton")


if __name__ == "__main__":
    unittest.main()
