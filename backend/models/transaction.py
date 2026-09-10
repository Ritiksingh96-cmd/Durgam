from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TransactionRecord(BaseModel):
    transaction_id: Optional[str] = None
    to_account: str
    to_bank_ifsc: Optional[str] = None
    amount: float
    timestamp: datetime
    description: Optional[str] = None


class BankStatementUpload(BaseModel):
    account_no: str
    account_holder_name: str
    mobile: str
    address: str
    aadhar_no: Optional[str] = None
    pan_no: Optional[str] = None
    transactions: List[TransactionRecord]


class TransferChainNode(BaseModel):
    account_no: str
    account_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    bank_ifsc_prefix: Optional[str] = None
    amount: float
    timestamp: Optional[datetime] = None
    transaction_id: Optional[str] = None
    depth: int = 0


class TransferChain(BaseModel):
    id: Optional[str] = None
    root_complaint_no: str
    root_mule_account: str
    chain_nodes: List[TransferChainNode] = []
    status: str = "active"
    created_at: datetime = None
