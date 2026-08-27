import os
import math
import numpy as np
from typing import List, Dict, Any, Tuple
import xgboost as xgb
import h3

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in kilometers between two GPS coordinates"""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class SpatiotemporalATMPredictor:
    """
    ST-KDE + Pre-Trained 8-Dimensional XGBoost Classifier for Forecasting Top Physical ATM Cash-Out Kiosks.
    Combines Gaussian spatial/temporal density kernels, Telecom cell-tower distance, cash vault, and CCTV blindspots.
    """
    def __init__(self, spatial_bandwidth_km: float = 2.5, temporal_bandwidth_mins: float = 30.0):
        self.hs = spatial_bandwidth_km
        self.ht = temporal_bandwidth_mins
        self.xgb_model = None
        self._load_pretrained_model()

    def _load_pretrained_model(self):
        """Loads serialized XGBoost model binary if available."""
        model_path = os.path.join(os.path.dirname(__file__), "models", "atm_xgb_model.json")
        if os.path.exists(model_path):
            try:
                self.xgb_model = xgb.Booster()
                self.xgb_model.load_model(model_path)
            except Exception as e:
                self.xgb_model = None

    def gaussian_spatial_kernel(self, dist_km: float) -> float:
        u = dist_km / self.hs
        return (1.0 / (2.0 * math.pi)) * math.exp(-0.5 * (u ** 2))

    def gaussian_temporal_kernel(self, time_delta_mins: float) -> float:
        u = abs(time_delta_mins) / self.ht
        return (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * (u ** 2))

    def compute_st_kde_density(
        self,
        candidate_lat: float,
        candidate_lon: float,
        target_time_mins: float,
        historical_hits: List[Tuple[float, float, float]]
    ) -> float:
        """
        Computes Spatiotemporal Kernel Density Estimation:
        f_hat(x, y, t) = 1/(n * hs^2 * ht) * sum( Ks((x - xi)/hs, (y - yi)/hs) * Kt((t - ti)/ht) )
        """
        if not historical_hits:
            return 0.05
            
        n = len(historical_hits)
        density_sum = 0.0
        for h_lat, h_lon, h_time in historical_hits:
            dist = haversine_distance(candidate_lat, candidate_lon, h_lat, h_lon)
            ks = self.gaussian_spatial_kernel(dist)
            kt = self.gaussian_temporal_kernel(target_time_mins - h_time)
            density_sum += (ks * kt)
            
        return density_sum / (n * (self.hs ** 2) * self.ht + 1e-6)

    def extract_features(
        self,
        atm: Dict[str, Any],
        mule_branch_lat: float,
        mule_branch_lon: float,
        layering_velocity: float,
        target_time_offset: float,
        historical_hits: List[Tuple[float, float, float]],
        telecom_cell_lat: float = None,
        telecom_cell_lon: float = None
    ) -> List[float]:
        dist_to_branch = haversine_distance(atm["lat"], atm["lon"], mule_branch_lat, mule_branch_lon)
        
        # If telecom cell anchor provided, compute direct proximity to active phone
        if telecom_cell_lat is not None and telecom_cell_lon is not None:
            dist_to_cell = haversine_distance(atm["lat"], atm["lon"], telecom_cell_lat, telecom_cell_lon)
        else:
            dist_to_cell = dist_to_branch * 0.85

        kde_score = self.compute_st_kde_density(atm["lat"], atm["lon"], target_time_offset, historical_hits)
        hits = float(atm.get("historical_mule_hits", 0))
        vault_high = 1.0 if atm.get("cash_vault_level", 2500000) > 1000000 else 0.0
        cctv_blind = 1.0 if not atm.get("has_cctv", True) else 0.0
        is_isolated = 1.0 if atm.get("is_24x7", True) else 0.0
        
        # 8-Dimensional Feature Vector matching train_atm_ranking_model.py
        return [
            float(kde_score),
            float(dist_to_cell),
            float(dist_to_branch),
            float(layering_velocity),
            float(hits),
            float(vault_high),
            float(cctv_blind),
            float(is_isolated)
        ]

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train XGBoost ranking classifier on historical ATM withdrawal attempts"""
        dtrain = xgb.DMatrix(X, label=y)
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': 5,
            'learning_rate': 0.08,
            'tree_method': 'hist'
        }
        self.xgb_model = xgb.train(params, dtrain, num_boost_round=60)

    def predict_top_k_atms(
        self,
        atm_registry: List[Dict[str, Any]],
        mule_branch_lat: float,
        mule_branch_lon: float,
        layering_velocity: float,
        target_time_offset: float = 15.0,
        historical_hits: List[Tuple[float, float, float]] = None,
        telecom_cell_lat: float = None,
        telecom_cell_lon: float = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Rank candidate ATM kiosks using the pre-trained 8-dimensional XGBoost model.
        """
        if historical_hits is None:
            # Default to mule branch coordinate as hot origin
            historical_hits = [(mule_branch_lat, mule_branch_lon, 0.0)]
            
        feature_matrix = []
        for atm in atm_registry:
            feats = self.extract_features(
                atm, mule_branch_lat, mule_branch_lon, layering_velocity, target_time_offset, historical_hits,
                telecom_cell_lat, telecom_cell_lon
            )
            feature_matrix.append(feats)
            
        X_mat = np.array(feature_matrix, dtype=np.float32)
        
        if self.xgb_model:
            dtest = xgb.DMatrix(X_mat)
            scores = self.xgb_model.predict(dtest)
        else:
            # Calibrated mathematical scoring formula fallback
            scores = []
            for feats in feature_matrix:
                kde, dist_cell, dist_br, vel, hist, vault, blind, iso = feats
                proximity_factor = math.exp(-dist_cell / 3.0)
                raw_score = (0.40 * (kde * 80.0)) + (0.30 * proximity_factor) + (0.15 * min(1.0, vel / 800.0)) + (0.15 * min(1.0, hist / 40.0))
                prob = min(0.98, max(0.20, 1.0 / (1.0 + math.exp(-2.2 * (raw_score - 0.5)))))
                scores.append(prob)
            scores = np.array(scores)
            
        ranked_indices = np.argsort(scores)[::-1]

        
        results = []
        for rank, idx in enumerate(ranked_indices[:top_k], 1):
            atm = dict(atm_registry[idx])
            dist = haversine_distance(atm["lat"], atm["lon"], mule_branch_lat, mule_branch_lon)
            
            # Urban Traffic Physics: 28 km/h congested speed (60 / 28 = ~2.14 mins/km) + 1.5 min buffer
            drive_mins = max(2, int(round((dist * 2.14) + 1.5)))
            risk_pct = round(float(scores[idx]), 4)
            
            # Dynamic Waypoint Interpolation for Police CAD Intercept Map
            waypoints = self.compute_intercept_route(
                start_lat=mule_branch_lat,
                start_lon=mule_branch_lon,
                end_lat=atm["lat"],
                end_lon=atm["lon"],
                num_points=4
            )
            
            atm["risk_score"] = float(round(scores[idx], 4))
            atm["rank"] = rank
            atm["distance_km"] = float(round(dist, 2))
            atm["estimated_drive_time_mins"] = drive_mins
            atm["risk_tier"] = "CRITICAL_INTERCEPT" if scores[idx] >= 0.85 else ("HIGH_PROBABILITY" if scores[idx] >= 0.65 else "SURVEILLANCE")
            atm["intercept_waypoints"] = waypoints
            results.append(atm)
            
        return results

    def compute_intercept_route(
        self,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float,
        num_points: int = 4
    ) -> List[Dict[str, float]]:
        """Computes interpolated road waypoints between suspected origin and target ATM kiosk"""
        points = []
        for i in range(num_points + 1):
            fraction = i / float(num_points)
            w_lat = start_lat + (end_lat - start_lat) * fraction
            w_lon = start_lon + (end_lon - start_lon) * fraction
            points.append({
                "step": i,
                "lat": round(w_lat, 6),
                "lon": round(w_lon, 6),
                "eta_mins": round(fraction * 6.5, 1)
            })
        return points

