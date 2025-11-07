import csv, os, random
os.makedirs("data", exist_ok=True)
with open("data/clients.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["id","name","lat","lon"])
    for i in range(1,51):
        writer.writerow([i,f"Client {i}",48.8566 + random.uniform(-0.01,0.01), 2.3522 + random.uniform(-0.01,0.01)])
print("Clients generated: data/clients.csv")
