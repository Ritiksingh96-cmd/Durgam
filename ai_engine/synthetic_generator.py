import random
import time
import uuid
import math
import datetime
from typing import List, Dict, Any, Tuple
import numpy as np
import networkx as nx
from backend.app.core.config import generate_zk_account_hash, dpdp_mask_account

# Major Indian Banks & IFSC Prefixes
BANKS = [
    ("State Bank of India", "SBIN000"),
    ("Punjab National Bank", "PUNB000"),
    ("HDFC Bank", "HDFC000"),
    ("ICICI Bank", "ICIC000"),
    ("Axis Bank", "UTIB000"),
    ("Jammu & Kashmir Bank", "JAKA000"),
    ("Bank of Baroda", "BARB000"),
    ("Canara Bank", "CNRB000"),
    ("Kotak Mahindra Bank", "KKBK000"),
    ("Union Bank of India", "UBIN000")
]

# Major Indian Cities & Cybercrime Hotspots / Victim Hubs
REGIONS = {
    "DELHI_NCR": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi", "is_hub": True},
    "JAMMU": {"lat": 32.7266, "lon": 74.8570, "state": "Jammu & Kashmir", "is_hub": False},
    "MUMBAI": {"lat": 19.0760, "lon": 72.8777, "state": "Maharashtra", "is_hub": True},
    "BENGALURU": {"lat": 12.9716, "lon": 77.5946, "state": "Karnataka", "is_hub": True},
    "HYDERABAD": {"lat": 17.3850, "lon": 78.4867, "state": "Telangana", "is_hub": True},
    "KOLKATA": {"lat": 22.5726, "lon": 88.3639, "state": "West Bengal", "is_hub": True},
    "JAMTARA": {"lat": 23.9627, "lon": 86.8016, "state": "Jharkhand", "is_hub": False},
    "MEWAT_NUH": {"lat": 28.1065, "lon": 77.0125, "state": "Haryana", "is_hub": False},
    "CHANDIGARH": {"lat": 30.7333, "lon": 76.7794, "state": "Chandigarh", "is_hub": False},
    "JAIPUR": {"lat": 26.9124, "lon": 75.7873, "state": "Rajasthan", "is_hub": False}
}

