import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_path = os.path.join(os.path.dirname(__file__), "taxi trips Fri 7_7_2017.csv")

df = pd.read_csv(data_path)

df = df.dropna(subset=["pickup_community_area", "dropoff_community_area"])
df["pickup_community_area"] = df["pickup_community_area"].astype(int)
df["dropoff_community_area"] = df["dropoff_community_area"].astype(int)

heatmap_data = df.groupby(["pickup_community_area", "dropoff_community_area"]).size().unstack(fill_value=0)

plt.figure(figsize=(14, 12))
sns.heatmap(heatmap_data, cmap="YlOrRd", linewidths=0.1)
plt.title("Trip Count: Pickup vs Dropoff Community Area (Fri 7/7/2017)")
plt.xlabel("Dropoff Community Area")
plt.ylabel("Pickup Community Area")
plt.tight_layout()

chart_path = os.path.join(os.path.dirname(__file__), "pickup_dropoff_heatmap.png")
plt.savefig(chart_path)
plt.show()
print(f"Chart saved to {chart_path}")
