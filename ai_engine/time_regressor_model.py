import numpy as np
import lightgbm as lgb
from typing import List, Dict, Any

class TimeToCashoutRegressor:
    """
    Time-to-Cashout Regressor (LightGBM) for predicting remaining minutes (T_remain)
    before physical ATM cash withdrawal occurs. Powers the Live Golden Hour Tactical Countdown.
    """
    def __init__(self):
        self.model = None

    def extract_features(
        self,
        hop_level: int,
        total_amount: float,
        avg_hop_velocity: float,
        time_elapsed_mins: float,
        channel_type: str = "UPI"
    ) -> List[float]:
        channel_code = 1.0 if channel_type == "UPI" else (2.0 if channel_type == "IMPS" else 3.0)
        return [
            float(hop_level),
            float(total_amount),
            float(avg_hop_velocity),
            float(time_elapsed_mins),
            float(channel_code)
        ]

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train LightGBM Regressor on synthetic + benchmark transaction intervals"""
        train_data = lgb.Dataset(X, label=y)
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'learning_rate': 0.05,
            'num_leaves': 31,
            'verbose': -1
        }
        self.model = lgb.train(params, train_data, num_boost_round=100)

    def predict_remaining_minutes(
        self,
        hop_level: int,
        total_amount: float,
        avg_hop_velocity: float,
        time_elapsed_mins: float,
        channel_type: str = "UPI"
    ) -> Dict[str, Any]:
        feats = np.array([self.extract_features(hop_level, total_amount, avg_hop_velocity, time_elapsed_mins, channel_type)])
        
        if self.model:
            pred_val = float(self.model.predict(feats)[0])
        else:
            # Baseline domain heuristic: T_total = 45 mins - (hop_level * 6) - (time_elapsed)
            base_window = 45.0
            hop_decay = hop_level * 5.5
            pred_val = max(5.0, base_window - hop_decay - time_elapsed_mins)
            
        remaining_mins = max(3.0, round(pred_val, 1))
        urgency = "CRITICAL" if remaining_mins <= 15.0 else ("HIGH" if remaining_mins <= 30.0 else "MEDIUM")
        
        return {
            "estimated_minutes_remaining": remaining_mins,
            "golden_hour_urgency": urgency,
            "time_elapsed_mins": time_elapsed_mins,
            "hop_level": hop_level
        }
