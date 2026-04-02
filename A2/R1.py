"""
R1.py - Sales Data Loader
Handles downloading, loading, validating, and cleaning the sales data CSV.
This module is imported by the main dashboard application.
"""

import pandas as pd
import time
import os
import sys
import gdown

FILENAME = "https://drive.google.com/uc?id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
LOCAL_PATH = "sales_data.csv"
REQUIRED_COLUMNS = ["order_id", "customer_id", "order_date", "sales_region", "customer_state", "product_category", "quantity", "unit_price", "order_type"]

# download the file if it doesn't exist locally
def download_file(url, output):
    """Download file from Google Drive using gdown."""
    try:
        gdown.download(url, output, quiet=False)
        print("File downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise SystemExit(1)
    
# Open the file time how long it takes and return it to dataframe
def load_data(filepath):
    print("Loading data, please wait...")
    start = time.time()
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        raise SystemExit(1)
    except pd.errors.EmptyDataError:
        print(f"File is empty: {filepath}")
        raise SystemExit(1)
    elapsed = time.time()-start
    return df, elapsed

def load_sales_data():
    """Main function to load pipeline"""
    # only download if file doesn't exist locally
    if not os.path.exists(LOCAL_PATH):
        download_file(FILENAME, LOCAL_PATH)

    # load the file and get elapsed time
    df, elapsed = load_data(LOCAL_PATH)

    # print success stats
    print(f"File loaded successfully in {elapsed:.3f} seconds.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # replace any missing values with 0
    missing_count = df.isnull().sum().sum()
    df = df.fillna(0)
    if missing_count > 0:
        print(f"Note: {missing_count} missing values replaced with 0.")

    # check that required columns exist, warn if any are missing
    actual_columns = [col.lower() for col in df.columns]
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in actual_columns]
    if missing_cols:
        print(f"[WARNING] Missing columns: {missing_cols}")
        print("Some analytics may not work correctly.")

    return df
if __name__ == "__main__":
    data = load_sales_data()