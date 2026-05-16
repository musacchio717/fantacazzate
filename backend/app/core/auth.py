import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("SECRET_KEY", "cambia-questa-stringa-con-qualcosa-di-random")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, username: str, role: str,
                        expires_delta: timedelta = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_token(token: str) -> dict:
    payload = decode_token(token)
    return {
        "user_id": int(payload.get("sub")),
        "username": payload.get("username"),
        "role": payload.get("role")
    }

async def get_current_user(credentials=Depends(security)) -> dict:
    token = credentials.credentials
    payload = decode_token(token)
    user_id = int(payload.get("sub"))
    username = payload.get("username")
    role = payload.get("role")
    if not user_id or not username or not role:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"user_id": user_id, "username": username, "role": role}

async def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

async def require_observer_or_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] not in ["admin", "observer"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return current_user