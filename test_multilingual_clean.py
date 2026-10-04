"""
Test script to verify 100% clean multilingual separation across all routes and features.
"""
import unittest
from app import app
from src.integrated_advisory import generate_comprehensive_farmer_advisory
from src.market_analysis import get_market_analyzer
from src.database import get_user_smart_summary, get_user_crop_predictions, get_user_yield_predictions

class TestCleanMultilingual(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_integrated_advisory_clean_separation(self):
        soil_inputs = {
            "N": 90.0,
            "P": 42.0,
            "K": 43.0,
            "temperature": 20.88,
            "humidity": 82.0,
            "ph": 6.5,
            "rainfall": 202.9,
        }
        res = generate_comprehensive_farmer_advisory(user_id=1, soil_inputs=soil_inputs, farm_area=5.0)
        crop_rec = res["crop_recommendation"]
        self.assertIn("crop_name_en", crop_rec)
        self.assertIn("crop_name_te", crop_rec)
        self.assertIn("crop_name_hi", crop_rec)
        self.assertEqual(crop_rec["crop_name_en"], "Rice")
        self.assertEqual(crop_rec["crop_name_te"], "వరి")
        
        # Ensure no mixed brackets in crop name
        self.assertNotIn("(", crop_rec["crop_name_te"])

        # Check diseases
        for d in res["disease_management"]["diseases"]:
            self.assertIn("disease_name_en", d)
            self.assertIn("disease_name_te", d)
            self.assertIn("threat_level_en", d)
            self.assertIn("threat_level_te", d)
            self.assertIn("organic_precautions_en", d)
            self.assertIn("organic_precautions_te", d)

    def test_market_alerts_clean_separation(self):
        ma = get_market_analyzer()
        alerts = ma.get_high_price_alerts()
        self.assertGreater(len(alerts), 0)
        for a in alerts:
            self.assertIn("badge_en", a)
            self.assertIn("badge_te", a)
            self.assertIn("badge_hi", a)
            self.assertIn("title_en", a)
            self.assertIn("title_te", a)
            self.assertIn("message_en", a)
            self.assertIn("message_te", a)
            # Ensure badges don't have mixed slashes
            self.assertNotIn("/", a["badge_en"])
            self.assertNotIn("/", a["badge_te"])

    def test_smart_summary_multilingual_enrichment(self):
        summary = get_user_smart_summary(1)
        if summary.get("latest_crop"):
            self.assertIn("predicted_crop_en", summary["latest_crop"])
            self.assertIn("predicted_crop_te", summary["latest_crop"])
            self.assertIn("predicted_crop_hi", summary["latest_crop"])
        if summary.get("latest_yield"):
            self.assertIn("crop_type_en", summary["latest_yield"])
            self.assertIn("crop_type_te", summary["latest_yield"])
            self.assertIn("crop_type_hi", summary["latest_yield"])

    def test_pages_render_successfully(self):
        routes = ["/", "/crop/recommend", "/notifications", "/market", "/disease", "/dashboard", "/weather", "/history", "/farms", "/yield"]
        for r in routes:
            resp = self.client.get(r, follow_redirects=True)
            self.assertEqual(resp.status_code, 200, f"Route {r} failed with status {resp.status_code}")

if __name__ == "__main__":
    unittest.main()