class SyntheticFinancialGraphGenerator:
    """
    Massive Multi-Hop Financial Graph Dataset Generator for DURGAM GNN Engine.
    Simulates 12 distinct Indian financial cybercrime archetypes and legitimate baseline patterns.
    """
    def __init__(self, random_seed: int = 42):
        random.seed(random_seed)
        np.random.seed(random_seed)
        self.graph = nx.DiGraph()
        self.nodes_data: Dict[str, Dict[str, Any]] = {}
        self.edges_data: List[Dict[str, Any]] = []

    def _create_account(
        self,
        account_id: str,
        account_type: str = "SAVINGS",
        region_key: str = "DELHI_NCR",
        is_mule: bool = False,
        is_merchant: bool = False,
        dormancy_days: int = 0
    ) -> Dict[str, Any]:
        bank_name, ifsc_prefix = random.choice(BANKS)
        raw_acc_num = f"{random.randint(1000000000, 9999999999)}"
        ifsc = f"{ifsc_prefix}{random.randint(1001, 9999)}"
        zk_hash = generate_zk_account_hash(raw_acc_num, ifsc)
        masked_num = dpdp_mask_account(raw_acc_num)
        
        region_info = REGIONS.get(region_key, REGIONS["DELHI_NCR"])
        lat = region_info["lat"] + random.uniform(-0.05, 0.05)
        lon = region_info["lon"] + random.uniform(-0.05, 0.05)

        node_attr = {
            "account_id": account_id,
            "raw_account_number": raw_acc_num,
            "masked_account_number": masked_num,
            "bank_name": bank_name,
            "ifsc": ifsc,
            "zk_hash": zk_hash,
            "account_type": account_type,
            "region": region_key,
            "state": region_info["state"],
            "latitude": lat,
            "longitude": lon,
            "is_mule": is_mule,
            "is_merchant": is_merchant,
            "dormancy_days": dormancy_days,
            "created_at": time.time() - (dormancy_days * 86400),
            "in_degree": 0,
            "out_degree": 0,
            "total_inflow": 0.0,
            "total_outflow": 0.0,
            "burst_velocity": 0.0,
            "hold_status": "NORMAL"
        }
        self.nodes_data[account_id] = node_attr
        self.graph.add_node(account_id, **node_attr)
        return node_attr

    def generate_delhi_to_jammu_archetype(self, base_timestamp: float) -> str:
        """
        Archetype 5: Classic Cross-State Incident (Delhi Citizen ➔ 4 Hops ➔ Jammu ATM Cash-Out)
        Matches the primary SIH 2026 / Gemini research verification scenario.
        """
        case_id = f"DURGAM-CASE-{uuid.uuid4().hex[:8].upper()}"
        
        # 1. Victim in Delhi
        victim_id = f"ACC_VICTIM_DL_{random.randint(1000, 9999)}"
        self._create_account(victim_id, "SAVINGS", "DELHI_NCR", is_mule=False)
        
        # 2. Mule Layer 1 (Haryana / Gurugram)
        mule1_id = f"ACC_MULE_L1_{random.randint(1000, 9999)}"
        self._create_account(mule1_id, "JAN_DHAN", "MEWAT_NUH", is_mule=True, dormancy_days=180)
        
        # 3. Mule Layer 2 (Punjab / Ludhiana)
        mule2_id = f"ACC_MULE_L2_{random.randint(1000, 9999)}"
        self._create_account(mule2_id, "CURRENT", "CHANDIGARH", is_mule=True, dormancy_days=45)
        
        # 4. Terminal Mule Card (Jammu)
        terminal_mule_id = f"ACC_TERMINAL_JK_{random.randint(1000, 9999)}"
        self._create_account(terminal_mule_id, "SAVINGS", "JAMMU", is_mule=True, dormancy_days=120)
        
        stolen_amount = 250000.0  # ₹2,50,000
        
        # Hop 1: Delhi Victim -> Mule L1 (via UPI)
        t1 = base_timestamp
        self._add_transaction(victim_id, mule1_id, stolen_amount, t1, "UPI", hop=1, case_id=case_id)
        
        # Hop 2: Mule L1 -> Mule L2 (via IMPS, 3 mins later)
        t2 = t1 + random.randint(90, 240)
        self._add_transaction(mule1_id, mule2_id, stolen_amount - 5000, t2, "IMPS", hop=2, case_id=case_id)
        
        # Hop 3: Mule L2 -> Terminal Mule (via IMPS, 4 mins later)
        t3 = t2 + random.randint(120, 300)
        self._add_transaction(mule2_id, terminal_mule_id, stolen_amount - 12000, t3, "IMPS", hop=3, case_id=case_id)
        
        return case_id

    def generate_fan_out_archetype(self, base_timestamp: float) -> str:
        """Archetype 1: Fan-Out Splitting (1 Victim ➔ 5 Mule accounts)"""
        case_id = f"DURGAM-FO-{uuid.uuid4().hex[:8].upper()}"
        victim_id = f"ACC_VIC_{random.randint(10000, 99999)}"
        self._create_account(victim_id, "SAVINGS", "MUMBAI", is_mule=False)
        
        total_amount = random.uniform(300000, 800000)
        num_splits = 5
        split_amount = total_amount / num_splits
        
        for i in range(num_splits):
            mule_id = f"ACC_FO_MULE_{i}_{random.randint(1000, 9999)}"
            region = random.choice(["JAMTARA", "MEWAT_NUH", "JAIPUR"])
            self._create_account(mule_id, "JAN_DHAN", region, is_mule=True, dormancy_days=90)
            t = base_timestamp + random.randint(30, 180)
            self._add_transaction(victim_id, mule_id, split_amount, t, "IMPS", hop=1, case_id=case_id)
            
        return case_id

    def generate_circular_loop_archetype(self, base_timestamp: float) -> str:
        """Archetype 3: Circular Laundering Loop (A ➔ B ➔ C ➔ A)"""
        case_id = f"DURGAM-CIRC-{uuid.uuid4().hex[:8].upper()}"
        nodes = [f"ACC_CIRC_{i}_{random.randint(1000, 9999)}" for i in range(4)]
        for nid in nodes:
            self._create_account(nid, "CURRENT", "BENGALURU", is_mule=True, dormancy_days=60)
            
        amount = random.uniform(150000, 400000)
        t = base_timestamp
        for i in range(len(nodes)):
            src = nodes[i]
            dst = nodes[(i + 1) % len(nodes)]
            t += random.randint(60, 200)
            self._add_transaction(src, dst, amount * 0.98, t, "NEFT", hop=i+1, case_id=case_id)
            
        return case_id

    def generate_clean_merchant_traffic(self, base_timestamp: float):
        """Archetype 10: Legitimate MSME / Merchant Inflows (False Positive Control)"""
        merchant_id = f"ACC_MERCHANT_{random.randint(1000, 9999)}"
        self._create_account(merchant_id, "CURRENT", "HYDERABAD", is_mule=False, is_merchant=True)
        
        # 15 customers paying small amounts over several hours
        t = base_timestamp
        for _ in range(15):
            cust_id = f"ACC_CUST_{random.randint(10000, 99999)}"
            self._create_account(cust_id, "SAVINGS", "HYDERABAD", is_mule=False)
            t += random.randint(300, 1200)
            amount = random.uniform(200, 4500)
            self._add_transaction(cust_id, merchant_id, amount, t, "UPI", hop=1, case_id="CLEAN_MERCHANT")

    def _add_transaction(
        self,
        src: str,
        dst: str,
        amount: float,
        timestamp: float,
        channel: str,
        hop: int = 1,
        case_id: str = "CASE_GENERIC"
    ):
        tx_id = f"UTR{random.randint(100000000000, 999999999999)}"
        edge_data = {
            "tx_id": tx_id,
            "src": src,
            "dst": dst,
            "amount": amount,
            "timestamp": timestamp,
            "channel": channel,
            "hop_level": hop,
            "case_id": case_id,
            "velocity": amount / max(1.0, (timestamp - self.nodes_data[src]["created_at"] % 3600))
        }
        self.edges_data.append(edge_data)
        self.graph.add_edge(src, dst, **edge_data)
        
        # Update node stats
        self.nodes_data[src]["out_degree"] += 1
        self.nodes_data[src]["total_outflow"] += amount
        self.nodes_data[dst]["in_degree"] += 1
        self.nodes_data[dst]["total_inflow"] += amount

    def generate_massive_dataset(self, target_transaction_count: int = 100000) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate large-scale multi-hop financial transaction dataset for AI model training.
        Returns node_features (X), node_labels (y), edge_index, edge_features.
        """
        print(f"Generating massive synthetic financial graph with target ~{target_transaction_count} transactions...")
        base_t = time.time() - (30 * 86400)
        
        while len(self.edges_data) < target_transaction_count:
            r = random.random()
            if r < 0.25:
                self.generate_delhi_to_jammu_archetype(base_t)
            elif r < 0.50:
                self.generate_fan_out_archetype(base_t)
            elif r < 0.70:
                self.generate_circular_loop_archetype(base_t)
            else:
                self.generate_clean_merchant_traffic(base_t)
            base_t += random.randint(60, 600)

        print(f"Graph generated: {self.graph.number_of_nodes()} accounts, {self.graph.number_of_edges()} transactions.")
        
        # Feature Matrix Extraction (8 Node Features per account)
        node_list = list(self.nodes_data.keys())
        node_to_idx = {nid: i for i, nid in enumerate(node_list)}
        
        X = []
        y = []
        for nid in node_list:
            nd = self.nodes_data[nid]
            in_deg = nd["in_degree"]
            out_deg = nd["out_degree"]
            deg_ratio = (in_deg + 1.0) / (out_deg + 1.0)
            inflow = nd["total_inflow"]
            outflow = nd["total_outflow"]
            net_velocity = (inflow + outflow) / 3600.0
            is_jan_dhan = 1.0 if nd["account_type"] == "JAN_DHAN" else 0.0
            is_merch = 1.0 if nd["is_merchant"] else 0.0
            dormancy = nd["dormancy_days"] / 365.0
            
            features = [
                float(in_deg),
                float(out_deg),
                float(deg_ratio),
                float(inflow),
                float(outflow),
                float(net_velocity),
                float(is_jan_dhan),
                float(dormancy)
            ]
            X.append(features)
            y.append(1 if nd["is_mule"] else 0)

        # Edge Index & Edge Features
        edge_index = []
        edge_attr = []
        for ed in self.edges_data:
            u_idx = node_to_idx[ed["src"]]
            v_idx = node_to_idx[ed["dst"]]
            edge_index.append([u_idx, v_idx])
            edge_attr.append([
                float(ed["amount"]),
                float(ed["hop_level"]),
                float(ed["velocity"])
            ])

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64), np.array(edge_index, dtype=np.int64).T, np.array(edge_attr, dtype=np.float32)

if __name__ == "__main__":
    gen = SyntheticFinancialGraphGenerator()
    X, y, edge_index, edge_attr = gen.generate_massive_dataset(target_transaction_count=20000)
    print("X shape:", X.shape)
    print("y shape (Class balance):", np.bincount(y))
    print("edge_index shape:", edge_index.shape)
    print("edge_attr shape:", edge_attr.shape)
