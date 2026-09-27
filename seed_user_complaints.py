import sqlite3
import json
import time
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "backend", "durgam_sovereign.db")

COMPLAINTS_TO_SEED = [
    {
        "case_id": "DURGAM-DL-7782",
        "ack_number": "NCRP-1930-77821940",
        "complaint_id": "NCRP-1930-77821940",
        "victim_name": "Ritik Singh",
        "victim_phone": "9811029481",
        "victim_city": "Delhi NCR",
        "victim_state": "Delhi",
        "utr_number": "582910481920",
        "source_bank": "State Bank of India",
        "source_account": "XXXX-XXXX-2948",
        "suspect_account": "902148102941",
        "loss_amount": 350000.0,
        "amount": 350000.0,
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Counterfeit video call from fake law enforcement threatening digital arrest. Victim coerced into depositing funds into mule escrow.",
        "status": "MICRO_HOLD_PLACED",
        "hold_status": "ACTIVE_30_MIN_HOLD",
        "execution_latency_ms": 89.2,
        "candidate_atms": [
            { "name": "SBI ATM Sector 29 Market", "bank_name": "SBI ATM Sector 29", "address": "Sector 29 Market, Gurugram", "lat": 28.4595, "lon": 77.0266, "eta_minutes": 3, "risk_score": "96.5%" }
        ],
        "terminal_node": {
            "account_id": "ACC_MULE_9021",
            "masked_account": "902148102941",
            "bank_name": "Punjab National Bank",
            "ifsc": "PUNB0001024",
            "region": "Sector 29, Gurugram",
            "state": "Haryana",
            "latitude": 28.4595,
            "longitude": 77.0266,
            "atm_name": "SBI ATM Sector 29 Market"
        },
        "evidence_certificate": {
            "sha256_case_hash": "0x7a8f9c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90",
            "merkle_root": "0x7a8f9c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90",
            "polygon_tx_hash": "0x4a920194810248a1c92847190284719284719284719284719284719284719284",
            "block_number": 4920194
        }
    },
    {
        "case_id": "DURGAM-HR-6648",
        "ack_number": "NCRP-1930-66481029",
        "complaint_id": "NCRP-1930-66481029",
        "victim_name": "Deepak Verma",
        "victim_phone": "9822019482",
        "victim_city": "Gurugram",
        "victim_state": "Haryana",
        "utr_number": "774102981234",
        "source_bank": "HDFC Bank",
        "source_account": "XXXX-XXXX-8812",
        "suspect_account": "482910481024",
        "loss_amount": 210000.0,
        "amount": 210000.0,
        "crime_category": "PART_TIME_JOB",
        "narrative": "Telegram group promised high returns on hotel reviews. Funds layered through 3 mule hops within 6 minutes.",
        "status": "MICRO_HOLD_PLACED",
        "hold_status": "ACTIVE_30_MIN_HOLD",
        "execution_latency_ms": 78.4,
        "candidate_atms": [
            { "name": "HDFC Bank ATM Laxmi Nagar", "bank_name": "HDFC ATM Laxmi Nagar", "address": "Laxmi Nagar Metro, New Delhi", "lat": 28.6304, "lon": 77.2773, "eta_minutes": 5, "risk_score": "94.2%" }
        ],
        "terminal_node": {
            "account_id": "ACC_MULE_4829",
            "masked_account": "482910481024",
            "bank_name": "ICICI Bank Ltd",
            "ifsc": "ICIC0002941",
            "region": "Laxmi Nagar, Delhi",
            "state": "Delhi",
            "latitude": 28.6304,
            "longitude": 77.2773,
            "atm_name": "HDFC Bank ATM Laxmi Nagar"
        },
        "evidence_certificate": {
            "sha256_case_hash": "0x6b8c2d1a4e3f5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
            "merkle_root": "0x6b8c2d1a4e3f5a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
            "polygon_tx_hash": "0x3b81928471928471928471928471928471928471928471928471928471928471",
            "block_number": 4920195
        }
    },
    {
        "case_id": "DURGAM-KA-5591",
        "ack_number": "NCRP-1930-55910248",
        "complaint_id": "NCRP-1930-55910248",
        "victim_name": "Suhani Sharma",
        "victim_phone": "9833019483",
        "victim_city": "Bengaluru",
        "victim_state": "Karnataka",
        "utr_number": "661029481233",
        "source_bank": "ICICI Bank",
        "source_account": "XXXX-XXXX-3341",
        "suspect_account": "551029841923",
        "loss_amount": 185000.0,
        "amount": 185000.0,
        "crime_category": "FAKE_LOAN_APP",
        "narrative": "Predatory instant loan app accessed contacts and blackmailed victim. Auto-lien locked terminal mule.",
        "status": "MICRO_HOLD_PLACED",
        "hold_status": "ACTIVE_30_MIN_HOLD",
        "execution_latency_ms": 94.1,
        "candidate_atms": [
            { "name": "Axis Bank ATM Indiranagar", "bank_name": "Axis Bank ATM", "address": "100ft Road, Indiranagar, Bengaluru", "lat": 12.9784, "lon": 77.6408, "eta_minutes": 6, "risk_score": "91.8%" }
        ],
        "terminal_node": {
            "account_id": "ACC_MULE_5510",
            "masked_account": "551029841923",
            "bank_name": "Canara Bank",
            "ifsc": "CNRB0008819",
            "region": "Indiranagar, Bengaluru",
            "state": "Karnataka",
            "latitude": 12.9784,
            "longitude": 77.6408,
            "atm_name": "Axis Bank ATM Indiranagar"
        },
        "evidence_certificate": {
            "sha256_case_hash": "0x5c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d",
            "merkle_root": "0x5c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d",
            "polygon_tx_hash": "0x2c71928471928471928471928471928471928471928471928471928471928471",
            "block_number": 4920196
        }
    },
    {
        "case_id": "DURGAM-MH-4482",
        "ack_number": "NCRP-1930-44820194",
        "complaint_id": "NCRP-1930-44820194",
        "victim_name": "Himanshi Rawat",
        "victim_phone": "9844019484",
        "victim_city": "Mumbai",
        "victim_state": "Maharashtra",
        "utr_number": "229481029344",
        "source_bank": "Punjab National Bank",
        "source_account": "XXXX-XXXX-9901",
        "suspect_account": "882019481022",
        "loss_amount": 420000.0,
        "amount": 420000.0,
        "crime_category": "INVESTMENT_SCAM",
        "narrative": "Fake institutional trading portal showing fabricated profits. Quarantined in PNB clearing switch within 89ms.",
        "status": "MICRO_HOLD_PLACED",
        "hold_status": "ACTIVE_30_MIN_HOLD",
        "execution_latency_ms": 86.7,
        "candidate_atms": [
            { "name": "ICICI Bank ATM Nariman Point", "bank_name": "ICICI ATM Nariman Point", "address": "Nariman Point, South Mumbai", "lat": 18.9256, "lon": 72.8242, "eta_minutes": 4, "risk_score": "95.0%" }
        ],
        "terminal_node": {
            "account_id": "ACC_MULE_8820",
            "masked_account": "882019481022",
            "bank_name": "Bank of Baroda",
            "ifsc": "BARB0NARIMA",
            "region": "Nariman Point, Mumbai",
            "state": "Maharashtra",
            "latitude": 18.9256,
            "longitude": 72.8242,
            "atm_name": "ICICI Bank ATM Nariman Point"
        },
        "evidence_certificate": {
            "sha256_case_hash": "0x4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c",
            "merkle_root": "0x4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8f0a2b4c6d8e0f2a4b6c",
            "polygon_tx_hash": "0x1b61928471928471928471928471928471928471928471928471928471928471",
            "block_number": 4920197
        }
    },
    {
        "case_id": "DURGAM-JK-3371",
        "ack_number": "NCRP-1930-33719028",
        "complaint_id": "NCRP-1930-33719028",
        "victim_name": "Eklavya Dhruv Malhotra",
        "victim_phone": "9855019485",
        "victim_city": "Jammu",
        "victim_state": "Jammu & Kashmir",
        "utr_number": "339102948110",
        "source_bank": "Axis Bank",
        "source_account": "XXXX-XXXX-6623",
        "suspect_account": "771029481944",
        "loss_amount": 290000.0,
        "amount": 290000.0,
        "crime_category": "AEPS_FRAUD",
        "narrative": "Unauthorized biometric cashout alert triggered at Jammu corridor CSP kiosk. PCR Falcon 1 dispatched.",
        "status": "MICRO_HOLD_PLACED",
        "hold_status": "ACTIVE_30_MIN_HOLD",
        "execution_latency_ms": 91.3,
        "candidate_atms": [
            { "name": "J&K Bank ATM Residency Road", "bank_name": "J&K Bank ATM", "address": "Residency Road, Jammu", "lat": 32.7266, "lon": 74.8570, "eta_minutes": 3, "risk_score": "97.4%" }
        ],
        "terminal_node": {
            "account_id": "ACC_MULE_7710",
            "masked_account": "771029481944",
            "bank_name": "J&K Bank Ltd",
            "ifsc": "JAKO0RESIDN",
            "region": "Residency Road, Jammu",
            "state": "Jammu & Kashmir",
            "latitude": 32.7266,
            "longitude": 74.8570,
            "atm_name": "J&K Bank ATM Residency Road"
        },
        "evidence_certificate": {
            "sha256_case_hash": "0x3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b",
            "merkle_root": "0x3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7e9f1a3b5c7d9e1f3a5b",
            "polygon_tx_hash": "0x0a51928471928471928471928471928471928471928471928471928471928471",
            "block_number": 4920198
        }
    }
]

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for c in COMPLAINTS_TO_SEED:
        now = time.time()
        c["created_at"] = now
        nodes_json = json.dumps(c.get("nodes", [
            { "id": "0", "label": "Source: Remitter", "bank": c["source_bank"], "account": c["source_account"], "type": "Savings", "amount": f"₹{c['loss_amount']:,.0f}", "risk": "Source Remitter" },
            { "id": "1", "label": "Hop 1: Layer 1 Mule", "bank": "PNB (Mewat)", "account": c["suspect_account"], "type": "Current", "amount": f"₹{c['loss_amount']*0.98:,.0f}", "risk": "94% Mule Risk" },
            { "id": "2", "label": "Hop 2: Terminal Kiosk", "bank": c["terminal_node"]["bank_name"], "account": c["terminal_node"]["masked_account"], "type": "ATM Kiosk", "amount": f"₹{c['loss_amount']:,.0f}", "risk": "✓ MICRO-HOLD (89ms)" }
        ]))
        terminal_json = json.dumps(c["terminal_node"])
        extra_json = json.dumps({
            "candidate_atms": c["candidate_atms"],
            "evidence_certificate": c["evidence_certificate"],
            "hold_status": c["hold_status"],
            "suspect_account": c["suspect_account"],
            "amount": c["amount"]
        })
        
        cursor.execute("""
            INSERT OR REPLACE INTO incidents 
            (case_id, ack_number, victim_name, victim_phone, victim_city, victim_state, utr_number, source_bank, source_account, loss_amount, crime_category, narrative, status, execution_latency_ms, nodes_json, terminal_node_json, extra_data_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c["case_id"],
            c["ack_number"],
            c["victim_name"],
            c["victim_phone"],
            c["victim_city"],
            c["victim_state"],
            c["utr_number"],
            c["source_bank"],
            c["source_account"],
            c["loss_amount"],
            c["crime_category"],
            c["narrative"],
            c["status"],
            c["execution_latency_ms"],
            nodes_json,
            terminal_json,
            extra_json,
            now
        ))
        
    conn.commit()
    conn.close()
    print(f"Successfully seeded {len(COMPLAINTS_TO_SEED)} complaints into SQLite {DB_PATH}")

if __name__ == "__main__":
    seed_database()
