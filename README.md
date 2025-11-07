# 🚚 Livraison Intelligente avec Machine Learning

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![ML](https://img.shields.io/badge/ML-RandomForest%20%7C%20BERT-orange.svg)

## 📋 Description

Système intelligent de gestion de livraison utilisant l'IA pour :
- 📍 Optimiser les itinéraires de livraison
- 🤖 Prédire le trafic en temps réel avec Random Forest
- 🧠 Analyser les sentiments clients avec BERT (optionnel)
- 📊 Regrouper géographiquement les clients avec KMeans
- ⏱️ Suivre les livreurs en temps réel via un dashboard Streamlit
- 💰 Calculer les coûts et indicateurs métier

## 🚀 Installation Rapide

```bash
# Cloner le projet
git clone https://github.com/votre-username/livraison-intelligente-ml.git
cd livraison-intelligente-ml

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# (Optionnel) Télécharger les modèles BERT (première utilisation)
python scripts/download_models.py
```

## 🎯 Utilisation

### Mode CLI - Simulation de livraison
```bash
python main.py --mode simulation --deliveries 20
```

### API REST
```bash
uvicorn api.app:app --reload --port 5000
# API disponible sur http://localhost:5000
```

### Dashboard Web
```bash
streamlit run dashboard/app.py
# Dashboard sur http://localhost:8501
```

## 📁 Structure du Projet

```
livraison-intelligente-ml/
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── main.py
├── .env.example
├── api/
│   ├── app.py
│   ├── routes.py
│   └── schemas.py
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── core/
│   │   ├── delivery_manager.py
│   │   ├── cost_calculator.py
│   │   └── real_time_tracker.py
│   └── utils/
│       ├── data_loader.py
│       ├── clustering.py
│       ├── traffic_predictor.py
│       └── sentiment_analyzer.py
│
└── scripts/
    ├── generate_data.py
    └── train_models.py
```

## 🧪 Tests

Exemples de tests à ajouter (pytest).

## 🤝 Contribution

Contributions bienvenues — voir CONTRIBUTING.md (à ajouter).

## 📝 License

MIT License - voir LICENSE
