from fastapi import Depends
from api.dependencies import get_database
import random
from ai.models.utils import run_cc_pca_model

class ClassifyService:
    def classify(self, user_id: str) -> dict:
        db=Depends(get_database)
        transaction = db["transactions"].find({"user_id": user_id})
        if transaction:
            balance = transaction.balance
            balance_frequency = transaction.balance_frequency
            output = run_cc_pca_model([[balance,balance_frequency]])
        
        # Mock: Pretend we analyzed transactions, return random spender type
        spender_types = [
            {"type": "HIHS", "summary": "You earn big and spend big—living large!"},  # Cluster 1
            {"type": "LILS", "summary": "You’re cautious, keeping both income and spending low."},  # Cluster 2
            {"type": "HILS", "summary": "You’re a saver! You earn a lot but spend little."},  # Cluster 3
            {"type": "LIHS", "summary": "You’re a big spender on a tight budget."},  # Cluster 4
        ]
        # ummm no
        result = random.choice(spender_types)
        return {"user_id": user_id, "spender_type": result["type"], "summary": result["summary"]}

classify_service = ClassifyService()