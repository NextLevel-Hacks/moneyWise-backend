from pydantic import BaseModel

class Recommendation(BaseModel):
    recommendation_id: str
    asset: str           
    type: str            
    expected_return: str 
    risk_level: str      
      
class RecommendationInsights(BaseModel):
    user_id: str
    spender_type: str
    summary: str
