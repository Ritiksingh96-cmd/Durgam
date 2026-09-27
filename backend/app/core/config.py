import os
import hashlib
import hmac
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

class Settings:
    PROJECT_NAME: str = "DURGAM (Dynamic Unified Risk-Grid & Geospatial Analytics Module)"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("DURGAM_SECRET_KEY", "durgam_sovereign_nic_secret_key_2026_mha_i4c")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # DPDP Act 2023 Salt
    DPDP_CONSORTIUM_SALT: str = os.getenv("DPDP_SALT", "durgam_consortium_salted_hash_v1_dpdp2023")
    
    # Blockchain Configuration (Polygon Amoy Testnet / Infura / Hyperledger Besu)
    INFURA_API_KEY: str = os.getenv("INFURA_API_KEY", "99fdfbaefa39455c9100a4a79b6e79ce")
    POLYGON_AMOY_RPC: str = os.getenv("POLYGON_AMOY_RPC", f"https://polygon-amoy.infura.io/v3/{os.getenv('INFURA_API_KEY', '99fdfbaefa39455c9100a4a79b6e79ce')}")
    POLYGON_MAINNET_RPC: str = os.getenv("POLYGON_MAINNET_RPC", f"https://polygon-mainnet.infura.io/v3/{os.getenv('INFURA_API_KEY', '99fdfbaefa39455c9100a4a79b6e79ce')}")
    EVIDENCE_CONTRACT_ADDRESS: str = os.getenv("EVIDENCE_CONTRACT_ADDRESS", "0x7E6cD5Db49019A96f77293DA7F9b000000000000")
    
    # Sovereign API Keys & Gateways
    DURGAM_ADMIN_API_KEY: str = os.getenv("DURGAM_ADMIN_API_KEY", "durgam_sovereign_mha_admin_master_key_2026")
    DURGAM_POLICE_API_KEY: str = os.getenv("DURGAM_POLICE_API_KEY", "durgam_nc4_police_command_token_2026")
    DURGAM_BANK_API_KEY: str = os.getenv("DURGAM_BANK_API_KEY", "durgam_npci_iso20022_switch_token_2026")

    # Telegram Bot API for Police Tactical CAD Turn-by-Turn Dispatch
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_POLICE_CHAT_ID: str = os.getenv("TELEGRAM_POLICE_CHAT_ID", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    POLICE_OFFICER_NAME: str = os.getenv("POLICE_OFFICER_NAME", "ASI Virender / SI Rajesh Hooda")
    
    # Auto-Trigger Autonomous Rule Matrix
    AUTO_TRIGGER_ENABLED: bool = os.getenv("AUTO_TRIGGER_ENABLED", "True").lower() in ("true", "1", "yes")
    AUTO_HOLD_THRESHOLD_INR: float = float(os.getenv("AUTO_HOLD_THRESHOLD_INR", "50000.0"))
    AUTO_HOLD_RISK_SCORE_THRESHOLD: float = float(os.getenv("AUTO_HOLD_RISK_SCORE_THRESHOLD", "0.85"))
    AUTO_CAD_DISPATCH_PROBABILITY: float = float(os.getenv("AUTO_CAD_DISPATCH_PROBABILITY", "0.80"))
    AUTO_CAD_MAX_ETA_MINUTES: float = float(os.getenv("AUTO_CAD_MAX_ETA_MINUTES", "8.0"))
    AUTO_IMEI_BLOCK_COMPLAINT_COUNT: int = int(os.getenv("AUTO_IMEI_BLOCK_COMPLAINT_COUNT", "2"))
    AUTO_ALERT_RBI_FIU_THRESHOLD_INR: float = float(os.getenv("AUTO_ALERT_RBI_FIU_THRESHOLD_INR", "1000000.0"))
    
    # Micro-Hold Configuration
    MICRO_HOLD_DURATION_MINUTES: int = int(os.getenv("MICRO_HOLD_DURATION_MINUTES", "30"))
    AUTO_DECAY_ENABLED: bool = True
    
    # Sovereign Telemetry
    ZERO_COMMERCIAL_CLOUD_TELEMETRY: bool = True

    # External API Integration Endpoints
    SANCHAR_SAATHI_CEIR_URL: str = os.getenv("SANCHAR_SAATHI_CEIR_URL", "https://sancharsaathi.gov.in/api/v1/ceir/blacklist")
    NPCI_CAMT056_SWITCH_URL: str = os.getenv("NPCI_CAMT056_SWITCH_URL", "https://npci.org.in/switch/iso20022/camt056")
    BSA_SECTION63_LEDGER_URL: str = os.getenv("BSA_SECTION63_LEDGER_URL", "https://amoy.polygonscan.com/address/0x7E6cD5Db49019A96f77293DA7F9b000000000000")

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
