from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_database, get_current_user
from api.services.chatbot_service import chatbot_service



router = APIRouter(tags=["Chat"])

@router.post("/chat/{user_id}/chat")
async def chat(
    user_id: str,
    message: str,
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    # Ensure the user is authorized to chat as themselves
    user = db["users"].find_one({"email": current_user["email"]})
    if str(user["_id"]) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to chat as this user")
    
    # Get chatbot response
    response = chatbot_service.get_response(user_id, message, db)
    return {"response": response}