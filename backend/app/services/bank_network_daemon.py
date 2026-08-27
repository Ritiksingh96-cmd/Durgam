"""
DURGAM Continuous Bank Network Daemon Simulator
Runs an autonomous background worker generating realistic multi-bank transactions,
layering hops, and ISO 20022 camt.056 pre-settlement holds every 3.5 seconds.
"""

import asyncio
import random
import time
from typing import Dict, Any, List
from backend.app.services.banking_switch import banking_switch

class ContinuousBankNetworkDaemon:
    def __init__(self):
        self.is_running = False
        self.total_transactions_processed = 14890
        self.total_quarantined_volume_inr = 284500000.0  # ₹28.45 Cr
        self.participating_banks = ["SBIN", "PUNB", "HDFC", "ICIC", "BARB", "CNRB", "UTIB"]
        self.cities = ["Delhi", "Mumbai", "Bengaluru", "Mewat", "Jamtara", "Hyderabad"]

    async def start_simulation_loop(self):
        self.is_running = True
        print("[+] DURGAM Continuous Bank Network Daemon Simulator Started.")

        while self.is_running:
            try:
                await asyncio.sleep(3.5)
                self.total_transactions_processed += random.randint(3, 8)
                
                # 30% chance of a high-risk suspicious mule transfer requiring ISO hold
                if random.random() < 0.35:
                    origin = random.choice(self.participating_banks)
                    dest = random.choice([b for b in self.participating_banks if b != origin])
                    amount = float(random.choice([45000, 95000, 150000, 250000, 480000]))
                    mule_score = round(random.uniform(0.72, 0.98), 2)
                    
                    hold_rec = banking_switch.execute_pre_settlement_hold(
                        account_number=f"{random.randint(10000000000, 99999999999)}",
                        bank_ifsc=f"{dest}00010{random.randint(10, 99)}",
                        amount=amount,
                        mule_score=mule_score
                    )
                    self.total_quarantined_volume_inr += amount
            except Exception as e:
                print(f"[!] Daemon simulation tick exception: {e}")
                await asyncio.sleep(5)

    def get_simulation_telemetry(self) -> Dict[str, Any]:
        return {
            "status": "RUNNING" if self.is_running else "PAUSED",
            "total_transactions_processed": self.total_transactions_processed,
            "total_quarantined_volume_inr": self.total_quarantined_volume_inr,
            "total_quarantined_volume_crores": round(self.total_quarantined_volume_inr / 10000000.0, 2),
            "active_cbs_nodes_count": len(self.participating_banks),
            "tick_interval_seconds": 3.5
        }

bank_network_daemon = ContinuousBankNetworkDaemon()
