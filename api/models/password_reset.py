from pydantic import BaseModel
from datetime import datetime, timedelta
from config.settings import settings

class PasswordResetToken(BaseModel):
    user_id: str
    token: str
    expiry: datetime

    @classmethod
    def create(cls, user_id: str, token: str) -> "PasswordResetToken":
        expiry = datetime.utcnow() + timedelta(minutes=settings.RESET_TOKEN_EXPIRY_MINUTES)
        return cls(user_id=user_id, token=token, expiry=expiry)