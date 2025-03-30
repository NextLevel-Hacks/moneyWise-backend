from fastapi import APIRouter, Depends
from api.dependencies import get_database, get_current_user
from api.services.classify_service import classify_service
from api.services.insights_service import insights_service
from api.models.insights import InsightsResponse

router = APIRouter(tags=["Classifier"])

@router.post("/users/{user_id}/classify", response_model=InsightsResponse)
async def classify_spender(
    user_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Mocked classification
    classification = classify_service.classify(user_id)
    
    # Save classification to MongoDB
    db["user_profiles"].update_one(
        {"user_id": user_id},
        {"$set": classification},
        upsert=True
    )
    
    # Generate AI insights (mocked LLM)
    insights = insights_service.generate_insights(
        user_id=user_id,
        spender_type=classification["spender_type"],
        summary=classification["summary"]
    )
    
    # Save insights to MongoDB (optional for PoC)
    db["insights"].update_one(
        {"user_id": user_id},
        {"$set": insights.dict()},
        upsert=True
    )
    
    return insights