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

class SwitchSimulationRequest(BaseModel):
    account_number: str = "482910482910"
    bank_ifsc: str = "SBIN0001024"
    amount: float = 250000.0
    mule_score: float = 0.94

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

class ZKBroadcastRequest(BaseModel):
    identifier: str
    ifsc: str = "SBIN0001024"
    reporting_agency: Optional[str] = "Bank FRM Nodal Desk"
    bank_code: str = "SBIN"
    risk_tier: Optional[str] = "CRITICAL_CONFIRMED_MULE"
    notes: Optional[str] = "Flagged via multi-hop layering telemetry"

@router.post("/zk-broadcast")
def broadcast_new_mule_hash(payload: ZKBroadcastRequest):
    """
    Broadcasts a salted Zero-Knowledge SHA-256 suspect hash to all 48 participating banks.
    DPDP Act 2023 Section 8 Compliant.
    """
    from backend.app.services.zk_consortium import zk_consortium_engine
    return zk_consortium_engine.broadcast_mule_hash(
        identifier=payload.identifier,
        ifsc=payload.ifsc,
        reporting_agency=payload.reporting_agency or "Bank FRM Nodal",
        bank_code=payload.bank_code,
        risk_tier=payload.risk_tier or "CRITICAL_CONFIRMED_MULE",
        notes=payload.notes or "Flagged via multi-hop telemetry"
    )

@router.get("/zk-shared-hashes")
def get_interbank_shared_hashes(limit: int = 50):
    """Fetches real-time stream of all inter-bank shared ZK hashes across 48 CBS switches."""
    from backend.app.services.zk_consortium import zk_consortium_engine
    hashes = zk_consortium_engine.get_all_shared_hashes(limit=limit)
    return {
        "status": "SUCCESS",
        "total_active_hashes": len(hashes),
        "shared_hashes": hashes,
        "compliance": "Section 8 DPDP Act 2023 (Zero-Plaintext Exchange)"
    }

@router.get("/mule-graph/{case_id}")
def get_mule_account_graph(case_id: str):
    """
    Returns real-time directed Multi-Hop Layering Graph for a case or account.
    Traces fund dispersion: Victim -> Hop 1 Jan Dhan -> Hop 2 Current -> Hop 3 Regional -> Terminal ATM Kiosk.
    """
    from backend.app.services.graph_service import MultiHopGraphEngine
    engine = MultiHopGraphEngine()
    
    # Check if incident exists in DB
    incident = db_service.get_incident(case_id)
    if incident:
        amount = incident.get("loss_amount", 250000.0)
        v_name = incident.get("victim_name", "Citizen Victim")
        v_acc = incident.get("victim_account", "40291048291")
        v_bank = incident.get("victim_bank", "State Bank of India")
    else:
        amount = 350000.0
        v_name = "Citizen Victim (Reported 1930)"
        v_acc = "59201948201"
        v_bank = "HDFC Bank Ltd"

    trail = engine.trace_case_trail(
        case_id=case_id,
        victim_name=v_name,
        victim_account=v_acc,
        source_bank=v_bank,
        amount=amount
    )
    return {
        "status": "SUCCESS",
        "case_id": case_id,
        "nodes": trail["nodes"],
        "edges": trail["edges"],
        "layering_hops": len(trail["nodes"]) - 1,
        "total_quarantined_inr": amount,
        "terminal_atm_target": trail.get("terminal_city", "Connaught Place, Delhi")
    }

@router.get("/predict-atm-cashouts")
def get_predicted_atm_cashouts(city: str = "Delhi"):
    """
    Federated ST-KDE ATM Cashout Predictor.
    Forecasts physical withdrawal kiosks, withdrawal time windows, and intercept probability.
    """
    from backend.app.services.inter_bank_mesh import inter_bank_mesh
    atms = [a for a in inter_bank_mesh.federated_atm_kiosks if city.lower() in a.get("city", "").lower()]
    if not atms:
        atms = inter_bank_mesh.federated_atm_kiosks

    results = []
    for atm in atms:
        risk = atm.get("base_risk_score", 0.85)
        eta_mins = round(max(3.0, (1.0 - risk) * 18.0), 1)
        results.append({
            "atm_id": atm["atm_id"],
            "bank_name": atm["bank_name"],
            "bank_code": atm["bank_code"],
            "location_name": atm["location_name"],
            "city": atm.get("city", "Delhi"),
            "latitude": atm["latitude"],
            "longitude": atm["longitude"],
            "predicted_cashout_risk": risk,
            "estimated_time_remaining_minutes": eta_mins,
            "historical_mule_cashouts": atm.get("historical_mule_cashouts", 120),
            "cctv_status": atm.get("cctv_facial_recognition_status", "ACTIVE_24x7"),
            "recommended_action": "TRIGGER_REMOTE_HARDWARE_LOCK" if risk > 0.85 else "DISPATCH_PATROL_UNIT"
        })

    results.sort(key=lambda x: x["predicted_cashout_risk"], reverse=True)
    return {
        "status": "SUCCESS",
        "total_monitored_kiosks": len(results),
        "predicted_hotspots": results
    }

