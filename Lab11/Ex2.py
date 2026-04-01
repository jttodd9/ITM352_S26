import pandas as pd
import numpy as np

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

# Show all columns when printing
pd.set_option("display.max_columns", None)

# Load the CSV file
df = pd.read_csv(filename, dtype_backend="pyarrow", on_bad_lines="skip")
print("Data loaded successfully.\n")

# Convert order_date to a real date
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", format="mixed")

# Make sure quantity and unit_price are numbers
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

# Create a new sales column
df["sales"] = df["quantity"] * df["unit_price"]

# Show the first 5 rows with the new sales column
print("=== First 5 rows ===")
print(df[["sales_region", "order_type", "quantity", "unit_price", "sales"]].head(5))

# Create a pivot table: total sales by region and order type
pivot = pd.pivot_table(
    df,
    values="sales",
    index="sales_region",
    columns="order_type",
    aggfunc=np.sum,
    margins=True,
    margins_name="Total",
    fill_value=0,
)

print("\n=== Sales by Region and Order Type ===")
print(pivot)
