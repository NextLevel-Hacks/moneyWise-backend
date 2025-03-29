from api.models.insights import AIInsight, SpendingCategory, InsightsResponse

class InsightsService:
    def generate_insights(self, user_id: str, spender_type: str, summary: str) -> InsightsResponse:
        # Mock: Generate AI insights based on spender type
        insights_map = {
            "HILS": [
                AIInsight(title="Spending Reduced", description="Your dining out expenses were 15% lower than last month. Great job!", icon="up"),
                AIInsight(title="Savings Opportunity", description="You could save $240 annually by switching phone plans.", icon="piggy_bank")
            ],
            "LIHS": [
                AIInsight(title="Unusual Expense", description="We detected an unusual $59.99 subscription charge yesterday.", icon="dollar"),
                AIInsight(title="Spending Alert", description="Your food expenses are up 20% this month.", icon="warning")
            ],
            "HIHS": [
                AIInsight(title="High Spending", description="Your shopping expenses spiked by 30% this month.", icon="warning"),
                AIInsight(title="Investment Opportunity", description="Consider investing $500 in ETFs to diversify.", icon="dollar")
            ],
            "LILS": [
                AIInsight(title="Steady Habits", description="Your spending is consistent—great for budgeting!", icon="check"),
                AIInsight(title="Small Wins", description="You could save $50 by cutting back on transport.", icon="piggy_bank")
            ]
        }
        
        # Mock: Spending analysis (weekly/monthly chart data)
        spending_analysis = [
            SpendingCategory(category="Food", amount=650),
            SpendingCategory(category="Shopping", amount=420),
            SpendingCategory(category="Transport", amount=310)
        ]
        
        return InsightsResponse(
            user_id=user_id,
            spender_type=spender_type,
            summary=summary,
            ai_insights=insights_map.get(spender_type, []),
            spending_analysis=spending_analysis
        )

insights_service = InsightsService()