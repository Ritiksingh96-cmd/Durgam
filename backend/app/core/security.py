import re
import html
import time
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.config import settings

# Password Hashing with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Security Bearer
security_bearer = HTTPBearer(auto_error=False)

def hash_password(plain_password: str) -> str:
    """Hash a password using bcrypt with 12 rounds"""
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its bcrypt hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a short-lived signed JWT access token"""
    to_encode = data.copy()
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)
    to_encode.update({"iat": int(now.timestamp()), "exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create an 8-hour signed JWT refresh token"""
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + timedelta(hours=8)
    to_encode.update({"iat": int(now.timestamp()), "exp": int(expire.timestamp()), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token claims"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid sovereign authorization credentials.")

def sanitize_input_text(text: str) -> str:
    """Sanitize user-provided text inputs against XSS and injection patterns"""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]*?>', '', text)
    # Escape special characters
    clean = html.escape(clean)
    # Strip dangerous SQL patterns
    clean = re.sub(r'(--|;|\/\*|\*\/|xp_)', '', clean)
    return clean.strip()

class SlidingWindowRateLimiter:
    """
    In-memory Sliding Window Rate Limiter for sovereign API endpoints.
    Protects against brute-force attacks and volumetric DoS.
    """
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = {}

    def is_allowed(self, client_identifier: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        
        if client_identifier not in self.requests:
            self.requests[client_identifier] = [now]
            return True
            
        # Filter timestamps within current window
        valid_requests = [t for t in self.requests[client_identifier] if t > window_start]
        self.requests[client_identifier] = valid_requests
        
        if len(valid_requests) < self.max_requests:
            self.requests[client_identifier].append(now)
            return True
            
        return False

# Global rate limiters (Allowing smooth multi-war room testing and high-throughput defense)
login_rate_limiter = SlidingWindowRateLimiter(max_requests=30, window_seconds=60)
incident_rate_limiter = SlidingWindowRateLimiter(max_requests=100, window_seconds=60)
