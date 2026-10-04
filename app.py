"""
Agri Smart AI - Flask Web Application
Precision Agriculture Intelligence Platform
"""

import os
import json
import functools
from pathlib import Path
from typing import Optional, Dict, Any

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import numpy as np
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
    jsonify,
)

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
    get_user_dashboard_stats,
    save_disease_lookup,
    get_user_disease_lookups,
    save_yield_prediction,
    get_user_yield_predictions,
    save_assistant_message,
    get_user_assistant_messages,
    clear_user_assistant_messages,
    get_user_smart_summary,
    create_user_notification,
    get_user_notifications,
    get_unread_notification_count,
    mark_notification_read,
    mark_all_notifications_read,
    delete_notification,
)
from src.integrated_advisory import (
    generate_comprehensive_farmer_advisory,
    generate_farm_advisory_from_profile,
)
from src.crop_recommendation import get_crop_recommender, CROP_FEATURE_COLS
from src.yield_prediction import (
    get_yield_predictor,
    YIELD_FEATURE_COLS,
    YIELD_NUMERICAL_COLS,
    YIELD_CATEGORICAL_COLS,
)
from src.disease_lookup import get_disease_lookup, lookup_disease, get_crop_diseases_and_precautions
from src.weather_analysis import get_weather_analyzer, fetch_live_weather, WeatherAnalyzer
from src.market_analysis import get_market_analyzer
from src.ai_assistant import generate_assistant_response, get_ai_config, UNCONFIGURED_MESSAGE


# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "agri-smart-ai-production-secret-key-phase3"
)

# Ensure database is initialized on startup
init_db()


# ==========================================
# AUTHENTICATION DECORATOR & CONTEXT
# ==========================================

