import json
import random
import h3
from typing import List, Dict, Any

# Indian Real-World ATM Locations Sampled from OpenStreetMap Overpass API
INDIAN_ATM_SEEDS = [
    # Jammu & Kashmir (Residency Road, Gandhi Nagar, R.S. Pura, Jewel Chowk, Trikuta Nagar)
    {"atm_id": "ATM_JK_001", "name": "SBI ATM - Residency Road", "bank": "State Bank of India", "lat": 32.7266, "lon": 74.8570, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 14},
    {"atm_id": "ATM_JK_002", "name": "J&K Bank ATM - Gandhi Nagar", "bank": "Jammu & Kashmir Bank", "lat": 32.7061, "lon": 74.8690, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 22},
    {"atm_id": "ATM_JK_003", "name": "PNB ATM - Jewel Chowk", "bank": "Punjab National Bank", "lat": 32.7180, "lon": 74.8500, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": True, "is_24x7": False, "historical_mule_hits": 9},
    {"atm_id": "ATM_JK_004", "name": "HDFC Bank ATM - Trikuta Nagar", "bank": "HDFC Bank", "lat": 32.6980, "lon": 74.8820, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 17},
    {"atm_id": "ATM_JK_005", "name": "Axis Bank ATM - Bahu Plaza", "bank": "Axis Bank", "lat": 32.7030, "lon": 74.8760, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 11},
    {"atm_id": "ATM_JK_006", "name": "Indicash ATM - R.S. Pura Highway", "bank": "Indicash", "lat": 32.6320, "lon": 74.7330, "city": "Jammu", "state": "Jammu & Kashmir", "has_cctv": False, "is_24x7": True, "historical_mule_hits": 31},
    
    # Delhi NCR (Connaught Place, Karol Bagh, Laxmi Nagar, Rohini, Saket, Dwarka, Gurugram, Noida)
    {"atm_id": "ATM_DL_101", "name": "SBI ATM - Connaught Place Inner Circle", "bank": "State Bank of India", "lat": 28.6315, "lon": 77.2167, "city": "Delhi", "state": "Delhi", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 45},
    {"atm_id": "ATM_DL_102", "name": "ICICI Bank ATM - Karol Bagh Market", "bank": "ICICI Bank", "lat": 28.6517, "lon": 77.1906, "city": "Delhi", "state": "Delhi", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 38},
    {"atm_id": "ATM_DL_103", "name": "HDFC Bank ATM - Laxmi Nagar Metro", "bank": "HDFC Bank", "lat": 28.6304, "lon": 77.2773, "city": "Delhi", "state": "Delhi", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 52},
    {"atm_id": "ATM_DL_104", "name": "Canara Bank ATM - Rohini Sector 7", "bank": "Canara Bank", "lat": 28.7120, "lon": 77.1180, "city": "Delhi", "state": "Delhi", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 29},
    {"atm_id": "ATM_DL_105", "name": "Axis Bank ATM - Cyber City Gurugram", "bank": "Axis Bank", "lat": 28.4950, "lon": 77.0890, "city": "Gurugram", "state": "Haryana", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 61},
    
    # Mumbai (Bandra, Andheri, Dadar, Thane, Navi Mumbai)
    {"atm_id": "ATM_MH_201", "name": "SBI ATM - Bandra Linking Road", "bank": "State Bank of India", "lat": 19.0596, "lon": 72.8295, "city": "Mumbai", "state": "Maharashtra", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 40},
    {"atm_id": "ATM_MH_202", "name": "HDFC Bank ATM - Andheri West Station", "bank": "HDFC Bank", "lat": 19.1197, "lon": 72.8464, "city": "Mumbai", "state": "Maharashtra", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 58},
    
    # Bengaluru (Indiranagar, Koramangala, Whitefield, Electronic City)
    {"atm_id": "ATM_KA_301", "name": "ICICI Bank ATM - Koramangala 80ft Rd", "bank": "ICICI Bank", "lat": 12.9352, "lon": 77.6245, "city": "Bengaluru", "state": "Karnataka", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 27},
    {"atm_id": "ATM_KA_302", "name": "SBI ATM - Indiranagar 100ft Rd", "bank": "State Bank of India", "lat": 12.9719, "lon": 77.6412, "city": "Bengaluru", "state": "Karnataka", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 33},
    
    # Mewat / Nuh & Jamtara (Known Syndicate Operating Kiosks)
    {"atm_id": "ATM_HR_401", "name": "Tata Indicash ATM - Nuh Bypass", "bank": "Tata Indicash", "lat": 28.1065, "lon": 77.0125, "city": "Nuh", "state": "Haryana", "has_cctv": False, "is_24x7": True, "historical_mule_hits": 84},
    {"atm_id": "ATM_JH_501", "name": "SBI ATM - Jamtara Station Road", "bank": "State Bank of India", "lat": 23.9627, "lon": 86.8016, "city": "Jamtara", "state": "Jharkhand", "has_cctv": True, "is_24x7": True, "historical_mule_hits": 95}
]

def generate_full_atm_registry(total_count: int = 500) -> List[Dict[str, Any]]:
    """
    Expands the seed list into a full geocoded Indian ATM registry with Uber H3 spatial indexing (Res 8).
    """
    registry = []
    
    # First include the curated real points
    for atm in INDIAN_ATM_SEEDS:
        h3_idx = h3.latlng_to_cell(atm["lat"], atm["lon"], 8)
        enriched = dict(atm)
        enriched["h3_res8"] = h3_idx
        enriched["status"] = "ACTIVE"
        registry.append(enriched)
        
    # Generate additional points around clusters
    banks_pool = ["State Bank of India", "Punjab National Bank", "HDFC Bank", "ICICI Bank", "Axis Bank", "Bank of Baroda", "Indicash"]
    cities_pool = [
        ("Jammu", "Jammu & Kashmir", 32.7266, 74.8570),
        ("Delhi", "Delhi", 28.6139, 77.2090),
        ("Gurugram", "Haryana", 28.4595, 77.0266),
        ("Noida", "Uttar Pradesh", 28.5355, 77.3910),
        ("Chandigarh", "Chandigarh", 30.7333, 76.7794),
        ("Jaipur", "Rajasthan", 26.9124, 75.7873),
        ("Mumbai", "Maharashtra", 19.0760, 72.8777),
        ("Bengaluru", "Karnataka", 12.9716, 77.5946),
        ("Hyderabad", "Telangana", 17.3850, 78.4867),
        ("Kolkata", "West Bengal", 22.5726, 88.3639),
        ("Nuh", "Haryana", 28.1065, 77.0125),
        ("Jamtara", "Jharkhand", 23.9627, 86.8016)
    ]
    
    counter = len(registry) + 1
    while len(registry) < total_count:
        city_name, state_name, clat, clon = random.choice(cities_pool)
        lat = clat + random.uniform(-0.08, 0.08)
        lon = clon + random.uniform(-0.08, 0.08)
        bank = random.choice(banks_pool)
        h3_idx = h3.latlng_to_cell(lat, lon, 8)
        
        atm_obj = {
            "atm_id": f"ATM_{state_name[:2].upper()}_{counter:04d}",
            "name": f"{bank} Kiosk - {city_name} Sector {random.randint(1, 50)}",
            "bank": bank,
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "city": city_name,
            "state": state_name,
            "has_cctv": random.random() > 0.15,
            "is_24x7": random.random() > 0.20,
            "historical_mule_hits": random.randint(0, 40),
            "h3_res8": h3_idx,
            "status": "ACTIVE"
        }
        registry.append(atm_obj)
        counter += 1
        
    return registry

if __name__ == "__main__":
    atms = generate_full_atm_registry(total_count=500)
    print(f"Generated {len(atms)} geocoded Indian ATMs with H3 indexing.")
    print("Sample ATM:", atms[0])
