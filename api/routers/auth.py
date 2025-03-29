from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.dependencies import get_database
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