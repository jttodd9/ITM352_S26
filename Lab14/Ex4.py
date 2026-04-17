import json
import os

import matplotlib.pyplot as plt

data_path = os.path.join(os.path.dirname(__file__), "Trips_Fri07072017T4 trip_miles gt1.json")

with open(data_path, "r") as f:
    trips = json.load(f)

fares = []
tips = []
for trip in trips:
    fare_val = trip.get("fare")
    tips_val = trip.get("tips")
    if fare_val is None or tips_val is None or fare_val == "" or tips_val == "":
        continue
    fares.append(float(fare_val))
    tips.append(float(tips_val))

plt.figure(figsize=(10, 6))
plt.scatter(fares, tips, color="steelblue", alpha=0.5)
plt.title("Fares vs Tips (Fri 07/07/2017, Trip Miles > 1)")
plt.xlabel("Fare ($)")
plt.ylabel("Tips ($)")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "fares_vs_tips_scatter.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
