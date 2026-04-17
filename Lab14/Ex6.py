import json
import os

import matplotlib.pyplot as plt

data_path = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

with open(data_path, "r") as f:
    trips = json.load(f)

fares = []
miles = []
for trip in trips:
    fare_val = trip.get("fare")
    miles_val = trip.get("trip_miles")
    if fare_val is None or miles_val is None or fare_val == "" or miles_val == "":
        continue
    if float(miles_val) < 2:
        continue
    fares.append(float(fare_val))
    miles.append(float(miles_val))

plt.figure(figsize=(10, 6))
plt.scatter(fares, miles, color="steelblue", alpha=0.5)
plt.title("Fares vs Trip Miles (Area 8)")
plt.xlabel("Fare ($)")
plt.ylabel("Trip Miles")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "FaresXmiles.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
