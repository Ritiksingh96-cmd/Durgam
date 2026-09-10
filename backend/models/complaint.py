from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ComplaintStatus(str, Enum):
    PENDING = "pending"
    UNDER_INVESTIGATION = "under_investigation"
    CHAIN_DETECTED = "chain_detected"
    RESOLVED = "resolved"
    CLOSED = "closed"


class FraudType(str, Enum):
    UPI_FRAUD = "UPI Fraud"
    ATM_FRAUD = "ATM Fraud"
    ONLINE_BANKING_FRAUD = "Online Banking Fraud"
    CREDIT_CARD_FRAUD = "Credit Card Fraud"
    INVESTMENT_SCAM = "Investment Scam"
    JOB_SCAM = "Job Scam"
    LOTTERY_SCAM = "Lottery Scam"
    OTHER = "Other"


class ComplaintCreate(BaseModel):
    description: str
    amount: float
    to_account: str          # Mule account number victim sent money TO
    to_bank_ifsc: Optional[str] = None
    transaction_id: Optional[str] = None
    fraud_type: FraudType
    transaction_date: Optional[datetime] = None


class ComplaintResponse(BaseModel):
    id: str
    complaint_no: str
    user_id: str
    user_name: str
    user_mobile: str
    description: str
    amount: float
    to_account: str
    to_bank_ifsc: Optional[str]
    transaction_id: Optional[str]
    fraud_type: str
    status: ComplaintStatus
    created_at: datetime
