from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from datetime import datetime
from bson import ObjectId
import json
from database import get_database
from middleware.auth import require_bank
from models.transaction import BankStatementUpload
from services.chain_detection import process_bank_statement

router = APIRouter()


def serialize(doc) -> dict:
    if doc is None:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# ─── GET BANK PROFILE ───
@router.get("/me")
async def get_bank_profile(current_user=Depends(require_bank), db=Depends(get_database)):
    bank = await db.banks.find_one({"_id": ObjectId(current_user["user_id"])})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    bank.pop("hashed_password", None)
    return serialize(bank)


# ─── GET MULE ACCOUNT NOTIFICATIONS ───
@router.get("/notifications")
async def get_notifications(current_user=Depends(require_bank), db=Depends(get_database)):
    bank = await db.banks.find_one({"_id": ObjectId(current_user["user_id"])})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    # Notifications for this bank's IFSC prefix
    cursor = db.notifications.find(
        {"bank_ifsc_prefix": bank["ifsc_prefix"]}
    ).sort("created_at", -1)
    notifications = await cursor.to_list(length=200)
    return [serialize(n) for n in notifications]


# ─── GET SINGLE NOTIFICATION ───
@router.get("/notification/{notification_id}")
async def get_notification(notification_id: str, current_user=Depends(require_bank), db=Depends(get_database)):
    notif = await db.notifications.find_one({"_id": ObjectId(notification_id)})
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return serialize(notif)


# ─── SUBMIT ACCOUNT HOLDER DATA + TRANSACTIONS ───
@router.post("/statement/upload")
async def upload_bank_statement(
    data: BankStatementUpload,
    current_user=Depends(require_bank),
    db=Depends(get_database),
):
    bank = await db.banks.find_one({"_id": ObjectId(current_user["user_id"])})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    now = datetime.utcnow()

    # Save account holder data
    account_data = {
        "account_no": data.account_no,
        "account_holder_name": data.account_holder_name,
        "mobile": data.mobile,
        "address": data.address,
        "aadhar_no": data.aadhar_no,
        "pan_no": data.pan_no,
        "bank_id": str(bank["_id"]),
        "bank_name": bank["bank_name"],
        "bank_ifsc_prefix": bank["ifsc_prefix"],
        "submitted_at": now,
    }
    await db.account_holders.replace_one(
        {"account_no": data.account_no},
        account_data,
        upsert=True,
    )

    # Save transactions
    txns_to_insert = []
    for txn in data.transactions:
        txns_to_insert.append({
            "from_account": data.account_no,
            "from_account_name": data.account_holder_name,
            "to_account": txn.to_account,
            "to_bank_ifsc": txn.to_bank_ifsc,
            "amount": txn.amount,
            "timestamp": txn.timestamp,
            "transaction_id": txn.transaction_id,
            "description": txn.description,
            "bank_id": str(bank["_id"]),
            "bank_ifsc_prefix": bank["ifsc_prefix"],
            "submitted_at": now,
        })

    if txns_to_insert:
        await db.transactions.insert_many(txns_to_insert)

    # Mark related notifications as data_submitted
    await db.notifications.update_many(
        {"account_no": data.account_no, "bank_ifsc_prefix": bank["ifsc_prefix"]},
        {"$set": {"status": "data_submitted", "updated_at": now}},
    )

    # Process chain detection on newly submitted data
    await process_bank_statement(db=db, account_no=data.account_no, bank_name=bank["bank_name"])

    return {
        "message": "Bank statement submitted successfully",
        "account_no": data.account_no,
        "transactions_saved": len(txns_to_insert),
    }


# ─── GET TRANSFER CHAINS FOR THIS BANK ───
@router.get("/chains")
async def get_chains(current_user=Depends(require_bank), db=Depends(get_database)):
    bank = await db.banks.find_one({"_id": ObjectId(current_user["user_id"])})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    cursor = db.transfer_chains.find(
        {"chain_nodes.bank_ifsc_prefix": bank["ifsc_prefix"]}
    ).sort("created_at", -1)
    chains = await cursor.to_list(length=100)
    return [serialize(c) for c in chains]


# ─── GET ALL SUBMITTED ACCOUNT DATA FOR THIS BANK ───
@router.get("/accounts")
async def get_submitted_accounts(current_user=Depends(require_bank), db=Depends(get_database)):
    bank = await db.banks.find_one({"_id": ObjectId(current_user["user_id"])})
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    cursor = db.account_holders.find({"bank_ifsc_prefix": bank["ifsc_prefix"]}).sort("submitted_at", -1)
    accounts = await cursor.to_list(length=200)
    return [serialize(a) for a in accounts]


# ─── UPDATE NOTIFICATION STATUS ───
@router.put("/notification/{notification_id}/status")
async def update_notification_status(
    notification_id: str,
    body: dict,
    current_user=Depends(require_bank),
    db=Depends(get_database),
):
    new_status = body.get("status")
    await db.notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}},
    )
    return {"message": "Status updated"}
