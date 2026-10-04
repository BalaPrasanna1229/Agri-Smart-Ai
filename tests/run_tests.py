"""
Comprehensive Test Suite for Agri Smart AI — Phase 2 & Phase 3
Verifies:
- Phase 2: All 5 datasets, Scikit-learn pipelines, disease lookup, weather, market analytics
- Phase 3: SQLite database, authentication, user isolation, farm CRUD, crop recommendation web flow, history
"""

import os
import sys
import json
import unittest
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Setup dedicated test database
TEST_DB_PATH = PROJECT_ROOT / "database" / "agri_smart_test.db"
os.environ["AGRI_DB_PATH"] = str(TEST_DB_PATH)

import src.database
src.database.DB_PATH = TEST_DB_PATH

from src.data_loader import (
    load_crop_data,
    load_disease_metadata,
    load_weather_data,
    load_yield_data,
    load_market_data,
    load_all_datasets,
)
from src.preprocessing import (
    get_crop_features_and_target,
    get_yield_features_and_target,
    format_crop_input,
    format_yield_input,
)
from src.crop_recommendation import (
    CropRecommendationModel,
    get_crop_recommender,
    MODEL_PATH as CROP_MODEL_PATH,
)
from src.yield_prediction import (
    YieldPredictionModel,
    get_yield_predictor,
    MODEL_PATH as YIELD_MODEL_PATH,
)
from src.disease_lookup import get_disease_lookup, lookup_disease
from src.weather_analysis import get_weather_analyzer
from src.market_analysis import get_market_analyzer

from src.database import (
    init_db,
    create_user,
    authenticate_user,
    get_user_by_id,
    add_farm,
    get_user_farms,
    get_farm_by_id,
    update_farm,
    delete_farm,
    save_crop_prediction,
    get_user_crop_predictions,
    save_yield_prediction,
    get_user_yield_predictions,
    save_disease_lookup,
    get_user_disease_lookups,
    get_user_dashboard_stats,
)
from app import app


