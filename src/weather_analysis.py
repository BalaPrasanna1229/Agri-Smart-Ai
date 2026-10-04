"""
Weather Analysis & Agro-Meteorology Module for Agri Smart AI

IMPORTANT NOTICE:
This module performs analytical modeling and trend assessment using the historical
meteorological dataset (weather_dataset.csv.xls: 1,780 daily records from Jan 2021 to Dec 2025).
It does not fabricate live weather data, but provides real historical analytics,
seasonal baselines, and agro-weather advisory triggers.
"""

from typing import Dict, Any, List, Optional, Tuple, Union
import pandas as pd
import numpy as np

from src.data_loader import load_weather_data


class WeatherAnalyzer:
    """
    Provides statistical analytics, time-series trend analysis, and agricultural
    weather advisory metrics for historical meteorological records.
    """

    def __init__(self, df: Optional[pd.DataFrame] = None):
        self.df = df if df is not None else load_weather_data()
        self._prepare_data()

    def _prepare_data(self) -> None:
        """Ensures datetime sorting and feature engineering for time-series analytics."""
        self.df = self.df.sort_values(by="date").reset_index(drop=True)
        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month
        self.df["month_name"] = self.df["date"].dt.strftime("%b")
        self.df["day_of_year"] = self.df["date"].dt.dayofyear
        self.df["season"] = self.df["month"].apply(self._get_indian_season)

    @staticmethod
    def _get_indian_season(month: int) -> str:
        """Maps calendar month to standard Indian agricultural season."""
        if month in [6, 7, 8, 9]:
            return "Kharif (Monsoon)"
        elif month in [10, 11, 12, 1, 2]:
            return "Rabi (Winter)"
        else:
            return "Zaid (Summer)"

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Calculates global statistical summaries across all recorded weather parameters."""
        numeric_cols = ["temperature", "humidity", "rainfall", "wind_speed"]
        stats = self.df[numeric_cols].describe().to_dict()
        
        return {
            "total_records": int(len(self.df)),
            "start_date": self.df["date"].min().strftime("%Y-%m-%d"),
            "end_date": self.df["date"].max().strftime("%Y-%m-%d"),
            "location": str(self.df["location"].iloc[0]),
            "summary_metrics": {
                col: {
                    "mean": round(float(stats[col]["mean"]), 2),
                    "min": round(float(stats[col]["min"]), 2),
                    "max": round(float(stats[col]["max"]), 2),
                    "std": round(float(stats[col]["std"]), 2),
                    "25%": round(float(stats[col]["25%"]), 2),
                    "50%": round(float(stats[col]["50%"]), 2),
                    "75%": round(float(stats[col]["75%"]), 2),
                }
                for col in numeric_cols
            },
            "data_source": "Historical Recorded Weather Dataset (weather_dataset.csv.xls)",
        }

    def filter_by_date_range(
        self, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Filters dataset within a specified ISO date range (YYYY-MM-DD)."""
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        mask = (self.df["date"] >= start) & (self.df["date"] <= end)
        return self.df.loc[mask].copy().reset_index(drop=True)

    def filter_by_location(self, location_query: str) -> pd.DataFrame:
        """Filters dataset by location substring."""
        mask = self.df["location"].str.contains(location_query, case=False, na=False)
        return self.df.loc[mask].copy().reset_index(drop=True)

    def analyze_temperature(self) -> Dict[str, Any]:
        """Computes comprehensive temperature dynamics across seasons and months."""
        monthly_avg = (
            self.df.groupby("month_name", sort=False)["temperature"]
            .agg(["mean", "min", "max", "std"])
            .round(2)
            .to_dict(orient="index")
        )
        seasonal_avg = (
            self.df.groupby("season")["temperature"]
            .agg(["mean", "min", "max"])
            .round(2)
            .to_dict(orient="index")
        )
        hot_days = int((self.df["temperature"] >= 35.0).sum())
        cold_days = int((self.df["temperature"] <= 22.0).sum())

        return {
            "overall_avg_temperature_c": round(float(self.df["temperature"].mean()), 2),
            "hottest_recorded_temp_c": round(float(self.df["temperature"].max()), 2),
            "coldest_recorded_temp_c": round(float(self.df["temperature"].min()), 2),
            "heatwave_days_above_35c": hot_days,
            "cold_days_below_22c": cold_days,
            "monthly_temperature_breakdown": monthly_avg,
            "seasonal_temperature_breakdown": seasonal_avg,
        }

    def analyze_rainfall(self) -> Dict[str, Any]:
        """Analyzes precipitation patterns, monsoonal volume, dry spells, and heavy rain days."""
        total_precip = float(self.df["rainfall"].sum())
        annual_avg_precip = float(self.df.groupby("year")["rainfall"].sum().mean())
        
        heavy_rain_days = int((self.df["rainfall"] >= 20.0).sum())
        torrential_rain_days = int((self.df["rainfall"] >= 50.0).sum())
        dry_days = int((self.df["rainfall"] == 0.0).sum())
        
        monthly_rainfall = (
            self.df.groupby("month_name", sort=False)["rainfall"]
            .agg(["sum", "mean", "max"])
            .round(2)
            .to_dict(orient="index")
        )
        seasonal_rainfall = (
            self.df.groupby("season")["rainfall"]
            .agg(["sum", "mean"])
            .round(2)
            .to_dict(orient="index")
        )

        return {
            "total_recorded_rainfall_mm": round(total_precip, 2),
            "estimated_annual_rainfall_mm": round(annual_avg_precip, 2),
            "heavy_rain_days_gt_20mm": heavy_rain_days,
            "torrential_rain_days_gt_50mm": torrential_rain_days,
            "dry_days_count": dry_days,
            "dry_days_percentage": round((dry_days / len(self.df)) * 100, 2),
            "monthly_rainfall_profile": monthly_rainfall,
            "seasonal_rainfall_profile": seasonal_rainfall,
        }

    def analyze_humidity(self) -> Dict[str, Any]:
        """Evaluates relative humidity patterns and high-humidity fungal risk windows."""
        avg_hum = float(self.df["humidity"].mean())
        high_risk_fungal_days = int(((self.df["humidity"] >= 85.0) & (self.df["temperature"] >= 24.0)).sum())

        monthly_humidity = (
            self.df.groupby("month_name", sort=False)["humidity"]
            .agg(["mean", "min", "max"])
            .round(2)
            .to_dict(orient="index")
        )

        return {
            "average_relative_humidity_pct": round(avg_hum, 2),
            "minimum_recorded_humidity_pct": round(float(self.df["humidity"].min()), 2),
            "maximum_recorded_humidity_pct": round(float(self.df["humidity"].max()), 2),
            "fungal_disease_high_risk_days": high_risk_fungal_days,
            "monthly_humidity_profile": monthly_humidity,
        }

    def analyze_trends(self, window: int = 7) -> pd.DataFrame:
        """
        Calculates moving rolling averages for temperature, rainfall, humidity, and wind.
        Useful for charting trends and visualizing meteorological cycles.
        """
        trends_df = self.df[["date", "location", "temperature", "humidity", "rainfall", "wind_speed"]].copy()
        trends_df[f"temp_rolling_{window}d"] = trends_df["temperature"].rolling(window=window, min_periods=1).mean().round(2)
        trends_df[f"humidity_rolling_{window}d"] = trends_df["humidity"].rolling(window=window, min_periods=1).mean().round(2)
        trends_df[f"rainfall_rolling_{window}d"] = trends_df["rainfall"].rolling(window=window, min_periods=1).sum().round(2)
        trends_df[f"wind_rolling_{window}d"] = trends_df["wind_speed"].rolling(window=window, min_periods=1).mean().round(2)
        return trends_df

    def get_agro_advisory(self, latest_n_days: int = 7) -> Dict[str, Any]:
        """
        Generates practical agro-meteorological advisory rules based on recent window metrics.
        """
        recent = self.df.tail(latest_n_days)
        avg_temp = float(recent["temperature"].mean())
        avg_hum = float(recent["humidity"].mean())
        total_rain = float(recent["rainfall"].sum())
        avg_wind = float(recent["wind_speed"].mean())

        advisories = []
        # Spray conditions
        if avg_wind > 20.0:
            spray_status = "Unfavorable (High wind drift risk > 20 km/h)"
            advisories.append("Avoid pesticide and foliar fertilizer sprays due to high wind drift.")
        elif total_rain > 10.0:
            spray_status = "Unfavorable (Wash-off risk from recent rain)"
            advisories.append("Hold foliar chemical applications until foliage is dry.")
        else:
            spray_status = "Favorable for spraying"
            advisories.append("Ideal atmospheric window for pest/nutrient spraying.")

        # Irrigation recommendation
        if total_rain > 25.0:
            irrigation_status = "Suspend Irrigation"
            advisories.append("Recent rainfall is sufficient. Suspend supplemental irrigation to prevent waterlogging.")
        elif avg_temp > 30.0 and avg_hum < 60.0:
            irrigation_status = "High Irrigation Need"
            advisories.append("High evapotranspiration conditions. Provide light and frequent irrigation.")
        else:
            irrigation_status = "Normal Scheduled Irrigation"
            advisories.append("Maintain standard crop-specific irrigation schedule.")

        # Fungal disease risk
        if avg_hum >= 80.0 and avg_temp >= 23.0:
            disease_risk = "Elevated Fungal / Bacterial Risk"
            advisories.append("High humidity and warm temperatures elevate blight and mildew risks. Scout fields closely.")
        else:
            disease_risk = "Low / Moderate Risk"

        return {
            "analysis_window_days": latest_n_days,
            "window_avg_temperature_c": round(avg_temp, 2),
            "window_avg_humidity_pct": round(avg_hum, 2),
            "window_total_rainfall_mm": round(total_rain, 2),
            "window_avg_wind_speed_kmh": round(avg_wind, 2),
            "spray_suitability": spray_status,
            "irrigation_advice": irrigation_status,
            "disease_risk_alert": disease_risk,
            "actionable_recommendations": advisories,
        }


