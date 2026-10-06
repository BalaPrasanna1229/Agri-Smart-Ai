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

    def test_land_analyzer_and_photo_crop_prediction(self):
        from src.land_analyzer import classify_land_soil_photo, SOIL_SAMPLE_GALLERY
        
        # Test preset classification for all gallery samples
        for sample in SOIL_SAMPLE_GALLERY:
            result = classify_land_soil_photo(preset_id=sample['id'])
            self.assertTrue(result['success'])
            self.assertIn('soil_profile', result)
            self.assertIn('top_3_recommendations', result)
            self.assertIn('top_crop', result)
            self.assertGreaterEqual(len(result['top_3_recommendations']), 1)
            # Verify soil DNA parameters are present
            dna = result['soil_dna']
            self.assertIn('N', dna)
            self.assertIn('P', dna)
            self.assertIn('K', dna)
            self.assertIn('ph', dna)
            # Verify Tamil crop translation is included
            for crop in result['top_3_recommendations']:
                self.assertIn('crop_ta', crop)
                self.assertIn('confidence_pct', crop)

        # Test endpoint /crop/analyze-land with preset (with logged in user)
        with app.test_client() as client:
            client.post('/login', data={
                'login_id': 'advisory_farmer_test',
                'password': 'password123'
            }, follow_redirects=True)
            resp = client.post('/crop/analyze-land', json={'sample_preset_id': 'black_cotton'})
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertTrue(data['success'])
            self.assertEqual(data['soil_profile']['name_en'], 'Deep Black Cotton Soil (Regur / Clayey)')
            self.assertIn('Cotton', [c['crop_en'] for c in data['top_3_recommendations']])

            # Test rejection on non-land image (e.g. leaf or blue sky)
            from PIL import Image
            import numpy as np
            sky_arr = np.zeros((200, 200, 3), dtype=np.uint8)
            sky_arr[:, :] = [80, 160, 245]
            sky_res = classify_land_soil_photo(image_input=Image.fromarray(sky_arr))
            self.assertFalse(sky_res['success'], "Non-soil sky photo should be rejected")
            self.assertFalse(sky_res['is_valid_land'])
            self.assertIn('message_te', sky_res)

            # Test plant leaf rejection on land scanner
            leaf_arr = np.zeros((200, 200, 3), dtype=np.uint8)
            leaf_arr[:, :] = [35, 140, 45]
            leaf_res = classify_land_soil_photo(image_input=Image.fromarray(leaf_arr))
            self.assertFalse(leaf_res['success'], "Plant leaf photo should be rejected on Land Scanner")
            self.assertEqual(leaf_res['reason_code'], 'plant_leaf_photo')

    def test_tamil_multilingual_coverage(self):
        from src.integrated_advisory import CROP_NAME_TRANSLATIONS
        from src.disease_lookup import MULTILINGUAL_PLANTS
        from src.ai_assistant import _generate_local_agronomist_response

        # Verify all crops have Tamil translation
        for crop_key, trans in CROP_NAME_TRANSLATIONS.items():
            self.assertIn('ta', trans, f"Crop {crop_key} is missing Tamil translation")
            self.assertTrue(len(trans['ta']) > 0)

        # Verify plants have Tamil translation
        for plant_key, trans in MULTILINGUAL_PLANTS.items():
            self.assertIn('ta', trans, f"Plant {plant_key} is missing Tamil translation")
            self.assertTrue(len(trans['ta']) > 0)

        # Verify AI Assistant handles Tamil queries with user_id
        with app.app_context():
            tamil_reply = _generate_local_agronomist_response(
                user_id=1,
                user_message="கரும்பில் பூச்சி தாக்குதல் மற்றும் உர மேலாண்மை பற்றி கூறுங்கள்"
            )
            self.assertTrue(len(tamil_reply) > 20)
            # Check Tamil unicode range exists in reply
            has_tamil = any(0x0B80 <= ord(c) <= 0x0BFF for c in tamil_reply)
            self.assertTrue(has_tamil, "AI response should contain Tamil characters")
            print("\n[+] Verification successful: Tamil multilingual coverage and Land photo ML predictions 100% verified!")

    def test_plant_leaf_validation_and_rejection(self):
        from src.disease_lookup import get_disease_lookup
        from PIL import Image
        import numpy as np

        lookup = get_disease_lookup()

        # 1. Non-plant image tests:
        # A. Barren land / desert image (brown sand)
        sand_arr = np.zeros((224, 224, 3), dtype=np.uint8)
        sand_arr[:, :] = [185, 125, 75]
        sand_img = Image.fromarray(sand_arr)
        res_sand = lookup.predict_disease_from_image(sand_img, filename="barren_field.jpg")
        self.assertFalse(res_sand["is_valid_plant"], "Barren soil image should be rejected")
        self.assertEqual(res_sand["status"], "rejected")
        self.assertIn("message_te", res_sand)

        # B. Blue sky / ocean image
        sky_arr = np.zeros((224, 224, 3), dtype=np.uint8)
        sky_arr[:, :] = [80, 160, 240]
        sky_img = Image.fromarray(sky_arr)
        res_sky = lookup.predict_disease_from_image(sky_img, filename="blue_sky.jpg")
        self.assertFalse(res_sky["is_valid_plant"], "Sky image should be rejected")

        # C. Human selfie / skin tone
        skin_arr = np.zeros((224, 224, 3), dtype=np.uint8)
        skin_arr[:, :] = [230, 180, 150]
        skin_img = Image.fromarray(skin_arr)
        res_skin = lookup.predict_disease_from_image(skin_img, filename="selfie.jpg")
        self.assertFalse(res_skin["is_valid_plant"], "Selfie image should be rejected")

        # 2. Genuine plant leaf tests:
        # A. Green plant leaf
        leaf_arr = np.zeros((224, 224, 3), dtype=np.uint8)
        leaf_arr[:, :] = [40, 140, 50]
        leaf_img = Image.fromarray(leaf_arr)
        res_leaf = lookup.predict_disease_from_image(leaf_img, filename="healthy_crop.jpg")
        self.assertTrue(res_leaf["is_valid_plant"], "Green leaf photo should be accepted as plant")
        self.assertTrue(res_leaf.get("is_prediction", False))
        self.assertGreater(res_leaf.get("confidence_pct", 0), 80.0)

        # B. Diseased tomato leaf photo
        tomato_leaf = np.zeros((224, 224, 3), dtype=np.uint8)
        tomato_leaf[:, :] = [45, 130, 50] # green base
        tomato_leaf[60:160, 60:160] = [130, 90, 40] # blight lesions
        tomato_img = Image.fromarray(tomato_leaf)
        res_tomato = lookup.predict_disease_from_image(tomato_img, filename="tomato_leaf_sample.jpg")
        self.assertTrue(res_tomato["is_valid_plant"], "Tomato leaf sample should be diagnosed")
        self.assertIn("Tomato", res_tomato["plant_name"])
        print("\n[+] Verification successful: Plant Leaf Quality Validation and Non-Plant Rejection 100% verified!")

    def test_out_of_domain_query_rejection(self):
        from src.ai_assistant import is_agricultural_query, generate_assistant_response, _generate_local_agronomist_response

        # Non-agricultural queries MUST be recognized as False
        self.assertFalse(is_agricultural_query("who is nitisha"))
        self.assertFalse(is_agricultural_query("tell me a joke"))
        self.assertFalse(is_agricultural_query("who is the president"))
        self.assertFalse(is_agricultural_query("what is quantum computing"))

        # Agricultural queries MUST be recognized as True
        self.assertTrue(is_agricultural_query("watermelon cultivation guide"))
        self.assertTrue(is_agricultural_query("వరి సాగు విధానం"))
        self.assertTrue(is_agricultural_query("tomato pest control"))
        self.assertTrue(is_agricultural_query("who are you"))
        self.assertTrue(is_agricultural_query("hi"))

        with app.app_context():
            # Test English refusal
            refusal_en = _generate_local_agronomist_response(user_id=1, user_message="who is nitisha")
            self.assertIn("only assist with agricultural and farming queries", refusal_en)

            # Test Telugu refusal
            refusal_te = _generate_local_agronomist_response(user_id=1, user_message="నితీషా ఎవరు")
            self.assertIn("వ్యవసాయేతర", refusal_te)

            # Test full API entry point
            resp = generate_assistant_response(user_id=1, user_message="who is nitisha")
            self.assertTrue(resp["success"])
            self.assertIn("only assist with agricultural and farming queries", resp["message"])
            print("\n[+] Verification successful: Out-of-domain query boundary refusal 100% verified!")

if __name__ == '__main__':
    unittest.main()



