from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BankCreate(BaseModel):
    bank_name: str
    ifsc_prefix: str   # First 4 chars of IFSC (e.g., SBIN, HDFC)
    email: str
    password: str
    contact_number: str


class BankLogin(BaseModel):
    email: str
    password: str


class BankResponse(BaseModel):
    id: str
    bank_name: str
    ifsc_prefix: str
    email: str
    contact_number: str
    role: str
    created_at: datetime
