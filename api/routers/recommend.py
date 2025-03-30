from fastapi import APIRouter, Depends
from api.dependencies import get_database, get_current_user
from api.models.recommendation import RecommendationInsights
from api.services.recommend_service import recommend_service

router = APIRouter()

@router.post("/users/{user_id}/recommendation", response_model=RecommendationInsights)
async def make_recommendation(
    user_id: str,
    db=Depends(get_database),
    current_user=Depends(get_current_user)
):
    # Mocked recommendation
    recommendation = recommend_service.recommend(user_id)
    
    # Save classification to MongoDB
    db["user_recommendations"].update_one(
        {"user_id": user_id},
        {"$set": recommendation},
        upsert=True
    )
    

    
    return recommendation