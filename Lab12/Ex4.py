

import pandas as pd
from sodapy import Socrata

#create a sodapy client to access the city of chicagos data portal
client = Socrata("data.cityofchicago.org", None)

#Specify the JSON file for license data
json_file = "rr23-ymub"

results = client.get(json_file, limit=500)
#Convert the results to a DataFrame
df = pd.DataFrame.from_records(results)

print(df.head())

vehicles_and_fuel_sources = df[["public_vehicle_number" , "vehicle_fuel_source"]]
print("Public vehicles and their fuel sources:")
print(vehicles_and_fuel_sources.head())


vehicles_by_fuel_source = vehicles_and_fuel_sources.groupby("vehicle_fuel_source").count()
print("Number of Public vehicles by fuel source:")
print(vehicles_by_fuel_source)

