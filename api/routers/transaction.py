from fastapi import APIRouter, Depends
from api.dependencies import get_database, get_current_user
from api.services.transaction_service import transaction_service
from api.models.transaction import TransactionSummary

router = APIRouter()

@router.post("/users/{user_id}/connect-account", response_model=TransactionSummary)
async def connect_account(
    user_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Mocked transaction summary
    summary = transaction_service.summarize_transactions(user_id)
    
    # Save to MongoDB
    db["transactions"].update_one(
        {"user_id": user_id},
        {"$set": summary.dict()},
        upsert=True
    )
    
    return summary