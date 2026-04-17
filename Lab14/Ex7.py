import json
import os

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data_path = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

with open(data_path, "r") as f:
    trips = json.load(f)

fares = []
miles = []
dropoff_areas = []
for trip in trips:
    fare_val = trip.get("fare")
    miles_val = trip.get("trip_miles")
    dropoff_val = trip.get("dropoff_community_area")
    if (fare_val is None or miles_val is None or dropoff_val is None
            or fare_val == "" or miles_val == "" or dropoff_val == ""):
        continue
    fares.append(float(fare_val))
    miles.append(float(miles_val))
    dropoff_areas.append(float(dropoff_val))

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(fares, miles, dropoff_areas, color="steelblue", alpha=0.5)
ax.set_xlabel("Fare ($)")
ax.set_ylabel("Trip Miles")
ax.set_zlabel("Dropoff Community Area")
ax.set_title("Fares vs Trip Miles vs Dropoff Area (Area 8)")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "fares_miles_dropoff_3d.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
