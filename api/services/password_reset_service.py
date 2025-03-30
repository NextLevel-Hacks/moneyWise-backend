import yagmail
import secrets
from datetime import datetime
from config.settings import settings
from fastapi import HTTPException
from api.models.password_reset import PasswordResetToken

class PasswordResetService:
    def __init__(self):
        self.email_client = yagmail.SMTP(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)

    def generate_reset_token(self) -> str:
        # Generate a secure random token
        return secrets.token_urlsafe(32)

    def send_reset_email(self, user: dict, token: str) -> None:
        # Mock reset link for the PoC (in production, this would point to your frontend)
        reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"
        subject = "CashFlow Compass - Password Reset Request"
        body = (
            f"Hi {user['first_name']},\n\n"
            f"You requested a password reset for your CashFlow Compass account.\n"
            f"Click the link below to reset your password:\n\n"
            f"{reset_link}\n\n"
            f"This link will expire in {settings.RESET_TOKEN_EXPIRY_MINUTES} minutes.\n"
            f"If you didn’t request this, please ignore this email.\n\n"
            f"Best,\nThe CashFlow Compass Team"
        )

        try:
            self.email_client.send(
                to=user["email"],
                subject=subject,
                contents=body
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

    def create_reset_token(self, user_id: str, db) -> str:
        token = self.generate_reset_token()
        reset_token = PasswordResetToken.create(user_id, token)
        db["password_reset_tokens"].insert_one(reset_token.dict())
        return token

    def verify_reset_token(self, token: str, db) -> str:
        reset_token = db["password_reset_tokens"].find_one({"token": token})
        if not reset_token:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
        
        if datetime.utcnow() > reset_token["expiry"]:
            db["password_reset_tokens"].delete_one({"token": token})
            raise HTTPException(status_code=400, detail="Token has expired")
        
        return reset_token["user_id"]

    def reset_password(self, user_id: str, new_password: str, token: str, db, auth_service):
        # Hash the new password
        hashed_password = auth_service.hash_password(new_password)
        # Update the user's password
        db["users"].update_one(
            {"_id": user_id},
            {"$set": {"hashed_password": hashed_password}}
        )
        # Delete the used token
        db["password_reset_tokens"].delete_one({"token": token})

password_reset_service = PasswordResetService()