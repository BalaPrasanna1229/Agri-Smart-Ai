# 🌾 Agri Smart AI — Precision Agriculture Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-35%2F35%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

**Agri Smart AI** is a production-ready, full-stack precision agriculture web application and decision-support system. It integrates machine learning classifiers and regressors, agronomic plant pathology databases, 5-year agro-meteorological analytics, historical mandi market bulletins, and an interactive context-aware AI Agronomist Assistant.

---

## 📑 Table of Contents

1. [Key Modules & Capabilities](#-key-modules--capabilities)
2. [Technology Stack](#-technology-stack)
3. [Repository Architecture](#-repository-architecture)
4. [Agricultural Datasets & ML Models](#-agricultural-datasets--ml-models)
5. [Installation & Setup](#-installation--setup)
6. [Environment Configuration](#-environment-configuration)
7. [Running the Application](#-running-the-application)
8. [Automated Test Suite](#-automated-test-suite)
9. [Production Deployment](#-production-deployment)
10. [Data Privacy & Safety Principles](#-data-privacy--safety-principles)
11. [Dataset Limitations & Future Roadmap](#-dataset-limitations--future-roadmap)

---

## 🌟 Key Modules & Capabilities

### 1. 🌱 Soil-to-Crop Recommendation Engine (`/crop/recommend`)
* **ML Model:** Random Forest Classifier (`StandardScaler + RandomForestClassifier(n_estimators=100)`) with **99.55% test accuracy**.
* **Features:** Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$), Soil pH, Temperature (°C), Humidity (%), and Rainfall (mm).
* **Output:** Optimal recommended crop, confidence score (%), top-3 suitability breakdown, and soil test summary table.
* **Farm Profile Linkage:** Automatically binds soil queries to registered farm holdings.
* **History Log (`/crop/history`):** Complete user-isolated recommendation history.

### 2. 🏡 Farm Parcel Management (`/farms`)
* **Full CRUD Lifecycle:** Add (`/farm/add`), Edit (`/farm/edit/<id>`), and Delete (`/farm/delete/<id>`).
* **Profile Attributes:** Farm name, location, district, state, land area (acres), soil type, irrigation system, previous crop, current crop, and agronomic notes.
* **Strict Isolation:** User data is strictly segregated by authenticated `user_id`.

### 3. 🦠 Plant Pathology & Disease Information (`/disease`)
* **Ontology:** 38 distinct condition classes across 14 plant species from `plant_disease_dataset (1).csv.xls`.
* **Pathology Diagnostic Cards:**
  * Pathogen type & biological cause (Fungal, Bacterial, Viral, Pest, Healthy).
  * Field symptoms & visual identifiers.
  * 🌿 **Organic Remedies** (Neem oil, copper fungicides, bio-agents, Bordeaux mixture).
  * 🧪 **Chemical Controls** (Mancozeb, Azoxystrobin, Difenoconazole, etc.).
  * 🛡️ **Cultural & Preventive Practices** (Crop rotation, sanitation, drip irrigation).
* **Architecture-Ready Leaf Upload:** Honest diagnostic scanner that validates image formats while clearly stating image model readiness.

### 4. 🌦️ Agro-Meteorological Analytics & Advisory (`/weather`)
* **Dataset:** 1,780 daily meteorological records from `weather_dataset.csv.xls` (Jan 2021 to Dec 2025) for Kakinada, Andhra Pradesh.
* **Agro-Meteorological Advisories:**
  * 💨 **Chemical Spray Window:** Evaluates wind drift (>20 km/h) and rainfall wash-off risks.
  * 💧 **Irrigation Strategy:** Computes precipitation surplus vs. high evapotranspiration demand.
  * 🦠 **Fungal Disease Warning:** Evaluates high humidity ($\ge 80\%$) and warm temperature ($\ge 23\text{°C}$) risk periods.
* **Interactive Visualizations (Chart.js):** Temperature cycles (Mean, Min, Max), monthly rainfall volume, and relative humidity trends.
* **Live Weather Fallback:** Seamlessly connects to OpenWeatherMap when `WEATHER_API_KEY` is configured, or defaults to historical data with a clear notification.

### 5. 🌾 Farm Harvest Yield Prediction (`/yield`)
* **ML Model:** Scikit-Learn Regression Pipeline (`ColumnTransformer(OneHotEncoder, StandardScaler) + RandomForestRegressor(n_estimators=100)`).
* **8 Input Features:** `Crop_Type`, `Farm_Area(acres)`, `Soil_Type`, `Irrigation_Type`, `Season`, `Fertilizer_Used(tons)`, `Pesticide_Used(kg)`, `Water_Usage(cubic meters)`.
* **Output:** Estimated harvest yield (`tons`) and yield density (`tons/acre`).
* **⚠️ Small Dataset Notice:** Clearly marks baseline projections with a 50-record dataset reliability notice.
* **History Log (`/yield/history`):** Complete simulation history per user.

### 6. 📊 Mandi Market Intelligence Dashboard (`/market`)
* **Dataset:** Official wholesale mandi bulletin from `Market_Wise_Price_Arrival_csv.xls` (recorded 29-Sep to 01-Oct-2026).
* **Market KPIs:** 25 commodities across 6 groups, average market price (Rs./Quintal), total arrival volume in Metric Tonnes (MT), and 3-day price momentum.
* **Govt MSP Comparison:** Tracks commodities trading at a premium or discount relative to the 2026–27 Government Minimum Support Price.
* **Search & Filters:** Real-time commodity search, group filtering (Cereals, Pulses, Oil Seeds, Spices, Commercial, Vegetables), and sorting.
* **Charts (Chart.js):** Market Price vs. Govt MSP comparison and arrival volume breakdowns.

### 7. 🤖 AI Agriculture Assistant & Agronomist (`/assistant`)
* **Conversational Agronomist:** Interactive chat interface designed for precision agriculture guidance.
* **Context-Aware Engine:** Dynamically injects the logged-in farmer's saved holdings, recent soil recommendations, yield projections, disease lookups, and regional weather/mandi data into the LLM system prompt.
* **Provider Support:** Supports Google Gemini (`GEMINI_API_KEY`) and OpenAI (`OPENAI_API_KEY`).
* **Standing-by Notice:** In the absence of an API key, displays: `"AI Assistant is not configured yet. Please add the required API key to enable AI responses."` without fabricating answers.
* **Chat Persistence:** Full conversation history in SQLite (`assistant_messages`) with single-click history clear.

### 8. ✨ Smart Dashboard (`/dashboard`)
* Unified farmer cockpit with quick KPIs, latest activity highlight cards, registered farms table, and direct access to all 7 active AI modules.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend & Web Framework** | Python 3.10+, Flask 3.1+, Werkzeug |
| **Machine Learning & Analytics** | Scikit-Learn 1.7+, Pandas 2.3+, NumPy 2.2+, Joblib 1.5+ |
| **Database** | SQLite3 (with foreign key enforcement and connection pooling) |
| **Frontend & UI System** | Semantic HTML5, Vanilla CSS3 (Custom Agriculture Design System), Chart.js 4.4+ |
| **LLM & External APIs** | Google Gemini REST API, OpenAI REST API, OpenWeatherMap API |
| **Production WSGI** | Gunicorn (Linux/macOS) / Waitress (Windows) |
| **Testing** | Python `unittest` (35 Automated Tests, 100% Pass) |

---

## 📁 Repository Architecture

```
Agri Smart AI/
│
├── datasets/                                 # Preserved Raw Datasets (Do NOT modify)
│   ├── Crop_recommendation.csv               # 2,200 soil-climate crop records (22 classes)
│   ├── plant_disease_dataset (1).csv.xls     # 38-class PlantVillage diagnostic ontology
│   ├── weather_dataset.csv.xls               # 1,780 daily meteorological records (2021–2025)
│   ├── yield_dataset.csv.xls                 # 50 farm harvest input/output observations
│   └── Market_Wise_Price_Arrival_csv.xls     # Mandi wholesale bulletin (01-Oct-2026)
│
├── models/                                   # Serialized Scikit-Learn Pipeline Artifacts
│   ├── crop_recommendation_model.pkl         # 99.55% accuracy Random Forest classifier
│   └── yield_prediction_model.pkl            # Multi-feature ColumnTransformer regressor
│
├── src/                                      # Reusable Modular Core
│   ├── __init__.py
│   ├── data_loader.py                        # Unified loader with schema verification
│   ├── preprocessing.py                      # Feature extraction & pipeline constructors
│   ├── crop_recommendation.py                # Crop recommendation inference service
│   ├── yield_prediction.py                   # Harvest yield regression service
│   ├── disease_lookup.py                     # Plant pathology 38-class ontology engine
│   ├── weather_analysis.py                   # Agro-meteorological analytics & live API helper
│   ├── market_analysis.py                    # Mandi price, MSP spread & arrival analytics
│   ├── ai_assistant.py                       # Context-aware LLM agronomist engine
│   └── database.py                           # SQLite schema, user auth, farm CRUD & history
│
├── database/                                 # Database Directory
│   └── agri_smart.db                         # Auto-initialized SQLite database
│
├── templates/                                # Jinja2 HTML Templates
│   ├── base.html                             # Navigation layout & alerts
│   ├── login.html                            # User authentication
│   ├── register.html                         # User registration
│   ├── dashboard.html                        # Main dashboard & smart activity summary
│   ├── coming_soon.html                      # Fallback error / info template
│   ├── farm/                                 # Farm parcel management (list, add, edit)
│   ├── crop/                                 # Crop recommendation (form, result, history)
│   ├── disease/                              # Plant disease search & remedies
│   ├── weather/                              # Weather analytics & advisory charts
│   ├── yield/                                # Harvest yield estimation & history
│   ├── market/                               # Mandi market intelligence dashboard
│   └── assistant/                            # AI Assistant interactive chat
│
├── static/                                   # Frontend Static Assets
│   ├── css/style.css                         # Agriculture-themed design system
│   └── js/main.js                            # UI interaction helpers
│
├── tests/                                    # Test Suite
│   └── run_tests.py                          # 35 Unit, Integration & Web Flow tests
│
├── .env.example                              # Environment configuration template
├── .gitignore                                # Git ignore rules
├── requirements.txt                          # Production Python dependencies
├── app.py                                    # Flask Web Application entry point
└── README.md                                 # Technical documentation
```

---

## 📊 Agricultural Datasets & ML Models

| Dataset File | Module | Shape | Description & ML Model |
| :--- | :--- | :--- | :--- |
| `Crop_recommendation.csv` | Crop Recommendation | 2,200 × 8 | 22 crop classes. Trained with `StandardScaler + RandomForestClassifier`. **Accuracy: 99.55%**. |
| `plant_disease_dataset (1).csv.xls` | Disease Diagnostics | 38 × 6 | 38 PlantVillage crop conditions with pathogen descriptions, symptoms, and organic/chemical controls. |
| `weather_dataset.csv.xls` | Weather Analytics | 1,780 × 6 | Daily observations (2021–2025) for Kakinada, AP: temperature, humidity, rainfall, and wind speed. |
| `yield_dataset.csv.xls` | Yield Prediction | 50 × 10 | 10 crop varieties with acreage, fertilizer, pesticide, and water usage. Trained with `ColumnTransformer + RandomForestRegressor`. |
| `Market_Wise_Price_Arrival_csv.xls` | Market Dashboard | 25 × 9 | Wholesale prices, Government MSP spreads, and daily arrivals for 25 commodities (01-Oct-2026). |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/agri-smart-ai.git
cd agri-smart-ai
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a local `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Configure your environment parameters:
```ini
# Flask Web Server Settings
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secure-random-secret-key-here
PORT=5000
HOST=127.0.0.1

# Optional AI Assistant API Key (Google Gemini or OpenAI)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-flash

# Optional Live Weather API Key (OpenWeatherMap)
WEATHER_API_KEY=your-open-weather-map-key-here
```

---

## 🏃 Running the Application

### Development Server
```bash
python app.py
```
Access the application at **`http://127.0.0.1:5000`**.

### Default Test Account
You can register a new account on the registration page (`/register`) or create one programmatically.

---

## 🧪 Automated Test Suite

Run the full automated test suite containing **35 test cases**:

```bash
python -m unittest tests.run_tests
```

### Test Coverage Summary (35 Tests, 100% Pass Rate):
* **Tests 01–06 (Data Loaders):** Validates all 5 dataset schemas, column datatypes, missing values, and row bounds.
* **Tests 07–11 (ML Pipelines & Services):** Verifies Crop Classifier inference (99.55% accuracy), Yield Regressor pipeline, Disease lookup ontology, Weather analytics, and Mandi price calculations.
* **Tests 12–15 (Authentication & Data Isolation):** Tests registration, secure password hashing, farm CRUD operations, and cross-user data isolation.
* **Tests 16–19 (Web Flow Integration):** Tests unauthenticated redirection, login session management, farm management UI, and crop recommendation history.
* **Tests 20–22 (Disease Module):** Tests 38-class diagnosis retrieval, search filters, and leaf image upload disclaimer.
* **Tests 23–24 (Weather Module):** Tests historical weather filters, farm geographical linkage, and live weather API fallback.
* **Tests 25–27 (Yield Module):** Tests 8-feature harvest regression, input validation, farm auto-fill, and prediction history.
* **Tests 28–29 (Market Module):** Tests historical mandi dashboard banner, KPI cards, MSP charts, keyword search, group filters, and sorting.
* **Tests 30–35 (AI Assistant & Smart Dashboard):** Tests route authentication protection, unconfigured API key handling, multi-source user context aggregation, chat persistence, blank input validation, and smart dashboard activity summary.

---

## 🚢 Production Deployment

### Production WSGI with Gunicorn (Linux / macOS / Cloud VMs)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 60 app:app
```

### Production WSGI with Waitress (Windows Server)
```bash
waitress-serve --port=5000 app:app
```

### Docker Deployment (Dockerfile Blueprint)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## 🛡️ Data Privacy & Safety Principles

1. **User Data Isolation:** All farms, crop recommendations, yield estimations, disease searches, and AI conversations are scoped strictly to the authenticated `user_id`.
2. **Password Security:** Passwords are never stored in plain text; they are hashed using Werkzeug's secure PBKDF2/SHA-256 algorithm.
3. **No Secret Leakage:** `.env` is excluded via `.gitignore`. API keys and credentials are never output to templates, client-side scripts, or logs.
4. **Agricultural Safety:** The AI Assistant follows Integrated Pest Management (IPM) guidelines, advises adherence to official chemical manufacturer labels, and distinguishes statistical ML projections from commercial guarantees.

---

## 📌 Dataset Limitations & Future Roadmap

* **Yield Prediction Sample Size:** The `yield_dataset.csv.xls` contains 50 farm records. The model provides indicative baseline estimates with explicit small-dataset warnings on the UI.
* **Mandi Market Snapshot:** The market dataset is a static bulletin from 01-Oct-2026. Live intraday feeds can be connected via government e-NAM/Agmarknet APIs in future releases.
* **Computer Vision for Disease Detection:** The current disease dataset contains metadata for 38 classes. The leaf upload interface is architectured to integrate a Convolutional Neural Network (CNN) / Vision Transformer (ViT) model once image datasets (e.g. PlantVillage images) are attached.

---

## 📄 License

This project is licensed under the MIT License — feel free to use and adapt it for agricultural research and decision support.
