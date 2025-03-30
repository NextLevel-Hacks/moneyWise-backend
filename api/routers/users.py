from fastapi import APIRouter, Depends, HTTPException
from api.dependencies import get_database, get_current_user
from typing import Optional
from api.models.user import UpdateUserRequest
from bson import ObjectId

router = APIRouter(tags=["User"])

@router.patch("/users/{user_id}")
async def update_user(
    user_id: str,
    update_data: UpdateUserRequest,
    current_user=Depends(get_current_user),
    db=Depends(get_database)
):
    # Verify user exists
    existing_user = db["users"].find_one({"_id": ObjectId(user_id)})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Authorization check
    if str(existing_user["_id"]) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this user")
    
    # Build update dictionary
    update_dict = {}
    if update_data.first_name is not None:
        update_dict["first_name"] = update_data.first_name
    if update_data.last_name is not None:
        update_dict["last_name"] = update_data.last_name
    if update_data.email is not None:
        if db["users"].find_one({"email": update_data.email, "_id": {"$ne": ObjectId(user_id)}}):
            raise HTTPException(status_code=400, detail="Email already in use")
        update_dict["email"] = update_data.email
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Perform update
    result = db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_dict}
    )
    
    # Verify update was successful
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update user")
    
    # Return updated user
    updated_user = db["users"].find_one({"_id": ObjectId(user_id)})
    return {
        "id": str(updated_user["_id"]),
        "first_name": updated_user["first_name"],
        "last_name": updated_user["last_name"],
        "email": updated_user["email"]
    }