def login_required(view):
    """Decorator to require login for protected views."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)
    return wrapped_view


@app.context_processor
def inject_user_and_metadata():
    """Injects current user profile, notifications, and route metadata into all templates."""
    current_user = None
    notifications = []
    unread_notif_count = 0
    high_price_alerts = []

    try:
        market_analyzer = get_market_analyzer()
        high_price_alerts = market_analyzer.get_high_price_alerts()
    except Exception:
        high_price_alerts = []

    if "user_id" in session:
        user_id = session["user_id"]
        current_user = get_user_by_id(user_id)
        notifications = get_user_notifications(user_id, limit=8)
        unread_notif_count = get_unread_notification_count(user_id)

        # Auto-seed initial notifications from high price alerts if user has none
        if not notifications and high_price_alerts:
            for alert in high_price_alerts[:3]:
                create_user_notification(
                    user_id=user_id,
                    title=alert["title_en"],
                    message=alert["message_en"],
                    title_te=alert["title_te"],
                    message_te=alert["message_te"],
                    category="market_price",
                    action_url="/market",
                    badge_type="high_price",
                )
            notifications = get_user_notifications(user_id, limit=8)
            unread_notif_count = get_unread_notification_count(user_id)

    return {
        "current_user": current_user,
        "active_endpoint": request.endpoint,
        "notifications": notifications,
        "unread_notif_count": unread_notif_count,
        "high_price_alerts": high_price_alerts,
    }



# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route("/")
def index():
    """Root route: redirects to dashboard if authenticated, else to login."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration Route."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Optional Farm profile parameters
        farm_name = request.form.get("farm_name", "").strip() or f"{name}'s Farm"
        state = request.form.get("state", "").strip() or "Andhra Pradesh"
        district = request.form.get("district", "").strip() or "Guntur"
        location = request.form.get("location", "").strip() or f"{district}, {state}"
        land_area_raw = request.form.get("land_area", "").strip()
        try:
            land_area = float(land_area_raw) if land_area_raw else 5.0
        except ValueError:
            land_area = 5.0
        soil_type = request.form.get("soil_type", "").strip() or "Loamy Soil"
        irrigation_type = request.form.get("irrigation_type", "").strip() or "Drip Irrigation"
        current_crop = request.form.get("current_crop", "").strip() or "Rice"

        # Validation
        if not name or not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html", name=name, username=username, email=email, farm_name=farm_name, land_area=land_area, district=district)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html", name=name, username=username, email=email, farm_name=farm_name, land_area=land_area, district=district)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", name=name, username=username, email=email, farm_name=farm_name, land_area=land_area, district=district)

        try:
            user = create_user(name, username, email, password)
            # Automatically create default primary farm holding for the registered farmer
            try:
                add_farm(
                    user_id=user["id"],
                    farm_name=farm_name,
                    location=location,
                    state=state,
                    district=district,
                    soil_type=soil_type,
                    land_area=land_area,
                    irrigation_type=irrigation_type,
                    current_crop=current_crop,
                    description="Primary registered farm holding",
                )
            except Exception:
                pass

            flash("Registration successful! Your farm profile is ready. Please log in with your credentials.", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("register.html", name=name, username=username, email=email, farm_name=farm_name, land_area=land_area, district=district)
        except Exception as e:
            flash("An unexpected error occurred during registration. Please try again.", "danger")
            return render_template("register.html", name=name, username=username, email=email, farm_name=farm_name, land_area=land_area, district=district)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User Login Route."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        login_id = request.form.get("login_id", "").strip()
        password = request.form.get("password", "")
        next_url = request.args.get("next") or url_for("dashboard")

        if not login_id or not password:
            flash("Please enter both your username/email and password.", "danger")
            return render_template("login.html", login_id=login_id)

        user = authenticate_user(login_id, password)
        if user:
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["username"] = user["username"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(next_url)
        else:
            flash("Invalid username/email or password.", "danger")
            return render_template("login.html", login_id=login_id)

    return render_template("login.html")


@app.route("/logout")
def logout():
    """User Logout Route."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("login"))


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route("/dashboard")
@login_required
def dashboard():
    """Main Agri Smart AI Dashboard with Smart Summary and High Price Alerts."""
    user_id = session["user_id"]
    stats = get_user_dashboard_stats(user_id)
    farms = get_user_farms(user_id)
    recent_predictions = get_user_crop_predictions(user_id, limit=5)
    recent_yield_predictions = get_user_yield_predictions(user_id, limit=5)
    smart_summary = get_user_smart_summary(user_id)
    ai_config = get_ai_config()
    market_analyzer = get_market_analyzer()
    high_price_alerts = market_analyzer.get_high_price_alerts()
    
    return render_template(
        "dashboard.html",
        stats=stats,
        farms=farms,
        recent_predictions=recent_predictions,
        recent_yield_predictions=recent_yield_predictions,
        smart_summary=smart_summary,
        ai_config=ai_config,
        high_price_alerts=high_price_alerts,
    )



# ==========================================
# FARM MANAGEMENT ROUTES
# ==========================================

@app.route("/farms")
@login_required
def farm_list():
    """Lists all farms belonging to the current user."""
    user_id = session["user_id"]
    farms = get_user_farms(user_id)
    return render_template("farm/list.html", farms=farms)


@app.route("/farm/add", methods=["GET", "POST"])
@login_required
def farm_add():
    """Add a new farm."""
    user_id = session["user_id"]

    if request.method == "POST":
        farm_name = request.form.get("farm_name", "").strip()
        location = request.form.get("location", "").strip()
        state = request.form.get("state", "").strip()
        district = request.form.get("district", "").strip()
        soil_type = request.form.get("soil_type", "").strip()
        land_area_raw = request.form.get("land_area", "").strip()
        irrigation_type = request.form.get("irrigation_type", "").strip()
        previous_crop = request.form.get("previous_crop", "").strip()
        current_crop = request.form.get("current_crop", "").strip()
        description = request.form.get("description", "").strip()

        # Validation
        if not farm_name or not location or not state or not district or not soil_type or not land_area_raw or not irrigation_type:
            flash("Please fill in all required farm fields.", "danger")
            return render_template("farm/add.html", form_data=request.form)

        try:
            land_area = float(land_area_raw)
            if land_area <= 0:
                raise ValueError("Land area must be greater than 0.")
        except ValueError:
            flash("Please enter a valid positive number for Land Area (acres).", "danger")
            return render_template("farm/add.html", form_data=request.form)

        try:
            farm_id = add_farm(
                user_id=user_id,
                farm_name=farm_name,
                location=location,
                state=state,
                district=district,
                soil_type=soil_type,
                land_area=land_area,
                irrigation_type=irrigation_type,
                previous_crop=previous_crop,
                current_crop=current_crop,
                description=description,
            )
            action = request.form.get("action", "save")
            if action == "save_and_predict":
                flash(f"✨ Farm '{farm_name}' added successfully! Generating your complete 360° Farm Intelligence Output...", "success")
                return redirect(url_for("farm_advisory_direct", farm_id=farm_id))

            flash(f"Farm '{farm_name}' added successfully!", "success")
            return redirect(url_for("farm_list"))
        except Exception as e:
            flash("Could not save farm details. Please check your inputs.", "danger")
            return render_template("farm/add.html", form_data=request.form)

    return render_template("farm/add.html")


@app.route("/farm/<int:farm_id>/advisory", methods=["GET"])
@login_required
def farm_advisory_direct(farm_id: int):
    """
    1-Click Complete 360° Farm Intelligence Output:
    Directly computes and presents all 8 pillars of agricultural intelligence
    calibrated to the farmer's registered land holdings.
    """
    user_id = session["user_id"]
    farm = get_farm_by_id(farm_id, user_id)
    if not farm:
        flash("Farm holding not found or you do not have permission to view it.", "danger")
        return redirect(url_for("farm_list"))

    try:
        advisory = generate_farm_advisory_from_profile(farm_id, user_id)
        field_labels = {
            "N": "Nitrogen (N)",
            "P": "Phosphorus (P)",
            "K": "Potassium (K)",
            "temperature": "Temperature (°C)",
            "humidity": "Humidity (%)",
            "ph": "Soil pH",
            "rainfall": "Rainfall (mm)",
        }
        flash(
            f"🏡 360° Farm Intelligence Generated for '{farm['farm_name']}' ({farm['land_area']} Acres • {farm['soil_type']} Soil)",
            "success",
        )
        return render_template(
            "crop/result.html",
            advisory=advisory,
            result=advisory["crop_recommendation"],
            inputs=advisory["soil_inputs"],
            field_labels=field_labels,
            farm=farm,
            pred_id=advisory["pred_id"],
        )
    except Exception as e:
        flash(f"Could not generate farm intelligence report: {str(e)}", "danger")
        return redirect(url_for("farm_list"))


@app.route("/farm/edit/<int:farm_id>", methods=["GET", "POST"])
@login_required
def farm_edit(farm_id: int):
    """Edit an existing farm owned by the user."""
    user_id = session["user_id"]
    farm = get_farm_by_id(farm_id, user_id)
    if not farm:
        flash("Farm not found or you do not have permission to edit it.", "danger")
        return redirect(url_for("farm_list"))

    if request.method == "POST":
        farm_name = request.form.get("farm_name", "").strip()
        location = request.form.get("location", "").strip()
        state = request.form.get("state", "").strip()
        district = request.form.get("district", "").strip()
        soil_type = request.form.get("soil_type", "").strip()
        land_area_raw = request.form.get("land_area", "").strip()
        irrigation_type = request.form.get("irrigation_type", "").strip()
        previous_crop = request.form.get("previous_crop", "").strip()
        current_crop = request.form.get("current_crop", "").strip()
        description = request.form.get("description", "").strip()

        if not farm_name or not location or not state or not district or not soil_type or not land_area_raw or not irrigation_type:
            flash("Please fill in all required farm fields.", "danger")
            return render_template("farm/edit.html", farm=farm)

        try:
            land_area = float(land_area_raw)
            if land_area <= 0:
                raise ValueError("Land area must be greater than 0.")
        except ValueError:
            flash("Please enter a valid positive number for Land Area (acres).", "danger")
            return render_template("farm/edit.html", farm=farm)

        success = update_farm(
            farm_id=farm_id,
            user_id=user_id,
            farm_name=farm_name,
            location=location,
            state=state,
            district=district,
            soil_type=soil_type,
            land_area=land_area,
            irrigation_type=irrigation_type,
            previous_crop=previous_crop,
            current_crop=current_crop,
            description=description,
        )

        if success:
            flash(f"Farm '{farm_name}' updated successfully!", "success")
            return redirect(url_for("farm_list"))
        else:
            flash("Failed to update farm details.", "danger")
            return render_template("farm/edit.html", farm=farm)

    return render_template("farm/edit.html", farm=farm)


@app.route("/farm/delete/<int:farm_id>", methods=["POST", "GET"])
@login_required
def farm_delete(farm_id: int):
    """Delete a farm owned by the user."""
    user_id = session["user_id"]
    success = delete_farm(farm_id, user_id)
    if success:
        flash("Farm record deleted successfully.", "success")
    else:
        flash("Could not delete farm. You may not be the owner of this record.", "danger")
    return redirect(url_for("farm_list"))


# ==========================================
# CROP RECOMMENDATION / SMART FARM ADVISORY ROUTES
# ==========================================

@app.route("/advisory", methods=["GET", "POST"])
@app.route("/crop/recommend", methods=["GET", "POST"])
@login_required
def crop_recommend():
    """Crop Recommendation Form and ML Prediction Handler."""
    user_id = session["user_id"]
    farms = get_user_farms(user_id)

    if request.method == "POST":
        farm_id_raw = request.form.get("farm_id", "").strip()
        farm_id = int(farm_id_raw) if farm_id_raw.isdigit() else None
        
        # Selected farm verification (if specified)
        selected_farm = None
        if farm_id:
            selected_farm = get_farm_by_id(farm_id, user_id)

        # 1. Extract & validate 7 exact model features
        raw_inputs = {}
        parsed_inputs = {}
        validation_errors = []

        field_labels = {
            "N": "Nitrogen (N)",
            "P": "Phosphorus (P)",
            "K": "Potassium (K)",
            "temperature": "Temperature (°C)",
            "humidity": "Humidity (%)",
            "ph": "Soil pH",
            "rainfall": "Rainfall (mm)",
        }

        for col in CROP_FEATURE_COLS:
            val = request.form.get(col, "").strip()
            raw_inputs[col] = val
            if not val:
                validation_errors.append(f"{field_labels.get(col, col)} is required.")
                continue
            try:
                numeric_val = float(val)
                # Specific biological/environmental boundary checks
                if col in ["N", "P", "K", "rainfall"] and numeric_val < 0:
                    validation_errors.append(f"{field_labels[col]} cannot be negative.")
                elif col == "humidity" and (numeric_val < 0 or numeric_val > 100):
                    validation_errors.append("Humidity must be between 0% and 100%.")
                elif col == "ph" and (numeric_val < 0 or numeric_val > 14):
                    validation_errors.append("Soil pH must be between 0 and 14.")
                elif col == "temperature" and (numeric_val < -20 or numeric_val > 65):
                    validation_errors.append("Temperature value is out of realistic agricultural range (-20°C to 65°C).")
                else:
                    parsed_inputs[col] = numeric_val
            except ValueError:
                validation_errors.append(f"Invalid numeric value for {field_labels.get(col, col)}.")

        # Optional farm profile inputs for yield & market simulation
        farm_area_raw = request.form.get("farm_area", "").strip()
        farm_area = float(farm_area_raw) if farm_area_raw else (float(selected_farm["land_area"]) if selected_farm else 5.0)
        soil_type = request.form.get("soil_type", "").strip() or (selected_farm["soil_type"] if selected_farm else "Loamy")
        irrigation_type = request.form.get("irrigation_type", "").strip() or (selected_farm["irrigation_type"] if selected_farm else "Drip")
        season = request.form.get("season", "").strip() or "Kharif"

        if validation_errors:
            for err in validation_errors:
                flash(err, "danger")
            return render_template(
                "crop/recommend.html",
                farms=farms,
                form_data=raw_inputs,
                selected_farm_id=farm_id,
            )

        # 2. Invoke Comprehensive 4-Pillar Farmer Advisory Engine
        try:
            advisory = generate_comprehensive_farmer_advisory(
                user_id=user_id,
                soil_inputs=parsed_inputs,
                farm_id=farm_id,
                farm_area=farm_area,
                soil_type=soil_type,
                irrigation_type=irrigation_type,
                season=season,
            )

            rec_crop = advisory["crop_recommendation"]["recommended_crop"].title()
            if advisory["market_economics"].get("is_high_price"):
                flash(
                    f"🔥 మార్కెట్ అలర్ట్: {rec_crop} పంటకు ప్రస్తుతం మార్కెట్లో అధిక ధర లభిస్తోంది! వివరాలు క్రింది నివేదికలో చూడండి.",
                    "success",
                )

            # 3. Render Rich 4-Pillar Result View (Crop, Yield, Disease Precautions, Mandi Prices)
            return render_template(
                "crop/result.html",
                advisory=advisory,
                result=advisory["crop_recommendation"],
                inputs=parsed_inputs,
                field_labels=field_labels,
                farm=selected_farm or advisory.get("farm"),
                pred_id=advisory["pred_id"],
            )

        except Exception as e:
            flash(
                f"An error occurred while generating crop recommendation: {str(e)}",
                "danger",
            )
            return render_template(
                "crop/recommend.html",
                farms=farms,
                form_data=raw_inputs,
                selected_farm_id=farm_id,
            )

    # GET Request: Pre-populate farm parameters if farm_id specified or user has registered farms
    farm_id_raw = request.args.get("farm_id", "").strip()
    selected_farm_id = int(farm_id_raw) if farm_id_raw.isdigit() else None
    selected_farm = None
    form_data = {}

    if selected_farm_id:
        selected_farm = get_farm_by_id(selected_farm_id, user_id)
    elif farms:
        selected_farm = farms[0]
        selected_farm_id = selected_farm["id"]

    if selected_farm:
        s_low = selected_farm["soil_type"].lower()
        if "clay" in s_low or "black" in s_low:
            n, p, k, ph = 88.0, 48.0, 42.0, 7.2
        elif "sand" in s_low:
            n, p, k, ph = 68.0, 38.0, 35.0, 6.4
        elif "red" in s_low:
            n, p, k, ph = 76.0, 34.0, 39.0, 6.3
        else:
            n, p, k, ph = 90.0, 45.0, 44.0, 6.8

        form_data = {
            "N": n, "P": p, "K": k, "ph": ph,
            "temperature": 26.5, "humidity": 78.0, "rainfall": 195.0,
            "farm_area": selected_farm["land_area"],
            "soil_type": selected_farm["soil_type"],
            "irrigation_type": selected_farm["irrigation_type"],
        }

    return render_template(
        "crop/recommend.html",
        farms=farms,
        selected_farm_id=selected_farm_id,
        selected_farm=selected_farm,
        form_data=form_data,
    )



@app.route("/crop/history")
@login_required
def crop_history():
    """Displays user's crop prediction history."""
    user_id = session["user_id"]
    history_records = get_user_crop_predictions(user_id)
    
    # Parse top recommendations JSON for display
    formatted_history = []
    for r in history_records:
        rec = dict(r)
        try:
            rec["top_3"] = json.loads(rec.get("top_recommendations_json") or "[]")
        except Exception:
            rec["top_3"] = []
        rec["confidence_pct"] = round(float(rec.get("confidence", 0.0)) * 100, 1)
        formatted_history.append(rec)

    return render_template("crop/history.html", history=formatted_history)


@app.route("/history")
@login_required
def unified_history():
    """
    Unified Activity & Prediction History Hub:
    Consolidates Crop Recommendations, Yield Harvest Simulations, and Plant Disease Lookups in one single page.
    """
    user_id = session["user_id"]
    farms = get_user_farms(user_id)

    # 1. Crop predictions
    crop_records = get_user_crop_predictions(user_id, limit=100)
    formatted_crop_history = []
    for r in crop_records:
        rec = dict(r)
        try:
            rec["top_3"] = json.loads(rec.get("top_recommendations_json") or "[]")
        except Exception:
            rec["top_3"] = []
        rec["confidence_pct"] = round(float(rec.get("confidence", 0.0)) * 100, 1)
        formatted_crop_history.append(rec)

    # 2. Yield predictions
    yield_history = get_user_yield_predictions(user_id, limit=100)

    # 3. Disease lookups
    disease_history = get_user_disease_lookups(user_id, limit=100)

    return render_template(
        "history.html",
        crop_history=formatted_crop_history,
        yield_history=yield_history,
        disease_history=disease_history,
        farms=farms,
    )


# ==========================================
# DISEASE INFORMATION & DIAGNOSTICS ROUTES
# ==========================================

@app.route("/disease", methods=["GET"])
@login_required
def disease_page():
    """Disease Detection and Metadata Lookup View - Farm Profile Driven."""
    user_id = session["user_id"]
    lookup_engine = get_disease_lookup()
    all_classes = lookup_engine.get_all_classes()
    farms = get_user_farms(user_id)
    
    # Extract farmer's registered crops
    farmer_crop_set = set()
    for f in farms:
        if f.get("current_crop"):
            farmer_crop_set.add(f["current_crop"].strip())
        if f.get("previous_crop"):
            farmer_crop_set.add(f["previous_crop"].strip())

    if farmer_crop_set:
        farmer_crops = sorted(list(farmer_crop_set))
    else:
        farmer_crops = ["Rice", "Cotton", "Tomato", "Maize", "Sugarcane", "Wheat", "Groundnut", "Chilli", "Soybean"]

    # Build crop disease advisories
    crop_advisories = {}
    for crop in farmer_crops:
        crop_advisories[crop] = get_crop_diseases_and_precautions(crop)
    
    query = request.args.get("q", "").strip()
    selected_class_name = request.args.get("selected_class", "").strip()
    plant_filter = request.args.get("plant", "").strip()
    
    selected_disease = None
    search_results = []

    # Case 1: Specific class selected
    if selected_class_name:
        card = lookup_engine.format_disease_card(selected_class_name)
        if card and card.get("found"):
            selected_disease = card
            # Log lookup to user history
            save_disease_lookup(
                user_id=user_id,
                class_name=card["class_name"],
                disease_name=card["disease_name"],
                plant_name=card["plant_name"],
                lookup_type="class_select",
            )
        else:
            flash(f"Disease class '{selected_class_name}' not found.", "warning")

    # Case 2: Plant filter clicked
    elif plant_filter:
        search_results = lookup_engine.get_by_plant_name(plant_filter)
        if not search_results:
            flash(f"No disease records found for plant species '{plant_filter}'.", "info")

    # Case 3: Keyword search query
    elif query:
        search_results = lookup_engine.search(query)
        if len(search_results) == 1:
            card = lookup_engine.format_disease_card(search_results[0]["class_name"])
            if card and card.get("found"):
                selected_disease = card
                save_disease_lookup(
                    user_id=user_id,
                    class_name=card["class_name"],
                    disease_name=card["disease_name"],
                    plant_name=card["plant_name"],
                    lookup_type="search_query",
                )
        elif len(search_results) == 0:
            flash(f"No disease records matched keyword '{query}'.", "warning")

    lookup_history = get_user_disease_lookups(user_id, limit=10)
    sample_gallery = lookup_engine.get_sample_gallery()

    return render_template(
        "disease/index.html",
        all_classes=all_classes,
        selected_disease=selected_disease,
        search_results=search_results,
        query=query,
        plant_filter=plant_filter,
        lookup_history=lookup_history,
        sample_gallery=sample_gallery,
        farms=farms,
        farmer_crops=farmer_crops,
        crop_advisories=crop_advisories,
    )


@app.route("/disease/upload", methods=["POST"])
@login_required
def disease_upload_image():
    """
    Handles leaf image upload and live camera snapshots for disease diagnostics.
    Saves image, runs intelligent botanical diagnosis, and provides full chemical and organic remedies.
    Supports both multipart file uploads and base64 camera snapshot data.
    """
    import time
    import base64
    from werkzeug.utils import secure_filename

    user_id = session["user_id"]
    lookup_engine = get_disease_lookup()
    all_classes = lookup_engine.get_all_classes()
    sample_gallery = lookup_engine.get_sample_gallery()
    farms = get_user_farms(user_id)

    # Extract farmer's registered crops
    farmer_crop_set = set()
    for f in farms:
        if f.get("current_crop"):
            farmer_crop_set.add(f["current_crop"].strip())
        if f.get("previous_crop"):
            farmer_crop_set.add(f["previous_crop"].strip())

    if farmer_crop_set:
        farmer_crops = sorted(list(farmer_crop_set))
    else:
        farmer_crops = ["Rice", "Cotton", "Tomato", "Maize", "Sugarcane", "Wheat", "Groundnut", "Chilli", "Soybean"]

    crop_advisories = {}
    for crop in farmer_crops:
        crop_advisories[crop] = get_crop_diseases_and_precautions(crop)

    upload_dir = Path(app.root_path) / "static" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file = request.files.get("leaf_image")
    camera_base64 = request.form.get("camera_image_base64", "").strip()

    saved_filepath = None
    orig_filename = "leaf_scan.jpg"
    uploaded_image_url = None

    if file and file.filename != "":
        orig_filename = file.filename
        allowed_extensions = {".png", ".jpg", ".jpeg", ".webp"}
        file_ext = Path(orig_filename).suffix.lower()

        if file_ext not in allowed_extensions:
            flash("Invalid image format. Allowed formats: PNG, JPG, JPEG, WEBP.", "danger")
            return redirect(url_for("disease_page"))

        clean_base = secure_filename(Path(orig_filename).stem) or "leaf"
        unique_filename = f"leaf_{int(time.time())}_{clean_base}{file_ext}"
        saved_filepath = upload_dir / unique_filename

        try:
            file.save(str(saved_filepath))
            uploaded_image_url = f"/static/uploads/{unique_filename}"
        except Exception:
            saved_filepath = None

    elif camera_base64:
        try:
            if "," in camera_base64:
                _, b64data = camera_base64.split(",", 1)
            else:
                b64data = camera_base64
            img_bytes = base64.b64decode(b64data)
            unique_filename = f"leaf_cam_{int(time.time())}.jpg"
            saved_filepath = upload_dir / unique_filename
            with open(saved_filepath, "wb") as f:
                f.write(img_bytes)
            orig_filename = "camera_snapshot.jpg"
            uploaded_image_url = f"/static/uploads/{unique_filename}"
        except Exception as e:
            flash(f"Could not process camera image snapshot: {str(e)}", "danger")
            return redirect(url_for("disease_page"))
    else:
        flash("Please choose or capture a valid leaf image before uploading.", "warning")
        return redirect(url_for("disease_page"))

    # Run Intelligent AI Leaf Diagnosis
    if saved_filepath and saved_filepath.exists():
        predicted_card = lookup_engine.predict_disease_from_image(saved_filepath, filename=orig_filename)
    else:
        file.seek(0)
        predicted_card = lookup_engine.predict_disease_from_image(file, filename=orig_filename)

    predicted_card["uploaded_image_url"] = uploaded_image_url

    # Log diagnosis to user history
    save_disease_lookup(
        user_id=user_id,
        class_name=predicted_card["class_name"],
        disease_name=predicted_card["disease_name"],
        plant_name=predicted_card["plant_name"],
        lookup_type="image_upload_scan" if file else "camera_live_scan",
    )

    flash(
        f"✅ ఆకు వ్యాధి విజయవంతంగా గుర్తించబడింది: {predicted_card['plant_name']} — {predicted_card['disease_name']} ({predicted_card.get('confidence_pct', 95.0)}% Match)",
        "success",
    )

    lookup_history = get_user_disease_lookups(user_id, limit=10)

    return render_template(
        "disease/index.html",
        all_classes=all_classes,
        selected_disease=predicted_card,
        search_results=[],
        query="",
        plant_filter="",
        lookup_history=lookup_history,
        sample_gallery=sample_gallery,
        farms=farms,
        farmer_crops=farmer_crops,
        crop_advisories=crop_advisories,
    )


# ==========================================
# WEATHER MODULE ROUTES
# ==========================================

@app.route("/weather", methods=["GET"])
@login_required
def weather_page():
    """Agro-Meteorological Analytics, Historical Trends, and Advisory."""
    user_id = session["user_id"]
    farms = get_user_farms(user_id)

    farm_id_raw = request.args.get("farm_id", "").strip()
    selected_year = request.args.get("year", "").strip()
    selected_season = request.args.get("season", "").strip()

    selected_farm = None
    location_query = "Kakinada, Andhra Pradesh"

    if farm_id_raw.isdigit():
        farm_match = get_farm_by_id(int(farm_id_raw), user_id)
        if farm_match:
            selected_farm = farm_match
            location_query = f"{selected_farm['district']}, {selected_farm['state']}"
    elif farms:
        selected_farm = farms[0]
        location_query = f"{selected_farm['district']}, {selected_farm['state']}"

    # 1. Check optional Live Weather API
    live_weather = fetch_live_weather(location_query)

    # 2. Historical Weather Analytics Engine
    base_analyzer = get_weather_analyzer()
    filtered_df = base_analyzer.df.copy()

    if selected_year and selected_year.isdigit():
        filtered_df = filtered_df[filtered_df["year"] == int(selected_year)]
    if selected_season:
        filtered_df = filtered_df[filtered_df["season"].str.contains(selected_season, case=False, na=False)]

    # Use specialized analyzer on filtered slice if filtered, else global
    active_analyzer = WeatherAnalyzer(df=filtered_df) if len(filtered_df) > 0 else base_analyzer

    summary_stats = active_analyzer.get_summary_statistics()
    temp_analysis = active_analyzer.analyze_temperature()
    rain_analysis = active_analyzer.analyze_rainfall()
    humidity_analysis = active_analyzer.analyze_humidity()
    advisory = active_analyzer.get_agro_advisory(latest_n_days=7)

    # 3. Monthly Chart Data preparation (Jan to Dec averages across the dataset)
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_temp = temp_analysis["monthly_temperature_breakdown"]
    monthly_rain = rain_analysis["monthly_rainfall_profile"]
    monthly_hum = humidity_analysis["monthly_humidity_profile"]

    chart_data = {
        "temp_means": [monthly_temp.get(m, {}).get("mean", 27.0) for m in months_order],
        "temp_mins": [monthly_temp.get(m, {}).get("min", 22.0) for m in months_order],
        "temp_maxs": [monthly_temp.get(m, {}).get("max", 35.0) for m in months_order],
        "rain_sums": [monthly_rain.get(m, {}).get("sum", 0.0) for m in months_order],
        "humidity_means": [monthly_hum.get(m, {}).get("mean", 75.0) for m in months_order],
    }

    return render_template(
        "weather/index.html",
        farms=farms,
        selected_farm=selected_farm,
        selected_year=selected_year,
        selected_season=selected_season,
        live_weather=live_weather,
        summary_stats=summary_stats,
        temp_analysis=temp_analysis,
        rain_analysis=rain_analysis,
        humidity_analysis=humidity_analysis,
        advisory=advisory,
        chart_data=chart_data,
    )



# ==========================================
# YIELD PREDICTION ROUTES
# ==========================================

@app.route("/yield", methods=["GET", "POST"])
@login_required
def yield_page():
    """Farm Crop Yield Estimation and Regression Pipeline Handler."""
    user_id = session["user_id"]
    farms = get_user_farms(user_id)

    if request.method == "POST":
        farm_id_raw = request.form.get("farm_id", "").strip()
        farm_id = int(farm_id_raw) if farm_id_raw.isdigit() else None

        selected_farm = None
        if farm_id:
            selected_farm = get_farm_by_id(farm_id, user_id)

        # 1. Extract & validate 8 exact model features
        # Features: Crop_Type, Farm_Area(acres), Irrigation_Type, Fertilizer_Used(tons),
        #           Pesticide_Used(kg), Soil_Type, Season, Water_Usage(cubic meters)
        raw_inputs = {}
        parsed_inputs = {}
        validation_errors = []

        field_labels = {
            "Crop_Type": "Crop Variety",
            "Farm_Area(acres)": "Farm Land Area (Acres)",
            "Soil_Type": "Soil Type",
            "Irrigation_Type": "Irrigation System",
            "Season": "Agricultural Season",
            "Fertilizer_Used(tons)": "Fertilizer Used (Tons)",
            "Pesticide_Used(kg)": "Pesticide Used (kg)",
            "Water_Usage(cubic meters)": "Water Usage (m³)",
        }

        # Categorical fields validation
        for col in YIELD_CATEGORICAL_COLS:
            val = request.form.get(col, "").strip()
            raw_inputs[col] = val
            if not val:
                validation_errors.append(f"{field_labels.get(col, col)} is required.")
            else:
                parsed_inputs[col] = val

        # Numerical fields validation
        for col in YIELD_NUMERICAL_COLS:
            val = request.form.get(col, "").strip()
            raw_inputs[col] = val
            if not val:
                validation_errors.append(f"{field_labels.get(col, col)} is required.")
                continue
            try:
                numeric_val = float(val)
                if col == "Farm_Area(acres)" and numeric_val <= 0:
                    validation_errors.append("Farm Land Area must be greater than 0.")
                elif col in ["Fertilizer_Used(tons)", "Pesticide_Used(kg)", "Water_Usage(cubic meters)"] and numeric_val < 0:
                    validation_errors.append(f"{field_labels.get(col, col)} cannot be negative.")
                else:
                    parsed_inputs[col] = numeric_val
            except ValueError:
                validation_errors.append(f"Invalid numeric value for {field_labels.get(col, col)}.")

        if validation_errors:
            for err in validation_errors:
                flash(err, "danger")
            return render_template(
                "yield/index.html",
                farms=farms,
                form_data=raw_inputs,
                selected_farm_id=farm_id,
                prediction_result=None,
            )

        # 2. Invoke Saved Machine Learning Pipeline (singleton / cached)
        try:
            predictor = get_yield_predictor()
            prediction_result = predictor.predict(parsed_inputs)

            # 3. Save to database history
            save_yield_prediction(
                user_id=user_id,
                farm_id=farm_id,
                crop_type=str(parsed_inputs["Crop_Type"]),
                farm_area=float(parsed_inputs["Farm_Area(acres)"]),
                soil_type=str(parsed_inputs["Soil_Type"]),
                irrigation_type=str(parsed_inputs["Irrigation_Type"]),
                season=str(parsed_inputs["Season"]),
                fertilizer_used=float(parsed_inputs["Fertilizer_Used(tons)"]),
                pesticide_used=float(parsed_inputs["Pesticide_Used(kg)"]),
                water_usage=float(parsed_inputs["Water_Usage(cubic meters)"]),
                predicted_yield=float(prediction_result["predicted_yield_tons"]),
                yield_per_acre=float(prediction_result["yield_per_acre_tons"]),
            )

            # 4. Render prediction result
            return render_template(
                "yield/index.html",
                farms=farms,
                form_data=raw_inputs,
                selected_farm_id=farm_id,
                selected_farm=selected_farm,
                prediction_result=prediction_result,
            )

        except Exception as e:
            flash(f"An error occurred while calculating harvest yield: {str(e)}", "danger")
            return render_template(
                "yield/index.html",
                farms=farms,
                form_data=raw_inputs,
                selected_farm_id=farm_id,
                prediction_result=None,
            )

    # GET Request: Pre-populate farm parameters if farm_id specified or user has registered farms
    farm_id_raw = request.args.get("farm_id", "").strip()
    selected_farm_id = int(farm_id_raw) if farm_id_raw.isdigit() else None
    selected_farm = None
    form_data = {}

    if selected_farm_id:
        selected_farm = get_farm_by_id(selected_farm_id, user_id)
    elif farms:
        selected_farm = farms[0]
        selected_farm_id = selected_farm["id"]

    if selected_farm:
        area = float(selected_farm["land_area"])
        form_data = {
            "Farm_Area(acres)": area,
            "Soil_Type": selected_farm["soil_type"],
            "Irrigation_Type": selected_farm["irrigation_type"],
            "Crop_Type": selected_farm.get("current_crop") or selected_farm.get("previous_crop") or "Cotton",
            "Season": "Kharif",
            "Fertilizer_Used(tons)": round(area * 0.08, 2),
            "Pesticide_Used(kg)": round(area * 0.45, 2),
            "Water_Usage(cubic meters)": round(area * 250.0, 1),
        }

    return render_template(
        "yield/index.html",
        farms=farms,
        selected_farm_id=selected_farm_id,
        selected_farm=selected_farm,
        form_data=form_data,
        prediction_result=None,
    )


@app.route("/yield/history")
@login_required
def yield_history():
    """Displays user's farm crop yield prediction history log."""
    user_id = session["user_id"]
    history = get_user_yield_predictions(user_id)
    return render_template("yield/history.html", history=history)


# ==========================================
# MARKET DASHBOARD ROUTES
# ==========================================

@app.route("/market", methods=["GET"])
@login_required
def market_page():
    """Mandi Market Dashboard with Historical Prices, MSP Comparison, and Arrival Analytics."""
    analyzer = get_market_analyzer()
    commodity_groups = analyzer.get_commodity_groups()

    search_query = request.args.get("q", "").strip()
    selected_group = request.args.get("group", "").strip()
    sort_by = request.args.get("sort_by", "price_desc").strip()

    # Get data slice
    df = analyzer.df.copy()

    # Filter by commodity group
    if selected_group:
        df = df[df["Commodity Group"].str.contains(selected_group, case=False, na=False)]

    # Filter by keyword search
    if search_query:
        df = df[df["Commodity"].str.contains(search_query, case=False, na=False)]

    # Sort data
    if sort_by == "price_desc":
        df = df.sort_values(by="Price on 01 Oct, 2026", ascending=False, na_position="last")
    elif sort_by == "price_asc":
        df = df.sort_values(by="Price on 01 Oct, 2026", ascending=True, na_position="last")
    elif sort_by == "arrival_desc":
        df = df.sort_values(by="Arrival on 01 Oct, 2026", ascending=False, na_position="last")
    elif sort_by == "name_asc":
        df = df.sort_values(by="Commodity", ascending=True)

    market_items = df.replace({np.nan: None}).to_dict(orient="records")

    # Analytics for KPIs & Charts
    market_stats = analyzer.get_price_statistics()
    msp_analysis = analyzer.get_msp_comparison()
    arrival_analysis = analyzer.get_arrival_analysis()
    trend_analysis = analyzer.get_price_volatility_and_trends()

    # Prepare chart data for Chart.js
    # Chart 1: Price vs MSP (top commodities with both values)
    valid_msp = analyzer.df.dropna(
        subset=["MSP (Rs./Quintal) 2026-27", "Price on 01 Oct, 2026"]
    ).sort_values(by="Price on 01 Oct, 2026", ascending=False).head(7)

    # Chart 2: Top Arrivals
    top_arrivals = analyzer.df.dropna(
        subset=["Arrival on 01 Oct, 2026"]
    ).sort_values(by="Arrival on 01 Oct, 2026", ascending=False).head(6)

    chart_data = {
        "price_msp_labels": valid_msp["Commodity"].tolist(),
        "market_prices": [float(p) for p in valid_msp["Price on 01 Oct, 2026"]],
        "msp_prices": [float(p) for p in valid_msp["MSP (Rs./Quintal) 2026-27"]],
        "arrival_labels": top_arrivals["Commodity"].tolist(),
        "arrival_values": [float(v) for v in top_arrivals["Arrival on 01 Oct, 2026"]],
    }

    top_insights = analyzer.get_top_insights()
    all_commodities_data = analyzer.get_summary_table()

    user_id = session["user_id"]
    farms = get_user_farms(user_id)

    return render_template(
        "market/index.html",
        farms=farms,
        market_items=market_items,
        commodity_groups=commodity_groups,
        selected_group=selected_group,
        search_query=search_query,
        sort_by=sort_by,
        market_stats=market_stats,
        msp_analysis=msp_analysis,
        arrival_analysis=arrival_analysis,
        trend_analysis=trend_analysis,
        top_insights=top_insights,
        all_commodities_data=all_commodities_data,
        chart_data=chart_data,
    )


# ==========================================
# NOTIFICATION SYSTEM ROUTES
# ==========================================

@app.route("/notifications", methods=["GET"])
@login_required
def notifications_page():
    """Full notifications center showing high price alerts and disease advisories."""
    user_id = session["user_id"]
    notifications = get_user_notifications(user_id, limit=50)
    market_analyzer = get_market_analyzer()
    high_price_alerts = market_analyzer.get_high_price_alerts()
    
    return render_template(
        "notifications.html",
        notifications=notifications,
        high_price_alerts=high_price_alerts,
    )


@app.route("/api/notifications", methods=["GET"])
@login_required
def api_notifications():
    """JSON API for real-time notification bell dropdown."""
    user_id = session["user_id"]
    notifications = get_user_notifications(user_id, limit=10)
    unread_count = get_unread_notification_count(user_id)
    return jsonify({
        "success": True,
        "unread_count": unread_count,
        "notifications": notifications,
    })


@app.route("/notifications/read/<int:notif_id>", methods=["POST", "GET"])
@login_required
def mark_single_notification_read(notif_id: int):
    """Marks a single notification as read."""
    user_id = session["user_id"]
    mark_notification_read(notif_id, user_id)
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True})
    next_url = request.args.get("next") or request.referrer or url_for("dashboard")
    return redirect(next_url)


