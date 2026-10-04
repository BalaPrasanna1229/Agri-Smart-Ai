import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, init_db

class TestFarmerAdvisoryFeatures(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            init_db()

    def test_crop_recommendation_and_advisory_pillars(self):
        with app.test_client() as client:
            client.post('/register', data={
                'name': 'Advisory Farmer',
                'username': 'advisory_farmer_test',
                'email': 'adv@farmer.com',
                'password': 'password123',
                'confirm_password': 'password123',
                'state': 'Andhra Pradesh',
                'district': 'Guntur',
                'soil_type': 'Loamy Soil',
                'irrigation_type': 'Drip Irrigation',
                'farm_area': '5.0'
            }, follow_redirects=True)

            client.post('/login', data={
                'login_id': 'advisory_farmer_test',
                'password': 'password123'
            }, follow_redirects=True)

            resp = client.post('/crop/recommend', data={
                'N': '90',
                'P': '42',
                'K': '43',
                'ph': '6.5',
                'temperature': '25',
                'humidity': '80',
                'rainfall': '200',
                'soil_type': 'Loamy Soil',
                'irrigation_type': 'Drip Irrigation',
                'farm_area': '5.0',
                'season': 'Kharif'
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)

            # Check all 3 newly requested features in output
            self.assertIn("Pesticide Spray", html)
            self.assertIn("Farmer Land Irrigation", html)
            self.assertIn("Soil-to-Crop Suitability", html)
            self.assertIn("Dosage", html)
            self.assertIn("Water Volume Per Cycle", html)
            self.assertIn("Soil Health", html)
            print("\n[+] Verification successful: Crop Recommendation generated full Pesticide, Irrigation & Soil Suitability advisory!")

if __name__ == '__main__':
    unittest.main()
