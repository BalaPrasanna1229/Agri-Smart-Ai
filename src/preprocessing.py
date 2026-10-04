"""
Preprocessing Module for Agri Smart AI
Constructs reproducible Scikit-Learn Preprocessing Pipelines and ColumnTransformers.
"""

from typing import List, Tuple, Union, Dict, Any
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


# ==========================================
# CROP RECOMMENDATION PREPROCESSING
# ==========================================

CROP_FEATURE_COLS = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]

CROP_TARGET_COL = "label"


def get_crop_features_and_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Extracts features X and target y for Crop Recommendation."""
    missing_cols = [c for c in CROP_FEATURE_COLS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required crop feature columns: {missing_cols}")
    if CROP_TARGET_COL not in df.columns:
        raise ValueError(f"Missing required crop target column: '{CROP_TARGET_COL}'")
        
    X = df[CROP_FEATURE_COLS].copy()
    y = df[CROP_TARGET_COL].copy()
    return X, y


def build_crop_pipeline(estimator: BaseEstimator) -> Pipeline:
    """
    Builds a full end-to-end pipeline with StandardScaler + Classifier for Crop Recommendation.
    """
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", estimator),
        ]
    )
    return pipeline


# ==========================================
# YIELD PREDICTION PREPROCESSING
# ==========================================

YIELD_NUMERICAL_COLS = [
    "Farm_Area(acres)",
    "Fertilizer_Used(tons)",
    "Pesticide_Used(kg)",
    "Water_Usage(cubic meters)",
]

YIELD_CATEGORICAL_COLS = [
    "Crop_Type",
    "Irrigation_Type",
    "Soil_Type",
    "Season",
]

YIELD_FEATURE_COLS = YIELD_NUMERICAL_COLS + YIELD_CATEGORICAL_COLS
YIELD_TARGET_COL = "Yield(tons)"
YIELD_IGNORE_COLS = ["Farm_ID"]


def get_yield_features_and_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Extracts features X and target y for Yield Prediction."""
    missing_features = [c for c in YIELD_FEATURE_COLS if c not in df.columns]
    if missing_features:
        raise ValueError(f"Missing required yield feature columns: {missing_features}")
    if YIELD_TARGET_COL not in df.columns:
        raise ValueError(f"Missing required yield target column: '{YIELD_TARGET_COL}'")
        
    X = df[YIELD_FEATURE_COLS].copy()
    y = df[YIELD_TARGET_COL].copy()
    return X, y


def build_yield_preprocessor() -> ColumnTransformer:
    """
    Constructs a ColumnTransformer that scales numeric inputs and one-hot encodes categoricals.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), YIELD_NUMERICAL_COLS),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                YIELD_CATEGORICAL_COLS,
            ),
        ],
        remainder="drop",
    )
    return preprocessor


def build_yield_pipeline(estimator: BaseEstimator) -> Pipeline:
    """
    Builds a full end-to-end pipeline with ColumnTransformer + Regressor for Yield Prediction.
    """
    preprocessor = build_yield_preprocessor()
    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", estimator),
        ]
    )
    return pipeline


# ==========================================
# INPUT VALIDATION UTILITIES
# ==========================================

def format_crop_input(input_data: Union[Dict[str, Any], pd.DataFrame]) -> pd.DataFrame:
    """Converts a raw dictionary or DataFrame into standard crop feature DataFrame."""
    if isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        raise TypeError("input_data must be a dict or a pandas DataFrame")
        
    for col in CROP_FEATURE_COLS:
        if col not in df.columns:
            raise KeyError(f"Input missing feature '{col}'. Required: {CROP_FEATURE_COLS}")
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isnull().any():
            raise ValueError(f"Invalid non-numeric value supplied for '{col}'")
            
    return df[CROP_FEATURE_COLS]


def format_yield_input(input_data: Union[Dict[str, Any], pd.DataFrame]) -> pd.DataFrame:
    """Converts a raw dictionary or DataFrame into standard yield feature DataFrame."""
    if isinstance(input_data, dict):
        df = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df = input_data.copy()
    else:
        raise TypeError("input_data must be a dict or a pandas DataFrame")
        
    for col in YIELD_NUMERICAL_COLS:
        if col not in df.columns:
            raise KeyError(f"Input missing numeric feature '{col}'. Required: {YIELD_FEATURE_COLS}")
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isnull().any():
            raise ValueError(f"Invalid non-numeric value supplied for '{col}'")
            
    for col in YIELD_CATEGORICAL_COLS:
        if col not in df.columns:
            raise KeyError(f"Input missing categorical feature '{col}'. Required: {YIELD_FEATURE_COLS}")
        df[col] = df[col].astype(str).str.strip()
        
    return df[YIELD_FEATURE_COLS]
