"""
DURGAM Platform End-to-End Automated Diagnostic Verification Suite
Tests all core FastAPI endpoints:
1. Bank Master Registry & Branch Resolution
2. Real JWT Multi-Role Authentication
3. LightGBM Time-to-Cashout Regressor
4. ST-KDE + XGBoost ATM Cashout Anomaly Predictor
5. ISO 20022 camt.056 Inter-Bank Holds Queue
6. Citizen 1930 Incident Reporting Pipeline
"""

import sys
import os
import requests

BASE_URL = "http://127.0.0.1:8000"

def test_bank_registry():
    print("\n[1/6] Testing Bank Master Registry Endpoint...")
    res = requests.get(f"{BASE_URL}/api/v1/auth/banks")
    assert res.status_code == 200, f"Failed: {res.status_code}"
    data = res.json()
    assert data["total_banks"] >= 7, "Expected at least 7 major banks"
    print(f"  [PASS] SUCCESS: {data['total_banks']} Scheduled Banks retrieved.")

def test_jwt_auth():
    print("\n[2/6] Testing JWT Multi-Role Authentication with Branch Selection...")
    payload = {
        "username": "sbi_nodal_officer",
        "password": "password123",
        "role": "BANK_NODAL",
        "bank_code": "SBI",
        "branch_code": "SBIN0001024"
    }
    res = requests.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
    assert res.status_code == 200, f"Login failed: {res.text}"
    data = res.json()
    assert "access_token" in data, "No access token in response"
    assert data["role"] == "BANK_NODAL"
    print(f"  [PASS] SUCCESS: JWT Token issued for {data['full_name']} [{data['jurisdiction']}].")
    return data["access_token"]

