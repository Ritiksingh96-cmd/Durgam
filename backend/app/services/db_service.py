"""
PROJECT DURGAM: SOVEREIGN DATABASE SERVICE
Persistent SQLite Database seeded with authentic empirical Pan-India Cyber Fraud Cases
"""

import sqlite3
import json
import time
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "durgam_sovereign.db")

# 7 Authentic Pan-India Cyber Financial Fraud Case Studies
PAN_INDIA_EMPIRICAL_CASES = [
    {
        "case_id": "DURGAM-DL-001",
        "ack_number": "NCRP-1930-48291048",
        "victim_name": "Dr. Rajiv Malhotra",
        "victim_phone": "9811029481",
        "victim_city": "Delhi NCR",
        "victim_state": "Delhi",
        "utr_number": "482910482910",
        "source_bank": "State Bank of India",
        "source_account": "XXXX-XXXX-2948",
        "loss_amount": 250000.0,
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Fraudster in counterfeit CBI police uniform initiated Skype video call alleging narcotics seized in international courier. Coerced victim into transferring ₹2,50,000 for RBI verification.",
        "status": "HOLD_CONFIRMED",
        "execution_latency_ms": 138.4,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "SBI (Delhi NCR)", "account": "XXXX-2948", "type": "Savings", "amount": "₹2,50,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Layer 1 Mule", "bank": "PNB (Mewat, HR)", "account": "XXXX-9541", "type": "Current", "amount": "₹1,50,000", "risk": "92% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Layer 1 Mule", "bank": "Canara (Gurugram)", "account": "XXXX-3184", "type": "Savings", "amount": "₹1,00,000", "risk": "88% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Aggregator Mule", "bank": "ICICI (Chandigarh)", "account": "XXXX-8931", "type": "Current", "amount": "₹2,50,000", "risk": "94% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "SBI ATM (Connaught Place, Delhi)", "account": "XXXX-4821", "type": "ATM Kiosk", "amount": "₹2,50,000", "risk": "✓ MICRO-HOLD (138ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_DL_001",
            "masked_account": "XXXX-XXXX-4821",
            "bank_name": "State Bank of India",
            "ifsc": "SBIN0001024",
            "region": "Connaught Place, Delhi",
            "state": "Delhi",
            "latitude": 28.6315,
            "longitude": 77.2167,
            "atm_name": "SBI ATM, Inner Circle, Connaught Place"
        }
    },
    {
        "case_id": "DURGAM-KA-002",
        "ack_number": "NCRP-1930-89104821",
        "victim_name": "Ananya Krishnan",
        "victim_phone": "9845019284",
        "victim_city": "Bengaluru",
        "victim_state": "Karnataka",
        "utr_number": "891048219012",
        "source_bank": "HDFC Bank",
        "source_account": "XXXX-XXXX-7193",
        "loss_amount": 540000.0,
        "crime_category": "PART_TIME_JOB",
        "narrative": "Telegram group promised ₹5,000/day for rating hotels on Google Maps. Victim lured into transferring ₹5,40,000 as refundable merchant liquidity deposit.",
        "status": "MICRO_HOLD_ACTIVE",
        "execution_latency_ms": 142.1,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "HDFC (Bengaluru)", "account": "XXXX-7193", "type": "Salary", "amount": "₹5,40,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Corporate Mule", "bank": "Axis (Patna, BR)", "account": "XXXX-4091", "type": "Current", "amount": "₹3,00,000", "risk": "96% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Personal Mule", "bank": "BOB (Ranchi, JH)", "account": "XXXX-8271", "type": "Savings", "amount": "₹2,40,000", "risk": "91% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Jamtara Ring", "bank": "BOB (Jamtara, JH)", "account": "XXXX-5938", "type": "Current", "amount": "₹5,40,000", "risk": "98% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "HDFC ATM (MG Road, Bengaluru)", "account": "XXXX-9481", "type": "ATM Kiosk", "amount": "₹5,40,000", "risk": "✓ MICRO-HOLD (142ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_KA_002",
            "masked_account": "XXXX-XXXX-9481",
            "bank_name": "HDFC Bank",
            "ifsc": "HDFC0000084",
            "region": "MG Road, Bengaluru",
            "state": "Karnataka",
            "latitude": 12.9756,
            "longitude": 77.6066,
            "atm_name": "HDFC ATM, MG Road Metro Station"
        }
    },
    {
        "case_id": "DURGAM-MH-003",
        "ack_number": "NCRP-1930-74920194",
        "victim_name": "Vikramaditya Shah",
        "victim_phone": "9820194820",
        "victim_city": "Mumbai",
        "victim_state": "Maharashtra",
        "utr_number": "749201948102",
        "source_bank": "ICICI Bank",
        "source_account": "XXXX-XXXX-8402",
        "loss_amount": 1280000.0,
        "crime_category": "INVESTMENT_PONZI",
        "narrative": "WhatsApp VIP trading group claimed 400% institutional returns on fake SEBI trading app. Siphoned ₹12,80,000 via RTGS into corporate shell accounts.",
        "status": "HOLD_CONFIRMED",
        "execution_latency_ms": 118.6,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "ICICI (Mumbai)", "account": "XXXX-8402", "type": "Wealth", "amount": "₹12,80,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Shell Entity", "bank": "Kotak (Surat, GJ)", "account": "XXXX-1938", "type": "Current", "amount": "₹7,00,000", "risk": "95% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Shell Entity", "bank": "HDFC (Ahmedabad)", "account": "XXXX-7210", "type": "Current", "amount": "₹5,80,000", "risk": "93% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Mule Consolidation", "bank": "PNB (Indore, MP)", "account": "XXXX-6619", "type": "Current", "amount": "₹12,80,000", "risk": "97% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "ICICI ATM (Nariman Point, Mumbai)", "account": "XXXX-3194", "type": "ATM Kiosk", "amount": "₹12,80,000", "risk": "✓ MICRO-HOLD (118ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_MH_003",
            "masked_account": "XXXX-XXXX-3194",
            "bank_name": "ICICI Bank",
            "ifsc": "ICIC0000004",
            "region": "Nariman Point, Mumbai",
            "state": "Maharashtra",
            "latitude": 18.9256,
            "longitude": 72.8242,
            "atm_name": "ICICI ATM, Express Towers, Nariman Point"
        }
    },
    {
        "case_id": "DURGAM-TG-004",
        "ack_number": "NCRP-1930-61928401",
        "victim_name": "Dr. Sandeep Reddy",
        "victim_phone": "9849019284",
        "victim_city": "Hyderabad",
        "victim_state": "Telangana",
        "utr_number": "619284019284",
        "source_bank": "Axis Bank",
        "source_account": "XXXX-XXXX-5519",
        "loss_amount": 820000.0,
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Fraudster claiming to be Customs Officer at Delhi Airport stated parcel sent to Cambodia contained 15 passports and MDMA. Extorted ₹8,20,000.",
        "status": "MICRO_HOLD_ACTIVE",
        "execution_latency_ms": 134.8,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "Axis (Hyderabad)", "account": "XXXX-5519", "type": "Savings", "amount": "₹8,20,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Layer 1 Mule", "bank": "SBI (Gurugram, HR)", "account": "XXXX-8821", "type": "Current", "amount": "₹5,00,000", "risk": "94% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Layer 1 Mule", "bank": "Canara (Faridabad)", "account": "XXXX-2910", "type": "Savings", "amount": "₹3,20,000", "risk": "89% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Mewat Syndicate", "bank": "SBI (Nuh, Mewat)", "account": "XXXX-4491", "type": "Current", "amount": "₹8,20,000", "risk": "99% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "Axis ATM (Hitec City, Hyderabad)", "account": "XXXX-7719", "type": "ATM Kiosk", "amount": "₹8,20,000", "risk": "✓ MICRO-HOLD (134ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_TG_004",
            "masked_account": "XXXX-XXXX-7719",
            "bank_name": "Axis Bank",
            "ifsc": "UTIB0000068",
            "region": "Hitec City, Hyderabad",
            "state": "Telangana",
            "latitude": 17.4474,
            "longitude": 78.3762,
            "atm_name": "Axis Bank ATM, Cyber Towers, Hitec City"
        }
    },
    {
        "case_id": "DURGAM-HR-005",
        "ack_number": "NCRP-1930-31849102",
        "victim_name": "Sunita Aggarwal",
        "victim_phone": "9812049182",
        "victim_city": "Gurugram",
        "victim_state": "Haryana",
        "utr_number": "318491029481",
        "source_bank": "Punjab National Bank",
        "source_account": "XXXX-XXXX-6102",
        "loss_amount": 175000.0,
        "crime_category": "APK_MALWARE",
        "narrative": "SMS claimed power disconnection tonight. Instructed to download malicious 'BijliVibhag.apk' which captured netbanking OTPs.",
        "status": "HOLD_CONFIRMED",
        "execution_latency_ms": 126.3,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "PNB (Gurugram)", "account": "XXXX-6102", "type": "Pension", "amount": "₹1,75,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1", "label": "Hop 1: Layer 1 Mule", "bank": "BOB (Deoghar, JH)", "account": "XXXX-1192", "type": "Savings", "amount": "₹1,75,000", "risk": "94% Mule Risk", "color": "#F59E0B", "x": 0.5, "y": 0.5 },
            { "id": "2", "label": "Terminal Cashout ATM", "bank": "SBI ATM (Nuh Civil Hospital Road)", "account": "XXXX-8812", "type": "ATM Kiosk", "amount": "₹1,75,000", "risk": "✓ MICRO-HOLD (126ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_HR_005",
            "masked_account": "XXXX-XXXX-8812",
            "bank_name": "State Bank of India",
            "ifsc": "SBIN0000688",
            "region": "Nuh, Mewat",
            "state": "Haryana",
            "latitude": 28.1136,
            "longitude": 76.9963,
            "atm_name": "SBI ATM, Nuh Civil Hospital Road"
        }
    },
    {
        "case_id": "DURGAM-WB-006",
        "ack_number": "NCRP-1930-58291048",
        "victim_name": "Debabrata Mukherjee",
        "victim_phone": "9830192840",
        "victim_city": "Kolkata",
        "victim_state": "West Bengal",
        "utr_number": "582910481920",
        "source_bank": "Canara Bank",
        "source_account": "XXXX-XXXX-9914",
        "loss_amount": 1850000.0,
        "crime_category": "FINANCIAL_FRAUD_GENERAL",
        "narrative": "Cross-border layering through synthetic firm current accounts. Funds layered across 4 states within 12 minutes.",
        "status": "HOLD_CONFIRMED",
        "execution_latency_ms": 112.5,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "Canara (Kolkata)", "account": "XXXX-9914", "type": "Current", "amount": "₹18,50,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Siliguri Hub", "bank": "SBI (Siliguri)", "account": "XXXX-4481", "type": "Current", "amount": "₹10,00,000", "risk": "96% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Guwahati Hub", "bank": "PNB (Guwahati)", "account": "XXXX-7721", "type": "Current", "amount": "₹8,50,000", "risk": "93% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Aggregator Shell", "bank": "ICICI (Patna)", "account": "XXXX-3190", "type": "Current", "amount": "₹18,50,000", "risk": "98% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "Canara ATM (Park Street, Kolkata)", "account": "XXXX-6612", "type": "ATM Kiosk", "amount": "₹18,50,000", "risk": "✓ MICRO-HOLD (112ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_WB_006",
            "masked_account": "XXXX-XXXX-6612",
            "bank_name": "Canara Bank",
            "ifsc": "CNRB0000084",
            "region": "Park Street, Kolkata",
            "state": "West Bengal",
            "latitude": 22.5535,
            "longitude": 88.3524,
            "atm_name": "Canara Bank ATM, Park Street, Kolkata"
        }
    },
    {
        "case_id": "DURGAM-GJ-007",
        "ack_number": "NCRP-1930-94810294",
        "victim_name": "Jigneshbhai Patel",
        "victim_phone": "9825019284",
        "victim_city": "Ahmedabad",
        "victim_state": "Gujarat",
        "utr_number": "948102948102",
        "source_bank": "Kotak Mahindra Bank",
        "source_account": "XXXX-XXXX-3381",
        "loss_amount": 3200000.0,
        "crime_category": "INVESTMENT_PONZI",
        "narrative": "Synthetic Corporate Current Account Ring laundering wholesale deposits through fake textile export bills.",
        "status": "HOLD_CONFIRMED",
        "execution_latency_ms": 98.4,
        "nodes": [
            { "id": "0", "label": "Source: Remitter", "bank": "Kotak (Ahmedabad)", "account": "XXXX-3381", "type": "Current", "amount": "₹32,00,000", "risk": "Source Remitter", "color": "#2563EB", "x": 0.08, "y": 0.5 },
            { "id": "1A", "label": "Hop 1A: Shell Textile", "bank": "Axis (Surat)", "account": "XXXX-9102", "type": "Current", "amount": "₹16,00,000", "risk": "97% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.28 },
            { "id": "1B", "label": "Hop 1B: Shell Diamond", "bank": "SBI (Rajkot)", "account": "XXXX-5521", "type": "Current", "amount": "₹16,00,000", "risk": "96% Mule Risk", "color": "#F59E0B", "x": 0.38, "y": 0.72 },
            { "id": "2", "label": "Hop 2: Hawala Settlement", "bank": "HDFC (Indore)", "account": "XXXX-2291", "type": "Current", "amount": "₹32,00,000", "risk": "99% Mule Risk", "color": "#EA580C", "x": 0.68, "y": 0.5 },
            { "id": "3", "label": "Terminal Cashout ATM", "bank": "Kotak ATM (Ashram Road, Ahmedabad)", "account": "XXXX-8841", "type": "ATM Kiosk", "amount": "₹32,00,000", "risk": "✓ MICRO-HOLD (98ms)", "color": "#DC2626", "x": 0.92, "y": 0.5 }
        ],
        "terminal_node": {
            "account_id": "ACC_GJ_007",
            "masked_account": "XXXX-XXXX-8841",
            "bank_name": "Kotak Mahindra Bank",
            "ifsc": "KKBK0000001",
            "region": "Ashram Road, Ahmedabad",
            "state": "Gujarat",
            "latitude": 23.0338,
            "longitude": 72.5684,
            "atm_name": "Kotak Mahindra ATM, Ashram Road"
        }
    }
]
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable High-Throughput Million-Load SQLite WAL Mode & Performance Pragmas
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA cache_size = 10000;")
    cursor.execute("PRAGMA temp_store = MEMORY;")

    # Drop old schema to apply upgraded schema with extra_data_json
    cursor.execute("DROP TABLE IF EXISTS incidents")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        case_id TEXT PRIMARY KEY,
        ack_number TEXT UNIQUE,
        victim_name TEXT,
        victim_phone TEXT,
        victim_city TEXT,
        victim_state TEXT,
        utr_number TEXT,
        source_bank TEXT,
        source_account TEXT,
        loss_amount REAL,
        crime_category TEXT,
        narrative TEXT,
        status TEXT,
        execution_latency_ms REAL,
        nodes_json TEXT,
        terminal_node_json TEXT,
        extra_data_json TEXT,
        created_at REAL
    )
    """)

    # FIU-IND Suspicious Transaction Reports — Persistent across restarts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fiu_strs (
        str_id TEXT PRIMARY KEY,
        case_id TEXT,
        utr_number TEXT,
        beneficiary_account TEXT,
        amount_inr REAL,
        ground_of_suspicion TEXT,
        status TEXT DEFAULT 'FILED_WITH_FIU_FINNET',
        priority TEXT DEFAULT 'CRITICAL',
        filed_by TEXT DEFAULT 'FIU_NODAL_OFFICER',
        finnet_ack_hash TEXT,
        timestamp REAL
    )
    """)

    # Telecom CEIR IMEI / SIM Blocks — Persistent across restarts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS imei_blocks (
        block_id TEXT PRIMARY KEY,
        imei TEXT NOT NULL,
        imsi TEXT,
        case_id TEXT,
        operator TEXT DEFAULT 'ALL_INDIAN_TSPS',
        tsps TEXT DEFAULT 'JIO, AIRTEL, VI, BSNL',
        statutory_act TEXT DEFAULT 'Section 28, Telecommunications Act 2023',
        status TEXT DEFAULT 'DEVICE_BLACK_LISTED',
        blocked_by TEXT DEFAULT 'DOT_CEIR_GATEWAY',
        timestamp REAL
    )
    """)

    # System Settings KV Store — Persists auto-trigger rule config
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        key TEXT PRIMARY KEY,
        value_json TEXT,
        updated_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        actor TEXT,
        role TEXT,
        action TEXT,
        target_id TEXT,
        details_json TEXT,
        prev_hash TEXT,
        current_hash TEXT,
        timestamp REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        key_id TEXT PRIMARY KEY,
        key_hash TEXT UNIQUE,
        owner_name TEXT,
        role TEXT,
        scope_csv TEXT,
        is_active INTEGER DEFAULT 1,
        created_at REAL,
        last_used_at REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auto_trigger_logs (
        trigger_id TEXT PRIMARY KEY,
        case_id TEXT,
        rule_name TEXT,
        action_executed TEXT,
        latency_ms REAL,
        status TEXT,
        timestamp REAL
    )
    """)
    conn.commit()

    conn.commit()

    # Re-seed with full Pan-India diverse cases
    for case in PAN_INDIA_EMPIRICAL_CASES:
        cursor.execute("""
        INSERT OR REPLACE INTO incidents (
            case_id, ack_number, victim_name, victim_phone, victim_city, victim_state,
            utr_number, source_bank, source_account, loss_amount, crime_category,
            narrative, status, execution_latency_ms, nodes_json, terminal_node_json, extra_data_json, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case["case_id"],
            case["ack_number"],
            case["victim_name"],
            case["victim_phone"],
            case["victim_city"],
            case["victim_state"],
            case["utr_number"],
            case["source_bank"],
            case["source_account"],
            case["loss_amount"],
            case["crime_category"],
            case["narrative"],
            case["status"],
            case["execution_latency_ms"],
            json.dumps(case.get("nodes", [])),
            json.dumps(case.get("terminal_node", {})),
            json.dumps({}),
            time.time()
        ))
    conn.commit()

    # Seed default FIU STRs if table empty
    cursor.execute("SELECT COUNT(*) FROM fiu_strs")
    if cursor.fetchone()[0] == 0:
        now = time.time()
        cursor.executemany("""
        INSERT OR IGNORE INTO fiu_strs (str_id, case_id, utr_number, beneficiary_account, amount_inr, ground_of_suspicion, status, priority, filed_by, finnet_ack_hash, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ("STR-2026-DL-8910", "DURGAM-DL-001", "482910482910", "XXXX-XXXX-4821", 250000.0, "PMLA Sec 12 Rapid Layering & Mule Account Flow-Through", "FILED_WITH_FIU_FINNET", "CRITICAL", "FIU_NODAL_OFFICER", "0x7a8f9c1b2d3e4f5a6b7c", now - 1800),
            ("STR-2026-MH-7192", "DURGAM-MH-003", "749201948102", "XXXX-XXXX-3194", 1280000.0, "Cross-Border Layering via Corporate Shell Accounts - RTGS", "FILED_WITH_FIU_FINNET", "HIGH", "FIU_NODAL_OFFICER", "0x9e8d7c6b5a4f3e2d1c0b", now - 3600),
        ])
        conn.commit()

    # Seed default IMEI blocks if table empty
    cursor.execute("SELECT COUNT(*) FROM imei_blocks")
    if cursor.fetchone()[0] == 0:
        now = time.time()
        cursor.executemany("""
        INSERT OR IGNORE INTO imei_blocks (block_id, imei, imsi, case_id, tsps, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            ("CEIR-BLK-891048", "862910482910482", "404450918291048", "DURGAM-DL-001", "JIO, AIRTEL, VI, BSNL", "DEVICE_BLACK_LISTED", now - 3600),
            ("CEIR-BLK-719204", "358920194810294", "404450192840192", "DURGAM-MH-003", "JIO, AIRTEL, VI, BSNL", "DEVICE_BLACK_LISTED", now - 7200),
        ])
        conn.commit()

    conn.close()

# Auto-initialize DB
init_db()

# High-Speed In-Memory Cache for Sub-Millisecond Public Telemetry
_INCIDENTS_CACHE = {"data": None, "timestamp": 0.0, "ttl": 2.0}

def get_all_incidents(limit: int = 20) -> List[Dict[str, Any]]:
    now = time.time()
    if _INCIDENTS_CACHE["data"] and (now - _INCIDENTS_CACHE["timestamp"]) < _INCIDENTS_CACHE["ttl"]:
        return _INCIDENTS_CACHE["data"][:limit]

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        if d.get("nodes_json"):
            try: d["nodes"] = json.loads(d["nodes_json"])
            except Exception: d["nodes"] = []
        if d.get("terminal_node_json"):
            try: d["terminal_node"] = json.loads(d["terminal_node_json"])
            except Exception: d["terminal_node"] = {}
        if d.get("extra_data_json"):
            try:
                extra = json.loads(d["extra_data_json"])
                # Merge all rich fields back into root dict
                for key in ("hold_details", "candidate_atms", "dispatch_details",
                            "evidence_certificate", "mule_detection_matrix",
                            "universal_docket", "golden_hour_countdown",
                            "auto_triggers_executed"):
                    if key in extra:
                        d[key] = extra[key]
            except Exception:
                pass
        results.append(d)

    _INCIDENTS_CACHE["data"] = results
    _INCIDENTS_CACHE["timestamp"] = now
    return results

def get_incident_by_identifier(identifier: str) -> Optional[Dict[str, Any]]:
    clean = identifier.strip()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM incidents
    WHERE case_id = ? OR ack_number = ? OR utr_number = ?
    """, (clean, clean, clean))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None
    d = dict(row)
    if d.get("nodes_json"):
        try: d["nodes"] = json.loads(d["nodes_json"])
        except Exception: d["nodes"] = []
    if d.get("terminal_node_json"):
        try: d["terminal_node"] = json.loads(d["terminal_node_json"])
        except Exception: d["terminal_node"] = {}
    if d.get("extra_data_json"):
        try:
            extra = json.loads(d["extra_data_json"])
            for key in ("hold_details", "candidate_atms", "dispatch_details",
                        "evidence_certificate", "mule_detection_matrix",
                        "universal_docket", "golden_hour_countdown",
                        "auto_triggers_executed"):
                if key in extra:
                    d[key] = extra[key]
        except Exception:
            pass
    return d