# Singleton helper
_weather_analyzer_instance: Optional[WeatherAnalyzer] = None

def get_weather_analyzer() -> WeatherAnalyzer:
    """Returns a singleton instance of WeatherAnalyzer."""
    global _weather_analyzer_instance
    if _weather_analyzer_instance is None:
        _weather_analyzer_instance = WeatherAnalyzer()
    return _weather_analyzer_instance


def fetch_live_weather(location_query: str) -> Dict[str, Any]:
    """
    Optional live weather integration.
    Reads WEATHER_API_KEY / OPENWEATHER_API_KEY from environment variables.
    If no API key is provided, returns clear non-configured status.
    """
    import os
    import requests

    api_key = os.environ.get("WEATHER_API_KEY") or os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return {
            "configured": False,
            "status": "not_configured",
            "message": "Live weather is not configured. Showing available historical weather analytics.",
            "is_live": False,
        }

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location_query, "appid": api_key, "units": "metric"}
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "configured": True,
                "status": "success",
                "is_live": True,
                "location": f"{data.get('name', location_query)}, {data.get('sys', {}).get('country', '')}",
                "temperature": round(float(data.get("main", {}).get("temp", 0)), 1),
                "feels_like": round(float(data.get("main", {}).get("feels_like", 0)), 1),
                "humidity": int(data.get("main", {}).get("humidity", 0)),
                "wind_speed": round(float(data.get("wind", {}).get("speed", 0)) * 3.6, 1), # m/s to km/h
                "weather_condition": data.get("weather", [{}])[0].get("description", "Clear").title(),
                "icon": data.get("weather", [{}])[0].get("icon", "01d"),
            }
        else:
            err_data = response.json()
            return {
                "configured": True,
                "status": "error",
                "is_live": False,
                "message": f"Weather API error ({response.status_code}): {err_data.get('message', 'Unable to fetch data')}",
            }
    except Exception as e:
        return {
            "configured": True,
            "status": "error",
            "is_live": False,
            "message": f"Could not connect to live weather service: {str(e)}",
        }


