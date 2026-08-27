import os
import hashlib
import hmac
from typing import Optional, Dict, Any

class Settings:
    PROJECT_NAME: str = "DURGAM (Dynamic Unified Risk-Grid & Geospatial Analytics Module)"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("DURGAM_SECRET_KEY", "durgam_sovereign_nic_secret_key_2026_mha_i4c")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # DPDP Act 2023 Salt
    DPDP_CONSORTIUM_SALT: str = os.getenv("DPDP_SALT", "durgam_consortium_salted_hash_v1_dpdp2023")
    
    # Blockchain Configuration (Polygon Amoy Testnet / Hyperledger Besu)
    POLYGON_AMOY_RPC: str = "https://rpc-amoy.polygon.technology"
    EVIDENCE_CONTRACT_ADDRESS: str = "0x7E6cD5Db49019A96f77293DA7F9b000000000000"
    
    # Sovereign API Keys & Gateways
    DURGAM_ADMIN_API_KEY: str = os.getenv("DURGAM_ADMIN_API_KEY", "durgam_sovereign_mha_admin_master_key_2026")
    DURGAM_POLICE_API_KEY: str = os.getenv("DURGAM_POLICE_API_KEY", "durgam_nc4_police_command_token_2026")
    DURGAM_BANK_API_KEY: str = os.getenv("DURGAM_BANK_API_KEY", "durgam_npci_iso20022_switch_token_2026")
    
    # Auto-Trigger Autonomous Rule Matrix
    AUTO_TRIGGER_ENABLED: bool = True
    AUTO_HOLD_THRESHOLD_INR: float = 50000.0  # Auto-hold if financial loss >= 50k
    AUTO_HOLD_RISK_SCORE_THRESHOLD: float = 0.85  # GNN Mule score >= 0.85
    AUTO_CAD_DISPATCH_PROBABILITY: float = 0.80  # ST-KDE ATM cashout probability >= 80%
    AUTO_CAD_MAX_ETA_MINUTES: float = 8.0  # CAD Unit ETA under 8 minutes
    AUTO_IMEI_BLOCK_COMPLAINT_COUNT: int = 2  # Block IMEI automatically upon 2 corroborating complaints
    AUTO_ALERT_RBI_FIU_THRESHOLD_INR: float = 1000000.0  # Auto-alert RBI/FIU on >= ₹10 Lakhs
    
    # Micro-Hold Configuration
    MICRO_HOLD_DURATION_MINUTES: int = 30
    AUTO_DECAY_ENABLED: bool = True
    
    # Sovereign Telemetry
    ZERO_COMMERCIAL_CLOUD_TELEMETRY: bool = True

    # External API Integration Endpoints
    SANCHAR_SAATHI_CEIR_URL: str = "https://sancharsaathi.gov.in/api/v1/ceir/blacklist"
    NPCI_CAMT056_SWITCH_URL: str = "https://npci.org.in/switch/iso20022/camt056"
    BSA_SECTION63_LEDGER_URL: str = "https://amoy.polygonscan.com/address/0x7E6cD5Db49019A96f77293DA7F9b000000000000"

settings = Settings()

def dpdp_mask_account(account_number: str) -> str:
    """Mask account number for DPDP Act 2023 compliance (e.g. 'XXXX-XXXX-4821')"""
    if not account_number or len(account_number) < 4:
        return "XXXX-XXXX-0000"
    last_four = account_number[-4:]
    return f"XXXX-XXXX-{last_four}"

def dpdp_mask_name(name: str) -> str:
    """Mask citizen/suspect name for privacy (e.g. 'R*** K***')"""
    if not name:
        return "A*** N***"
    parts = name.split()
    masked_parts = [p[0] + "***" if len(p) > 1 else p for p in parts]
    return " ".join(masked_parts)

def generate_zk_account_hash(account_number: str, ifsc_code: str) -> str:
    """
    DPDP Act 2023 Compliant Zero-Knowledge Consortium Mule Registry Hash:
    AccountHash = SHA256(AccountNumber || IFSC || Salt)
    Allows inter-bank queries without disclosing sensitive customer PII or balances.
    """
    raw = f"{account_number.strip().upper()}:{ifsc_code.strip().upper()}:{settings.DPDP_CONSORTIUM_SALT}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def calculate_sha256(data: str) -> str:
    """Calculate SHA-256 hash of any string payload"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()