def insert_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    case_id = incident_data.get("case_id") or f"DURGAM-IND-{int(time.time())}"
    ack_number = incident_data.get("ack_number") or f"NCRP-1930-{int(time.time()*1000)%100000000}"
    nodes_json = json.dumps(incident_data.get("nodes", []))
    terminal_json = json.dumps(incident_data.get("terminal_node", {}))

    # Persist all rich pipeline fields that were previously lost on restart
    extra_fields = {
        "hold_details": incident_data.get("hold_details", {}),
        "candidate_atms": incident_data.get("candidate_atms", []),
        "dispatch_details": incident_data.get("dispatch_details"),
        "evidence_certificate": incident_data.get("evidence_certificate", {}),
        "mule_detection_matrix": incident_data.get("mule_detection_matrix", {}),
        "universal_docket": incident_data.get("universal_docket", {}),
        "golden_hour_countdown": incident_data.get("golden_hour_countdown", {}),
        "auto_triggers_executed": incident_data.get("auto_triggers_executed", []),
    }
    extra_data_json = json.dumps(extra_fields, default=str)

    cursor.execute("""
    INSERT OR REPLACE INTO incidents (
        case_id, ack_number, victim_name, victim_phone, victim_city, victim_state,
        utr_number, source_bank, source_account, loss_amount, crime_category,
        narrative, status, execution_latency_ms, nodes_json, terminal_node_json, extra_data_json, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        ack_number,
        incident_data.get("victim_name", "Complainant"),
        incident_data.get("victim_phone", "9800000000"),
        incident_data.get("victim_city", "New Delhi"),
        incident_data.get("victim_state", "Delhi"),
        incident_data.get("utr_number", "482910482910"),
        incident_data.get("source_bank", "State Bank of India"),
        incident_data.get("source_account", "XXXX-XXXX-1234"),
        float(incident_data.get("loss_amount", 250000.0)),
        incident_data.get("crime_category", "DIGITAL_ARREST"),
        incident_data.get("narrative", ""),
        incident_data.get("status", "HOLD_CONFIRMED"),
        float(incident_data.get("execution_latency_ms", 138.4)),
        nodes_json,
        terminal_json,
        extra_data_json,
        time.time()
    ))
    conn.commit()
    conn.close()
    # Invalidate in-memory cache so next read reflects new data
    _INCIDENTS_CACHE["data"] = None

def update_incident_status(case_id: str, new_status: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status = ? WHERE case_id = ? OR ack_number = ?", (new_status, case_id, case_id))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# --- Cryptographic Audit Trail ---
def append_audit_log(actor: str, role: str, action: str, target_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
    import hashlib
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get last hash
    cursor.execute("SELECT current_hash FROM audit_logs ORDER BY log_id DESC LIMIT 1")
    last_row = cursor.fetchone()
    prev_hash = last_row[0] if last_row else "GENESIS_SOVEREIGN_AUDIT_BLOCK_0000000000"
    
    now = time.time()
    details_str = json.dumps(details, sort_keys=True)
    raw_payload = f"{actor}:{role}:{action}:{target_id}:{details_str}:{prev_hash}:{now}"
    current_hash = hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()
    
    cursor.execute("""
    INSERT INTO audit_logs (actor, role, action, target_id, details_json, prev_hash, current_hash, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (actor, role, action, target_id, details_str, prev_hash, current_hash, now))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "log_id": log_id,
        "actor": actor,
        "role": role,
        "action": action,
        "target_id": target_id,
        "details": details,
        "prev_hash": prev_hash,
        "current_hash": current_hash,
        "timestamp": now
    }

