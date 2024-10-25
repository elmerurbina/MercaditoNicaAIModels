from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.pricing import PricingCalculator


router = APIRouter()

class PricingRequest(BaseModel):
    product_id: int

class PricingResponse(BaseModel):
    suggested_price: float
    earnings_percentage: float
    message: str

@router.post("/pricing/", response_model=PricingResponse)
def calculate_pricing(request: PricingRequest):
    try:
        calculator = PricingCalculator(request.product_id)
        suggested_price, earnings_percentage = calculator.suggest_price()
        message = calculator.generate_price_suggestion_message()
        return PricingResponse(suggested_price=suggested_price, earnings_percentage=earnings_percentage, message=message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
