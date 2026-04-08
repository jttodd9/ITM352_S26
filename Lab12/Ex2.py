# Grab 1 month interest rate date from the treasury website

import urllib.request
import ssl
import pandas as pd
import lxml

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"
ssl._create_default_https_context = ssl._create_unverified_context

#Open the URL and use read_html to read the data into a DataFrame
print("Opening URL:", url)
webpage = urllib.request.urlopen(url)
data = pd.read_html(webpage)

print("Data read into DataFrame:")
# print(data[0])  # Print the first DataFrame from the list of DataFrames read
# print(data.info())  # Print information about the DataFrame to understand its structure and contents

print("Column names in the DataFrame:")
print(data[0].columns) # Print the column names of the DataFrame to see what data is available
# Extract 1 month interest rates
one_mont_rates = data[0].loc[0, "1 Mo"]  # Access the first row and the "1 Mo" column to get the 1 month interest rate
print (f"1 Month Interest Rate: {one_mont_rates}")  # Print the extracted 1 month interest rate
#Iterate through the data using iterrows() to find the one month rate for a specific date
for index, row in data[0].iterrows():
    if row["Date"] == "2026-03-01":  # Check if the date matches the desired date
        one_month_rate = row["1 Mo"]  # Get the 1 month interest rate for that date
        print(f"1 Month Interest Rate on 2026-03-01: {one_month_rate}")  # Print the 1 month interest rate for the specified date