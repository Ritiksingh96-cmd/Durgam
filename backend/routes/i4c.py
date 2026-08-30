from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from bson import ObjectId
from database import get_database
from middleware.auth import require_i4c

router = APIRouter()


def serialize(doc) -> dict:
    if doc is None:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# ─── DASHBOARD STATS ───
@router.get("/dashboard")
async def get_dashboard(current_user=Depends(require_i4c), db=Depends(get_database)):
    total_complaints = await db.complaints.count_documents({})
    pending = await db.complaints.count_documents({"status": "pending"})
    under_investigation = await db.complaints.count_documents({"status": "under_investigation"})
    chain_detected = await db.complaints.count_documents({"status": "chain_detected"})
    resolved = await db.complaints.count_documents({"status": "resolved"})
    total_banks = await db.banks.count_documents({})
    total_notifications = await db.notifications.count_documents({})
    total_chains = await db.transfer_chains.count_documents({})
    total_users = await db.users.count_documents({})

    # Total amount involved
    pipeline = [{"$group": {"_id": None, "total": {"$sum": "$amount"}}}]
    amount_result = await db.complaints.aggregate(pipeline).to_list(1)
    total_amount = amount_result[0]["total"] if amount_result else 0

    # Complaints by fraud type
    fraud_pipeline = [
        {"$group": {"_id": "$fraud_type", "count": {"$sum": 1}, "total_amount": {"$sum": "$amount"}}},
        {"$sort": {"count": -1}},
    ]
    fraud_breakdown = await db.complaints.aggregate(fraud_pipeline).to_list(20)

    # Complaints per day (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    daily_pipeline = [
        {"$match": {"created_at": {"$gte": thirty_days_ago}}},
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"},
                },
                "count": {"$sum": 1},
                "amount": {"$sum": "$amount"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}},
    ]
    daily_complaints = await db.complaints.aggregate(daily_pipeline).to_list(30)

    return {
        "stats": {
            "total_complaints": total_complaints,
            "pending": pending,
            "under_investigation": under_investigation,
            "chain_detected": chain_detected,
            "resolved": resolved,
            "total_banks": total_banks,
            "total_notifications": total_notifications,
            "total_chains": total_chains,
            "total_users": total_users,
            "total_amount_involved": round(total_amount, 2),
        },
        "fraud_breakdown": fraud_breakdown,
        "daily_complaints": daily_complaints,
    }


# ─── ALL COMPLAINTS ───
@router.get("/complaints")
async def get_all_complaints(
    skip: int = 0,
    limit: int = 50,
    status: str = None,
    current_user=Depends(require_i4c),
    db=Depends(get_database),
):
    query = {}
    if status:
        query["status"] = status
    cursor = db.complaints.find(query).sort("created_at", -1).skip(skip).limit(limit)
    complaints = await cursor.to_list(length=limit)
    total = await db.complaints.count_documents(query)
    return {"complaints": [serialize(c) for c in complaints], "total": total}


# ─── ALL TRANSFER CHAINS ───
@router.get("/chains")
async def get_all_chains(
    current_user=Depends(require_i4c), db=Depends(get_database)
):
    cursor = db.transfer_chains.find({}).sort("created_at", -1)
    chains = await cursor.to_list(length=200)
    return [serialize(c) for c in chains]


# ─── SINGLE CHAIN DETAIL ───
@router.get("/chain/{complaint_no}")
async def get_chain_detail(
    complaint_no: str,
    current_user=Depends(require_i4c),
    db=Depends(get_database),
):
    chain = await db.transfer_chains.find_one({"root_complaint_no": complaint_no})
    complaint = await db.complaints.find_one({"complaint_no": complaint_no})
    notifications = await db.notifications.find(
        {"complaint_no": complaint_no}
    ).to_list(length=100)

    return {
        "chain": serialize(chain) if chain else None,
        "complaint": serialize(complaint) if complaint else None,
        "notifications": [serialize(n) for n in notifications],
    }


# ─── ALL BANK SUBMITTED DATA ───
@router.get("/bank-data")
async def get_bank_data(
    current_user=Depends(require_i4c), db=Depends(get_database)
):
    cursor = db.account_holders.find({}).sort("submitted_at", -1)
    accounts = await cursor.to_list(length=500)
    return [serialize(a) for a in accounts]


# ─── ALL USERS ───
@router.get("/users")
async def get_all_users(current_user=Depends(require_i4c), db=Depends(get_database)):
    cursor = db.users.find({}).sort("created_at", -1)
    users = await cursor.to_list(length=500)
    for u in users:
        u.pop("hashed_password", None)
    return [serialize(u) for u in users]


# ─── ALL BANKS ───
@router.get("/banks")
async def get_all_banks(current_user=Depends(require_i4c), db=Depends(get_database)):
    cursor = db.banks.find({}).sort("created_at", -1)
    banks = await cursor.to_list(length=200)
    for b in banks:
        b.pop("hashed_password", None)
    return [serialize(b) for b in banks]


# ─── ALL NOTIFICATIONS ───
@router.get("/notifications")
async def get_all_notifications(current_user=Depends(require_i4c), db=Depends(get_database)):
    cursor = db.notifications.find({}).sort("created_at", -1)
    notifications = await cursor.to_list(length=500)
    return [serialize(n) for n in notifications]


# ─── UPDATE COMPLAINT STATUS ───
@router.put("/complaint/{complaint_no}/status")
async def update_complaint_status(
    complaint_no: str,
    body: dict,
    current_user=Depends(require_i4c),
    db=Depends(get_database),
):
    new_status = body.get("status")
    await db.complaints.update_one(
        {"complaint_no": complaint_no},
        {"$set": {"status": new_status, "updated_at": datetime.utcnow()}},
    )
    return {"message": f"Complaint {complaint_no} status updated to {new_status}"}


# ─── MONEY FLOW ANALYTICS (graph data) ───
@router.get("/analytics/money-flow")
async def money_flow_analytics(current_user=Depends(require_i4c), db=Depends(get_database)):
    # Get all transactions to build a flow graph
    cursor = db.transactions.find({}).sort("timestamp", -1).limit(500)
    transactions = await cursor.to_list(length=500)

    nodes = {}
    links = []

    for txn in transactions:
        from_acc = txn.get("from_account", "")
        to_acc = txn.get("to_account", "")
        amount = txn.get("amount", 0)

        if from_acc not in nodes:
            nodes[from_acc] = {
                "id": from_acc,
                "name": txn.get("from_account_name", from_acc[:10]),
                "bank": txn.get("bank_ifsc_prefix", ""),
                "total_sent": 0,
            }
        nodes[from_acc]["total_sent"] += amount

        if to_acc not in nodes:
            nodes[to_acc] = {
                "id": to_acc,
                "name": to_acc[:10],
                "bank": txn.get("to_bank_ifsc", ""),
                "total_sent": 0,
            }

        links.append({"source": from_acc, "target": to_acc, "amount": amount})

    return {
        "nodes": list(nodes.values()),
        "links": links,
    }
