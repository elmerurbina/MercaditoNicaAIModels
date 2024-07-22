from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.market_analysis import MarketAnalysis
import requests

router = APIRouter()

class AnalysisRequest(BaseModel):
    user_id: int

@router.post("/run_analysis")
def run_analysis(request: AnalysisRequest):
    api_url = 'http://<django-backend-url>'  # Replace with your actual Django API URL
    analysis = MarketAnalysis(api_url)
    try:
        # Run the analysis
        analysis.run_analysis(request.user_id)
        return {"message": "Analysis completed successfully"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
