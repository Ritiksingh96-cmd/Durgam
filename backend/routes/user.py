from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from bson import ObjectId
import random
import string
from database import get_database
from middleware.auth import require_user, get_current_user
from models.complaint import ComplaintCreate
from services.chain_detection import trigger_chain_detection

router = APIRouter()


def generate_complaint_no() -> str:
    year = datetime.utcnow().year
    suffix = ''.join(random.choices(string.digits, k=6))
    return f"DURGAM-{year}-{suffix}"


def serialize(doc) -> dict:
    if doc is None:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# ─── GET CURRENT USER PROFILE ───
@router.get("/me")
async def get_me(current_user=Depends(require_user), db=Depends(get_database)):
    user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pop("hashed_password", None)
    return serialize(user)


# ─── FILE NEW COMPLAINT ───
@router.post("/complaint")
async def file_complaint(
    complaint: ComplaintCreate,
    current_user=Depends(require_user),
    db=Depends(get_database),
):
    user = await db.users.find_one({"_id": ObjectId(current_user["user_id"])})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate unique complaint number
    complaint_no = generate_complaint_no()
    while await db.complaints.find_one({"complaint_no": complaint_no}):
        complaint_no = generate_complaint_no()

    txn_date = complaint.transaction_date or datetime.utcnow()

    complaint_doc = {
        "complaint_no": complaint_no,
        "user_id": str(user["_id"]),
        "user_name": user["name"],
        "user_mobile": user["mobile"],
        "user_address": user["address"],
        "user_email": user["email"],
        "description": complaint.description,
        "amount": complaint.amount,
        "to_account": complaint.to_account,
        "to_bank_ifsc": complaint.to_bank_ifsc,
        "transaction_id": complaint.transaction_id,
        "fraud_type": complaint.fraud_type,
        "transaction_date": txn_date,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await db.complaints.insert_one(complaint_doc)

    # Trigger mule account notification for the receiving bank
    await trigger_chain_detection(
        db=db,
        complaint_no=complaint_no,
        mule_account=complaint.to_account,
        bank_ifsc=complaint.to_bank_ifsc,
        amount=complaint.amount,
        scam_time=txn_date,
    )

    return {
        "message": "Complaint filed successfully",
        "complaint_no": complaint_no,
        "complaint_id": str(result.inserted_id),
    }


# ─── TRACK COMPLAINT BY COMPLAINT NO ───
@router.get("/complaint/track/{complaint_no}")
async def track_complaint(complaint_no: str, db=Depends(get_database)):
    complaint = await db.complaints.find_one({"complaint_no": complaint_no})
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Get chain info if any
    chain = await db.transfer_chains.find_one({"root_complaint_no": complaint_no})
    chain_data = None
    if chain:
        chain["id"] = str(chain["_id"])
        del chain["_id"]
        chain_data = chain

    complaint = serialize(complaint)
    return {"complaint": complaint, "chain": chain_data}


# ─── LIST OWN COMPLAINTS ───
@router.get("/complaints")
async def list_my_complaints(current_user=Depends(require_user), db=Depends(get_database)):
    cursor = db.complaints.find({"user_id": current_user["user_id"]}).sort("created_at", -1)
    complaints = await cursor.to_list(length=100)
    return [serialize(c) for c in complaints]
