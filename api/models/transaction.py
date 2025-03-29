from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    date: datetime
    amount: float
    category: str  # e.g., "salary", "groceries"

class TransactionSummary(BaseModel):
    user_id: str
    total_amount: float
    amount_remaining: float
    amount_debited: float
    ai_investment: float = 0.0