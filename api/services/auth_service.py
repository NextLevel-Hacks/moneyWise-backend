from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from config.settings import settings
from api.models.user import UserCreate, UserInDB, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def signup(self, user: UserCreate, db) -> UserInDB:
        if db["users"].find_one({"email": user.email}):
            raise ValueError("Email already registered")
        
        hashed_password = self.hash_password(user.password)
        user_in_db = UserInDB(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password
        )
        db["users"].insert_one(user_in_db.dict())
        return user_in_db

    def login(self, email: str, password: str, db) -> Token:
        user = db["users"].find_one({"email": email})
        if not user or not self.verify_password(password, user["hashed_password"]):
            raise ValueError("Invalid credentials")
        
        token = self.create_access_token({"sub": user["email"]})
        return Token(access_token=token, token_type="bearer")

auth_service = AuthService()