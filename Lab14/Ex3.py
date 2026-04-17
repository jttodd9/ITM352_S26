import json
import os

import matplotlib.pyplot as plt

data_path = os.path.join(os.path.dirname(__file__), "Trips from area 8.json")

with open(data_path, "r") as f:
    trips = json.load(f)

tips_by_method = {}
for trip in trips:
    method = trip.get("payment_type")
    tips_val = trip.get("tips")
    if method is None or tips_val is None or method == "" or tips_val == "":
        continue
    tips_by_method[method] = tips_by_method.get(method, 0) + float(tips_val)

methods = list(tips_by_method.keys())
totals = list(tips_by_method.values())

plt.figure(figsize=(8, 6))
plt.bar(methods, totals, color="coral", edgecolor="black")
plt.title("Total Tips by Payment Method (Area 8)")
plt.xlabel("Payment Method")
plt.ylabel("Total Tips ($)")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "tips_by_payment_histogram.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
