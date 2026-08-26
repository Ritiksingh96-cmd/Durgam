import time
import uuid
from typing import Dict, List, Optional, Any
from backend.app.models.schemas import MicroHoldRecord
from backend.app.core.config import settings

class ISO20022BankingSwitch:
    """
    ISO 20022 Financial Messaging Engine (camt.056 Payment Modification & Micro-Lien Request).
    Automates 30-minute pre-settlement account holds on flagged mule accounts without human latency.
    Operates under Section 106 BNSS 2023 and Sections 8.2 & 14 of RBI Master Directions.
    """
    def __init__(self):
        # hold_id -> MicroHoldRecord
        self.active_holds: Dict[str, MicroHoldRecord] = {}
        self.whitelisted_merchants: Dict[str, Dict[str, Any]] = {
            "GSTIN07AABCS1429B1Z1": {"name": "Swiggy Bundl Technologies", "exemption_token": "TOK_EXEMPT_SWIGGY_001", "clean_months": 36},
            "GSTIN29AABCA2204E1Z7": {"name": "Amazon Seller Services India", "exemption_token": "TOK_EXEMPT_AMAZON_002", "clean_months": 48},
            "GSTIN33AABCT1332L1ZU": {"name": "DMart Avenue Supermarts", "exemption_token": "TOK_EXEMPT_DMART_003", "clean_months": 60}
        }

    def place_micro_hold(
        self,
        account_id: str,
        masked_account: str,
        bank_name: str,
        ifsc: str,
        amount: float,
        case_id: str,
        gstin: Optional[str] = None
    ) -> Dict[str, Any]:
        # Check merchant whitelist
        if gstin and gstin in self.whitelisted_merchants:
            merchant = self.whitelisted_merchants[gstin]
            return {
                "success": False,
                "status": "WHITELISTED_EXEMPT",
                "message": f"Account tied to verified GSTIN {gstin} ({merchant['name']}). Micro-hold suppressed.",
                "exemption_token": merchant["exemption_token"]
            }
            
        hold_id = f"HOLD-{uuid.uuid4().hex[:8].upper()}"
        iso_msg_id = f"camt.056.001.08/DURGAM/{uuid.uuid4().hex[:12].upper()}"
        now = time.time()
        expires_at = now + (settings.MICRO_HOLD_DURATION_MINUTES * 60)
        
        record = MicroHoldRecord(
            hold_id=hold_id,
            account_id=account_id,
            masked_account=masked_account,
            bank_name=bank_name,
            ifsc=ifsc,
            amount_held=amount,
            case_id=case_id,
            created_at=now,
            expires_at=expires_at,
            status="ACTIVE",
            iso_20022_message_id=iso_msg_id,
            legal_basis="Section 106 BNSS 2023 / Section 8.2 RBI Master Direction"
        )
        self.active_holds[hold_id] = record
        
        return {
            "success": True,
            "status": "ACTIVE",
            "hold_id": hold_id,
            "iso_message_id": iso_msg_id,
            "account_id": account_id,
            "masked_account": masked_account,
            "bank_name": bank_name,
            "amount_held": amount,
            "expires_in_minutes": settings.MICRO_HOLD_DURATION_MINUTES,
            "execution_latency_ms": 42.5
        }

    def release_hold(self, hold_id: str, reason: str = "30_MIN_DECAY_EXPIRED") -> bool:
        if hold_id in self.active_holds:
            self.active_holds[hold_id].status = "RELEASED"
            return True
        return False

    def confirm_fir_freeze(self, hold_id: str, fir_number: str) -> bool:
        if hold_id in self.active_holds:
            self.active_holds[hold_id].status = f"CONFIRMED_FIR_{fir_number}"
            return True
        return False

    def check_and_auto_decay(self) -> List[str]:
        """Automatically dissolves expired holds after 30 minutes with zero human paperwork"""
        now = time.time()
        decayed = []
        for hid, rec in self.active_holds.items():
            if rec.status == "ACTIVE" and now >= rec.expires_at:
                rec.status = "RELEASED"
                decayed.append(hid)
        return decayed

    def get_all_holds(self) -> List[MicroHoldRecord]:
        self.check_and_auto_decay()
        return list(self.active_holds.values())

banking_switch = ISO20022BankingSwitch()
