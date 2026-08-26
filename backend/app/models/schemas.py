from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
import time

class UserRole(str, Enum):
    CITIZEN = "CITIZEN"
    POLICE_NATIONAL = "POLICE_NATIONAL"
    POLICE_BEAT = "POLICE_BEAT"
    BANK_NODAL = "BANK_NODAL"
    JUDICIARY = "JUDICIARY"
    ADMIN = "ADMIN"

class CrimeCategory(str, Enum):
    DIGITAL_ARREST = "DIGITAL_ARREST"
    PART_TIME_JOB = "PART_TIME_JOB"
    SEXTORTION = "SEXTORTION"
    APK_MALWARE = "APK_MALWARE"
    INVESTMENT_PONZI = "INVESTMENT_PONZI"
    UPI_QR_FRAUD = "UPI_QR_FRAUD"
    FINANCIAL_FRAUD_GENERAL = "FINANCIAL_FRAUD_GENERAL"

class ComplaintCreate(BaseModel):
    victim_name: str = Field(..., example="Amit Kumar")
    victim_phone: str = Field(..., example="9876543210")
    victim_city: str = Field(default="Delhi", example="Delhi")
    victim_state: str = Field(default="Delhi", example="Delhi")
    utr_number: str = Field(..., example="UTR482910482910")
    source_bank: str = Field(default="State Bank of India", example="State Bank of India")
    source_account: str = Field(..., example="40291048291")
    loss_amount: float = Field(..., example=250000.0)
    incident_date: Optional[str] = None
    crime_category: Optional[CrimeCategory] = CrimeCategory.DIGITAL_ARREST
    narrative: Optional[str] = None

class MultiHopNode(BaseModel):
    account_id: str
    masked_account: str
    bank_name: str
    ifsc: str
    zk_hash: str
    account_type: str
    region: str
    state: str
    latitude: float
    longitude: float
    hop_level: int
    mule_probability: float
    is_terminal: bool
    hold_status: str  # NORMAL, MICRO_HOLD, FROZEN

class MultiHopEdge(BaseModel):
    src: str
    dst: str
    amount: float
    timestamp: float
    channel: str
    hop_level: int
    velocity: float

class CandidateATM(BaseModel):
    atm_id: str
    name: str
    bank: str
    lat: float
    lon: float
    city: str
    state: str
    distance_km: float
    estimated_drive_time_mins: int
    risk_score: float
    rank: int
    has_cctv: bool
    is_24x7: bool

class MicroHoldRecord(BaseModel):
    hold_id: str
    account_id: str
    masked_account: str
    bank_name: str
    ifsc: str
    amount_held: float
    case_id: str
    created_at: float
    expires_at: float
    status: str  # ACTIVE, RELEASED, CONFIRMED_FIR
    iso_20022_message_id: str
    legal_basis: str = "Section 106 BNSS 2023 / Section 8.2 RBI Master Direction"

class ZKConsortiumQuery(BaseModel):
    account_number: str
    ifsc_code: str

class ZKQueryResult(BaseModel):
    zk_hash: str
    is_flagged_mule: bool
    risk_tier: str
    last_associated_complaint: Optional[str] = None
    query_timestamp: float = Field(default_factory=time.time)

class EvidenceCertificate(BaseModel):
    certificate_id: str
    case_id: str
    utr_number: str
    victim_state: str
    terminal_state: str
    total_hops: int
    sha256_case_hash: str
    merkle_root: str
    batch_id: int
    polygon_tx_hash: str
    sealed_timestamp: float
    legal_section: str = "Section 63, Bharatiya Sakshya Adhiniyam (BSA) 2023"
    digital_signature: str