@app.route("/notifications/read-all", methods=["POST", "GET"])
@login_required
def mark_all_user_notifications_read():
    """Marks all notifications as read for current user."""
    user_id = session["user_id"]
    mark_all_notifications_read(user_id)
    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"success": True})
    flash("All notifications marked as read.", "info")
    next_url = request.args.get("next") or request.referrer or url_for("dashboard")
    return redirect(next_url)


# ==========================================
# AI AGRICULTURE ASSISTANT ROUTES (PHASE 6)
# ==========================================


@app.route("/assistant", methods=["GET"])
@login_required
def assistant_page():
    """AI Agriculture Assistant Chat Interface."""
    user_id = session["user_id"]
    ai_config = get_ai_config()
    messages = get_user_assistant_messages(user_id, limit=50)

    # Load user context overview
    user_farms = get_user_farms(user_id)
    user_crop_preds = get_user_crop_predictions(user_id, limit=5)
    user_yield_preds = get_user_yield_predictions(user_id, limit=5)

    return render_template(
        "assistant/index.html",
        ai_config=ai_config,
        messages=messages,
        user_farms=user_farms,
        user_crop_preds=user_crop_preds,
        user_yield_preds=user_yield_preds,
    )


@app.route("/ai-assistant", methods=["GET"])
@login_required
def ai_assistant_redirect():
    """Legacy alias redirect to /assistant."""
    return redirect(url_for("assistant_page"))


