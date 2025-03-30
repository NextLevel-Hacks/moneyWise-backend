from fastapi import Depends
from api.dependencies import get_database
from ai.models.utils import run_cc_pca_model

class RecommendService:
    def recommend(self, user_id: str) -> dict:
        db=Depends(get_database)
        profile = db["user_profile"].find({"user_id": user_id})
        if profile:
            spender_type = profile.spender_type
            # we would have a model here ideally
            # based on the spender type, we get the type of investment for them
        
        investment_types = [
            {"type": "HIHS", "summary": "We would suggest investing in Achieve's Global Tech, more volatile than a domestic fund yet offers higher growth potentials."},  # Cluster 1
            {"type": "LILS", "summary": "We would suggest investing in Achieve's Africa Eurobond Trust, it invests in USD-denominated securities to provide investors with competitive return."},  # Cluster 2
            {"type": "HILS", "summary": "We would suggest investing in Achieve's DigiSave, which offers you the highest possible return for money with a low risk. "},  # Cluster 3
            {"type": "LIHS", "summary": "We would suggest investing in Cryptocurrency, mainly BTC, USDT, ETH which offers a high reward for high risk but more stable than other cryptocurrencies"},  # Cluster 4
        ]
        # ummm no
        result = {}
        for i in investment_types:
           if  i.type == spender_type:
               result = i
            
        return {"user_id": user_id, "spender_type": result["type"], "recommendation": result["summary"]}

classify_service = RecommendService()