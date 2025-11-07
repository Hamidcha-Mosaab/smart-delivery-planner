class CostCalculator:
    def __init__(self, fuel_per_km=0.15, base_cost=5.0):
        self.fuel_per_km = fuel_per_km
        self.base_cost = base_cost

    def cost_for_route(self, distance_km, delay_minutes=0):
        return self.base_cost + distance_km*self.fuel_per_km + max(0, delay_minutes)*0.5
