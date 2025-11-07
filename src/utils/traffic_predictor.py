class SimpleTrafficPredictor:
    def __init__(self):
        pass
    def predict(self, from_lat, from_lon, to_lat, to_lon):
        # naive: distance -> time multiplier
        dist = ((from_lat-to_lat)**2 + (from_lon-to_lon)**2)**0.5 * 111  # approx km
        if dist < 2: level="light"
        elif dist < 5: level="moderate"
        else: level="heavy"
        return {"distance_km": dist, "predicted_level": level}
