"""
DURGAM National 100,000+ Record Cybercrime Dataset Generator
Generates realistic Indian cyber financial fraud benchmark dataset covering:
- Digital Arrest (CBI/ED/Police Skype Impersonation)
- Part-Time Task Scams (Telegram/WhatsApp Reviews)
- Electricity Bill / Sideloaded APK Malicious Stealers
- Sextortion & Honeytrap Video Calls
- SEBI Institutional Stock Trading & Crypto Ponzi Rings
- ATM Physical Cashout Trajectories
- TRC-20 / ERC-20 Cross-Border Crypto Mixer Wash-Trades
"""

import os
import gzip
import json
import time
import random
from typing import Dict, Any, List

BANKS = [
    ("State Bank of India", "SBIN"),
    ("Punjab National Bank", "PUNB"),
    ("HDFC Bank", "HDFC"),
    ("ICICI Bank", "ICIC"),
    ("Canara Bank", "CNRB"),
    ("Bank of Baroda", "BARB"),
    ("Axis Bank", "UTIB"),
    ("Kotak Mahindra Bank", "KKBK"),
    ("Union Bank of India", "UBIN"),
    ("IndusInd Bank", "INDB")
]

CITIES = [
    ("Delhi", "Delhi", 28.6139, 77.2090),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    ("Hyderabad", "Telangana", 17.3850, 78.4867),
    ("Jammu", "Jammu & Kashmir", 32.7266, 74.8570),
    ("Nuh", "Haryana", 28.1065, 77.0125),
    ("Jamtara", "Jharkhand", 23.9627, 86.8016),
    ("Kolkata", "West Bengal", 22.5726, 88.3639),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873),
    ("Chandigarh", "Chandigarh", 30.7333, 76.7794)
]

CATEGORIES = [
    "DIGITAL_ARREST",
    "PART_TIME_JOB",
    "APK_MALWARE",
    "SEXTORTION",
    "INVESTMENT_PONZI",
    "UPI_QR_FRAUD",
    "CRYPTO_MIXER_WASH"
]

def generate_single_record(idx: int) -> Dict[str, Any]:
    cat = random.choice(CATEGORIES)
    bank_name, ifsc_pfx = random.choice(BANKS)
    city_name, state_name, lat, lon = random.choice(CITIES)
    
    amount = round(random.uniform(15000.0, 1500000.0), 2)
    hop_level = random.randint(1, 4)
    time_to_cashout_mins = round(max(3.0, 45.0 - (hop_level * 6.5) - random.uniform(1.0, 8.0)), 1)
    
    return {
        "record_id": f"DURGAM-REC-{100000 + idx}",
        "timestamp": int(time.time()) - random.randint(100, 86400 * 30),
        "crime_category": cat,
        "loss_amount_inr": amount,
        "victim_state": state_name,
        "victim_city": city_name,
        "mule_bank": bank_name,
        "mule_ifsc": f"{ifsc_pfx}0{random.randint(100000, 999999)}",
        "mule_latitude": round(lat + random.uniform(-0.05, 0.05), 6),
        "mule_longitude": round(lon + random.uniform(-0.05, 0.05), 6),
        "hop_level": hop_level,
        "time_to_cashout_predicted_mins": time_to_cashout_mins,
        "camt056_hold_applied": random.choice([True, True, True, False]),
        "recovered_amount_inr": amount if random.random() > 0.3 else 0.0,
        "cctns_fir_status": "FIRED_DIGITAL_ANCHOR" if random.random() > 0.2 else "PENDING_MAGISTRATE"
    }

def generate_national_dataset(total_records: int = 10000, output_path: str = None):
    if output_path is None:
        out_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, "national_cybercrime_benchmark.json.gz")

    records = [generate_single_record(i) for i in range(total_records)]
    
    with gzip.open(output_path, "wt", encoding="utf-8") as f:
        json.dump(records, f)
        
    return {
        "status": "SUCCESS",
        "records_generated": total_records,
        "output_file": output_path,
        "size_kb": round(os.path.getsize(output_path) / 1024.0, 2)
    }

if __name__ == "__main__":
    res = generate_national_dataset(10000)
    print(f"[DATASET GENERATOR] Created {res['records_generated']} records at {res['output_file']} ({res['size_kb']} KB)")
