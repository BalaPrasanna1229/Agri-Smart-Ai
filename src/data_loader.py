"""
Data Loader Module for Agri Smart AI
Loads and validates datasets from the dataset directory.
Supports both 'datasets' and 'dataset' directories transparently.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd
import numpy as np


# Determine base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Candidate dataset folders
DATASET_DIRS = [
    BASE_DIR / "datasets",
    BASE_DIR / "dataset",
]


def get_dataset_dir() -> Path:
    """Finds the existing dataset directory."""
    for d in DATASET_DIRS:
        if d.exists() and d.is_dir():
            return d
    raise FileNotFoundError(
        f"Dataset directory not found. Checked: {[str(d) for d in DATASET_DIRS]}"
    )


def get_dataset_path(filename: str) -> Path:
    """Returns absolute path to a given dataset file."""
    dataset_dir = get_dataset_dir()
    filepath = dataset_dir / filename
    if not filepath.exists():
        raise FileNotFoundError(f"File not found in dataset folder: {filepath}")
    return filepath


def load_crop_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads Crop Recommendation dataset (Crop_recommendation.csv).
    Columns: N, P, K, temperature, humidity, ph, rainfall, label
    """
    if filepath is None:
        filepath = get_dataset_path("Crop_recommendation.csv")
    
    df = pd.read_csv(filepath)
    # Ensure expected columns are present
    expected_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "label"]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column '{col}' in Crop Recommendation dataset.")
    
    # Clean types
    numeric_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["label"] = df["label"].astype(str).str.strip().str.lower()
    
    return df


def load_disease_metadata(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads Plant Disease metadata dataset (plant_disease_dataset (1).csv.xls).
    Note: Contains 38 PlantVillage metadata classes, NOT raw image tensors.
    Columns: label_id, class_name, plant_name, disease_or_status, train_image_count, split
    """
    if filepath is None:
        filepath = get_dataset_path("plant_disease_dataset (1).csv.xls")
    
    # The file has UTF-8 BOM encoding and standard CSV format despite .xls extension
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    
    expected_cols = ["label_id", "class_name", "plant_name", "disease_or_status", "train_image_count", "split"]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column '{col}' in Disease metadata dataset.")
            
    df["label_id"] = pd.to_numeric(df["label_id"], errors="coerce").astype(int)
    df["train_image_count"] = pd.to_numeric(df["train_image_count"], errors="coerce").astype(int)
    for str_col in ["class_name", "plant_name", "disease_or_status", "split"]:
        df[str_col] = df[str_col].astype(str).str.strip()
        
    return df


def load_weather_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads Weather dataset (weather_dataset.csv.xls).
    Columns: date, location, temperature, humidity, rainfall, wind_speed
    """
    if filepath is None:
        filepath = get_dataset_path("weather_dataset.csv.xls")
        
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    expected_cols = ["date", "location", "temperature", "humidity", "rainfall", "wind_speed"]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column '{col}' in Weather dataset.")
            
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["location"] = df["location"].astype(str).str.strip()
    for col in ["temperature", "humidity", "rainfall", "wind_speed"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    # Sort chronologically
    df = df.sort_values(by="date").reset_index(drop=True)
    return df


def load_yield_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads Yield Prediction dataset (yield_dataset.csv.xls).
    Columns: Farm_ID, Crop_Type, Farm_Area(acres), Irrigation_Type, Fertilizer_Used(tons),
             Pesticide_Used(kg), Yield(tons), Soil_Type, Season, Water_Usage(cubic meters)
    Note: Contains 50 farm records (small sample size).
    """
    if filepath is None:
        filepath = get_dataset_path("yield_dataset.csv.xls")
        
    df = pd.read_csv(filepath, encoding="utf-8-sig")
    expected_cols = [
        "Farm_ID", "Crop_Type", "Farm_Area(acres)", "Irrigation_Type",
        "Fertilizer_Used(tons)", "Pesticide_Used(kg)", "Yield(tons)",
        "Soil_Type", "Season", "Water_Usage(cubic meters)"
    ]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column '{col}' in Yield dataset.")
            
    # Clean types
    numeric_cols = [
        "Farm_Area(acres)", "Fertilizer_Used(tons)", "Pesticide_Used(kg)",
        "Yield(tons)", "Water_Usage(cubic meters)"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        
    string_cols = ["Farm_ID", "Crop_Type", "Irrigation_Type", "Soil_Type", "Season"]
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
        
    return df


def load_market_data(filepath: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Loads Market Price & Arrival dataset (Market_Wise_Price_Arrival_csv.xls).
    Note: Static mandi snapshot (01 Oct 2026 report). First 2 rows are title metadata.
    Columns: Commodity Group, Commodity, MSP (Rs./Quintal) 2026-27, Price on 01 Oct, 2026,
             Price on 30 Sep, 2026, Price on 29 Sep, 2026, Arrival on 01 Oct, 2026,
             Arrival on 30 Sep, 2026, Arrival on 29 Sep, 2026
    """
    if filepath is None:
        filepath = get_dataset_path("Market_Wise_Price_Arrival_csv.xls")
        
    # The file has 2 title header rows, data begins at row index 2 (skiprows=2)
    df = pd.read_csv(filepath, skiprows=2, encoding="utf-8-sig")
    
    # Strip whitespace from column names
    df.columns = [col.strip() for col in df.columns]
    
    # Convert string '-' or spaces to NaN, then parse numeric columns
    numeric_cols = [
        "MSP (Rs./Quintal) 2026-27",
        "Price on 01 Oct, 2026",
        "Price on 30 Sep, 2026",
        "Price on 29 Sep, 2026",
        "Arrival on 01 Oct, 2026",
        "Arrival on 30 Sep, 2026",
        "Arrival on 29 Sep, 2026"
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            # Replace '-' with NaN
            df[col] = df[col].astype(str).str.replace(",", "").str.strip()
            df[col] = df[col].replace({"-": np.nan, "": np.nan})
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
    for col in ["Commodity Group", "Commodity"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    return df


def load_all_datasets() -> Dict[str, pd.DataFrame]:
    """Loads all 5 project datasets and returns them in a dictionary."""
    return {
        "crop_recommendation": load_crop_data(),
        "disease_metadata": load_disease_metadata(),
        "weather": load_weather_data(),
        "yield": load_yield_data(),
        "market": load_market_data(),
    }
