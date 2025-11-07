from pydantic import BaseModel

class PredictTravelRequest(BaseModel):
    from_lat: float
    from_lon: float
    to_lat: float
    to_lon: float

class AnalyzeFeedbackRequest(BaseModel):
    text: str
