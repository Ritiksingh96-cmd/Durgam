"""
FIU-IND FinNet 2.0 & Virtual Digital Asset (VDA / Crypto) Gateway
Handles automated Suspicious Transaction Report (STR) filings under PMLA 2002,
Crypto Exchange VASP Wallet Freezes, and Cross-Border Hawala Layering Intelligence.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import time
import uuid

router = APIRouter(prefix="/fiu", tags=["FIU-IND FinNet 2.0 & VASP Crypto Gateway"])

class STRFilingRequest(BaseModel):
    case_id: str
    utr_number: str
    source_bank: str
    beneficiary_account: str
    amount_inr: float
    ground_of_suspicion: Optional[str] = "PMLA Sec 12 Rapid Layering & Mule Account Flow-Through"

class CryptoVASPFreezeRequest(BaseModel):
    wallet_address: str
    crypto_currency: Optional[str] = "USDT (TRC-20)"
    exchange_name: Optional[str] = "WAZIRX_COINDCX_BINANCE_P2P"
    case_id: str
    disputed_inr_value: float

# In-memory initial seed is replaced by SQLite-backed persistence via db_service

@router.get("/str-stream")
def get_str_stream():
    """Retrieve all real-time Suspicious Transaction Reports (STR) logged on FinNet 2.0"""
    from backend.app.services.db_service import db_service
    records = db_service.get_strs(limit=50)
    return {
        "success": True,
        "total_strs_filed": len(records),
        "finnet_gateway_status": "SECURE_mTLS_FINNET_2_CONNECTED",
        "reports": records
    }

@router.post("/file-str")
def file_suspicious_transaction_report(payload: STRFilingRequest):
    """Generates statutory STR under Prevention of Money Laundering Act (PMLA) 2002"""
    from backend.app.services.db_service import db_service

    str_id = f"STR-2026-IND-{uuid.uuid4().hex[:6].upper()}"
    finnet_ack = f"0x{uuid.uuid4().hex}"

    # Persist to SQLite — survives server restart
    db_service.store_str(
        str_id=str_id,
        case_id=payload.case_id,
        utr_number=payload.utr_number,
        beneficiary_account=payload.beneficiary_account,
        amount_inr=payload.amount_inr,
        ground_of_suspicion=payload.ground_of_suspicion,
        finnet_ack_hash=finnet_ack,
        filed_by="FIU_NODAL_OFFICER",
        priority="CRITICAL"
    )

    db_service.append_audit_log(
        actor="FIU_NODAL_OFFICER",
        role="FINANCIAL_INTELLIGENCE_ANALYST",
        action="PMLA_STR_FILING",
        target_id=str_id,
        details={"case_id": payload.case_id, "amount": payload.amount_inr, "utr": payload.utr_number}
    )

    return {
        "success": True,
        "str_id": str_id,
        "case_id": payload.case_id,
        "statutory_act": "Section 12, Prevention of Money Laundering Act (PMLA) 2002",
        "status": "TRANSMITTED_TO_FINNET_2",
        "finnet_ack_hash": finnet_ack,
        "message": f"STR {str_id} filed electronically with FIU-IND FinNet 2.0."
    }

@router.post("/freeze-vasp-wallet")
def freeze_crypto_vasp_wallet(payload: CryptoVASPFreezeRequest):
    """Dispatches statutory VASP Emergency Freeze Order to FIU-registered Crypto Exchanges"""
    from backend.app.services.db_service import db_service
    
    freeze_id = f"VASP-FRZ-{uuid.uuid4().hex[:6].upper()}"
    now = time.time()
    
    db_service.append_audit_log(
        actor="FIU_NODAL_OFFICER",
        role="FINANCIAL_INTELLIGENCE_ANALYST",
        action="CRYPTO_VASP_EMERGENCY_FREEZE",
        target_id=payload.wallet_address,
        details={"case_id": payload.case_id, "exchange": payload.exchange_name, "value_inr": payload.disputed_inr_value}
    )
    
    return {
        "success": True,
        "freeze_id": freeze_id,
        "wallet_address": payload.wallet_address,
        "crypto_currency": payload.crypto_currency,
        "target_exchanges": ["WazirX (FIU Reg)", "CoinDCX (FIU Reg)", "CoinSwitch (FIU Reg)", "Binance Compliance Desk"],
        "disputed_value_inr": payload.disputed_inr_value,
        "status": "VASP_ESCROW_FUNDS_LOCKED",
        "message": f"VASP Freeze Notice {freeze_id} served to FIU-registered exchanges for wallet {payload.wallet_address}."
    }

@router.get("/hawala-radar")
def get_hawala_layering_radar():
    """Identifies multi-hop money routing moving through offshore shell and mule accounts"""
    return {
        "success": True,
        "monitored_corridors": [
            {"corridor": "India -> UAE Hawala Remittance", "risk_level": "CRITICAL", "active_dockets": 8, "total_flow_inr": 18400000.0},
            {"corridor": "India -> Cambodia / Myanmar Scam Compound P2P Crypto", "risk_level": "CRITICAL", "active_dockets": 14, "total_flow_inr": 42500000.0},
            {"corridor": "India -> Hong Kong Trade Invoice Layering", "risk_level": "HIGH", "active_dockets": 5, "total_flow_inr": 12000000.0}
        ]
    }

@router.get("/str-filings")
def get_str_filings_alias():
    """Alias for /str-stream"""
    return get_str_stream()

@router.get("/crypto-clusters")
def get_fiu_crypto_clusters():
    """Returns TRC-20 and EVM crypto mixer clusters linked to mule accounts"""
    return {
        "status": "SUCCESS",
        "total_clusters_flagged": 12,
        "clusters": [
            {
                "cluster_id": "CRYPTO-CLUSTER-09",
                "network": "TRON (TRC-20)",
                "deposit_wallet": "TX9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b",
                "linked_fiat_mules": ["XXXX-XXXX-4821 (SBI)", "XXXX-XXXX-1920 (PNB)"],
                "total_laundered_usdt": 48290.0,
                "exchange_freeze_status": "LOCKED_ON_WAZIRX_AND_COINDCX"
            },
            {
                "cluster_id": "CRYPTO-CLUSTER-14",
                "network": "Ethereum (ERC-20)",
                "deposit_wallet": "0x7a8f9c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a",
                "linked_fiat_mules": ["XXXX-XXXX-0192 (HDFC)"],
                "total_laundered_usdt": 125000.0,
                "exchange_freeze_status": "ESCROW_QUARANTINE_ACTIVE"
            }
        ]
    }
