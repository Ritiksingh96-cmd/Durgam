"""
DURGAM AI Engine — ATM Cashout Ranking Model Training & Serialization Script
Generates 50,000+ geocoded ATM transactions across Indian cyber hubs (Delhi, Mewat, Jamtara, Mumbai),
trains an 8-dimensional XGBoost classifier, evaluates Top-K precision, and serializes atm_xgb_model.json.
"""

import os
import math
import random
import numpy as np
import xgboost as xgb
from typing import Tuple, List, Dict, Any

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    return R * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

def generate_atm_training_dataset(num_samples: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generates 8-dimensional feature vectors representing candidate ATM cashout options:
    [0] kde_density: Spatiotemporal density (0.0 to 1.0)
    [1] dist_to_telecom_cell: Distance to active SIM / UPI IP cell (0.1 to 15.0 km)
    [2] dist_to_branch: Distance to beneficiary receiving branch (0.1 to 25.0 km)
    [3] layering_velocity: INR/sec transfer velocity (100 to 5000)
    [4] historical_mule_hits: Past illegal cashouts (0 to 60)
    [5] cash_vault_liquidity: High cash stock flag (0 or 1)
    [6] cctv_blindspot_flag: Disabled / obscured camera flag (0 or 1)
    [7] is_24x7_isolated: Standalone unguarded kiosk (0 or 1)
    """
    print(f"[*] Generating {num_samples} geocoded ATM cashout training instances...")
    X = []
    y = []

    for _ in range(num_samples):
        # 25% positive target cashout instances, 75% negative background kiosks
        is_target = 1 if random.random() < 0.25 else 0

        if is_target:
            # Positive Target ATM Characteristics
            dist_cell = random.uniform(0.1, 2.5)  # Within 2.5km of active phone
            dist_branch = random.uniform(0.2, 5.0)
            kde = random.uniform(0.55, 0.98)
            vel = random.uniform(800.0, 4500.0)
            hist_hits = random.randint(12, 55)
            vault = 1 if random.random() < 0.85 else 0
            cctv_blind = 1 if random.random() < 0.70 else 0
            isolated = 1 if random.random() < 0.80 else 0
        else:
            # Negative Background ATM Characteristics
            dist_cell = random.uniform(3.0, 18.0)
            dist_branch = random.uniform(4.0, 30.0)
            kde = random.uniform(0.01, 0.40)
            vel = random.uniform(50.0, 600.0)
            hist_hits = random.randint(0, 8)
            vault = 1 if random.random() < 0.40 else 0
            cctv_blind = 1 if random.random() < 0.20 else 0
            isolated = 1 if random.random() < 0.30 else 0

        feat = [
            float(kde),
            float(dist_cell),
            float(dist_branch),
            float(vel),
            float(hist_hits),
            float(vault),
            float(cctv_blind),
            float(isolated)
        ]
        X.append(feat)
        y.append(is_target)

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)

def train_and_save_model():
    X, y = generate_atm_training_dataset(num_samples=50000)

    # 80/20 Train-Test Split
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        'objective': 'binary:logistic',
        'eval_metric': ['logloss', 'auc'],
        'max_depth': 5,
        'learning_rate': 0.08,
        'tree_method': 'hist',
        'subsample': 0.85,
        'colsample_bytree': 0.85,
        'seed': 42
    }

    print("[*] Training 8-Dimensional XGBoost ATM Anomaly & Hotspot Forecaster...")
    evals = [(dtrain, 'train'), (dtest, 'val')]
    bst = xgb.train(params, dtrain, num_boost_round=80, evals=evals, verbose_eval=False)

    # Evaluate Metrics
    preds = bst.predict(dtest)
    preds_binary = (preds >= 0.5).astype(int)

    tp = np.sum((preds_binary == 1) & (y_test == 1))
    fp = np.sum((preds_binary == 1) & (y_test == 0))
    fn = np.sum((preds_binary == 0) & (y_test == 1))

    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)
    f1 = 2 * (precision * recall) / (precision + recall + 1e-6)

    # Top-3 Accuracy on simulated K-Candidate Groups
    num_eval_groups = 1000
    top1_correct = 0
    top3_correct = 0
    top5_correct = 0

    for _ in range(num_eval_groups):
        # 1 target ATM + 9 distractor ATMs
        target_idx = np.random.choice(np.where(y_test == 1)[0])
        distractor_indices = np.random.choice(np.where(y_test == 0)[0], size=9, replace=False)
        group_indices = [target_idx] + list(distractor_indices)
        
        group_preds = preds[group_indices]
        ranked_order = np.argsort(group_preds)[::-1]

        if ranked_order[0] == 0:
            top1_correct += 1
        if 0 in ranked_order[:3]:
            top3_correct += 1
        if 0 in ranked_order[:5]:
            top5_correct += 1

    top1_acc = (top1_correct / num_eval_groups) * 100.0
    top3_acc = (top3_correct / num_eval_groups) * 100.0
    top5_acc = (top5_correct / num_eval_groups) * 100.0

    print("\n" + "=" * 60)
    print("  DURGAM XGBOOST ATM HOTSPOT FORECASTER — BENCHMARK RESULTS")
    print("=" * 60)
    print(f"  Precision:           {precision * 100:.2f}%")
    print(f"  Recall:              {recall * 100:.2f}%")
    print(f"  F1-Score:            {f1:.4f}")
    print(f"  Top-1 ATM Precision: {top1_acc:.2f}%")
    print(f"  Top-3 ATM Precision: {top3_acc:.2f}%")
    print(f"  Top-5 ATM Coverage:  {top5_acc:.2f}%")
    print("=" * 60)

    # Serialize Model Binary
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "atm_xgb_model.json")
    bst.save_model(model_path)
    print(f"[+] Trained model binary serialized successfully to: {model_path}\n")

if __name__ == "__main__":
    train_and_save_model()
