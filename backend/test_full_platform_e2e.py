import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app, raise_server_exceptions=True)

def run_tests():
    print("=== 1. Health & Root Check ===")
    r = client.get("/health")
    print("GET /health:", r.status_code, r.json().get("status"))
    assert r.status_code == 200

    r = client.get("/")
    print("GET /:", r.status_code, len(r.content), "bytes")
    assert r.status_code == 200

    print("\n=== 2. Static Pages Resolution ===")
    pages = [
        "index.html", "citizen.html", "bank.html", "police.html",
        "judiciary.html", "command.html", "verify.html",
        "login.html", "register.html", "about.html", "contact.html",
        "resources.html", "style.css", "script.js", "app.js"
    ]
    for p in pages:
        res = client.get(f"/{p}")
        print(f"GET /{p}:", res.status_code, f"({len(res.content)} bytes)")
        assert res.status_code == 200, f"Failed on {p}"

    print("\n=== 3. Authentication & RBAC ===")
    login_payload = {
        "username": "sp_delhi_cyber",
        "password": "password123",
        "role": "police"
    }
    r = client.post("/api/v1/auth/login", json=login_payload)
    print("POST /api/v1/auth/login:", r.status_code, r.json().get("role"), r.json().get("full_name"))
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token is not None

    r = client.get("/api/v1/auth/users")
    print("GET /api/v1/auth/users:", r.status_code, f"({r.json().get('total_users')} users)")
    assert r.status_code == 200

    r = client.get("/api/v1/auth/audit-trail")
    print("GET /api/v1/auth/audit-trail:", r.status_code, f"({r.json().get('total_logs')} logs)")
    assert r.status_code == 200

    print("\n=== 4. Public Telemetry & Incident Ingestion ===")
    r = client.get("/api/v1/public/telemetry")
    print("GET /api/v1/public/telemetry:", r.status_code, r.json())
    assert r.status_code == 200

    payload = {
        "victim_name": "Dr. Rajiv Malhotra",
        "victim_phone": "9811029481",
        "victim_city": "Delhi NCR",
        "victim_state": "Delhi",
        "source_bank": "State Bank of India",
        "source_account": "XXXX-XXXX-2948",
        "utr_number": "482910482910",
        "loss_amount": 250000.0,
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Scammer impersonated police officer on video call and coerced transfer to escrow account."
    }
    r = client.post("/api/v1/citizen/report-incident", json=payload)
    print("POST /api/v1/citizen/report-incident:", r.status_code, r.json().get("status"), r.json().get("ack_number"))
    assert r.status_code == 200

    r = client.post("/api/v1/user/complaint", json=payload)
    print("POST /api/v1/user/complaint:", r.status_code, r.json().get("complaint_id"))
    assert r.status_code == 200

    print("\n=== 5. Bank Nodal & ZK-Consortium ===")
    r = client.get("/api/v1/bank/holds")
    print("GET /api/v1/bank/holds:", r.status_code, f"({len(r.json())} active holds)")
    assert r.status_code == 200

    r = client.get("/api/v1/bank/flagged-accounts")
    print("GET /api/v1/bank/flagged-accounts:", r.status_code, f"({len(r.json().get('accounts', []))} accounts)")
    assert r.status_code == 200

    r = client.post("/api/v1/bank/zk-consortium-query", json={"account_number": "902148102941", "ifsc": "SBIN0001024"})
    print("POST /api/v1/bank/zk-consortium-query:", r.status_code, r.json().get("status"))
    assert r.status_code == 200

    print("\n=== 6. Police Tactical CAD, Hotspots & Telegram Navigation ===")
    r = client.get("/api/v1/police/hotspots")
    print("GET /api/v1/police/hotspots:", r.status_code, f"({len(r.json().get('hotspots', []))} hotspots)")
    assert r.status_code == 200

    r = client.post("/api/v1/police/dispatch", json={"complaint_id": "NCRP-1930-48291048", "atm_id": "ATM_SBI_101", "unit_id": "FALCON_1"})
    print("POST /api/v1/police/dispatch:", r.status_code, r.json().get("status"), r.json().get("eta_minutes"), "mins")
    assert r.status_code == 200

    r = client.post("/api/v1/police/auto-detect-and-alert-pcr", json={"case_id": "DURGAM-2026-DL-8421", "city": "Delhi"})
    print("POST /api/v1/police/auto-detect-and-alert-pcr:", r.status_code, r.json().get("assigned_pcr_unit"))
    assert r.status_code == 200

    r = client.post("/api/v1/police/dispatch-telegram-navigation", json={
        "pcr_callsign": "PCR Eagle 4",
        "case_id": "DURGAM-DL-001",
        "target_atm": "SBI ATM #14, Inner Circle, Connaught Place, New Delhi",
        "target_lat": 28.6315,
        "target_lon": 77.2167,
        "stolen_amount": 250000.0
    })
    print("POST /api/v1/police/dispatch-telegram-navigation:", r.status_code, r.json().get("status"))
    assert r.status_code == 200

    print("\n=== 7. Telegram Bot API Integration ===")
    r = client.get("/api/v1/telegram/status")
    print("GET /api/v1/telegram/status:", r.status_code, r.json().get("configured"), r.json().get("message"))
    assert r.status_code == 200

    print("\n=== 8. Judiciary Evidence Vault & Decrees ===")
    r = client.get("/api/v1/judiciary/cases")
    print("GET /api/v1/judiciary/cases:", r.status_code, f"({len(r.json())} cases)")
    assert r.status_code == 200

    r = client.get("/api/v1/court/records")
    print("GET /api/v1/court/records:", r.status_code, f"({len(r.json().get('records', []))} records)")
    assert r.status_code == 200

    r = client.post("/api/v1/court/issue-decree?complaint_id=NCRP-1930-48291048")
    print("POST /api/v1/court/issue-decree:", r.status_code, r.json().get("message"))
    assert r.status_code == 200

    print("\n=== 9. AI Threat Models & Blockchain ===")
    r = client.get("/api/v1/admin/blockchain-batches")
    print("GET /api/v1/admin/blockchain-batches:", r.status_code, r.json().get("blockchain_network"))
    assert r.status_code == 200

    r = client.get("/api/v1/ai/models-metadata")
    print("GET /api/v1/ai/models-metadata:", r.status_code, list(r.json().get("models", {}).keys()))
    assert r.status_code == 200

    print("\n=== 11. Android Mobile API Connectivity ===")
    r = client.get("/api/v1/android/handshake")
    print("GET /api/v1/android/handshake:", r.status_code, r.json().get("protocol_version"))
    assert r.status_code == 200
    assert r.json().get("min_supported_android_sdk") == 26

    r = client.get("/api/v1/android/config")
    print("GET /api/v1/android/config:", r.status_code, r.json().get("app_title"))
    assert r.status_code == 200

    reg_payload = {
        "device_id": "android_pixel_test_001",
        "fcm_token": "fcm_test_token_84920481029",
        "app_version": "1.0.0",
        "android_os_version": "14.0",
        "device_model": "Pixel 8 Pro",
        "role": "citizen"
    }
    r = client.post("/api/v1/android/devices/register", json=reg_payload)
    print("POST /api/v1/android/devices/register:", r.status_code, r.json().get("status"))
    assert r.status_code == 200

    login_mobile = {
        "username": "citizen_mobile_test",
        "password": "password123",
        "role": "citizen",
        "device_id": "android_pixel_test_001",
        "biometric_authenticated": True
    }
    r = client.post("/api/v1/android/auth/login", json=login_mobile)
    print("POST /api/v1/android/auth/login:", r.status_code, r.json().get("status"), r.json().get("user_profile", {}).get("role"))
    assert r.status_code == 200
    mobile_token = r.json().get("access_token")
    assert mobile_token is not None

    sos_payload = {
        "victim_name": "Meera Nambiar",
        "victim_phone": "9845112233",
        "utr_number": "482910482999",
        "loss_amount": 175000.0,
        "source_bank": "State Bank of India",
        "source_account": "XXXX-XXXX-9912",
        "suspect_account": "902148102941",
        "crime_category": "DIGITAL_ARREST",
        "narrative": "Urgent SOS: Blackmailed via video call impersonating customs officer",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "city": "Bengaluru",
        "state": "Karnataka"
    }
    r = client.post("/api/v1/android/citizen/sos-freeze", json=sos_payload)
    print("POST /api/v1/android/citizen/sos-freeze:", r.status_code, r.json().get("status"), r.json().get("docket", {}).get("ack_number"))
    assert r.status_code == 200
    created_ack = r.json().get("docket", {}).get("ack_number")

    r = client.get(f"/api/v1/android/citizen/cases/{created_ack}")
    print(f"GET /api/v1/android/citizen/cases/{created_ack}:", r.status_code, r.json().get("status_text"))
    assert r.status_code == 200

    r = client.get("/api/v1/android/police/field-radar?latitude=28.6139&longitude=77.2090&radius_km=10.0")
    print("GET /api/v1/android/police/field-radar:", r.status_code, f"({r.json().get('total_hotspots_detected')} hotspots)")
    assert r.status_code == 200
    assert "android_navigation_intent" in r.json().get("hotspots", [{}])[0]

    ack_payload = {
        "officer_badge": "DL-POLICE-048",
        "unit_id": "PCR Eagle 4",
        "case_id": "DURGAM-DL-001",
        "target_atm_id": "ATM_SBI_101",
        "officer_latitude": 28.6145,
        "officer_longitude": 77.2100,
        "response_status": "DISPATCH_EN_ROUTE",
        "eta_minutes": 3
    }
    r = client.post("/api/v1/android/police/patrol-ack", json=ack_payload)
    print("POST /api/v1/android/police/patrol-ack:", r.status_code, r.json().get("status"))
    assert r.status_code == 200

    r = client.get("/api/v1/android/bank/holds")
    print("GET /api/v1/android/bank/holds:", r.status_code, f"({r.json().get('total_active_holds')} active holds)")
    assert r.status_code == 200

    batch_payload = {
        "device_id": "android_pixel_test_001",
        "queued_complaints": [
            {
                "client_uuid": "offline_uuid_99182",
                "timestamp_local": 1727482910.0,
                "victim_name": "Rohan Deshmukh",
                "victim_phone": "9820019284",
                "utr_number": "992810481029",
                "loss_amount": 80000.0,
                "source_bank": "Bank of Baroda",
                "suspect_account": "902148102941",
                "narrative": "Fake electricity bill payment disconnection fraud"
            }
        ]
    }
    r = client.post("/api/v1/android/sync/offline-batch", json=batch_payload)
    print("POST /api/v1/android/sync/offline-batch:", r.status_code, r.json().get("status"), f"({r.json().get('total_items_processed')} items synced)")
    assert r.status_code == 200

    print("\n🎉 ALL FULL-STACK & ANDROID MOBILE CONNECTIVITY TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_tests()

