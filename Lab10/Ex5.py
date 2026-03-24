#Read a csv file and put it into a dataframe

import pandas as pd
import csv


homes_df = pd.read_csv("homes_data.csv")


#Print out dimensions and 
# first 10 rows of the dataframe
print(f"Dimensions: {homes_df.shape}")
print(homes_df.head(10))

#Select only the properties that are