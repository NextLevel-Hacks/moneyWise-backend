from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_database, get_current_user
from api.models.user import UserCreate, Token
from api.services.auth_service import auth_service
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/auth/signup", response_model=Token)
async def signup(user: UserCreate, db=Depends(get_database)):
    try:
        auth_service.signup(user, db)
        token = auth_service.login(user.email, user.password, db)
        return token
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db=Depends(get_database)):
    try:
        token = auth_service.login(login_data.email, login_data.password, db)
        return token
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get('/auth/me')
async def get_user_details(current_user=Depends(get_current_user), db=Depends(get_database)):
    user = db["users"].find_one({"email": current_user["email"]})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "id": str(user["_id"]),
    }