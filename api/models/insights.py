from pydantic import BaseModel

class AIInsight(BaseModel):
    title: str
    description: str
    icon: str  # e.g., "up", "dollar", "piggy_bank"

class SpendingCategory(BaseModel):
    category: str
    amount: float

class InsightsResponse(BaseModel):
    user_id: str
    spender_type: str
    summary: str
    ai_insights: list[AIInsight]
    spending_analysis: list[SpendingCategory]