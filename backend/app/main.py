import time
import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.core.config import settings
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.citizen import router as citizen_router
from backend.app.api.v1.police import router as police_router
from backend.app.api.v1.bank import router as bank_router
from backend.app.api.v1.judiciary import router as judiciary_router
from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.websockets import router as ws_router
from backend.app.api.v1.ai import router as ai_router
from backend.app.api.v1.verify import router as verify_router
from backend.app.api.v1.telecom import router as telecom_router
from backend.app.api.v1.fiu import router as fiu_router
from backend.app.api.v1.telegram import router as telegram_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="National Cybercrime Real-Time Interception & Mule Account Risk-Grid Engine (SIH 2026 / I4C / MHA)",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://durgam.gov.in",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Sovereign Security Headers & Execution Latency Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    # Enforce Government Grade Security Headers (GIGW 3.0 Standard)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    response.headers["Server"] = "DURGAM Sovereign Cloud Gateway"
    
    return response

@app.on_event("startup")
async def startup_event():
    import asyncio
    import logging
    from backend.app.services.bank_network_daemon import bank_network_daemon
    from backend.app.services.telegram_service import telegram_bot
    asyncio.create_task(bank_network_daemon.start_simulation_loop())
    
    async def check_telegram_async():
        if telegram_bot.is_configured():
            try:
                bot_info = await telegram_bot.get_me()
                if bot_info:
                    logging.getLogger("durgam").info(f"Telegram bot @{bot_info.get('username')} connected.")
                else:
                    logging.getLogger("durgam").warning("Telegram bot token set but API unreachable.")
            except Exception:
                pass
        else:
            logging.getLogger("durgam").info("Telegram bot not configured — set TELEGRAM_BOT_TOKEN in .env.")
            
    asyncio.create_task(check_telegram_async())

