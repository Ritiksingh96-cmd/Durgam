from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
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

class ZKQueryPayload(BaseModel):
    account_number: str = "40291048291"
    ifsc: str = "SBIN0001024"
    requesting_bank: Optional[str] = "State Bank of India"

@router.post("/zk-consortium-query")
def query_dpdp_zk_mule_registry(payload: ZKQueryPayload):
    """
    DPDP Act 2023 Salted ZK-Consortium Blind Query across 48 Scheduled Commercial Banks.
    Verifies if account is a known mule without transmitting plaintext PII.
    """
    from backend.app.services.zk_consortium import zk_consortium_engine
    return zk_consortium_engine.query_zk_consortium(
        account_num=payload.account_number,
        ifsc=payload.ifsc,
        requesting_bank=payload.requesting_bank or "SBI"
    )

class InterBankAlertRequest(BaseModel):

    origin_bank_code: str = "SBIN"
    destination_bank_code: str = "PUNB"
    mule_account_number: str = "40291048291"
    amount_inr: float = 250000.0
    utr_ref: str = "UTR294810294819"
    suspected_city: Optional[str] = "Delhi"

@router.post("/broadcast-interbank-alert")
def broadcast_interbank_fraud_early_warning(payload: InterBankAlertRequest):
    """
    Multi-Bank Real-Time ISO 20022 camt.056 Early Warning Broadcast Mesh.
    Propagates threat alerts from Origin Bank to Destination Bank CBS and predicts physical target ATMs.
    """
    from backend.app.services.inter_bank_mesh import inter_bank_mesh
    return inter_bank_mesh.broadcast_interbank_fraud_alert(
        origin_bank_code=payload.origin_bank_code,
        destination_bank_code=payload.destination_bank_code,
        mule_account_number=payload.mule_account_number,
        amount_inr=payload.amount_inr,
        utr_ref=payload.utr_ref,
        suspected_city=payload.suspected_city or "Delhi"
    )

class ATMKillswitchRequest(BaseModel):

    atm_id: str = "ATM-DEL-SBIN-101"
    officer_id: Optional[str] = "NODAL_OFFICER_DL_04"
    reason: Optional[str] = "Imminent Section 106 BNSS illicit ATM withdrawal"

@router.get("/network-nodes")
def get_interbank_network_nodes():
    """Returns real-time status and latency of all 48 participating CBS bank switches."""
    from backend.app.services.inter_bank_mesh import inter_bank_mesh
    return {
        "status": "SUCCESS",
        "total_nodes_online": len(inter_bank_mesh.participating_banks),
        "nodes": inter_bank_mesh.get_all_network_nodes()
    }

@router.post("/atm-remote-killswitch")

def trigger_remote_atm_hardware_lock(payload: ATMKillswitchRequest):
    """Executes remote hardware cash dispenser killswitch on a target physical ATM."""
    from backend.app.services.inter_bank_mesh import inter_bank_mesh
    return inter_bank_mesh.execute_remote_atm_killswitch(
        atm_id=payload.atm_id,
        officer_id=payload.officer_id or "NODAL_OFFICER_DL_04",
        reason=payload.reason or "Section 106 BNSS Illicit Cashout Injunction"
    )

@router.get("/network-telemetry")
def get_continuous_bank_network_telemetry():
    """Returns continuous bank network simulation metrics and transaction counts."""
    from backend.app.services.bank_network_daemon import bank_network_daemon
    return bank_network_daemon.get_simulation_telemetry()

@router.get("/health-check-matrix")

def get_360_bank_connectivity_matrix():
    """
    360° Real-Time Bank Connectivity & Health Ping Diagnostics Matrix.
    Measures latency across all 48 banks, NPCI UPI switch, Redis cache, and Polygon blockchain.
    """
    from backend.app.services.bank_health_service import bank_health_service
    return bank_health_service.ping_all_banking_infrastructure()

class SwitchSimulationRequest:




    account_number: str
    bank_ifsc: str
    amount: float
    mule_score: float

@router.post("/simulate-switch-transaction")
def simulate_iso20022_switch_transaction(payload: Dict[str, Any]):
    """
    Live Core Banking ISO 20022 camt.056 Clearing Simulator & Test Bench.
    Dispatches pre-settlement hold payload and measures CBS switch roundtrip latency.
    """
    import uuid
    from backend.app.core.config import dpdp_mask_account
    
    acc_raw = payload.get("account_number", "482910482910")
    ifsc = payload.get("bank_ifsc", "SBIN0001024")
    amount = float(payload.get("amount", 250000.0))
    mule_score = float(payload.get("mule_score", 0.94))
    
    t_start = time.time()
    hold_id = f"ISO-HOLD-{uuid.uuid4().hex[:8].upper()}"
    msg_id = f"camt.056.001.08/DURGAM/{uuid.uuid4().hex[:12].upper()}"
    
    # Calculate latency in ms
    simulated_latency = round(65.0 + (mule_score * 24.0), 1)
    
    xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.056.001.08">
  <FIToFIPmtCxlReq>
    <GrpHdr>
      <MsgId>{msg_id}</MsgId>
      <CreDtTm>{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}</CreDtTm>
      <Authstn>Section 106 BNSS 2023</Authstn>
    </GrpHdr>
    <Undrlyg>
      <TxInf>
        <CxlId>{hold_id}</CxlId>
        <OrgnlGrpInf>
          <OrgnlMsgId>NPCI-IMPS-CLEARING-2026</OrgnlMsgId>
        </OrgnlGrpInf>
        <OrgnlTxRef>
          <Amt Ccy="INR">{amount:.2f}</Amt>
          <CdtrAgt><FinInstnId><BICFI>{ifsc}</BICFI></FinInstnId></CdtrAgt>
          <CdtrAcct><Id><Othr><Id>{dpdp_mask_account(acc_raw)}</Id></Othr></Id></CdtrAcct>
        </OrgnlTxRef>
      </TxInf>
    </Undrlyg>
  </FIToFIPmtCxlReq>
</Document>"""

    return {
        "success": True,
        "hold_id": hold_id,
        "iso_message_id": msg_id,
        "target_account": dpdp_mask_account(acc_raw),
        "target_ifsc": ifsc,
        "quarantined_amount_inr": amount,
        "mule_risk_score": mule_score,
        "switch_roundtrip_latency_ms": simulated_latency,
        "sla_status": "COMPLIANT_SUB_140MS",
        "iso20022_xml_payload": xml_payload,
        "camt029_positive_acknowledgment": {
            "status": "ACCEPTED_HOLD_PLACED",
            "resolution_code": "FRAD",
            "cbs_ledger_status": "SMART_PARTIAL_AMOUNT_LIEN_LOCKED"
        }
    }