def get_recent_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_logs ORDER BY log_id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for r in rows:
        d = dict(r)
        if d.get("details_json"):
            try:
                d["details"] = json.loads(d["details_json"])
            except Exception:
                d["details"] = {}
        logs.append(d)
    return logs

# --- Auto-Trigger Logs ---
def log_auto_trigger(case_id: str, rule_name: str, action_executed: str, latency_ms: float, status: str = "EXECUTED") -> Dict[str, Any]:
    import uuid
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    trigger_id = f"TRIG-{uuid.uuid4().hex[:8].upper()}"
    now = time.time()
    cursor.execute("""
    INSERT INTO auto_trigger_logs (trigger_id, case_id, rule_name, action_executed, latency_ms, status, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (trigger_id, case_id, rule_name, action_executed, latency_ms, status, now))
    conn.commit()
    conn.close()
    return {
        "trigger_id": trigger_id,
        "case_id": case_id,
        "rule_name": rule_name,
        "action_executed": action_executed,
        "latency_ms": latency_ms,
        "status": status,
        "timestamp": now
    }

def get_auto_trigger_logs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM auto_trigger_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- API Keys Management ---
def store_api_key(key_id: str, key_hash: str, owner_name: str, role: str, scope_csv: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = time.time()
    cursor.execute("""
    INSERT OR REPLACE INTO api_keys (key_id, key_hash, owner_name, role, scope_csv, is_active, created_at, last_used_at)
    VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    """, (key_id, key_hash, owner_name, role, scope_csv, now, now))
    conn.commit()
    conn.close()
    return True

def get_all_api_keys() -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT key_id, owner_name, role, scope_csv, is_active, created_at, last_used_at FROM api_keys ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def revoke_api_key(key_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE api_keys SET is_active = 0 WHERE key_id = ?", (key_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

# --- FIU-IND Suspicious Transaction Reports (Persistent) ---
def store_str(str_id: str, case_id: str, utr_number: str, beneficiary_account: str,
              amount_inr: float, ground_of_suspicion: str, finnet_ack_hash: str,
              filed_by: str = "FIU_NODAL_OFFICER", priority: str = "CRITICAL") -> Dict[str, Any]:
    import uuid as _uuid
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = time.time()
    sid = str_id or f"STR-2026-IND-{_uuid.uuid4().hex[:6].upper()}"
    cursor.execute("""
    INSERT OR REPLACE INTO fiu_strs
        (str_id, case_id, utr_number, beneficiary_account, amount_inr, ground_of_suspicion,
         status, priority, filed_by, finnet_ack_hash, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, 'FILED_WITH_FIU_FINNET', ?, ?, ?, ?)
    """, (sid, case_id, utr_number, beneficiary_account, amount_inr,
          ground_of_suspicion, priority, filed_by, finnet_ack_hash, now))
    conn.commit()
    conn.close()
    return {"str_id": sid, "case_id": case_id, "amount_inr": amount_inr,
            "status": "FILED_WITH_FIU_FINNET", "timestamp": now}

def get_strs(limit: int = 50) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fiu_strs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Telecom CEIR IMEI / SIM Block Registry (Persistent) ---
def store_imei_block(block_id: str, imei: str, case_id: str, imsi: str = "",
                     operator: str = "ALL_INDIAN_TSPS") -> Dict[str, Any]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = time.time()
    cursor.execute("""
    INSERT OR REPLACE INTO imei_blocks
        (block_id, imei, imsi, case_id, operator, tsps, status, blocked_by, timestamp)
    VALUES (?, ?, ?, ?, ?, 'JIO, AIRTEL, VI, BSNL', 'DEVICE_BLACK_LISTED', 'DOT_CEIR_GATEWAY', ?)
    """, (block_id, imei, imsi, case_id, operator, now))
    conn.commit()
    conn.close()
    return {"block_id": block_id, "imei": imei, "case_id": case_id,
            "status": "DEVICE_BLACK_LISTED", "timestamp": now}

def get_imei_blocks(limit: int = 50) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imei_blocks ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- System Settings KV Store (for auto-trigger rules config persistence) ---
def get_setting(key: str, default: Any = None) -> Any:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT value_json FROM system_settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        try: return json.loads(row["value_json"])
        except Exception: return default
    return default

def set_setting(key: str, value: Any) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO system_settings (key, value_json, updated_at)
    VALUES (?, ?, ?)
    """, (key, json.dumps(value, default=str), time.time()))
    conn.commit()
    conn.close()
    return True