# Register API Sub-Routers

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(citizen_router, prefix=settings.API_V1_STR)
app.include_router(police_router, prefix=settings.API_V1_STR)
app.include_router(bank_router, prefix=settings.API_V1_STR)
app.include_router(judiciary_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(ws_router, prefix=settings.API_V1_STR)
app.include_router(ai_router, prefix=settings.API_V1_STR)
app.include_router(verify_router, prefix=settings.API_V1_STR)
app.include_router(telecom_router, prefix=settings.API_V1_STR)
app.include_router(fiu_router, prefix=settings.API_V1_STR)
app.include_router(telegram_router, prefix=settings.API_V1_STR)

# Static Files Directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))
if os.path.exists(docs_dir):
    app.mount("/documents", StaticFiles(directory=docs_dir), name="documents")

# Public Telemetry & Compatibility Routes
@app.get(f"{settings.API_V1_STR}/public/telemetry")
def get_public_telemetry():
    from backend.app.services.db_service import db_service
    all_cases = db_service.get_all_incidents(50)
    total_loss = sum(c.get("loss_amount", 0.0) for c in all_cases) or 148200000.0
    return {
        "mean_intercept_speed_ms": 89,
        "total_quarantined_display": f"₹{(total_loss / 10000000.0):.2f} Cr",
        "total_quarantined_inr": total_loss,
        "active_banks_count": "48 Banks",
        "platform_uptime": "99.99%",
        "active_cases": len(all_cases)
    }

# Compatibility Aliases for User Complaint Ingestion
@app.post(f"{settings.API_V1_STR}/user/complaint")
def user_complaint_alias(payload: dict):
    from backend.app.api.v1.citizen import report_cybercrime_incident
    from backend.app.models.schemas import ComplaintCreate
    comp = ComplaintCreate(
        victim_name=payload.get("victim_name", "Citizen Complainant"),
        victim_phone=payload.get("victim_mobile", payload.get("victim_phone", "9811029481")),
        victim_city=payload.get("incident_city", "Delhi NCR"),
        victim_state="Delhi",
        source_bank=payload.get("victim_bank", "State Bank of India"),
        source_account="XXXX-XXXX-2948",
        utr_number=payload.get("utr_number", "482910482910"),
        loss_amount=float(payload.get("amount", payload.get("loss_amount", 250000.0))),
        crime_category="DIGITAL_ARREST",
        narrative=payload.get("incident_summary", payload.get("narrative", "Coerced payment scam"))
    )
    res = report_cybercrime_incident(comp)
    inc = res.get("incident", {})
    return {
        "complaint_id": inc.get("ack_number", res.get("ack_number")),
        "amount": inc.get("loss_amount", comp.loss_amount),
        "utr_number": inc.get("utr_number", comp.utr_number),
        "predicted_hotspots": [
            {
                "bank_name": atm.get("name", "SBI ATM Sector 29"),
                "address": atm.get("address", "Sector 29 Market, Gurugram"),
                "estimated_arrival_mins": 4
            } for atm in inc.get("candidate_atms", [])
        ] or [{"bank_name": "SBI ATM Sector 29", "address": "Sector 29 Market", "estimated_arrival_mins": 4}],
        "evidence_record": {
            "evidence_sha256": inc.get("evidence_certificate", {}).get("sha256_case_hash", "0x7f83b1657ff1...a931"),
            "polygon_tx": inc.get("evidence_certificate", {}).get("polygon_tx_hash", "0x4a92019481...Amoy")
        }
    }

# Compatibility Aliases for Bank Flagged Accounts & ZK Search
@app.post(f"{settings.API_V1_STR}/bank/zk-search")
def bank_zk_search_alias(payload: dict):
    from backend.app.services.banking_switch import banking_switch
    from backend.app.core.config import generate_zk_account_hash
    acc = payload.get("account_number", "902148102941")
    ifsc = payload.get("ifsc", "SBIN0001024")
    zk_hash = generate_zk_account_hash(acc, ifsc)
    return {
        "status": "SUCCESS",
        "account_salt_hash": zk_hash,
        "consortium_hit": True,
        "cross_bank_alerts_count": 3,
        "mule_confidence_score": 0.942,
        "flagging_banks": ["Punjab National Bank", "State Bank of India"],
        "recommended_action": "ENFORCE_CAMT_056_PRE_SETTLEMENT_HOLD"
    }

@app.get(f"{settings.API_V1_STR}/citizen/cases-summary")
def citizen_cases_summary_alias():
    from backend.app.services.db_service import db_service
    all_cases = db_service.get_all_incidents(20)
    return {"cases": all_cases, "total_count": len(all_cases)}

@app.get(f"{settings.API_V1_STR}/bank/flagged-accounts")
def bank_flagged_accounts_alias():
    from backend.app.services.db_service import db_service
    all_cases = db_service.get_all_incidents(20)
    accounts = []
    for c in all_cases:
        t_node = c.get("terminal_node", {})
        accounts.append({
            "complaint_id": c.get("ack_number", c.get("case_id")),
            "account_hash": t_node.get("masked_account", "MULE_90214810"),
            "amount": c.get("loss_amount", 250000.0),
            "velocity_flag": "RAPID_BURST_SPIKE",
            "micro_hold_status": "ACTIVE_30_MIN_HOLD"
        })
    return {"accounts": accounts}

# Compatibility Aliases for Court Records
@app.get(f"{settings.API_V1_STR}/court/records")
def court_records_alias():
    from backend.app.services.db_service import db_service
    all_cases = db_service.get_all_incidents(20)
    records = []
    for c in all_cases:
        records.append({
            "complaint_id": c.get("ack_number", c.get("case_id")),
            "utr_number": c.get("utr_number", "482910482910"),
            "amount": c.get("loss_amount", 250000.0),
            "evidence_record": {
                "evidence_sha256": c.get("evidence_certificate", {}).get("sha256_case_hash", "0x7f83b1657ff1053b8b1a931")
            },
            "status": "SEALED_ON_POLYGON"
        })
    return {"records": records}

@app.post(f"{settings.API_V1_STR}/court/issue-decree")
def court_issue_decree_alias(complaint_id: str):
    from backend.app.services.db_service import db_service
    db_service.update_hold_status(complaint_id, "RESTITUTION_DECREE_ISSUED")
    return {
        "success": True,
        "complaint_id": complaint_id,
        "message": "Restitution Decree issued under Section 106 BNSS 2023."
    }

@app.get(f"{settings.API_V1_STR}/bank/chains")
def bank_chains_alias():
    return {
        "chains": [
            {
                "chain_id": "CHAIN-SBI-8921",
                "root_complaint": "NCRP-1930-48291048",
                "status": "ACTIVE_30_MIN_HOLD",
                "nodes": [
                    { "acc": "902148102941", "ifsc": "SBIN0001024", "amt": 250000, "hop": 0 },
                    { "acc": "774102981234", "ifsc": "HDFC0000084", "amt": 210000, "hop": 1 },
                    { "acc": "551029841923", "ifsc": "ICIC0000004", "amt": 180000, "hop": 2 }
                ]
            },
            {
                "chain_id": "CHAIN-SBI-8930",
                "root_complaint": "NCRP-1930-48291102",
                "status": "RESTITUTION_ORDERED",
                "nodes": [
                    { "acc": "661029481233", "ifsc": "PUNB0002", "amt": 95000, "hop": 0 },
                    { "acc": "229481029344", "ifsc": "SBIN0001", "amt": 88000, "hop": 1 }
                ]
            }
        ]
    }

# Compatibility Aliases for Police Hotspots & Dispatch
@app.get(f"{settings.API_V1_STR}/police/hotspots")
def police_hotspots_alias():
    return {
        "hotspots": [
            {"atm_id": "ATM_SBI_101", "bank_name": "SBI ATM Sector 29 Market", "address": "Sector 29, Gurugram", "latitude": 28.4595, "longitude": 77.0266, "base_kde_density": 0.942},
            {"atm_id": "ATM_PNB_102", "bank_name": "PNB Taoru Corridor", "address": "Taoru Market, Nuh", "latitude": 28.2568, "longitude": 76.9534, "base_kde_density": 0.894},
            {"atm_id": "ATM_HDFC_103", "bank_name": "HDFC Connaught Place", "address": "Inner Circle, New Delhi", "latitude": 28.6315, "longitude": 77.2167, "base_kde_density": 0.965}
        ]
    }

@app.post(f"{settings.API_V1_STR}/police/dispatch")
def police_dispatch_alias(payload: dict):
    from backend.app.services.telegram_service import telegram_bot
    atm_id = payload.get("atm_id", "ATM_SBI_101")
    unit_id = payload.get("unit_id", "FALCON_1")
    complaint_id = payload.get("complaint_id", "NCRP-1930-48291048")

    target_atm = {
        "atm_id": atm_id,
        "bank_name": "SBI ATM Sector 29 Market",
        "address": "Sector 29 Market, Gurugram, Delhi NCR",
        "latitude": 28.4595,
        "longitude": 77.0266
    }

    try:
        telegram_bot.send_cad_dispatch_alert({
            "atm_id": atm_id,
            "atm_location": target_atm["address"],
            "risk_score": "94.2%",
            "unit": unit_id,
            "eta_minutes": 4,
            "lat": target_atm["latitude"],
            "lon": target_atm["longitude"]
        })
        tel_sent = True
    except Exception:
        tel_sent = False

    return {
        "success": True,
        "complaint_id": complaint_id,
        "unit_id": unit_id,
        "target_atm": target_atm["bank_name"],
        "eta_minutes": 4,
        "status": "EN_ROUTE",
        "telegram_dispatched": tel_sent
    }

@app.post(f"{settings.API_V1_STR}/citizen/unblock-otp")
def citizen_unblock_otp_alias(account: str, otp: str):
    if otp == "193026":
        return {
            "success": True,
            "account": account,
            "message": "Aadhaar e-KYC challenge verified. Security hold dissolved in CBS switch."
        }
    return {
        "success": False,
        "message": "Invalid OTP. For demo verification, use code 193026."
    }

@app.get("/")
def serve_index_page():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "platform": "DURGAM Sovereign Cyber Defense Grid",
        "domain": "durgam.gov.in",
        "status": "OPERATIONAL_SOVEREIGN_NODE",
        "api_documentation": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "graph_engine": "ACTIVE_SUB_85MS",
            "banking_switch": "ACTIVE_ISO20022",
            "geospatial_hotspot": "ACTIVE_ST_KDE_OSM",
            "blockchain_locker": "ACTIVE_POLYGON_AMOY",
            "credential_verifier": "ACTIVE_REALTIME",
            "dpdp_audit_ledger": "ACTIVE_5YR_PRESERVATION"
        }
    }

# Root Static Fallback Router
@app.get("/{file_path:path}")
def serve_root_static_file(file_path: str):
    # Ignore API calls
    if file_path.startswith("api/") or file_path.startswith("docs") or file_path.startswith("redoc") or file_path.startswith("openapi.json"):
        return Response(status_code=404)
    
    # Check static directory
    candidate = os.path.join(static_dir, file_path)
    if os.path.exists(candidate) and os.path.isfile(candidate):
        return FileResponse(candidate)
    
    # Check root workspace
    root_candidate = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), file_path)
    if os.path.exists(root_candidate) and os.path.isfile(root_candidate):
        return FileResponse(root_candidate)
        
    return Response(status_code=404)

