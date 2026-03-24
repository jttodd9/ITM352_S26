#Read the json file of taxi trip data at and create a dataframe from it. Print summary statistics about the dataframe, as well as the median.

import pandas as pd
import json

taxidf = pd.read_json("taxi_trips.json")
median_fare = taxidf["fare"].median()
print(taxidf.describe())


print(taxidf.head())
print(f"Median fare: {median_fare}")