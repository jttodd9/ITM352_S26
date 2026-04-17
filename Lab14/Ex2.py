import json
import os

import matplotlib.pyplot as plt

data_path = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

with open(data_path, "r") as f:
    trips = json.load(f)

trip_miles = [float(trip["trip_miles"]) for trip in trips]

plt.figure(figsize=(10, 6))
plt.hist(trip_miles, bins=30, color="steelblue", edgecolor="black")
plt.title("Distribution of Trip Miles (Area 8)")
plt.xlabel("Trip Miles")
plt.ylabel("Frequency")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "trip_miles_histogram.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
