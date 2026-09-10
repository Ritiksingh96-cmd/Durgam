from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from config import settings
from database import get_database
from models.user import UserCreate, UserLogin
from models.bank import BankCreate, BankLogin
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


# ─────────────────── USER ───────────────────
@router.post("/user/register")
async def register_user(user_data: UserCreate, db=Depends(get_database)):
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(user_data.password)
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "mobile": user_data.mobile,
        "address": user_data.address,
        "hashed_password": hashed_pwd,
        "role": "user",
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    result = await db.users.insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id), "role": "user"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "user",
        "name": user_data.name,
        "user_id": str(result.inserted_id),
    }


@router.post("/user/login")
async def login_user(credentials: UserLogin, db=Depends(get_database)):
    user = await db.users.find_one({"email": credentials.email, "role": "user"})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user["_id"]), "role": "user"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "user",
        "name": user["name"],
        "user_id": str(user["_id"]),
    }


# ─────────────────── BANK ───────────────────
@router.post("/bank/register")
async def register_bank(bank_data: BankCreate, db=Depends(get_database)):
    existing = await db.banks.find_one({"email": bank_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Bank email already registered")

    hashed_pwd = get_password_hash(bank_data.password)
    bank_doc = {
        "bank_name": bank_data.bank_name,
        "ifsc_prefix": bank_data.ifsc_prefix.upper(),
        "email": bank_data.email,
        "hashed_password": hashed_pwd,
        "contact_number": bank_data.contact_number,
        "role": "bank",
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    result = await db.banks.insert_one(bank_doc)
    token = create_access_token({"sub": str(result.inserted_id), "role": "bank"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "bank",
        "bank_name": bank_data.bank_name,
        "bank_id": str(result.inserted_id),
    }


@router.post("/bank/login")
async def login_bank(credentials: BankLogin, db=Depends(get_database)):
    bank = await db.banks.find_one({"email": credentials.email, "role": "bank"})
    if not bank or not verify_password(credentials.password, bank["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(bank["_id"]), "role": "bank"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "bank",
        "bank_name": bank["bank_name"],
        "bank_id": str(bank["_id"]),
        "ifsc_prefix": bank["ifsc_prefix"],
    }


# ─────────────────── I4C ───────────────────
@router.post("/i4c/login")
async def login_i4c(credentials: dict, db=Depends(get_database)):
    officer = await db.i4c_officers.find_one({"email": credentials.get("email"), "role": "i4c"})
    if not officer or not verify_password(credentials.get("password", ""), officer["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(officer["_id"]), "role": "i4c"})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "i4c",
        "name": officer["name"],
        "officer_id": str(officer["_id"]),
    }
