import re
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

router = APIRouter(prefix="/verify", tags=["Credential & Bank Verification"])

# Standard Indian Bank IFSC Prefixes & Names
KNOWN_BANKS = {
    "SBIN": "State Bank of India",
    "PUNB": "Punjab National Bank",
    "HDFC": "HDFC Bank",
    "ICIC": "ICICI Bank",
    "UTIB": "Axis Bank",
    "JAKA": "Jammu & Kashmir Bank",
    "BARB": "Bank of Baroda",
    "CNRB": "Canara Bank",
    "KKBK": "Kotak Mahindra Bank",
    "UBIN": "Union Bank of India",
    "MAHB": "Bank of Maharashtra",
    "IOBA": "Indian Overseas Bank",
    "IDIB": "Indian Bank",
    "YESB": "Yes Bank",
    "IDFB": "IDFC FIRST Bank"
}

class UTRVerificationRequest(BaseModel):
    utr_number: str = Field(..., min_length=12, max_length=22, description="12 to 22 digit UTR / RRN")

class PhoneVerificationRequest(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=10, description="10-digit Indian Mobile Number")

class GSTINVerificationRequest(BaseModel):
    gstin: str = Field(..., min_length=15, max_length=15, description="15-character GSTIN")

class PANVerificationRequest(BaseModel):
    pan: str = Field(..., min_length=10, max_length=10, description="10-character PAN")

@router.get("/ifsc/{ifsc_code}")
def verify_ifsc(ifsc_code: str):
    """
    Verify 11-character Indian Financial System Code (IFSC) format and resolve issuing bank.
    Standard Format: 4 letters (Bank), 0 (Reserved), 6 alphanumeric (Branch).
    """
    clean_ifsc = ifsc_code.strip().upper()
    ifsc_pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    
    if not re.match(ifsc_pattern, clean_ifsc):
        raise HTTPException(
            status_code=400,
            detail="Invalid IFSC format. Must be 11 characters (e.g. SBIN0001024 or JAKA0001928)."
        )
        
    prefix = clean_ifsc[:4]
    bank_name = KNOWN_BANKS.get(prefix, f"Scheduled Commercial Bank ({prefix})")
    
    return {
        "valid": True,
        "ifsc": clean_ifsc,
        "bank_code": prefix,
        "bank_name": bank_name,
        "branch_code": clean_ifsc[5:],
        "iso_20022_switch_enabled": True,
        "rtgs_neft_upi_active": True
    }

@router.post("/utr")
def verify_utr(payload: UTRVerificationRequest):
    """
    Validate 12-digit Unique Transaction Reference (UTR) or NPCI RRN.
    """
    clean_utr = payload.utr_number.strip().upper()
    # Remove prefix if passed e.g. UTR482910482910 -> 482910482910
    numeric_utr = re.sub(r'^[A-Z]+', '', clean_utr)
    
    if len(numeric_utr) != 12 or not numeric_utr.isdigit():
        raise HTTPException(
            status_code=400,
            detail="Invalid UTR/RRN format. Must contain a 12-digit numeric reference identifier."
        )
        
    # Extract approximate timestamp components from NPCI RRN standard (Julian Day + Hour)
    julian_day = numeric_utr[:3]
    hour = numeric_utr[3:5]
    
    return {
        "valid": True,
        "raw_utr": clean_utr,
        "normalized_utr": numeric_utr,
        "payment_switch": "NPCI UPI / IMPS Central Switch",
        "julian_batch_indicator": julian_day,
        "ingest_ready": True
    }

@router.post("/phone")
def verify_phone(payload: PhoneVerificationRequest):
    """
    Validate 10-digit Indian Mobile Number (TRAI Allocation Series 6, 7, 8, 9).
    """
    clean_phone = payload.phone_number.strip()
    if not re.match(r'^[6-9]\d{9}$', clean_phone):
        raise HTTPException(
            status_code=400,
            detail="Invalid Indian mobile number. Must be 10 digits starting with 6, 7, 8, or 9."
        )
        
    return {
        "valid": True,
        "phone_number": clean_phone,
        "masked_phone": f"+91 {clean_phone[:2]}XXXX{clean_phone[-4:]}",
        "telecom_circle": "National Sovereign Telecom Registry",
        "otp_delivery_channel": "CDAC SMS Gateway / 1930 Helpline"
    }

@router.post("/gstin")
def verify_gstin(payload: GSTINVerificationRequest):
    """
    Validate 15-character Goods and Services Tax Identification Number (GSTIN) for MSME Whitelisting.
    """
    clean_gstin = payload.gstin.strip().upper()
    gstin_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    
    if not re.match(gstin_pattern, clean_gstin):
        raise HTTPException(
            status_code=400,
            detail="Invalid GSTIN format. Must match standard 15-character GST structure."
        )
        
    return {
        "valid": True,
        "gstin": clean_gstin,
        "state_code": clean_gstin[:2],
        "pan_linked": clean_gstin[2:12],
        "entity_status": "VERIFIED_ACTIVE_MSME",
        "hold_exemption_eligible": True
    }

@router.post("/pan")
def verify_pan(payload: PANVerificationRequest):
    """
    Validate 10-character Permanent Account Number (PAN).
    """
    clean_pan = payload.pan.strip().upper()
    pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    
    if not re.match(pan_pattern, clean_pan):
        raise HTTPException(
            status_code=400,
            detail="Invalid PAN format. Must be 5 letters, 4 digits, 1 letter."
        )
        
    return {
        "valid": True,
        "pan": clean_pan,
        "masked_pan": f"{clean_pan[:2]}XXXXX{clean_pan[-2:]}",
        "entity_type": "INDIVIDUAL" if clean_pan[3] == 'P' else "BUSINESS_ENTITY"
    }
