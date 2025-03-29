from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str

class UserProfile(BaseModel):
    user_id: str
    spender_type: str

class UserPermissions(BaseModel):
    max_per_action: float
    monthly_cap: float
    automation_mode: str
    agent_status: str

class Token(BaseModel):
    access_token: str
    token_type: str