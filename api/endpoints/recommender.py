from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.recommender import Recommender


router = APIRouter()

class RecommendationRequest(BaseModel):
    user_id: int
    top_n: int = 5

@router.post("/recommendations/")
def get_recommendations(request: RecommendationRequest):
    try:
        recommender = Recommender(django_api_base_url='http://<django-backend-url>')
        recommendations = recommender.recommend(user_id=request.user_id, top_n=request.top_n)
        return recommendations.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