class TestAgriSmartAI(unittest.TestCase):
    """Full Unit and Integration Test Suite."""

    @classmethod
    def setUpClass(cls):
        # Reset test database
        if TEST_DB_PATH.exists():
            TEST_DB_PATH.unlink()
        init_db(TEST_DB_PATH)
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"

    @classmethod
    def tearDownClass(cls):
        # Clean up test database
        if TEST_DB_PATH.exists():
            try:
                TEST_DB_PATH.unlink()
            except Exception:
                pass

    # -------------------------------------------------------------
    # PHASE 2: DATA LOADER TESTS (Tests 1 - 6)
    # -------------------------------------------------------------
    def test_01_load_crop_data(self):
        df = load_crop_data()
        self.assertEqual(df.shape, (2200, 8))
        self.assertListEqual(
            list(df.columns),
            ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"],
        )
        self.assertEqual(df.isnull().sum().sum(), 0)
        self.assertEqual(len(df["label"].unique()), 22)

    def test_02_load_disease_metadata(self):
        df = load_disease_metadata()
        self.assertEqual(df.shape, (38, 6))
        self.assertListEqual(
            list(df.columns),
            ["label_id", "class_name", "plant_name", "disease_or_status", "train_image_count", "split"],
        )
        self.assertEqual(df.isnull().sum().sum(), 0)

    def test_03_load_weather_data(self):
        df = load_weather_data()
        self.assertEqual(df.shape, (1780, 6))
        self.assertListEqual(
            list(df.columns),
            ["date", "location", "temperature", "humidity", "rainfall", "wind_speed"],
        )
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df["date"]))
        self.assertEqual(df.isnull().sum().sum(), 0)

    def test_04_load_yield_data(self):
        df = load_yield_data()
        self.assertEqual(df.shape, (50, 10))
        self.assertIn("Yield(tons)", df.columns)
        self.assertEqual(df.isnull().sum().sum(), 0)

    def test_05_load_market_data(self):
        df = load_market_data()
        self.assertEqual(df.shape, (25, 9))
        self.assertIn("Commodity Group", df.columns)
        self.assertIn("Commodity", df.columns)
        self.assertIn("Price on 01 Oct, 2026", df.columns)

    def test_06_load_all_datasets(self):
        all_ds = load_all_datasets()
        self.assertEqual(len(all_ds), 5)
        for name, d in all_ds.items():
            self.assertIsInstance(d, pd.DataFrame)
            self.assertGreater(len(d), 0)

    # -------------------------------------------------------------
    # PHASE 2: ML PIPELINES & DOMAIN SERVICES (Tests 7 - 11)
    # -------------------------------------------------------------
    def test_07_crop_model_pipeline_and_prediction(self):
        self.assertTrue(CROP_MODEL_PATH.exists())
        recommender = get_crop_recommender()
        self.assertIsNotNone(recommender.pipeline)
        
        sample = {
            "N": 90, "P": 42, "K": 43,
            "temperature": 20.88, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9,
        }
        res = recommender.predict(sample)
        self.assertEqual(res["recommended_crop"], "rice")
        self.assertGreater(res["confidence_pct"], 50.0)
        self.assertEqual(len(res["top_3_recommendations"]), 3)

    def test_08_yield_model_pipeline_and_prediction(self):
        self.assertTrue(YIELD_MODEL_PATH.exists())
        predictor = get_yield_predictor()
        self.assertIsNotNone(predictor.pipeline)
        
        sample = {
            "Crop_Type": "Cotton", "Farm_Area(acres)": 329.4, "Irrigation_Type": "Sprinkler",
            "Fertilizer_Used(tons)": 8.14, "Pesticide_Used(kg)": 2.21, "Soil_Type": "Loamy",
            "Season": "Kharif", "Water_Usage(cubic meters)": 76648.2,
        }
        res = predictor.predict(sample)
        self.assertIn("predicted_yield_tons", res)
        self.assertGreater(res["predicted_yield_tons"], 0)

    def test_09_disease_lookup_service(self):
        lookup = get_disease_lookup()
        card = lookup.format_disease_card("Tomato___Late_blight")
        self.assertTrue(card["found"])
        self.assertEqual(card["plant_name"], "Tomato")
        self.assertEqual(card["disease_name"], "Late blight")

    def test_10_weather_analytics(self):
        weather = get_weather_analyzer()
        stats = weather.get_summary_statistics()
        self.assertEqual(stats["total_records"], 1780)
        advisory = weather.get_agro_advisory(latest_n_days=7)
        self.assertIn("spray_suitability", advisory)

    def test_11_market_analytics(self):
        market = get_market_analyzer()
        summary_table = market.get_summary_table()
        self.assertEqual(len(summary_table), 25)
        msp_comp = market.get_msp_comparison()
        self.assertIn("top_premium_over_msp", msp_comp)

    # -------------------------------------------------------------
    # PHASE 3: AUTHENTICATION & DATABASE TESTS (Tests 12 - 16)
    # -------------------------------------------------------------
    def test_12_user_registration_and_auth(self):
        # Unique user test
        user = create_user("Kiran Patel", "kiran_farmer", "kiran@example.com", "password123")
        self.assertIsNotNone(user["id"])
        self.assertEqual(user["username"], "kiran_farmer")

        # Authenticate with correct credentials
        auth_success = authenticate_user("kiran_farmer", "password123")
        self.assertIsNotNone(auth_success)
        self.assertEqual(auth_success["email"], "kiran@example.com")

        # Authenticate with email
        auth_email = authenticate_user("kiran@example.com", "password123")
        self.assertIsNotNone(auth_email)

        # Wrong password
        auth_fail = authenticate_user("kiran_farmer", "wrongpass")
        self.assertIsNone(auth_fail)

        # Duplicate username prevention
        with self.assertRaises(ValueError):
            create_user("Another User", "kiran_farmer", "another@example.com", "password123")

    def test_13_farm_crud_operations(self):
        user = create_user("Sita Devi", "sita_farm", "sita@example.com", "pass456")
        user_id = user["id"]

        # 1. Add Farm
        farm_id = add_farm(
            user_id=user_id,
            farm_name="Sita Organic Valley",
            location="Guntur",
            state="Andhra Pradesh",
            district="Guntur",
            soil_type="Black",
            land_area=12.5,
            irrigation_type="Drip",
            previous_crop="Cotton",
            current_crop="Chilli",
            description="Organic certified chilli plot",
        )
        self.assertGreater(farm_id, 0)

        # 2. Get User Farms
        farms = get_user_farms(user_id)
        self.assertEqual(len(farms), 1)
        self.assertEqual(farms[0]["farm_name"], "Sita Organic Valley")

        # 3. Update Farm
        updated = update_farm(
            farm_id=farm_id,
            user_id=user_id,
            farm_name="Sita Organic Valley East",
            location="Guntur",
            state="Andhra Pradesh",
            district="Guntur",
            soil_type="Black",
            land_area=15.0,
            irrigation_type="Drip",
        )
        self.assertTrue(updated)
        farm_fetched = get_farm_by_id(farm_id, user_id)
        self.assertEqual(farm_fetched["farm_name"], "Sita Organic Valley East")
        self.assertEqual(farm_fetched["land_area"], 15.0)

        # 4. Delete Farm
        deleted = delete_farm(farm_id, user_id)
        self.assertTrue(deleted)
        self.assertEqual(len(get_user_farms(user_id)), 0)

    def test_14_farm_user_isolation(self):
        user_a = create_user("Farmer A", "farmer_a", "fa@example.com", "pass123")
        user_b = create_user("Farmer B", "farmer_b", "fb@example.com", "pass123")

        farm_a_id = add_farm(
            user_id=user_a["id"],
            farm_name="Plot A",
            location="Loc A",
            state="State A",
            district="Dist A",
            soil_type="Loamy",
            land_area=5.0,
            irrigation_type="Drip",
        )

        # User B should NOT be able to access or edit User A's farm
        farm_for_b = get_farm_by_id(farm_a_id, user_id=user_b["id"])
        self.assertIsNone(farm_for_b)

        edit_attempt = update_farm(
            farm_id=farm_a_id,
            user_id=user_b["id"],
            farm_name="Hacked Plot",
            location="Loc",
            state="State",
            district="Dist",
            soil_type="Clay",
            land_area=10.0,
            irrigation_type="Flood",
        )
        self.assertFalse(edit_attempt)

        delete_attempt = delete_farm(farm_a_id, user_id=user_b["id"])
        self.assertFalse(delete_attempt)

    def test_15_crop_prediction_history_isolation(self):
        user_1 = create_user("User 1", "user1", "u1@example.com", "pass123")
        user_2 = create_user("User 2", "user2", "u2@example.com", "pass123")

        # Save prediction for User 1
        save_crop_prediction(
            user_id=user_1["id"],
            farm_id=None,
            n=90.0, p=42.0, k=43.0,
            temperature=20.88, humidity=82.0, ph=6.5, rainfall=202.9,
            predicted_crop="rice",
            confidence=0.95,
            top_recommendations_json=json.dumps([{"crop": "rice", "confidence": 0.95}]),
        )

        preds_u1 = get_user_crop_predictions(user_1["id"])
        preds_u2 = get_user_crop_predictions(user_2["id"])

        self.assertEqual(len(preds_u1), 1)
        self.assertEqual(preds_u1[0]["predicted_crop"], "rice")
        self.assertEqual(len(preds_u2), 0)

    # -------------------------------------------------------------
    # PHASE 3: FLASK WEB APPLICATION END-TO-END FLOW (Tests 16 - 19)
    # -------------------------------------------------------------
    def test_16_flask_auth_protection(self):
        client = app.test_client()

        # Unauthenticated access to dashboard should redirect to login
        res = client.get("/dashboard", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers["Location"])

        # Unauthenticated access to crop recommend
        res_crop = client.get("/crop/recommend", follow_redirects=False)
        self.assertEqual(res_crop.status_code, 302)
        self.assertIn("/login", res_crop.headers["Location"])

    def test_17_flask_registration_and_login_flow(self):
        client = app.test_client()

        # 1. Register via POST
        reg_res = client.post(
            "/register",
            data={
                "name": "Arjun Varma",
                "username": "arjun_farm",
                "email": "arjun@example.com",
                "password": "secretpassword",
                "confirm_password": "secretpassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b"Registration successful", reg_res.data)

        # 2. Login via POST in session context
        login_res = client.post(
            "/login",
            data={
                "login_id": "arjun_farm",
                "password": "secretpassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b"Welcome back, Arjun Varma", login_res.data)
        self.assertIn(b"Agri Smart AI Platform", login_res.data)

    def test_18_flask_farm_management_flow(self):
        # Create dedicated client with persisted session cookie
        with app.test_client() as client:
            # Login
            client.post("/login", data={"login_id": "arjun_farm", "password": "secretpassword"}, follow_redirects=True)

            # Add Farm via POST
            add_res = client.post(
                "/farm/add",
                data={
                    "farm_name": "Arjun Paddy Fields",
                    "location": "Amalapuram",
                    "state": "Andhra Pradesh",
                    "district": "Konaseema",
                    "soil_type": "Clay",
                    "land_area": "8.5",
                    "irrigation_type": "Flood",
                    "previous_crop": "Paddy",
                    "current_crop": "Rice",
                    "description": "Fertile delta land",
                },
                follow_redirects=True,
            )
            self.assertEqual(add_res.status_code, 200)
            self.assertIn(b"Arjun Paddy Fields", add_res.data)
            self.assertIn(b"added successfully", add_res.data)

            # List Farms
            list_res = client.get("/farms")
            self.assertEqual(list_res.status_code, 200)
            self.assertIn(b"Arjun Paddy Fields", list_res.data)

    def test_19_flask_crop_recommendation_and_history_flow(self):
        # Create dedicated client with persisted session cookie
        with app.test_client() as client:
            # Login
            client.post("/login", data={"login_id": "arjun_farm", "password": "secretpassword"}, follow_redirects=True)

            # Submit Crop Recommendation Form with exact 7 model features
            rec_res = client.post(
                "/crop/recommend",
                data={
                    "N": "90",
                    "P": "42",
                    "K": "43",
                    "temperature": "20.88",
                    "humidity": "82.0",
                    "ph": "6.5",
                    "rainfall": "202.9",
                },
                follow_redirects=True,
            )
            self.assertEqual(rec_res.status_code, 200)
            self.assertIn(b"Optimal Recommended Crop", rec_res.data)
            self.assertIn(b"rice", rec_res.data.lower())
            self.assertIn(b"Crop Recommendation", rec_res.data)

            # View History
            hist_res = client.get("/crop/history")
            self.assertEqual(hist_res.status_code, 200)
            self.assertIn(b"rice", hist_res.data.lower())
            self.assertIn(b"Saved Recommendations", hist_res.data)

    def _create_and_login_user(self, client, username="test_farmer", password="password123"):
        """Helper to create and authenticate a user in the test client."""
        try:
            user = create_user("Test Farmer", username, f"{username}@test.com", password)
            user_id = user["id"]
        except ValueError:
            auth = authenticate_user(username, password)
            user_id = auth["id"]
            
        with client.session_transaction() as sess:
            sess["user_id"] = user_id
            sess["user_name"] = "Test Farmer"
            sess["username"] = username
        return user_id

    # -------------------------------------------------------------
    # PHASE 4: DISEASE INFORMATION & DETECTION TESTS (Tests 20 - 22)
    # -------------------------------------------------------------
    def test_20_flask_disease_page_and_class_select(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "disease_user_1")
            
            # View disease page
            res = client.get("/disease")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Plant Disease", res.data)
            self.assertIn(b"Leaf Photo Scanner", res.data)

            # Select specific class
            res_select = client.get("/disease?selected_class=Tomato___Late_blight")
            self.assertEqual(res_select.status_code, 200)
            self.assertIn(b"Late blight", res_select.data)
            self.assertIn(b"Phytophthora infestans", res_select.data)
            self.assertIn(b"Copper-based fungicides", res_select.data)

    def test_21_flask_disease_search_and_plant_filter(self):
        lookup_engine = get_disease_lookup()
        
        # Keyword search
        search_res = lookup_engine.search("mildew")
        self.assertTrue(len(search_res) > 0)
        self.assertTrue(any("mildew" in x["class_name"].lower() for x in search_res))

        # Plant filter
        plant_res = lookup_engine.get_by_plant_name("Grape")
        self.assertTrue(len(plant_res) > 0)
        self.assertTrue(all("grape" in x["plant_name"].lower() for x in plant_res))

    def test_22_flask_disease_upload_disclaimer(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "disease_user_3")
            
            import io
            dummy_image = (io.BytesIO(b"dummy image bytes"), "test_leaf.png")
            res_upload = client.post(
                "/disease/upload",
                data={"leaf_image": dummy_image},
                content_type="multipart/form-data",
                follow_redirects=True,
            )
            self.assertEqual(res_upload.status_code, 200)
            self.assertIn(b"Tomato", res_upload.data)
            self.assertIn(b"Match", res_upload.data)

    # -------------------------------------------------------------
    # PHASE 4: WEATHER MODULE & LIVE FALLBACK TESTS (Tests 23 - 24)
    # -------------------------------------------------------------
    def test_23_flask_weather_page_and_historical_filters(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "weather_user_1")
            
            # General weather page
            res = client.get("/weather")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Agro-Meteorological", res.data)
            self.assertIn(b"Average Temperature", res.data)
            self.assertIn(b"CHEMICAL SPRAY WINDOW", res.data)

            # Year filter
            res_year = client.get("/weather?year=2023")
            self.assertEqual(res_year.status_code, 200)
            self.assertIn(b'value="2023" selected', res_year.data)

            # Season filter
            res_season = client.get("/weather?season=Kharif")
            self.assertEqual(res_season.status_code, 200)
            self.assertIn(b"Kharif (Monsoon", res_season.data)

    def test_24_flask_weather_farm_integration_and_live_fallback(self):
        with app.test_client() as client:
            uid = self._create_and_login_user(client, "weather_user_2")
            
            # Add a farm for this user
            farm_id = add_farm(
                user_id=uid,
                farm_name="Godavari Green Farm",
                location="Kakinada",
                state="Andhra Pradesh",
                district="East Godavari",
                soil_type="Loamy",
                land_area=10.0,
                irrigation_type="Drip",
            )

            # Weather page with farm filter
            res_farm = client.get(f"/weather?farm_id={farm_id}")
            self.assertEqual(res_farm.status_code, 200)
            self.assertIn(b"Godavari Green Farm", res_farm.data)

            # Weather page fallback message verification
            res = client.get("/weather")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Live weather is not configured", res.data)

            # Verify fetch_live_weather returns proper non-configured dict when no API key
            from src.weather_analysis import fetch_live_weather
            res_live = fetch_live_weather("Kakinada, Andhra Pradesh")
            self.assertFalse(res_live["is_live"])
            self.assertEqual(res_live["status"], "not_configured")

    # -------------------------------------------------------------
    # PHASE 5: YIELD PREDICTION TESTS (Tests 25 - 27)
    # -------------------------------------------------------------
    def test_25_flask_yield_page_and_prediction_submission(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "yield_user_1")

            # 1. GET /yield page loads form and parameters
            res_get = client.get("/yield")
            self.assertEqual(res_get.status_code, 200)
            self.assertIn(b"Harvest Yield Estimation Engine", res_get.data)
            self.assertIn(b"Farm Parameters & Input Data", res_get.data)

            # 2. POST /yield with valid 8 features
            res_post = client.post(
                "/yield",
                data={
                    "Crop_Type": "Cotton",
                    "Farm_Area(acres)": "329.4",
                    "Soil_Type": "Loamy",
                    "Irrigation_Type": "Sprinkler",
                    "Season": "Kharif",
                    "Fertilizer_Used(tons)": "8.14",
                    "Pesticide_Used(kg)": "2.21",
                    "Water_Usage(cubic meters)": "76648.2",
                },
                follow_redirects=True,
            )
            self.assertEqual(res_post.status_code, 200)
            self.assertIn(b"Estimated Harvest Output", res_post.data)
            self.assertIn(b"Tons", res_post.data)
            self.assertIn(b"Yield Density", res_post.data)
            self.assertIn(b"tons/acre", res_post.data)

            # 3. POST /yield with missing required field -> validation error
            res_invalid = client.post(
                "/yield",
                data={
                    "Crop_Type": "Cotton",
                    # Missing Farm_Area(acres)
                    "Soil_Type": "Loamy",
                    "Irrigation_Type": "Sprinkler",
                    "Season": "Kharif",
                    "Fertilizer_Used(tons)": "8.14",
                    "Pesticide_Used(kg)": "2.21",
                    "Water_Usage(cubic meters)": "76648.2",
                },
                follow_redirects=True,
            )
            self.assertEqual(res_invalid.status_code, 200)
            self.assertIn(b"is required", res_invalid.data)

    def test_26_flask_yield_history_and_user_isolation(self):
        # Create User A and User B
        with app.test_client() as client_a:
            uid_a = self._create_and_login_user(client_a, "yield_iso_a")
            # Submit prediction for User A
            client_a.post(
                "/yield",
                data={
                    "Crop_Type": "Tomato",
                    "Farm_Area(acres)": "50.0",
                    "Soil_Type": "Clay",
                    "Irrigation_Type": "Drip",
                    "Season": "Zaid",
                    "Fertilizer_Used(tons)": "3.5",
                    "Pesticide_Used(kg)": "1.2",
                    "Water_Usage(cubic meters)": "30000",
                },
                follow_redirects=True,
            )
            # View User A's history
            hist_a = client_a.get("/yield/history")
            self.assertEqual(hist_a.status_code, 200)
            self.assertIn(b"Tomato", hist_a.data)
            self.assertIn(b"50.0", hist_a.data)
            self.assertIn(b"acres", hist_a.data)

        # User B should NOT see User A's history
        with app.test_client() as client_b:
            self._create_and_login_user(client_b, "yield_iso_b")
            hist_b = client_b.get("/yield/history")
            self.assertEqual(hist_b.status_code, 200)
            self.assertNotIn(b"50.0", hist_b.data)
            self.assertIn(b"No Yield Estimates Found", hist_b.data)

    def test_27_flask_yield_farm_auto_fill(self):
        with app.test_client() as client:
            uid = self._create_and_login_user(client, "yield_farm_user")
            farm_id = add_farm(
                user_id=uid,
                farm_name="Krishna Delta Farms",
                location="Vijayawada",
                state="Andhra Pradesh",
                district="Krishna",
                soil_type="Loamy",
                land_area=45.0,
                irrigation_type="Flood",
            )

            # Submit with linked farm_id
            res = client.post(
                "/yield",
                data={
                    "farm_id": str(farm_id),
                    "Crop_Type": "Sugarcane",
                    "Farm_Area(acres)": "45.0",
                    "Soil_Type": "Loamy",
                    "Irrigation_Type": "Flood",
                    "Season": "Kharif",
                    "Fertilizer_Used(tons)": "4.0",
                    "Pesticide_Used(kg)": "1.0",
                    "Water_Usage(cubic meters)": "60000",
                },
                follow_redirects=True,
            )
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Krishna Delta Farms", res.data)
            self.assertIn(b"Estimated Harvest Output", res.data)

    # -------------------------------------------------------------
    # PHASE 5: MARKET DASHBOARD TESTS (Tests 28 - 29)
    # -------------------------------------------------------------
    def test_28_flask_market_dashboard_page_and_kpis(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "market_user_1")
            res = client.get("/market")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"APMC WHOLESALE MANDI COMMODITY BULLETIN", res.data)
            self.assertIn(b"Agmarknet Benchmark", res.data)
            self.assertIn(b"Commodities Tracked", res.data)
            self.assertIn(b"Average Market Price", res.data)
            self.assertIn(b"priceMspChart", res.data)
            self.assertIn(b"arrivalChart", res.data)
            self.assertIn(b"Mandi Daily Price & Arrival Report Table", res.data)

    def test_29_flask_market_filters_search_and_sorting(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "market_user_2")

            # 1. Search Query
            res_q = client.get("/market?q=Cotton")
            self.assertEqual(res_q.status_code, 200)
            self.assertIn(b"Cotton", res_q.data)

            # 2. Group Filter
            res_grp = client.get("/market?group=Cereals")
            self.assertEqual(res_grp.status_code, 200)
            self.assertIn(b"Cereals", res_grp.data)

            # 3. Sort by Price Ascending
            res_sort_asc = client.get("/market?sort_by=price_asc")
            self.assertEqual(res_sort_asc.status_code, 200)

            # 4. Sort by Arrival Descending
            res_sort_arr = client.get("/market?sort_by=arrival_desc")
            self.assertEqual(res_sort_arr.status_code, 200)

    # -------------------------------------------------------------
    # PHASE 6: AI AGRICULTURE ASSISTANT TESTS (Tests 30 - 35)
    # -------------------------------------------------------------
    def test_30_assistant_auth_protection(self):
        client = app.test_client()
        res = client.get("/assistant", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers["Location"])

    def test_31_assistant_unconfigured_api_key_behavior(self):
        # Ensure API keys are clear in environment
        old_gemini = os.environ.pop("GEMINI_API_KEY", None)
        old_openai = os.environ.pop("OPENAI_API_KEY", None)
        old_ai = os.environ.pop("AI_API_KEY", None)

        try:
            with app.test_client() as client:
                self._create_and_login_user(client, "ai_user_unconfigured")
                
                # 1. GET /assistant displays configuration warning
                res_get = client.get("/assistant")
                self.assertEqual(res_get.status_code, 200)
                self.assertIn(b"AI Assistant Configuration Notice", res_get.data)
                self.assertIn(b"AI Assistant is not configured yet. Please add the required API key to enable AI responses.", res_get.data)

                # 2. POST /assistant/message returns unconfigured message without inventing answers
                res_post = client.post(
                    "/assistant/message",
                    data={"message": "What crop should I grow?"},
                    headers={"X-Requested-With": "XMLHttpRequest", "Accept": "application/json"},
                )
                self.assertEqual(res_post.status_code, 200)
                data = res_post.get_json()
                self.assertFalse(data["is_configured"])
                self.assertEqual(data["status"], "not_configured")
                self.assertEqual(
                    data["message"],
                    "AI Assistant is not configured yet. Please add the required API key to enable AI responses.",
                )
        finally:
            if old_gemini: os.environ["GEMINI_API_KEY"] = old_gemini
            if old_openai: os.environ["OPENAI_API_KEY"] = old_openai
            if old_ai: os.environ["AI_API_KEY"] = old_ai

    def test_32_assistant_user_context_building_and_isolation(self):
        from src.ai_assistant import build_user_agriculture_context

        # Create User 1 with unique farm and predictions
        u1 = create_user("Ramesh Kumar", "ramesh_farmer", "ramesh@example.com", "pass123")
        u1_id = u1["id"]
        farm1_id = add_farm(
            user_id=u1_id,
            farm_name="Ramesh Krishna Delta Plot",
            location="Guntur",
            state="Andhra Pradesh",
            district="Guntur",
            soil_type="Black",
            land_area=25.0,
            irrigation_type="Drip",
            current_crop="Cotton",
        )
        save_crop_prediction(
            user_id=u1_id,
            farm_id=farm1_id,
            n=80.0, p=40.0, k=40.0,
            temperature=25.0, humidity=80.0, ph=6.5, rainfall=150.0,
            predicted_crop="cotton",
            confidence=0.92,
            top_recommendations_json=json.dumps([{"crop": "cotton", "confidence": 0.92}]),
        )

        # Create User 2 with distinct farm
        u2 = create_user("Suresh Sharma", "suresh_farmer", "suresh@example.com", "pass123")
        u2_id = u2["id"]
        add_farm(
            user_id=u2_id,
            farm_name="Suresh Malwa Plateau Plot",
            location="Indore",
            state="Madhya Pradesh",
            district="Indore",
            soil_type="Clay",
            land_area=40.0,
            irrigation_type="Sprinkler",
            current_crop="Soybean",
        )

        # Context for User 1 should include their own farm/crops and NOT User 2's
        ctx1 = build_user_agriculture_context(u1_id)
        self.assertIn("Ramesh Krishna Delta Plot", ctx1)
        self.assertIn("Cotton", ctx1)
        self.assertNotIn("Suresh Malwa Plateau Plot", ctx1)
        self.assertNotIn("Soybean", ctx1)

        # Context for User 2 should include their own farm/crops and NOT User 1's
        ctx2 = build_user_agriculture_context(u2_id)
        self.assertIn("Suresh Malwa Plateau Plot", ctx2)
        self.assertIn("Soybean", ctx2)
        self.assertNotIn("Ramesh Krishna Delta Plot", ctx2)

    def test_33_assistant_chat_history_persistence_and_isolation(self):
        from src.database import (
            save_assistant_message,
            get_user_assistant_messages,
            clear_user_assistant_messages,
        )

        u_alpha = create_user("User Alpha", "user_alpha", "alpha@example.com", "pass123")
        u_beta = create_user("User Beta", "user_beta", "beta@example.com", "pass123")

        save_assistant_message(u_alpha["id"], "user", "Alpha message about soil NPK")
        save_assistant_message(u_alpha["id"], "assistant", "Alpha response regarding nitrogen")

        save_assistant_message(u_beta["id"], "user", "Beta message about irrigation schedule")
        save_assistant_message(u_beta["id"], "assistant", "Beta response regarding drip frequency")

        # Check Alpha sees only Alpha's messages
        msgs_alpha = get_user_assistant_messages(u_alpha["id"])
        self.assertEqual(len(msgs_alpha), 2)
        self.assertIn("Alpha message", msgs_alpha[0]["message"])
        self.assertNotIn("Beta message", msgs_alpha[0]["message"])

        # Check Beta sees only Beta's messages
        msgs_beta = get_user_assistant_messages(u_beta["id"])
        self.assertEqual(len(msgs_beta), 2)
        self.assertIn("Beta message", msgs_beta[0]["message"])

        # Clear Alpha's messages
        clear_user_assistant_messages(u_alpha["id"])
        self.assertEqual(len(get_user_assistant_messages(u_alpha["id"])), 0)
        self.assertEqual(len(get_user_assistant_messages(u_beta["id"])), 2)

    def test_34_assistant_empty_message_validation(self):
        from src.ai_assistant import generate_assistant_response
        u = create_user("User Blank", "user_blank", "blank@example.com", "pass123")
        res = generate_assistant_response(u["id"], "   ")
        self.assertFalse(res["success"])
        self.assertEqual(res["status"], "empty_message")

    def test_35_dashboard_smart_summary_and_assistant_shortcut(self):
        with app.test_client() as client:
            self._create_and_login_user(client, "dashboard_smart_user")
            res = client.get("/dashboard")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Smart Farm Activity Summary", res.data)
            self.assertIn(b"AI Agronomist Assistant", res.data)
            self.assertIn(b"Chat with AI Assistant", res.data)
            self.assertIn(b"/assistant", res.data)

    def test_36_unified_history_page(self):
        with app.test_client() as client:
            user_id = self._create_and_login_user(client, "history_hub_user")
            
            # Save crop prediction
            save_crop_prediction(user_id, None, 90, 42, 43, 20.8, 82.0, 6.5, 202.9, "rice", 0.99, "[]")
            
            # Save yield prediction
            save_yield_prediction(user_id, None, "Wheat", 5.0, "Loamy", "Drip", "Rabi", 1.2, 0.5, 2500.0, 18.5, 3.7)
            
            # Save disease lookup
            save_disease_lookup(user_id, "Tomato___Late_blight", "Late blight", "Tomato", "class_select")

            # Request unified /history
            res = client.get("/history")
            self.assertEqual(res.status_code, 200)
            self.assertIn(b"Unified Farm History", res.data)
            self.assertIn(b"Crop Recommendation History", res.data)
            self.assertIn(b"Yield Simulation History", res.data)
            self.assertIn(b"Disease Lookup", res.data)
            self.assertIn(b"rice", res.data.lower())
            self.assertIn(b"Wheat", res.data)
            self.assertIn(b"Tomato", res.data)


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgriSmartAI)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


