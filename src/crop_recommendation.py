"""
Crop Recommendation Module for Agri Smart AI
Builds, evaluates, saves, and serves the Crop Recommendation Machine Learning Pipeline.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

from src.data_loader import load_crop_data
from src.preprocessing import (
    get_crop_features_and_target,
    build_crop_pipeline,
    format_crop_input,
    CROP_FEATURE_COLS,
    CROP_TARGET_COL,
)


MODEL_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODEL_DIR / "crop_recommendation_model.pkl"


class CropRecommendationModel:
    """
    Manages training, evaluation, persistence, and inference for Crop Recommendation.
    """

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or MODEL_PATH
        self.pipeline = None
        self.classes_ = None
        self.metrics_ = {}

    def train_and_evaluate(
        self,
        test_size: float = 0.2,
        random_state: int = 42,
        save_model: bool = True,
    ) -> Dict[str, Any]:
        """
        Loads dataset, splits into train/test, trains Pipeline, evaluates, and saves model.
        """
        print("\n==========================================")
        print("[*] Training Crop Recommendation Pipeline")
        print("==========================================")
        
        # 1. Load Dataset
        df = load_crop_data()
        print(f"Dataset Loaded. Shape: {df.shape} (Rows: {df.shape[0]}, Columns: {df.shape[1]})")
        print(f"Columns: {list(df.columns)}")
        print(f"Missing Values: {df.isnull().sum().to_dict()}")
        print(f"Duplicate Rows: {df.duplicated().sum()}")
        print(f"Unique Crop Classes ({len(df[CROP_TARGET_COL].unique())}): {sorted(df[CROP_TARGET_COL].unique())}")

        # 2. Extract Features & Target
        X, y = get_crop_features_and_target(df)
        print(f"Target Column: '{CROP_TARGET_COL}'")
        print(f"Feature Columns ({len(CROP_FEATURE_COLS)}): {CROP_FEATURE_COLS}")

        # 3. Stratified Train / Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"Train Set: {X_train.shape[0]} samples | Test Set: {X_test.shape[0]} samples")

        # 4. Build End-to-End Pipeline (StandardScaler + RandomForestClassifier)
        estimator = RandomForestClassifier(
            n_estimators=100,
            max_depth=None,
            min_samples_split=2,
            random_state=random_state,
            n_jobs=-1,
        )
        self.pipeline = build_crop_pipeline(estimator)

        # 5. Fit Pipeline
        print("Fitting Pipeline (StandardScaler -> RandomForestClassifier)...")
        self.pipeline.fit(X_train, y_train)

        # 6. Evaluate on Test Data
        y_pred = self.pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec_weighted = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        rec_weighted = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        prec_macro = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec_macro = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred)
        cls_report = classification_report(y_test, y_pred, zero_division=0)

        self.classes_ = list(self.pipeline.classes_)
        self.metrics_ = {
            "accuracy": float(acc),
            "precision_weighted": float(prec_weighted),
            "recall_weighted": float(rec_weighted),
            "f1_weighted": float(f1_weighted),
            "precision_macro": float(prec_macro),
            "recall_macro": float(rec_macro),
            "f1_macro": float(f1_macro),
            "confusion_matrix": cm.tolist(),
            "classification_report": cls_report,
            "train_samples": int(X_train.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "features": CROP_FEATURE_COLS,
            "target": CROP_TARGET_COL,
            "num_classes": len(self.classes_),
            "classes": self.classes_,
        }

        print("\n[+] Model Evaluation Results:")
        print(f"  - Accuracy:           {acc * 100:.2f}%")
        print(f"  - Weighted Precision: {prec_weighted * 100:.2f}%")
        print(f"  - Weighted Recall:    {rec_weighted * 100:.2f}%")
        print(f"  - Weighted F1-Score:  {f1_weighted * 100:.2f}%")
        print(f"  - Macro F1-Score:     {f1_macro * 100:.2f}%")
        print("\nClassification Report (summary excerpt):")
        print("\n".join(cls_report.splitlines()[:10]))

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
            "classes": self.classes_,
            "metrics": self.metrics_,
            "features": CROP_FEATURE_COLS,
            "target": CROP_TARGET_COL,
        }
        joblib.dump(payload, self.model_path)
        print(f"[+] Saved Crop Recommendation Pipeline to: {self.model_path}")

    def load_model(self) -> None:
        """Loads the saved pipeline from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. Train the model first."
            )
        payload = joblib.load(self.model_path)
        self.pipeline = payload["pipeline"]
        self.classes_ = payload["classes"]
        self.metrics_ = payload.get("metrics", {})
        print(f"[+] Loaded Crop Recommendation Pipeline from: {self.model_path}")

    def predict(self, input_data: Union[Dict[str, Any], pd.DataFrame]) -> Dict[str, Any]:
        """
        Predicts the recommended crop and returns top-3 probabilities.
        Accepts dict or DataFrame with: N, P, K, temperature, humidity, ph, rainfall
        """
        if self.pipeline is None:
            self.load_model()
            
        X_df = format_crop_input(input_data)
        prediction = self.pipeline.predict(X_df)[0]
        
        # Probabilities
        if hasattr(self.pipeline, "predict_proba"):
            probs = self.pipeline.predict_proba(X_df)[0]
            top_indices = np.argsort(probs)[::-1][:3]
            top_recommendations = [
                {
                    "rank": rank + 1,
                    "crop": self.classes_[idx],
                    "confidence": float(probs[idx]),
                    "confidence_pct": round(float(probs[idx]) * 100, 2),
                }
                for rank, idx in enumerate(top_indices)
            ]
            primary_confidence = float(probs[top_indices[0]])
        else:
            top_recommendations = [{"rank": 1, "crop": prediction, "confidence": 1.0, "confidence_pct": 100.0}]
            primary_confidence = 1.0

        return {
            "recommended_crop": prediction,
            "confidence": primary_confidence,
            "confidence_pct": round(primary_confidence * 100, 2),
            "top_3_recommendations": top_recommendations,
            "input_features": X_df.iloc[0].to_dict(),
        }


def get_crop_recommender() -> CropRecommendationModel:
    """Helper factory that returns a ready-to-use CropRecommendationModel instance."""
    model = CropRecommendationModel()
    if not MODEL_PATH.exists():
        model.train_and_evaluate(save_model=True)
    else:
        model.load_model()
    return model


if __name__ == "__main__":
    # Self-test when executed directly
    model = CropRecommendationModel()
    metrics = model.train_and_evaluate()
    
    # Test sample prediction (Rice test sample: N=90, P=42, K=43, temp=20.88, hum=82.0, ph=6.5, rain=202.9)
    sample_input = {
        "N": 90,
        "P": 42,
        "K": 43,
        "temperature": 20.88,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9,
    }
    result = model.predict(sample_input)
    print("\n[+] Sample Prediction Result:")
    print(result)
