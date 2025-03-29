from api.models.transaction import Transaction
from api.models.user import UserProfile
import random

class ClassifyService:
    def classify(self, user_id: str) -> dict:
        # Mock: Pretend we analyzed transactions, return random spender type
        spender_types = [
            {"type": "HILS", "summary": "You’re a saver! You earn a lot but spend little."},
            {"type": "LIHS", "summary": "You’re a big spender on a tight budget."},
            {"type": "HIHS", "summary": "You earn big and spend big—living large!"},
            {"type": "LILS", "summary": "You’re cautious, keeping both income and spending low."}
        ]
        result = random.choice(spender_types)
        return {"user_id": user_id, "spender_type": result["type"], "summary": result["summary"]}

classify_service = ClassifyService()