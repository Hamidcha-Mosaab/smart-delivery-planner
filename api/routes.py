from fastapi import APIRouter
from api.schemas import PredictTravelRequest, AnalyzeFeedbackRequest
from typing import List
from fastapi import HTTPException
from loguru import logger
from src.utils.data_loader import DataLoader
from src.utils.traffic_predictor import SimpleTrafficPredictor
from src.core.delivery_manager import DeliveryManager

router = APIRouter()

@router.post("/predict-travel-time")
def predict_travel(req: PredictTravelRequest):
    predictor = SimpleTrafficPredictor()
    try:
        out = predictor.predict(req.from_lat, req.from_lon, req.to_lat, req.to_lon)
        return out
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-feedback")
def analyze_feedback(req: AnalyzeFeedbackRequest):
    from src.utils.sentiment_analyzer import simple_sentiment
    return {"text": req.text, "sentiment": simple_sentiment(req.text)}
