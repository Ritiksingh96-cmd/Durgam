import os
import sys
import time
import json

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app.services.graph_service import graph_engine
from backend.app.services.banking_switch import banking_switch
from backend.app.services.geospatial_service import geospatial_service
from backend.app.services.blockchain_service import blockchain_service
from ai_engine.time_regressor_model import TimeToCashoutRegressor
from ai_engine.nlp_parser import GrievanceParser1930

def run_delhi_to_jammu_simulation():
    print("=" * 70)
    print("   PROJECT DURGAM: END-TO-END CROSS-STATE INTERCEPTION SIMULATION")
    print("   Scenario: Delhi Citizen Complaint -> Multi-Hop Mule -> Jammu ATM")
    print("=" * 70)
    
    t_start = time.time()
    
    # Step 1: Ingestion
    print("\n[Step 1] Ingesting Citizen Incident Complaint from Delhi (Helpline 1930)...")
    raw_complaint = (
        "Received call claiming to be CBI Officer in Digital Arrest scam. "
        "Forced to transfer Rs 2,50,000 to fraud account. UTR: 482910482910."
    )
    parser = GrievanceParser1930()
    nlp_res = parser.parse(raw_complaint)
    print(f"  ✓ NLP Parsed: UTR={nlp_res['extracted_utr']}, Amount=₹{nlp_res['loss_amount_inr']:,.0f}, Category={nlp_res['crime_category']}")
    
    # Step 2: Multi-Hop GNN Graph Traversal (< 85ms)
    print("\n[Step 2] Executing Multi-Hop Graph Traversal Across Bank Boundaries...")
    case_id = "DURGAM-DL-JK-001"
    graph_res = graph_engine.trace_case_trail(
        case_id=case_id,
        victim_name="Dr. Rajiv Malhotra",
        victim_account="30948102948",
        source_bank="State Bank of India",
        amount=250000.0,
        victim_state="Delhi",
        target_terminal_city="Jammu"
    )
    print(f"  ✓ Graph Traversed: {len(graph_res['nodes'])} nodes across {graph_res['total_hops']} hops in {graph_res['traversal_latency_ms']} ms")
    for n in graph_res["nodes"]:
        print(f"    - Hop {n['hop_level']}: {n['bank_name']} ({n['masked_account']}) in {n['region']} [{n['state']}] | Mule Prob: {n['mule_probability']*100:.0f}%")
        
    terminal_node = graph_res["terminal_account"]
    
    # Step 3: ISO 20022 Banking Micro-Hold (< 500ms)
    print("\n[Step 3] Dispatching ISO 20022 camt.056 30-Minute Micro-Lien to Bank Switch...")
    hold_res = banking_switch.place_micro_hold(
        account_id=terminal_node["account_id"],
        masked_account=terminal_node["masked_account"],
        bank_name=terminal_node["bank_name"],
        ifsc=terminal_node["ifsc"],
        amount=250000.0,
        case_id=case_id
    )
    print(f"  ✓ Micro-Hold Placed: {hold_res['hold_id']} on {hold_res['bank_name']} ({hold_res['masked_account']})")
    print(f"  ✓ ISO Message ID: {hold_res['iso_message_id']}")
    print(f"  ✓ Auto-Decay Timer: 30 Minutes under Section 106 BNSS 2023")
    
    # Step 4: ST-KDE Spatiotemporal ATM Hotspot Forecast (< 80ms)
    print("\n[Step 4] Computing ST-KDE & Uber H3 Spatiotemporal ATM Hotspot Forecast...")
    candidate_atms = geospatial_service.get_candidate_atms_for_terminal_node(
        terminal_lat=terminal_node["latitude"],
        terminal_lon=terminal_node["longitude"],
        velocity=250000.0 / 120.0,
        top_k=3
    )
    top_atm = candidate_atms[0]
    print(f"  ✓ Top Forecasted ATM: {top_atm['name']} ({top_atm['city']}) | Risk Score: {top_atm['risk_score']*100:.0f}%")
    print(f"    Distance: {top_atm['distance_km']} km | ETA: ~{top_atm['estimated_drive_time_mins']} mins")
    
    # Step 5: Field Police CAD Dispatch
    print("\n[Step 5] Triggering Automated Field Police CAD Dispatch (PCR Van Alert)...")
    dispatch_res = geospatial_service.dispatch_nearest_patrol_unit(
        case_id=case_id,
        target_atm=top_atm,
        stolen_amount=250000.0
    )
    print(f"  ✓ CAD Alert Dispatched to: {dispatch_res['callsign']} ({dispatch_res['driver_name']})")
    print(f"  ✓ Action Message: {dispatch_res['tactical_alert_message']}")
    
    # Step 6: Section 63 BSA Blockchain Evidence Sealing
    print("\n[Step 6] Cryptographic Notarization & Section 63 BSA Evidence Sealing...")
    cert = blockchain_service.seal_case_evidence(
        case_id=case_id,
        utr_number=nlp_res["extracted_utr"],
        victim_state="Delhi",
        terminal_state=terminal_node["state"],
        total_hops=graph_res["total_hops"],
        loss_amount=250000.0,
        terminal_atm_id=top_atm["atm_id"],
        graph_telemetry=graph_res
    )
    print(f"  ✓ Evidence Sealed: Certificate ID {cert.certificate_id}")
    print(f"  ✓ SHA-256 State Hash: {cert.sha256_case_hash}")
    print(f"  ✓ Merkle Root: {cert.merkle_root}")
    print(f"  ✓ Polygon Tx: {cert.polygon_tx_hash}")
    print(f"  ✓ Statutory Admissibility: {cert.legal_section}")
    
    total_elapsed_ms = (time.time() - t_start) * 1000.0
    print("\n" + "=" * 70)
    print(f"   [SUCCESS] PIPELINE EXECUTED IN {total_elapsed_ms:.1f} ms (Target SLA: < 180 ms)")
    print("=" * 70)

if __name__ == "__main__":
    run_delhi_to_jammu_simulation()
