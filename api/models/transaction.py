from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    date: datetime
    amount: float
    category: str  # e.g., "salary", "groceries"