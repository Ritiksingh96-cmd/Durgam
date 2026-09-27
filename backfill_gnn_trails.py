import sqlite3
import json
import time
import os
import sys

# Ensure backend modules can be imported
sys.path.insert(0, os.path.abspath("."))

from backend.app.services.graph_service import graph_engine
from backend.app.services.geospatial_service import geospatial_service

db_path = os.path.join("backend", "durgam_sovereign.db")
if not os.path.exists(db_path):
    print(f"Error: Database not found at {db_path}")
    sys.exit(1)

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT case_id, ack_number, victim_name, victim_state, source_bank, source_account, loss_amount, extra_data_json FROM incidents")
rows = cursor.fetchall()

print(f"Found {len(rows)} incidents in database. Backfilling live GNN multi-hop trails...")

updated_count = 0
for r in rows:
    case_id = r["case_id"]
    victim_name = r["victim_name"] or "Complainant"
    victim_state = r["victim_state"] or "Delhi"
    source_bank = r["source_bank"] or "State Bank of India"
    source_acc = r["source_account"] or "XXXX-XXXX-1234"
    loss_amount = float(r["loss_amount"] or 250000.0)

    # Execute dynamic GNN multi-hop graph inference
    trail = graph_engine.trace_case_trail(
        case_id=case_id,
        victim_name=victim_name,
        victim_account=source_acc,
        source_bank=source_bank,
        amount=loss_amount,
        victim_state=victim_state
    )

    nodes = trail.get("nodes", [])
    terminal_node = trail.get("terminal_account", {})
    nodes_json = json.dumps(nodes)
    terminal_node_json = json.dumps(terminal_node)

    # Compute candidate ATMs for this terminal node
    lat = terminal_node.get("latitude", 28.6139)
    lon = terminal_node.get("longitude", 77.2090)
    candidate_atms = geospatial_service.get_candidate_atms_for_terminal_node(lat, lon, loss_amount / 120.0, top_k=3)

    # Update extra_data_json
    extra = {}
    if r["extra_data_json"]:
        try:
            extra = json.loads(r["extra_data_json"])
        except Exception:
            extra = {}

    extra["candidate_atms"] = candidate_atms
    if "universal_docket" in extra:
        extra["universal_docket"]["predicted_atm"] = candidate_atms[0]["name"] if candidate_atms else terminal_node.get("atm_name", "Terminal ATM")
    extra_data_json = json.dumps(extra, default=str)

    # Update database record
    cursor.execute("""
        UPDATE incidents
        SET nodes_json = ?,
            terminal_node_json = ?,
            extra_data_json = ?
        WHERE case_id = ?
    """, (nodes_json, terminal_node_json, extra_data_json, case_id))

    updated_count += 1
    print(f"[{updated_count}/{len(rows)}] Updated {case_id} ({source_bank} -> {nodes[1]['bank']} -> {nodes[2]['bank']} -> {nodes[3]['bank']})")

conn.commit()
conn.close()
print(f"\nSuccessfully backfilled all {updated_count} incidents with dynamic PyTorch GNN trails in {db_path}!")
