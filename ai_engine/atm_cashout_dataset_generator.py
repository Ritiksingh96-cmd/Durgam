import os
import sys
import json
import random
import datetime
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Major Indian Cybercrime & Commercial Corridors
INDIAN_CITIES = {
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946, "state": "Karnataka"},
    "Delhi": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi"},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777, "state": "Maharashtra"},
    "Jammu": {"lat": 32.7266, "lon": 74.8570, "state": "Jammu & Kashmir"},
    "Mewat": {"lat": 28.1065, "lon": 77.0125, "state": "Haryana"},
    "Jamtara": {"lat": 23.9629, "lon": 86.8014, "state": "Jharkhand"},
    "Hyderabad": {"lat": 17.3850, "lon": 78.4867, "state": "Telangana"},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639, "state": "West Bengal"},
    "Chennai": {"lat": 13.0827, "lon": 80.2707, "state": "Tamil Nadu"},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873, "state": "Rajasthan"},
    "Pune": {"lat": 18.5204, "lon": 73.8567, "state": "Maharashtra"},
    "Chandigarh": {"lat": 30.7333, "lon": 76.7794, "state": "Chandigarh"},
    "Ahmedabad": {"lat": 23.0225, "lon": 72.5714, "state": "Gujarat"},
    "Lucknow": {"lat": 26.8467, "lon": 80.9462, "state": "Uttar Pradesh"},
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def generate_atm_cashout_dataset(num_samples: int = 25000) -> pd.DataFrame:
    print(f"Generating massive ATM Cashout Hotspot dataset ({num_samples:,} records)...")
    random.seed(42)
    np.random.seed(42)

    base_time = datetime.datetime(2026, 8, 25, 0, 0, 0)
    city_names = list(INDIAN_CITIES.keys())

    records = []

    for i in range(num_samples):
        # 1. Timestamp (spread over last 30 days)
        delta_seconds = random.randint(0, 30 * 86400)
        ts = base_time + datetime.timedelta(seconds=delta_seconds)
        timestamp_str = ts.strftime("%Y-%m-%d %H:%M:%S")

        # 2. Amount (₹5,000 to ₹1,000,000)
        if random.random() < 0.6:
            amount = float(random.choice([10000, 20000, 25000, 50000, 85000, 99000, 150000, 250000]))
        else:
            amount = float(round(random.uniform(5000, 850000), 2))

        # 3. Victim City & Mule City
        victim_city = random.choice(city_names)
        mule_city = random.choice(city_names) if random.random() < 0.7 else victim_city
        mule_center = INDIAN_CITIES[mule_city]

        # 4. Mule Coordinates (with Gaussian jitter within 5-15km of city center)
        mule_lat = round(float(mule_center["lat"] + np.random.normal(0, 0.04)), 6)
        mule_lon = round(float(mule_center["lon"] + np.random.normal(0, 0.04)), 6)

        # 5. ATM Coordinates & Distance
        # 50% target actual nearby ATMs (0.1 to 3.5 km), 50% farther ATMs
        is_actual_hotspot = 1 if (random.random() < 0.45 and amount >= 25000) else 0

        if is_actual_hotspot == 1:
            atm_lat = round(float(mule_lat + np.random.normal(0, 0.008)), 6)
            atm_lon = round(float(mule_lon + np.random.normal(0, 0.008)), 6)
            dist_km = round(float(haversine_distance(mule_lat, mule_lon, atm_lat, atm_lon)), 2)
            velocity = round(float(random.uniform(2.5, 8.5)), 2)
            historical_score = round(float(random.uniform(0.70, 0.98)), 2)
        else:
            atm_lat = round(float(mule_lat + np.random.uniform(-0.15, 0.15)), 6)
            atm_lon = round(float(mule_lon + np.random.uniform(-0.15, 0.15)), 6)
            dist_km = round(float(haversine_distance(mule_lat, mule_lon, atm_lat, atm_lon)), 2)
            velocity = round(float(random.uniform(0.2, 2.8)), 2)
            historical_score = round(float(random.uniform(0.10, 0.65)), 2)

        records.append({
            "timestamp": timestamp_str,
            "amount": amount,
            "victim_city": victim_city,
            "mule_latitude": mule_lat,
            "mule_longitude": mule_lon,
            "atm_latitude": atm_lat,
            "atm_longitude": atm_lon,
            "distance_to_atm_km": dist_km,
            "transaction_velocity": velocity,
            "historical_hotspot_score": historical_score,
            "cashout_atm_label": is_actual_hotspot
        })

    df = pd.DataFrame(records)
    print(f"Generated DataFrame shape: {df.shape}")
    print(f"Hotspot (1) count: {(df['cashout_atm_label'] == 1).sum()}, Non-Hotspot (0) count: {(df['cashout_atm_label'] == 0).sum()}")
    return df

if __name__ == "__main__":
    df = generate_atm_cashout_dataset(25000)
    out_dir = os.path.join(os.path.dirname(__file__), "saved_models")
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, "atm_cashout_massive_dataset.csv"), index=False)
    print(f"Saved dataset to {os.path.join(out_dir, 'atm_cashout_massive_dataset.csv')}")
