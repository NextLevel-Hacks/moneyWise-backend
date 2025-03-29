from pydantic import BaseModel

class Recommendation(BaseModel):
    recommendation_id: str
    asset: str           
    type: str            
    expected_return: str 
    risk_level: str      