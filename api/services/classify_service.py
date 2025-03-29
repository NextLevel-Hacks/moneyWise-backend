from api.models.transaction import Transaction
from api.models.user import UserProfile

class ClassifyService:
    def classify(self, transactions: list[Transaction]) -> str:
        # Mock: Simple rule-based classification (replace with model later)
        total_income = sum(t.amount for t in transactions if t.category == "salary")
        total_spending = abs(sum(t.amount for t in transactions if t.amount < 0))
        
        if total_income > 1000 and total_spending < 200:
            return "HILS"
        elif total_income <= 1000 and total_spending >= 800:
            return "LIHS"
        elif total_income > 1000 and total_spending >= 800:
            return "HIHS"
        else:
            return "LILS"

classify_service = ClassifyService()