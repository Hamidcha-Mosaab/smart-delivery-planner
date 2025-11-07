import random, time
from typing import List, Dict
from src.utils.clustering import cluster_clients
from src.utils.traffic_predictor import SimpleTrafficPredictor
from src.core.real_time_tracker import RealTimeTracker

class DeliveryManager:
    def __init__(self):
        self.tracker = RealTimeTracker()
        self.predictor = SimpleTrafficPredictor()

    def create_deliveries(self, clients: List[dict]) -> List[dict]:
        # clients: list of dict with lat/lon
        deliveries = []
        for i,c in enumerate(clients):
            deliveries.append({"id": i+1, "client": c.get("name", f"Client{i}"), "lat": c["lat"], "lon": c["lon"]})
        return deliveries

    def optimize_route(self, deliveries: List[dict]) -> List[dict]:
        # simple nearest-neighbor greedy
        remaining = deliveries.copy()
        route = []
        current = (48.8566,2.3522)
        while remaining:
            best=None; bestd=1e9
            for d in remaining:
                dist = ((current[0]-d["lat"])**2 + (current[1]-d["lon"])**2)**0.5
                if dist<bestd:
                    bestd=dist; best=d
            route.append(best)
            remaining.remove(best)
            current = (best["lat"], best["lon"])
        return route

    def simulate_delivery_day(self, route: List[dict], tracker: RealTimeTracker=None, cost_calc=None) -> Dict:
        successful=0; failed=0; total_dist=0.0; total_time=0.0; satisfaction=[]
        for stop in route:
            # simulate travel and tracking
            if tracker:
                tracker.record_point(stop["client"], stop["lat"], stop["lon"], "clear", 20.0, "light")
            time.sleep(0.1)
            successful+=1
            satisfaction.append(0.9)
        return {
            "successful_deliveries": successful,
            "failed_deliveries": failed,
            "total_distance": total_dist,
            "total_time": total_time,
            "avg_satisfaction": sum(satisfaction)/len(satisfaction) if satisfaction else 0
        }
