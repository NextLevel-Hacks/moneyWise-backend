from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_database, get_current_user
from api.models.user import UserCreate, Token, LoginRequest
from api.services.auth_service import auth_service
from api.services.chatbot_service import chatbot_service
from api.services.password_reset_service import password_reset_service
from pydantic import BaseModel



router = APIRouter(tags=["Authentication"])

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


@router.post("/auth/password-reset-request")
async def request_password_reset(email: str, db=Depends(get_database)):
    user = db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate and save reset token
    token = password_reset_service.create_reset_token(str(user["_id"]), db)
    
    # Send reset email
    password_reset_service.send_reset_email(user, token)
    
    return {"message": "Password reset link sent to your email"}

@router.post("/auth/password-reset")
async def reset_password(token: str, new_password: str, db=Depends(get_database)):
    # Verify the reset token
    user_id = password_reset_service.verify_reset_token(token, db)
    
    # Reset the password
    password_reset_service.reset_password(user_id, new_password, token, db, auth_service)
    
    return {"message": "Password reset successfully"}