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
    
    # Micro-Hold Configuration
    MICRO_HOLD_DURATION_MINUTES: int = 30
    AUTO_DECAY_ENABLED: bool = True
    
    # Sovereign Telemetry
    ZERO_COMMERCIAL_CLOUD_TELEMETRY: bool = True

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