if __name__ == "__main__":
    # Self-test
    analyzer = get_weather_analyzer()
    print("==========================================")
    print("[*] Weather Analysis Module Test")
    print("==========================================")
    
    summary = analyzer.get_summary_statistics()
    print(f"Location: {summary['location']} | Records: {summary['total_records']} | Span: {summary['start_date']} to {summary['end_date']}")
    
    temp_analysis = analyzer.analyze_temperature()
    print(f"\n[+] Temperature Analysis: Avg: {temp_analysis['overall_avg_temperature_c']} C | Max: {temp_analysis['hottest_recorded_temp_c']} C | Min: {temp_analysis['coldest_recorded_temp_c']} C")

    rain_analysis = analyzer.analyze_rainfall()
    print(f"[+] Rainfall Analysis: Total: {rain_analysis['total_recorded_rainfall_mm']} mm | Heavy Rain Days (>20mm): {rain_analysis['heavy_rain_days_gt_20mm']}")

    advisory = analyzer.get_agro_advisory()
    print(f"\n[+] Agro Advisory Trigger:")
    print(f"  - Spray: {advisory['spray_suitability']}")
    print(f"  - Irrigation: {advisory['irrigation_advice']}")
    print(f"  - Disease Alert: {advisory['disease_risk_alert']}")

