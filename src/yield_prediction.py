"""
Yield Prediction Module for Agri Smart AI
Builds, evaluates, saves, and serves the Farm Yield Prediction Pipeline.

IMPORTANT NOTICE & DATASET LIMITATION:
The training dataset (yield_dataset.csv.xls) contains only 50 farm records across 10 crop types.
Model predictions may have limited statistical reliability on unseen farm conditions.
Cross-validation and regularization are utilized to mitigate overfitting.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.data_loader import load_yield_data
from src.preprocessing import (
    get_yield_features_and_target,
    build_yield_pipeline,
    format_yield_input,
    YIELD_FEATURE_COLS,
    YIELD_NUMERICAL_COLS,
    YIELD_CATEGORICAL_COLS,
    YIELD_TARGET_COL,
)


MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "yield_prediction_model.pkl"

LIMITATION_NOTE = (
    "Dataset contains only 50 rows across 10 crops. Predictions are indicative "
    "and should be interpreted with caution for commercial farming decisions."
)


class YieldPredictionModel:
    """
    Manages training, evaluation, persistence, and inference for Farm Crop Yield Regression.
    """

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_PATH
        self.pipeline = None
        self.metrics_ = {}

    def train_and_evaluate(
        self,
        test_size: float = 0.2,
        random_state: int = 42,
        save_model: bool = True,
    ) -> Dict[str, Any]:
        """
        Loads dataset, splits into train/test, trains Pipeline, evaluates R2/MAE/RMSE, and saves model.
        """
        print("\n==========================================")
        print("[*] Training Yield Prediction Pipeline")
        print("==========================================")
        print(f"[!] LIMITATION NOTICE: {LIMITATION_NOTE}")
        
        # 1. Load Dataset
        df = load_yield_data()
        print(f"Dataset Loaded. Shape: {df.shape} (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
        print(f"Columns: {list(df.columns)}")
        print(f"Missing Values: {df.isnull().sum().to_dict()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")
        print(f"Crops ({len(df['Crop_Type'].unique())}): {list(df['Crop_Type'].unique())}")
        print(f"Soil Types: {list(df['Soil_Type'].unique())}")
        print(f"Seasons: {list(df['Season'].unique())}")
        print(f"Irrigation Types: {list(df['Irrigation_Type'].unique())}")

        # 2. Extract Features & Target
        X, y = get_yield_features_and_target(df)
        print(f"Target Column: '{YIELD_TARGET_COL}'")
        print(f"Numerical Features ({len(YIELD_NUMERICAL_COLS)}): {YIELD_NUMERICAL_COLS}")
        print(f"Categorical Features ({len(YIELD_CATEGORICAL_COLS)}): {YIELD_CATEGORICAL_COLS}")

        # 3. Train / Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"Train Set: {X_train.shape[0]} samples | Test Set: {X_test.shape[0]} samples")

        # 4. Build End-to-End Pipeline (ColumnTransformer + Regressor)
        estimator = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_split=3,
            min_samples_leaf=2,
            random_state=random_state,
        )
        self.pipeline = build_yield_pipeline(estimator)

        # 5. Fit Pipeline
        print("Fitting Pipeline (ColumnTransformer -> RandomForestRegressor)...")
        self.pipeline.fit(X_train, y_train)

        # 6. Evaluate on Test Data
        y_pred = self.pipeline.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

        # 5-Fold Cross Validation on full dataset for robust estimation on small data
        kf = KFold(n_splits=5, shuffle=True, random_state=random_state)
        cv_r2_scores = cross_val_score(self.pipeline, X, y, cv=kf, scoring="r2")
        cv_mae_scores = -cross_val_score(self.pipeline, X, y, cv=kf, scoring="neg_mean_absolute_error")
        cv_rmse_scores = np.sqrt(-cross_val_score(self.pipeline, X, y, cv=kf, scoring="neg_mean_squared_error"))

        self.metrics_ = {
            "test_r2": float(r2),
            "test_mae": float(mae),
            "test_rmse": float(rmse),
            "cv_5fold_mean_r2": float(np.mean(cv_r2_scores)),
            "cv_5fold_std_r2": float(np.std(cv_r2_scores)),
            "cv_5fold_mean_mae": float(np.mean(cv_mae_scores)),
            "cv_5fold_mean_rmse": float(np.mean(cv_rmse_scores)),
            "train_samples": int(X_train.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "total_dataset_rows": int(df.shape[0]),
            "features": YIELD_FEATURE_COLS,
            "target": YIELD_TARGET_COL,
            "limitation_warning": LIMITATION_NOTE,
        }

        print("\n[+] Model Evaluation Results:")
        print(f"  - Test R^2 Score:        {r2:.4f}")
        print(f"  - Test MAE (tons):       {mae:.4f}")
        print(f"  - Test RMSE (tons):      {rmse:.4f}")
        print(f"  - 5-Fold CV Mean R^2:    {np.mean(cv_r2_scores):.4f} (+/- {np.std(cv_r2_scores):.4f})")
        print(f"  - 5-Fold CV Mean MAE:    {np.mean(cv_mae_scores):.4f} tons")
        print(f"  - 5-Fold CV Mean RMSE:   {np.mean(cv_rmse_scores):.4f} tons")

        # 7. Save Pipeline Artifact
        if save_model:
            self.save_model()

        return self.metrics_

    def save_model(self) -> None:
        """Saves the pipeline and its metadata to disk."""
        if self.pipeline is None:
            raise ValueError("No trained pipeline to save. Call train_and_evaluate() first.")
            
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "pipeline": self.pipeline,
            "metrics": self.metrics_,
            "features": YIELD_FEATURE_COLS,
            "target": YIELD_TARGET_COL,
            "limitation_note": LIMITATION_NOTE,
        }
        joblib.dump(payload, self.model_path)
        print(f"[+] Saved Yield Prediction Pipeline to: {self.model_path}")

    def load_model(self) -> None:
        """Loads the saved pipeline from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. Train the model first."
            )
        payload = joblib.load(self.model_path)
        self.pipeline = payload["pipeline"]
        self.metrics_ = payload.get("metrics", {})
        print(f"[+] Loaded Yield Prediction Pipeline from: {self.model_path}")

    def predict(self, input_data: Union[Dict[str, Any], pd.DataFrame]) -> Dict[str, Any]:
        """
        Predicts total harvest yield (tons) and estimated yield per acre.
        Accepts dict or DataFrame with:
        Crop_Type, Farm_Area(acres), Irrigation_Type, Fertilizer_Used(tons),
        Pesticide_Used(kg), Soil_Type, Season, Water_Usage(cubic meters)
        """
        if self.pipeline is None:
            self.load_model()
            
        X_df = format_yield_input(input_data)
        pred_tons = float(self.pipeline.predict(X_df)[0])
        farm_area = float(X_df["Farm_Area(acres)"].iloc[0])
        
        # Guard against zero/negative yield artifact
        pred_tons = max(0.0, round(pred_tons, 2))
        yield_per_acre = round(pred_tons / farm_area, 2) if farm_area > 0 else 0.0

        return {
            "predicted_yield_tons": pred_tons,
            "farm_area_acres": farm_area,
            "yield_per_acre_tons": yield_per_acre,
            "unit": "tons",
            "reliability_note": LIMITATION_NOTE,
            "input_features": X_df.iloc[0].to_dict(),
        }


def get_yield_predictor() -> YieldPredictionModel:
    """Helper factory that returns a ready-to-use YieldPredictionModel instance."""
    model = YieldPredictionModel()
    if not MODEL_PATH.exists():
        model.train_and_evaluate(save_model=True)
    else:
        model.load_model()
    return model


if __name__ == "__main__":
    # Self-test when executed directly
    model = YieldPredictionModel()
    metrics = model.train_and_evaluate()
    
    # Test sample prediction (F001 sample: Cotton, 329.4 acres, Sprinkler, 8.14 tons fert, 2.21 kg pest, Loamy, Kharif, 76648.2 m3 water)
    sample_farm = {
        "Crop_Type": "Cotton",
        "Farm_Area(acres)": 329.4,
        "Irrigation_Type": "Sprinkler",
        "Fertilizer_Used(tons)": 8.14,
        "Pesticide_Used(kg)": 2.21,
        "Soil_Type": "Loamy",
        "Season": "Kharif",
        "Water_Usage(cubic meters)": 76648.2,
    }
    result = model.predict(sample_farm)
    print("\n[+] Sample Prediction Result:")
    print(result)
