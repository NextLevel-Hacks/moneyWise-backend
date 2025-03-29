from api.models.transaction import TransactionSummary
import random

class TransactionService:
    def summarize_transactions(self, user_id: str) -> TransactionSummary:
        # Mock: Pretend we got transaction history and summarized it
        total_amount = round(random.uniform(4000, 6000), 2)  
        amount_debited = round(random.uniform(1000, 2000), 2)  
        amount_remaining = total_amount - amount_debited  
        ai_investment = 0.0  # Starts at 0
        
        return TransactionSummary(
            user_id=user_id,
            total_amount=total_amount,
            amount_remaining=amount_remaining,
            amount_debited=amount_debited,
            ai_investment=ai_investment
        )

transaction_service = TransactionService()