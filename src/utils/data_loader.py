import csv, os
def load_clients(path="data/clients.csv"):
    clients=[]
    if not os.path.exists(path):
        # generate sample clients
        for i in range(1,21):
            clients.append({"id":i, "name":f"Client {i}", "lat":48.8566 + (i*0.001)%0.01, "lon":2.3522 + (i*0.0015)%0.01})
        return clients
    with open(path,newline='') as f:
        reader=csv.DictReader(f)
        for r in reader:
            clients.append({"id":r.get("id"), "name":r.get("name"), "lat":float(r.get("lat")), "lon":float(r.get("lon"))})
    return clients
