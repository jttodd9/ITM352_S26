# Read in a CSV file and create a dataframe.
# Print some useful info

import pandas as pd


filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option("display.max_columns", None)  # Show all columns in the output


try:
    df = pd.read_csv(
        filename,
        dtype_backend="pyarrow",   # use PyArrow-backed dtypes
        on_bad_lines="skip",       # skip malformed rows instead of crashing
    )
    print("Data loaded successfully.\n")
except Exception as e:
    print(f"Failed to load data: {e}")
    raise SystemExit(1)

# First 5 rows
print("=== First 5 rows ===")
print(df.head(5))

# Column data types
print("\n=== Column data types ===")
print(df.dtypes)


df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

print("\n=== order_date after conversion ===")
print(df["order_date"].dtype)
print(df["order_date"].head(5))
