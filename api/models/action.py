from pydantic import BaseModel
from datetime import datetime

class Action(BaseModel):
    action_id: str
    user_id: str
    recommendation_id: str
    amount: float
    asset: str
    confidence_score: float
    timestamp: datetime
    status: str  # e.g., "completed", "pending"