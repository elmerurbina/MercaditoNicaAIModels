from fastapi import FastAPI
from api.enpoints import market_analysis, pricing, recommender, chatbot

app = FastAPI()

app.include_router(market_analysis.router, prefix="/market_analysis", tags=["market_analysis"])
app.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
app.include_router(recommender.router, prefix="/recommender", tags=["recommender"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MercaditoNica AI Models API"}
