from fastapi import APIRouter, Depends
from api.dependencies import get_database
from api.models.transaction import Transaction
from api.models.user import UserProfile

router = APIRouter()

@router.post("/users/{user_id}/classify")
async def classify_spender(
    user_id: str,
    transactions: list[Transaction],
    db=Depends(get_database)
):
    # Dummy classification (replace with AI model later)
    spender_type = "HILS"  # Placeholder
    profile = {"user_id": user_id, "spender_type": spender_type}
    
    # Save to MongoDB
    db["user_profiles"].update_one(
        {"user_id": user_id},
        {"$set": profile},
        upsert=True
    )
    
    return UserProfile(**profile)