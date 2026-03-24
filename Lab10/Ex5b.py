#Read a csv file and put it into a dataframe

import pandas as pd
import csv


homes_df = pd.read_csv("homes_data.csv")

#Select only properties that have 500 or more units.
#  Drop some unnecessary columns and print the first 
# 10 rows
large_homes_df = homes_df[homes_df["units"] >= 500]

#Drop some unnecessary columns
large_homes_df = large_homes_df.drop(columns=["id", "easement"])
                                              

#Convert Columns to appropriate data types.
large_homes_df["sale_price"] = pd.to_numeric(large_homes_df["sale_price"], errors="coerce") 
large_homes_df["land_sqft"] = pd.to_numeric(large_homes_df["land_sqft"], errors="coerce")
large_homes_df["gross_sqft"] = pd.to_numeric(large_homes_df["gross_sqft"], errors="coerce")

#drop rows with missing values
large_homes_df = large_homes_df.dropna()

#drop duplicates
large_homes_df = large_homes_df.drop_duplicates()

#print out first 10 rows after cleansing
print(large_homes_df.head(10))