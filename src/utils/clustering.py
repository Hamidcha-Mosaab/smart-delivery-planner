from sklearn.cluster import KMeans
def cluster_clients(clients, n_clusters=3):
    coords = [[c["lat"], c["lon"]] for c in clients]
    if len(coords)<n_clusters:
        n_clusters = max(1,len(coords))
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(coords)
    clusters = {}
    for lbl, c in zip(labels, clients):
        clusters.setdefault(lbl, []).append(c)
    return clusters
