# Get a .json file from the city of chicago and analyze driver types

import pandas as pd
import requests

# Create a rest query to get the json data
search_results = requests.get("https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type")
results_json = search_results.json()
print("Raw JSON results:")
print(results_json)  # Print the raw JSON results to understand the structure of the data

#create the datafram from the json results
results_df = pd.DataFrame(results_json)
results_df.columns = ["driver_type", "count"]  # Rename columns for clarity
results_df = results_df.set_index("driver_type")  # Set driver_type as the index for better readability
print("Driver types and their counts:")
print(results_df)