@app.route("/assistant/message", methods=["POST"])
@login_required
def assistant_send_message():
    """Processes user chat message and returns AI Agronomist response."""
    user_id = session["user_id"]

    # Support JSON payload or Form data
    if request.is_json:
        req_data = request.get_json() or {}
        user_msg = req_data.get("message", "").strip()
    else:
        user_msg = request.form.get("message", "").strip()

    result = generate_assistant_response(user_id=user_id, user_message=user_msg)

    # Return JSON for AJAX requests or when requested
    is_ajax = (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or "application/json" in request.headers.get("Accept", "")
    )

    if is_ajax:
        return jsonify(result), (200 if result.get("success") or result.get("status") == "not_configured" else 400)

    if not result.get("success") and result.get("status") != "not_configured":
        flash(result.get("message", "An error occurred."), "warning")

    return redirect(url_for("assistant_page"))


@app.route("/assistant/clear", methods=["POST"])
@login_required
def assistant_clear():
    """Clears assistant chat history for the authenticated user."""
    user_id = session["user_id"]
    clear_user_assistant_messages(user_id)
    flash("Your conversation history has been cleared.", "info")
    return redirect(url_for("assistant_page"))


@app.route("/assistant/set-key", methods=["POST"])
@login_required
def assistant_set_key():
    """Sets AI Assistant API key in environment and updates .env file."""
    api_key = request.form.get("api_key", "").strip()
    provider = request.form.get("provider", "gemini").strip().lower()

    if provider == "builtin":
        api_key = "builtin_agri_intelligence"

    if not api_key:
        flash("Please provide a valid API key.", "danger")
        return redirect(url_for("assistant_page"))

    if provider == "openai":
        os.environ["OPENAI_API_KEY"] = api_key
        key_var = "OPENAI_API_KEY"
    else:
        os.environ["GEMINI_API_KEY"] = api_key
        key_var = "GEMINI_API_KEY"

    # Persist to .env file in workspace root
    base_dir = Path(__file__).resolve().parent
    env_path = base_dir / ".env"
    try:
        env_lines = []
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                env_lines = f.readlines()

        # Update or append key
        key_found = False
        new_lines = []
        for line in env_lines:
            if line.startswith(f"{key_var}="):
                new_lines.append(f"{key_var}={api_key}\n")
                key_found = True
            else:
                new_lines.append(line)

        if not key_found:
            new_lines.append(f"\n{key_var}={api_key}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"Warning: Could not write to .env: {e}")

    if provider == "builtin":
        flash("✨ Built-in ICAR Agronomist Engine activated! 100% Free & Offline ready.", "success")
    else:
        flash(f"✨ AI Assistant activated successfully with {provider.title()} API! You can now ask any agricultural questions.", "success")
    return redirect(url_for("assistant_page"))


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("coming_soon.html", module_name="Page Not Found (404)", module_icon="🔍", module_phase="Error", description="The requested page could not be located."), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("coming_soon.html", module_name="Internal Server Error (500)", module_icon="⚠️", module_phase="Error", description="An unexpected error occurred. Please return to the dashboard."), 500


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1").lower() in ("1", "true")
    print(f"[*] Starting Agri Smart AI Web Server on http://{host}:{port} (Debug={debug})")
    app.run(host=host, port=port, debug=debug)
