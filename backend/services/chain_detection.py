"""
Chain Detection Service
=======================
Core logic for detecting mule account transfer chains.

Flow:
  User files complaint → mule account B identified
  → Bank of B gets notification
  → Bank B uploads B's statement
  → System finds B's outgoing transactions near scam time
  → Finds next account C → Bank of C gets notification
  → Continue chain...
"""
from datetime import datetime, timedelta
from bson import ObjectId
import re


def extract_ifsc_prefix(ifsc: str) -> str:
    """Extract first 4 chars (bank code) from IFSC."""
    if not ifsc:
        return ""
    return ifsc[:4].upper()


async def find_bank_for_ifsc(db, ifsc_prefix: str):
    """Find bank document by IFSC prefix."""
    if not ifsc_prefix:
        return None
    return await db.banks.find_one({"ifsc_prefix": ifsc_prefix.upper()})


async def create_notification(
    db,
    account_no: str,
    bank_ifsc_prefix: str,
    complaint_no: str,
    amount: float,
    depth: int = 0,
    parent_account: str = None,
):
    """Create a notification for a bank about a mule/suspect account."""
    # Avoid duplicate notifications
    existing = await db.notifications.find_one({
        "account_no": account_no,
        "complaint_no": complaint_no,
    })
    if existing:
        return existing

    bank = await find_bank_for_ifsc(db, bank_ifsc_prefix)

    notification = {
        "account_no": account_no,
        "bank_ifsc_prefix": bank_ifsc_prefix,
        "bank_name": bank["bank_name"] if bank else "Unknown Bank",
        "complaint_no": complaint_no,
        "amount": amount,
        "depth": depth,  # 0 = direct mule, 1 = one hop, 2 = two hops...
        "parent_account": parent_account,
        "status": "pending",  # pending | data_submitted | chain_tracked
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db.notifications.insert_one(notification)
    notification["_id"] = result.inserted_id
    return notification


async def trigger_chain_detection(
    db,
    complaint_no: str,
    mule_account: str,
    bank_ifsc: str,
    amount: float,
    scam_time: datetime,
):
    """
    Called when user files a complaint.
    Creates initial notification for mule account's bank.
    Initializes transfer chain record.
    """
    ifsc_prefix = extract_ifsc_prefix(bank_ifsc) if bank_ifsc else ""

    # Create notification for mule account's bank
    await create_notification(
        db=db,
        account_no=mule_account,
        bank_ifsc_prefix=ifsc_prefix,
        complaint_no=complaint_no,
        amount=amount,
        depth=0,
        parent_account=None,
    )

    # Initialize chain record
    existing_chain = await db.transfer_chains.find_one({"root_complaint_no": complaint_no})
    if not existing_chain:
        await db.transfer_chains.insert_one({
            "root_complaint_no": complaint_no,
            "root_mule_account": mule_account,
            "root_bank_ifsc": bank_ifsc,
            "scam_time": scam_time,
            "chain_nodes": [
                {
                    "account_no": mule_account,
                    "bank_ifsc_prefix": ifsc_prefix,
                    "amount": amount,
                    "depth": 0,
                    "status": "pending",
                }
            ],
            "status": "active",
            "created_at": datetime.utcnow(),
        })

    # Update complaint status
    await db.complaints.update_one(
        {"complaint_no": complaint_no},
        {"$set": {"status": "under_investigation", "updated_at": datetime.utcnow()}},
    )


async def process_bank_statement(db, account_no: str, bank_name: str):
    """
    Called after bank submits statement for an account.
    Finds outgoing transactions and continues chain detection.
    """
    # Find notifications for this account
    notifications = await db.notifications.find(
        {"account_no": account_no}
    ).to_list(length=50)

    for notif in notifications:
        complaint_no = notif["complaint_no"]
        depth = notif.get("depth", 0)
        amount = notif.get("amount", 0)

        # Get the complaint to find the scam time
        complaint = await db.complaints.find_one({"complaint_no": complaint_no})
        if not complaint:
            continue

        scam_time = complaint.get("transaction_date") or complaint.get("created_at")
        if not scam_time:
            continue

        # Look for outgoing transactions from this account within 48 hours of scam
        time_window_start = scam_time - timedelta(hours=1)
        time_window_end = scam_time + timedelta(hours=72)

        outgoing_txns = await db.transactions.find({
            "from_account": account_no,
            "timestamp": {
                "$gte": time_window_start,
                "$lte": time_window_end,
            }
        }).sort("timestamp", 1).to_list(length=50)

        if not outgoing_txns:
            continue

        # Update chain record
        new_chain_nodes = []
        for txn in outgoing_txns:
            to_acc = txn["to_account"]
            to_ifsc = txn.get("to_bank_ifsc", "")
            to_ifsc_prefix = extract_ifsc_prefix(to_ifsc)
            txn_amount = txn["amount"]

            new_chain_nodes.append({
                "account_no": to_acc,
                "bank_ifsc_prefix": to_ifsc_prefix,
                "amount": txn_amount,
                "timestamp": txn.get("timestamp"),
                "transaction_id": txn.get("transaction_id"),
                "depth": depth + 1,
                "status": "pending",
            })

            # Notify next bank in chain
            if depth < 5:  # max chain depth to prevent infinite loops
                await create_notification(
                    db=db,
                    account_no=to_acc,
                    bank_ifsc_prefix=to_ifsc_prefix,
                    complaint_no=complaint_no,
                    amount=txn_amount,
                    depth=depth + 1,
                    parent_account=account_no,
                )

        if new_chain_nodes:
            # Add nodes to the chain
            await db.transfer_chains.update_one(
                {"root_complaint_no": complaint_no},
                {
                    "$push": {"chain_nodes": {"$each": new_chain_nodes}},
                    "$set": {"status": "chain_detected", "updated_at": datetime.utcnow()},
                },
            )

            # Update complaint status
            await db.complaints.update_one(
                {"complaint_no": complaint_no},
                {"$set": {"status": "chain_detected", "updated_at": datetime.utcnow()}},
            )

        # Mark notification as chain_tracked
        await db.notifications.update_one(
            {"_id": notif["_id"]},
            {"$set": {"status": "chain_tracked", "updated_at": datetime.utcnow()}},
        )
