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
    ST-KDE + XGBoost Classifier for Forecasting Top 3-5 Physical ATM Cash-Out Kiosks.
    Combines Gaussian spatial/temporal density kernels, road distance, and transaction velocity.
    """
    def __init__(self, spatial_bandwidth_km: float = 2.5, temporal_bandwidth_mins: float = 30.0):
        self.hs = spatial_bandwidth_km
        self.ht = temporal_bandwidth_mins
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
        historical_hits: List[Tuple[float, float, float]]
    ) -> List[float]:
        dist_to_branch = haversine_distance(atm["lat"], atm["lon"], mule_branch_lat, mule_branch_lon)
        kde_score = self.compute_st_kde_density(atm["lat"], atm["lon"], target_time_offset, historical_hits)
        hits = float(atm.get("historical_mule_hits", 0))
        has_cctv = 1.0 if atm.get("has_cctv", True) else 0.0
        is_24x7 = 1.0 if atm.get("is_24x7", True) else 0.0
        
        # 6-Dimensional Feature Vector
        return [
            float(kde_score),
            float(dist_to_branch),
            float(layering_velocity),
            float(hits),
            float(has_cctv),
            float(is_24x7)
        ]

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train XGBoost ranking classifier on historical ATM withdrawal attempts"""
        dtrain = xgb.DMatrix(X, label=y)
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': 4,
            'learning_rate': 0.1,
            'tree_method': 'hist'
        }
        self.xgb_model = xgb.train(params, dtrain, num_boost_round=50)

    def predict_top_k_atms(
        self,
        atm_registry: List[Dict[str, Any]],
        mule_branch_lat: float,
        mule_branch_lon: float,
        layering_velocity: float,
        target_time_offset: float = 15.0,
        historical_hits: List[Tuple[float, float, float]] = None,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Rank candidate ATM kiosks and return the Top-K high-probability targets with tactical dispatch payload.
        """
        if historical_hits is None:
            # Default to mule branch coordinate as hot origin
            historical_hits = [(mule_branch_lat, mule_branch_lon, 0.0)]
            
        feature_matrix = []
        for atm in atm_registry:
            feats = self.extract_features(
                atm, mule_branch_lat, mule_branch_lon, layering_velocity, target_time_offset, historical_hits
            )
            feature_matrix.append(feats)
            
        X_mat = np.array(feature_matrix, dtype=np.float32)
        
        if self.xgb_model:
            dtest = xgb.DMatrix(X_mat)
            scores = self.xgb_model.predict(dtest)
        else:
            # Fallback heuristic formula matching PDF specification: Srisk = sigma(w1*KDE + w2*V + w3/(1+d) + w4*Hist)
            scores = []
            for feats in feature_matrix:
                kde, dist, vel, hist, cctv, is_24 = feats
                raw_score = (0.40 * kde * 100) + (0.25 * (vel / 1000.0)) + (0.20 / (1.0 + dist)) + (0.15 * (hist / 50.0))
                prob = 1.0 / (1.0 + math.exp(-raw_score))
                scores.append(prob)
            scores = np.array(scores)
            
        ranked_indices = np.argsort(scores)[::-1]
        
        results = []
        for rank, idx in enumerate(ranked_indices[:top_k], 1):
            atm = dict(atm_registry[idx])
            dist = haversine_distance(atm["lat"], atm["lon"], mule_branch_lat, mule_branch_lon)
            atm["risk_score"] = float(round(scores[idx], 4))
            atm["rank"] = rank
            atm["distance_km"] = float(round(dist, 2))
            atm["estimated_drive_time_mins"] = max(2, int(dist * 3.0)) # ~20 km/h city speed
            results.append(atm)
            
        return results
