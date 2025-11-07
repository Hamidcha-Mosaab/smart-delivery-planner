#!/usr/bin/env python3
import argparse, sys
from loguru import logger
from src.core.delivery_manager import DeliveryManager
from src.utils.data_loader import DataLoader
from src.core.real_time_tracker import RealTimeTracker
from src.core.cost_calculator import CostCalculator
from src.utils.traffic_predictor import SimpleTrafficPredictor
from src.utils.sentiment_analyzer import simple_sentiment

def main():
    parser = argparse.ArgumentParser(description="Livraison Intelligente ML")
    parser.add_argument('--mode', choices=['simulation','train'], default='simulation')
    parser.add_argument('--deliveries', type=int, default=10)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        logger.add("logs/app.log", rotation="1 day")

    logger.info("Démarrage du système")
    data_loader = DataLoader()
    clients = data_loader.load_clients()
    manager = DeliveryManager()
    tracker = RealTimeTracker()
    cost_calc = CostCalculator()

    if args.mode == 'train':
        from scripts.train_models import train_all
        train_all()
        return

    # Simulation
    deliveries = manager.create_deliveries(clients[:args.deliveries])
    route = manager.optimize_route(deliveries)
    results = manager.simulate_delivery_day(route, tracker=tracker, cost_calc=cost_calc)
    print_results(results)

def print_results(results):
    print("\\n" + "="*40)
    print("Résultats simulation")
    for k,v in results.items():
        print(f"{k}: {v}")
    print("="*40 + "\\n")

if __name__ == '__main__':
    main()