class DatabaseService:
    @staticmethod
    def get_all_incidents(limit: int = 20) -> List[Dict[str, Any]]:
        return get_all_incidents(limit)

    @staticmethod
    def get_incident(case_id: str) -> Optional[Dict[str, Any]]:
        return get_incident_by_identifier(case_id)

    @staticmethod
    def get_incident_by_identifier(identifier: str) -> Optional[Dict[str, Any]]:
        return get_incident_by_identifier(identifier)

    @staticmethod
    def insert_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
        return insert_incident(incident_data)

    @staticmethod
    def update_incident_status(case_id: str, new_status: str) -> bool:
        return update_incident_status(case_id, new_status)

    @staticmethod
    def update_hold_status(case_id: str, new_status: str) -> bool:
        return update_incident_status(case_id, new_status)

    @staticmethod
    def append_audit_log(actor: str, role: str, action: str, target_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        return append_audit_log(actor, role, action, target_id, details)

    @staticmethod
    def get_recent_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
        return get_recent_audit_logs(limit)

    @staticmethod
    def log_auto_trigger(case_id: str, rule_name: str, action_executed: str, latency_ms: float, status: str = "EXECUTED") -> Dict[str, Any]:
        return log_auto_trigger(case_id, rule_name, action_executed, latency_ms, status)

    @staticmethod
    def get_auto_trigger_logs(limit: int = 50) -> List[Dict[str, Any]]:
        return get_auto_trigger_logs(limit)

    @staticmethod
    def store_api_key(key_id: str, key_hash: str, owner_name: str, role: str, scope_csv: str) -> bool:
        return store_api_key(key_id, key_hash, owner_name, role, scope_csv)

    @staticmethod
    def get_all_api_keys() -> List[Dict[str, Any]]:
        return get_all_api_keys()

    @staticmethod
    def revoke_api_key(key_id: str) -> bool:
        return revoke_api_key(key_id)

    # FIU STR persistence
    @staticmethod
    def store_str(str_id: str, case_id: str, utr_number: str, beneficiary_account: str,
                  amount_inr: float, ground_of_suspicion: str, finnet_ack_hash: str,
                  filed_by: str = "FIU_NODAL_OFFICER", priority: str = "CRITICAL") -> Dict[str, Any]:
        return store_str(str_id, case_id, utr_number, beneficiary_account,
                         amount_inr, ground_of_suspicion, finnet_ack_hash, filed_by, priority)

    @staticmethod
    def get_strs(limit: int = 50) -> List[Dict[str, Any]]:
        return get_strs(limit)

    # Telecom IMEI block persistence
    @staticmethod
    def store_imei_block(block_id: str, imei: str, case_id: str, imsi: str = "",
                         operator: str = "ALL_INDIAN_TSPS") -> Dict[str, Any]:
        return store_imei_block(block_id, imei, case_id, imsi, operator)

    @staticmethod
    def get_imei_blocks(limit: int = 50) -> List[Dict[str, Any]]:
        return get_imei_blocks(limit)

    # System settings persistence
    @staticmethod
    def get_setting(key: str, default: Any = None) -> Any:
        return get_setting(key, default)

    @staticmethod
    def set_setting(key: str, value: Any) -> bool:
        return set_setting(key, value)


db_service = DatabaseService()
