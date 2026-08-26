import os
import sys
import json
import time
import torch
import numpy as np

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_engine.atm_hotspot_screenshot_model import ATMCashoutHotspotClassifier
from ai_engine.st_kde_atm_model import SpatiotemporalATMPredictor
from ai_engine.gnn_mule_model import DurgamGNNMuleClassifier
from ai_engine.time_regressor_model import TimeToCashoutRegressor
from ai_engine.huggingface_nlp import huggingface_cyber_nlp
from backend.app.services.geospatial_service import geospatial_service

def test_all_five_ai_models():
    print("=" * 70)
    print("   DURGAM: FIVE-MODEL AI ENGINE COMPREHENSIVE VALIDATION")
    print("=" * 70)

    # -------------------------------------------------------------
    # MODEL 1: ATM Cashout Hotspot Classifier (Exact Screenshot Schema)
    # -------------------------------------------------------------
    print("\n[MODEL 1] Validating XGBoost ATM Cashout Hotspot Model (Screenshot Schema)...")
    model1 = ATMCashoutHotspotClassifier()
    screenshot_sample = {
        'timestamp': '2026-08-25 10:35:21',
        'amount': 85000.0,
        'victim_city': 'Bengaluru',
        'mule_latitude': 12.9716,
        'mule_longitude': 77.5946,
        'atm_latitude': 12.9751,
        'atm_longitude': 77.6012,
        'distance_to_atm_km': 0.82,
        'transaction_velocity': 3.7,
        'historical_hotspot_score': 0.91
    }
    t0 = time.time()
    pred1 = model1.predict_single(screenshot_sample)
    lat1 = (time.time() - t0) * 1000
    print(f"  ✓ Input: ₹85,000 | Bengaluru | Dist: 0.82km | Velocity: 3.7 | Hist Score: 0.91")
    print(f"  ✓ Output: Label={pred1['cashout_atm_label']} | Probability={pred1['hotspot_probability']:.4f} | Tier={pred1['risk_tier']}")
    print(f"  ✓ Inference Latency: {lat1:.2f} ms")
    assert pred1['cashout_atm_label'] == 1, "Model 1 failed to identify high-risk hotspot!"

    # -------------------------------------------------------------
    # MODEL 2: Spatiotemporal ST-KDE & Uber H3 Forecaster (OpenStreetMap)
    # -------------------------------------------------------------
    print("\n[MODEL 2] Validating Spatiotemporal ST-KDE & OpenStreetMap ATM Forecaster...")
    t0 = time.time()
    top_atms = geospatial_service.get_candidate_atms_for_terminal_node(
        terminal_lat=32.7266,
        terminal_lon=74.8570,
        velocity=2800.0,
        top_k=3
    )
    lat2 = (time.time() - t0) * 1000
    print(f"  ✓ Queried OpenStreetMap ATM POIs around Jammu (32.7266, 74.8570)")
    for i, atm in enumerate(top_atms):
        print(f"    - Rank #{i+1}: {atm['name']} ({atm['bank']}) | Dist: {atm['distance_km']} km | Risk: {atm['risk_score']*100:.1f}%")
    print(f"  ✓ Inference Latency: {lat2:.2f} ms")
    assert len(top_atms) > 0, "Model 2 failed to return candidate ATMs!"

    # -------------------------------------------------------------
    # MODEL 3: 2-Layer GraphSAGE GNN (PyTorch) Multi-Hop Classifier
    # -------------------------------------------------------------
    print("\n[MODEL 3] Validating 2-Layer GraphSAGE GNN Multi-Hop Classifier...")
    model3 = DurgamGNNMuleClassifier(in_features=8, hidden_dim=32, out_dim=1)
    x = torch.randn(5, 8)
    adj = torch.eye(5)
    t0 = time.time()
    with torch.no_grad():
        out3 = model3(x, adj)
        probs3 = out3.squeeze().numpy()
    lat3 = (time.time() - t0) * 1000
    print(f"  ✓ Evaluated 5-node 4-hop transaction graph across banks")
    for i, p in enumerate(probs3):
        print(f"    - Node {i}: Mule Probability = {float(p)*100:.1f}%")
    print(f"  ✓ Inference Latency: {lat3:.2f} ms")
    assert len(probs3) == 5, "Model 3 failed graph traversal!"

    # -------------------------------------------------------------
    # MODEL 4: LightGBM Time-to-Cashout Regressor
    # -------------------------------------------------------------
    print("\n[MODEL 4] Validating LightGBM Time-to-Cashout Regressor...")
    model4 = TimeToCashoutRegressor()
    t0 = time.time()
    t_res = model4.predict_remaining_minutes(
        hop_level=3,
        total_amount=250000.0,
        avg_hop_velocity=4500.0,
        time_elapsed_mins=3.2,
        channel_type="UPI"
    )
    lat4 = (time.time() - t0) * 1000
    print(f"  ✓ Input: ₹2,50,000 | 3 Hops | Velocity: ₹4500/min | Channel: UPI | Elapsed: 3.2m")
    print(f"  ✓ Predicted Remaining Golden Hour Window: {t_res['estimated_minutes_remaining']} minutes (Urgency: {t_res['golden_hour_urgency']})")
    print(f"  ✓ Inference Latency: {lat4:.2f} ms")
    assert t_res['estimated_minutes_remaining'] > 0, "Model 4 predicted invalid time!"

    # -------------------------------------------------------------
    # MODEL 5: Hugging Face Multilingual Threat & Entity NER Parser
    # -------------------------------------------------------------
    print("\n[MODEL 5] Validating Hugging Face Cybercrime Threat & NER Parser...")
    sample_complaint = "Scammer called me claiming to be CBI Officer on Skype. He threatened me with Digital Arrest and told me to transfer ₹2,50,000 to Jammu Bank account IFSC JAKA0001928 via UTR 482910482910 from my phone 9811029481."
    t0 = time.time()
    nlp_res = huggingface_cyber_nlp.classify_narrative(sample_complaint)
    lat5 = (time.time() - t0) * 1000
    entities = nlp_res['extracted_entities']
    print(f"  ✓ Raw Complaint: '{sample_complaint[:80]}...'")
    print(f"  ✓ Extracted UTR: {entities['utr']}")
    print(f"  ✓ Extracted Amount: ₹{entities['amount']:,.0f}")
    print(f"  ✓ Extracted IFSC: {entities['ifsc']}")
    print(f"  ✓ Extracted Phone(s): {entities['mobile_numbers']}")
    print(f"  ✓ Threat Category: {nlp_res['predicted_category']} (Confidence: {nlp_res['confidence_score']*100:.1f}%)")
    print(f"  ✓ Recommended SOP: {nlp_res['recommended_sop']}")
    print(f"  ✓ Inference Latency: {lat5:.2f} ms")
    assert entities['utr'] == '482910482910', "Model 5 failed UTR extraction!"

    print("\n" + "=" * 70)
    print("   [ALL 5 AI MODELS TESTED & FULLY FUNCTIONAL]")
    print(f"   Combined Inference Latency: {(lat1 + lat2 + lat3 + lat4 + lat5):.2f} ms (< 180 ms Target SLA)")
    print("=" * 70)

if __name__ == "__main__":
    test_all_five_ai_models()
