from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config.settings import settings
from config.database import get_db

# Simple Bearer token scheme
bearer_scheme = HTTPBearer()

def get_database():
    db = get_db()
    try:
        yield db
    finally:
        pass

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db=Depends(get_database)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db["users"].find_one({"email": email})
    if user is None:
        raise credentials_exception
    return {"email": user["email"]}