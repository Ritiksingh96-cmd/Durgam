import json
import os
import time
from typing import List, Dict, Any, Tuple
from ai_engine.st_kde_atm_model import SpatiotemporalATMPredictor
from ai_engine.osm_atm_fetcher import generate_full_atm_registry
from backend.app.models.schemas import CandidateATM

class GeospatialHotspotService:
    """
    Spatiotemporal ATM Hotspot & Field Police CAD Dispatch Service.
    Queries geocoded Indian ATM nodes with Uber H3 indexing and generates geo-fenced tactical action cards.
    """
    def __init__(self):
        self.atm_registry = generate_full_atm_registry(total_count=300)
        self.predictor = SpatiotemporalATMPredictor()
        self.active_patrol_units: List[Dict[str, Any]] = [
            {"unit_id": "PCR_JK_01", "callsign": "Jammu Alpha 1", "driver": "SI Ramesh Sharma", "lat": 32.7220, "lon": 74.8520, "status": "AVAILABLE", "city": "Jammu", "vehicle": "Mahindra Scorpio PCR"},
            {"unit_id": "PCR_JK_02", "callsign": "Jammu Bravo 2", "driver": "ASI Kuldeep Singh", "lat": 32.7090, "lon": 74.8650, "status": "PATROLLING", "city": "Jammu", "vehicle": "Tata Safari CAD"},
            {"unit_id": "PCR_DL_01", "callsign": "Delhi Eagle 4", "driver": "SI Vikram Rathore", "lat": 28.6280, "lon": 77.2110, "status": "AVAILABLE", "city": "Delhi", "vehicle": "Toyota Innova PCR"},
            {"unit_id": "PCR_HR_01", "callsign": "Mewat Cobra 9", "driver": "Insp Amit Yadav", "lat": 28.1090, "lon": 77.0180, "status": "ON_PATROL", "city": "Nuh", "vehicle": "Mahindra Bolero"}
        ]
        self.dispatch_logs: List[Dict[str, Any]] = []

    def get_candidate_atms_for_terminal_node(
        self,
        terminal_lat: float,
        terminal_lon: float,
        velocity: float = 2500.0,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Forecast the top-5 ATM kiosks in the vicinity of the terminal mule account"""
        return self.predictor.predict_top_k_atms(
            atm_registry=self.atm_registry,
            mule_branch_lat=terminal_lat,
            mule_branch_lon=terminal_lon,
            layering_velocity=velocity,
            top_k=top_k
        )

    def dispatch_nearest_patrol_unit(
        self,
        case_id: str,
        target_atm: Dict[str, Any],
        stolen_amount: float
    ) -> Dict[str, Any]:
        """Auto-calculate and push turn-by-turn tactical action card to nearest police PCR unit"""
        best_unit = None
        min_dist = 999.0
        
        atm_lat = float(target_atm.get("lat") or target_atm.get("latitude") or 28.6315)
        atm_lon = float(target_atm.get("lon") or target_atm.get("longitude") or 77.2167)
        
        for u in self.active_patrol_units:
            # Simple distance approximation
            dist = ((u["lat"] - atm_lat)**2 + (u["lon"] - atm_lon)**2)**0.5 * 111.0
            if dist < min_dist:
                min_dist = dist
                best_unit = u
                
        if not best_unit:
            best_unit = self.active_patrol_units[0]
            min_dist = 1.4
            
        dispatch_record = {
            "dispatch_id": f"CAD-DISPATCH-{len(self.dispatch_logs)+101}",
            "case_id": case_id,
            "unit_id": best_unit["unit_id"],
            "callsign": best_unit["callsign"],
            "driver_name": best_unit["driver"],
            "target_atm_id": target_atm["atm_id"],
            "target_atm_name": target_atm["name"],
            "target_lat": target_atm["lat"],
            "target_lon": target_atm["lon"],
            "distance_km": round(min_dist, 2),
            "eta_minutes": max(2, int(min_dist * 2.5)),
            "stolen_amount": stolen_amount,
            "timestamp": time.time(),
            "status": "DISPATCHED",
            "navigation_deeplink": f"https://www.google.com/maps/dir/?api=1&destination={target_atm['lat']},{target_atm['lon']}",
            "tactical_alert_message": f"🚨 URGENT INTERCEPTION: Suspect mule cash-out forecasted at {target_atm['name']} ({min_dist:.1f} km away). Target: ₹{stolen_amount:,.0f}."
        }
        self.dispatch_logs.append(dispatch_record)
        return dispatch_record

geospatial_service = GeospatialHotspotService()