def test_time_to_cashout_ai():
    print("\n[3/6] Testing LightGBM Time-to-Cashout Regressor...")
    payload = {
        "hop_level": 2,
        "total_amount": 250000.0,
        "avg_hop_velocity": 1400.0,
        "time_elapsed_mins": 4.5,
        "channel_type": "UPI"
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/predict-time-to-cashout", json=payload)
    assert res.status_code == 200, f"AI Regressor failed: {res.text}"
    data = res.json()
    assert data["status"] == "SUCCESS"
    pred = data["time_prediction"]
    print(f"  [PASS] SUCCESS: Predicted Golden Hour Window: {pred['estimated_minutes_remaining']} mins | Urgency: {pred['golden_hour_urgency']}.")

def test_case_trajectory_ai():
    print("\n[4/6] Testing Unified Case Trajectory & ATM Anomaly Forecaster...")
    payload = {
        "case_id": "DURGAM-DL-001",
        "victim_state": "Delhi",
        "loss_amount": 250000.0,
        "mule_bank": "SBI",
        "mule_city": "Delhi",
        "time_elapsed_mins": 3.2
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/predict-case-trajectory", json=payload)
    assert res.status_code == 200, f"Trajectory failed: {res.text}"
    data = res.json()
    assert len(data["top_candidate_atms"]) > 0, "No candidate ATMs found"
    top_atm = data["top_candidate_atms"][0]
    print(f"  [PASS] SUCCESS: Top Target ATM Identified: {top_atm['name']} ({top_atm['risk_score']*100:.1f}% Risk).")

def test_bank_micro_holds():
    print("\n[5/6] Testing ISO 20022 camt.056 Micro-Hold Retrieval...")
    res = requests.get(f"{BASE_URL}/api/v1/bank/holds")
    assert res.status_code == 200, f"Holds endpoint failed: {res.text}"
    holds = res.json()
    assert len(holds) > 0, "No micro-holds found in database"
    print(f"  [PASS] SUCCESS: {len(holds)} active ISO 20022 inter-bank holds verified.")

def test_citizen_incident_ingestion():
    print("\n[6/6] Testing Citizen 1930 Incident Reporting Pipeline...")
    payload = {
        "victim_name": "Dr. Rajiv Malhotra",
        "victim_phone": "+91 98765 43210",
        "victim_city": "Delhi",
        "victim_state": "Delhi",
        "utr_number": "482910482910",
        "loss_amount": 250000.0,
        "source_bank": "SBI",
        "source_account": "XXXX-XXXX-4821",
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Coerced Skype digital arrest impersonating CBI inspector."
    }
    res = requests.post(f"{BASE_URL}/api/v1/citizen/report-incident", json=payload)
    assert res.status_code == 200, f"Incident report failed: {res.text}"
    data = res.json()
    assert data["case_id"] is not None
    print(f"  [PASS] SUCCESS: Incident Docket Generated: {data['ack_number']} | Case ID: {data['case_id']}.")

def test_multimodal_threat():
    print("\n[7/9] Testing Multi-Vector Deep Learning Threat Classifier...")
    payload = {
        "narrative": "Fake CBI Skype digital arrest warrant demanding funds transfer",
        "voice_stress_score": 0.88,
        "apk_suspicious_permissions_count": 5,
        "c2_ip_flagged": True
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/analyze-multivector-threat", json=payload)
    assert res.status_code == 200, f"Multimodal failed: {res.text}"
    data = res.json()
    assert data["composite_threat_probability"] > 0.70
    print(f"  [PASS] SUCCESS: Multimodal Threat Tier: {data['threat_tier']} ({data['composite_threat_probability']*100:.1f}%).")

def test_video_deepfake_detector():
    print("\n[8/9] Testing Biometric Video Deepfake & Face Swap Detector...")
    payload = {
        "caller_app": "Skype",
        "fps": 30.0,
        "detected_uniform": "Indian Police Uniform / CBI Badge",
        "boundary_blur_score": 0.88,
        "blink_rate_per_min": 4.0,
        "audio_video_phase_lag_ms": 140.0
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/detect-video-deepfake", json=payload)
    assert res.status_code == 200, f"Deepfake failed: {res.text}"
    data = res.json()
    assert data["is_synthetic_deepfake"] is True
    print(f"  [PASS] SUCCESS: Deepfake Probability: {data['deepfake_probability']*100:.1f}% [{data['confidence_tier']}].")

def test_crypto_mixer_tracer():
    print("\n[9/9] Testing Cross-Border Crypto Mixer & Peel Chain Tracer...")
    payload = {
        "tx_hash": "0x8f2a10b492019482910482910482910482910482910482910482910482910",
        "token": "USDT (TRC-20)",
        "amount": 30000.0,
        "hops_count": 3
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/trace-crypto-mixer", json=payload)
    assert res.status_code == 200, f"Mixer trace failed: {res.text}"
    data = res.json()
    assert data["is_mixer_obfuscated"] is True
    print(f"  [PASS] SUCCESS: Crypto Mixer Detected across {data['peel_chain_depth']} Hops | Action: {data['statutory_action']}.")

def test_zk_consortium():
    print("\n[10/10] Testing DPDP-Compliant ZK-Snark Bank Consortium Query Engine...")
    payload = {
        "account_number": "40291048291",
        "ifsc": "SBIN0001024",
        "requesting_bank": "State Bank of India"
    }
    res = requests.post(f"{BASE_URL}/api/v1/bank/zk-consortium-query", json=payload)
    assert res.status_code == 200, f"ZK query failed: {res.text}"
    data = res.json()
    assert data["is_flagged_mule"] is True
    print(f"  [PASS] SUCCESS: ZK Blind Query Result: {data['risk_tier']} | Hash: {data['zk_hash'][:18]}... | Compliance: {data['dpdp_compliance']}.")

def test_apk_threat():
    print("\n[11/11] Testing Dalvik Dex/Smali APK Opcode Threat Classifier...")
    payload = {
        "app_name": "SBI_YONO_Emergency_KYC_Update.apk",
        "package_name": "com.yono.sbi.kyc.stealer",
        "opcodes_str": "invoke-virtual android.accessibilityservice.AccessibilityService getDisplayMessageBody",
        "permissions": ["android.permission.RECEIVE_SMS", "android.permission.BIND_ACCESSIBILITY_SERVICE"]
    }
    res = requests.post(f"{BASE_URL}/api/v1/ai/analyze-apk-threat", json=payload)
    assert res.status_code == 200, f"APK threat analysis failed: {res.text}"
    data = res.json()
    assert data["is_malicious"] is True
    print(f"  [PASS] SUCCESS: APK Threat Level: {data['threat_level']} ({data['threat_score'] * 100:.1f}%) | Action: {data['statutory_action']}.")

def test_interbank_broadcast():
    print("\n[12/12] Testing Inter-Bank Early Warning Broadcast Mesh & ATM Hotspot Predictor...")
    payload = {
        "origin_bank_code": "SBIN",
        "destination_bank_code": "PUNB",
        "mule_account_number": "40291048291",
        "amount_inr": 250000.0,
        "utr_ref": "UTR294810294819",
        "suspected_city": "Delhi"
    }
    res = requests.post(f"{BASE_URL}/api/v1/bank/broadcast-interbank-alert", json=payload)
    assert res.status_code == 200, f"Inter-bank broadcast failed: {res.text}"
    data = res.json()
    assert data["status"] == "SUCCESS"
    target_atm = data["top_predicted_cashout_atm"]
    print(f"  [PASS] SUCCESS: Multi-Bank Alert Broadcasted in {data['mesh_propagation_latency_ms']} ms | Top Target ATM: {target_atm['bank_name']} ({target_atm['location_name']}) [Risk: {target_atm['predicted_cashout_risk']*100:.1f}%].")

def test_network_nodes_and_atm_killswitch():
    print("\n[13/13] Testing Live Inter-Bank CBS Node Manager & ATM Remote Killswitch...")
    res_nodes = requests.get(f"{BASE_URL}/api/v1/bank/network-nodes")
    assert res_nodes.status_code == 200, f"Network nodes failed: {res_nodes.text}"
    nodes_data = res_nodes.json()
    assert nodes_data["total_nodes_online"] >= 7
    print(f"  [PASS] SUCCESS: {nodes_data['total_nodes_online']} Scheduled Commercial Banks CBS Switches Synchronized.")

    payload = {
        "atm_id": "ATM-DEL-SBIN-101",
        "officer_id": "CHIEF_NODAL_OFFICER_01",
        "reason": "Section 106 BNSS 2023 Injunction"
    }
    res_kill = requests.post(f"{BASE_URL}/api/v1/bank/atm-remote-killswitch", json=payload)
    assert res_kill.status_code == 200, f"ATM killswitch failed: {res_kill.text}"
    kill_data = res_kill.json()
    assert kill_data["dispenser_hardware_state"] == "LOCKED_SHUTTER_SEALED"
    print(f"  [PASS] SUCCESS: Remote ATM Dispenser Killswitch Engaged on {kill_data['atm_id']} ({kill_data['location_name']}) -> {kill_data['dispenser_hardware_state']}.")

def test_bank_health_matrix():
    print("\n[14/14] Testing 360° Real-Time Bank Connectivity & Health Ping Diagnostics Matrix...")
    res = requests.get(f"{BASE_URL}/api/v1/bank/health-check-matrix")
    assert res.status_code == 200, f"Health matrix failed: {res.text}"
    data = res.json()
    assert data["status"] == "ALL_SYSTEMS_OPERATIONAL"
    assert data["healthy_nodes_count"] >= 7
    print(f"  [PASS] SUCCESS: 360° Health Matrix Verified -> {data['healthy_nodes_count']} Banks Online | Avg Latency: {data['average_network_latency_ms']} ms | Redis Cache Hit: {data['redis_microhold_fast_cache']['hit_rate_pct']}% | Blockchain: {data['blockchain_merkle_evidence_locker']['status']}.")

def test_bank_network_daemon():
    print("\n[15/15] Testing Continuous Autonomous Bank Network Daemon Simulator...")
    res = requests.get(f"{BASE_URL}/api/v1/bank/network-telemetry")
    assert res.status_code == 200, f"Network telemetry failed: {res.text}"
    data = res.json()
    assert data["status"] == "RUNNING"
    assert data["total_transactions_processed"] > 0
    print(f"  [PASS] SUCCESS: Continuous Bank Network Daemon Active -> {data['total_transactions_processed']} Transactions Processed | INR {data['total_quarantined_volume_crores']} Cr Quarantined across {data['active_cbs_nodes_count']} CBS Switches.")


if __name__ == "__main__":
    print("=" * 60)
    print("[+] RUNNING DURGAM FULL PLATFORM E2E DIAGNOSTIC SUITE")
    print("=" * 60)
    try:
        test_bank_registry()
        test_jwt_auth()
        test_time_to_cashout_ai()
        test_case_trajectory_ai()
        test_bank_micro_holds()
        test_citizen_incident_ingestion()
        test_multimodal_threat()
        test_video_deepfake_detector()
        test_crypto_mixer_tracer()
        test_zk_consortium()
        test_apk_threat()
        test_interbank_broadcast()
        test_network_nodes_and_atm_killswitch()
        test_bank_health_matrix()
        test_bank_network_daemon()
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL 15 CORE MODULES & AUTONOMOUS BANK NETWORK DAEMON PASSED 100%!")
        print("=" * 60)
    except Exception as e:
        print(f"\n[FAILED] TEST ERROR: {e}")
        sys.exit(1)






