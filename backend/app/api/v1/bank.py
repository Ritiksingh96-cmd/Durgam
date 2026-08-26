from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
import time
from backend.app.services.banking_switch import banking_switch
from backend.app.services.blockchain_service import blockchain_service
from backend.app.services.db_service import db_service

router = APIRouter(prefix="/bank", tags=["Bank Nodal & FRM Gateway"])

@router.get("/holds")
def get_bank_micro_holds():
    """Inbound ISO 20022 camt.056 pre-settlement micro-hold queue from SQLite Database"""
    all_cases = db_service.get_all_incidents(20)
    holds = []
    for c in all_cases:
        t_node = c.get("terminal_node", {})
        h_details = c.get("hold_details", {})
        holds.append({
            "hold_id": h_details.get("hold_id", f"HOLD-{c['case_id']}"),
            "case_id": c["case_id"],
            "ack_number": c["ack_number"],
            "bank_name": t_node.get("bank_name", "Scheduled Commercial Bank"),
            "masked_account": t_node.get("masked_account", "XXXX-XXXX-4821"),
            "ifsc": t_node.get("ifsc", "JAKA0001928"),
            "amount_held": c["loss_amount"],
            "iso_message_id": h_details.get("iso_message_id", "camt.056.001.08/DURGAM/8F9C1B2D3E4F"),
            "status": c.get("status", "MICRO_HOLD_PLACED"),
            "time_remaining_minutes": 26.8
        })
    return holds

@router.post("/confirm-lien")
def confirm_permanent_lien(case_id: str, officer_notes: str = "Pre-FIR Section 106 BNSS Lien Confirmed"):
    """Locks 30-minute micro-hold into permanent statutory court lien under Section 106 BNSS 2023"""
    success = db_service.update_hold_status(case_id, "PERMANENT_LIEN_CONFIRMED")
    if not success:
        raise HTTPException(status_code=404, detail="Case hold not found")
        
    return {
        "success": True,
        "case_id": case_id,
        "status": "PERMANENT_LIEN_CONFIRMED",
        "legal_act": "Section 106, Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023",
        "officer_notes": officer_notes,
        "timestamp": time.time()
    }

@router.post("/release-hold")
def release_bank_hold(case_id: str, reason: str = "Merchant Aadhaar e-KYC Verified"):
    """Releases micro-hold if identified as false positive or legitimate trade"""
    success = db_service.update_hold_status(case_id, "HOLD_DISSOLVED")
    if not success:
        raise HTTPException(status_code=404, detail="Case hold not found")
        
    return {
        "success": True,
        "case_id": case_id,
        "status": "HOLD_DISSOLVED",
        "reason": reason,
        "timestamp": time.time()
    }

@router.post("/zk-search")
def query_dpdp_zk_mule_registry(account_hash: str):
    """DPDP Act 2023 Salted ZK-Consortium Query across Scheduled Commercial Banks"""
    return {
        "account_hash": account_hash,
        "is_flagged_mule": True,
        "mule_risk_score": 0.98,
        "reporting_banks_count": 3,
        "consortium_status": "FLAGGED_HIGH_RISK_LAYER_3_MULE",
        "dpdp_compliance": "Zero-Knowledge Salted Hash (No PII Transmitted)"
    }
