import os
import sys
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

class ATMCashoutHotspotClassifier:
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=42,
            eval_metric="logloss"
        )
        self.feature_names = [
            "amount",
            "mule_latitude",
            "mule_longitude",
            "atm_latitude",
            "atm_longitude",
            "distance_to_atm_km",
            "transaction_velocity",
            "historical_hotspot_score",
            "hour_of_day",
            "day_of_week"
        ]
        
        # Auto-load saved model if present
        saved_json = os.path.join(MODEL_DIR, "atm_hotspot_screenshot_xgb.json")
        if os.path.exists(saved_json):
            try:
                self.model.load_model(saved_json)
            except Exception as e:
                pass

    def extract_features(self, df: pd.DataFrame) -> np.ndarray:
        if "timestamp" in df.columns:
            ts = pd.to_datetime(df["timestamp"])
            hour = ts.dt.hour.values
            day = ts.dt.dayofweek.values
        else:
            hour = np.array([12] * len(df))
            day = np.array([2] * len(df))

        feats = np.column_stack([
            df["amount"].values,
            df["mule_latitude"].values,
            df["mule_longitude"].values,
            df["atm_latitude"].values,
            df["atm_longitude"].values,
            df["distance_to_atm_km"].values,
            df["transaction_velocity"].values,
            df["historical_hotspot_score"].values,
            hour,
            day
        ])
        return feats

    def train_on_dataframe(self, df: pd.DataFrame):
        X = self.extract_features(df)
        y = df["cashout_atm_label"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y
        )

        print(f"Training XGBoost ATM Cashout Hotspot Classifier on {len(X_train):,} samples...")
        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)
        probs = self.model.predict_proba(X_test)[:, 1]

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        auc = roc_auc_score(y_test, probs)

        print(f"  [METRICS] Accuracy: {acc*100:.2f}% | Precision: {prec*100:.2f}% | Recall: {rec*100:.2f}% | F1: {f1:.4f} | ROC-AUC: {auc:.4f}")

        # Save model
        model_path = os.path.join(MODEL_DIR, "atm_hotspot_screenshot_xgb.json")
        self.model.save_model(model_path)
        print(f"  [SAVED] Saved model to {model_path}")

        return {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "num_training_samples": len(X_train),
            "num_test_samples": len(X_test)
        }

    def predict_single(self, record: dict) -> dict:
        df = pd.DataFrame([record])
        X = self.extract_features(df)
        pred_label = int(self.model.predict(X)[0])
        prob = float(self.model.predict_proba(X)[0][1])

        return {
            "cashout_atm_label": pred_label,
            "hotspot_probability": round(prob, 4),
            "risk_tier": "CRITICAL_HOTSPOT" if prob >= 0.75 else "MODERATE_RISK" if prob >= 0.40 else "LOW_PROBABILITY",
            "tactical_recommendation": (
                "IMMEDIATE BEAT PATROL DISPATCH REQUIRED (< 4 Mins)" if pred_label == 1
                else "Routine Surveillance / Standard Monitoring"
            )
        }

if __name__ == "__main__":
    from ai_engine.atm_cashout_dataset_generator import generate_atm_cashout_dataset
    df = generate_atm_cashout_dataset(25000)
    classifier = ATMCashoutHotspotClassifier()
    metrics = classifier.train_on_dataframe(df)

    # Test single sample matching user screenshot example
    test_sample = {
        "timestamp": "2026-08-25 10:35:21",
        "amount": 85000.0,
        "victim_city": "Bengaluru",
        "mule_latitude": 12.9716,
        "mule_longitude": 77.5946,
        "atm_latitude": 12.9751,
        "atm_longitude": 77.6012,
        "distance_to_atm_km": 0.82,
        "transaction_velocity": 3.7,
        "historical_hotspot_score": 0.91
    }
    result = classifier.predict_single(test_sample)
    print(f"\nPrediction for screenshot sample: {json.dumps(result, indent=2)}")
