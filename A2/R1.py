# R1.py - Handles downloading the file and loading it into a dataframe,

import pandas as pd
import time
import os
import gdown

REQUIRED_COLUMNS = ["order_id", "customer_id", "order_date", "sales_region", "customer_state", "product_category", "quantity", "unit_price", "order_type"]

# list of datasets the user can pick from
DATASETS = (
    ("Default sales data (Google Drive)",
     "https://drive.google.com/uc?id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA",
     "sales_data.csv"),
    ("Provide my own local CSV file", None, None),
)

# download the file from google drive
def download_file(url, output):
    try:
        gdown.download(url, output, quiet=False)
        print("File downloaded successfully.")
    except Exception as e:
        print(f"Error downloading file: {e}")
        raise SystemExit(1)
    
# open the file and return it as a dataframe
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

# let the user pick which dataset to load
def pick_dataset():
    print("\nAvailable datasets:")
    for i, (label, _, _) in enumerate(DATASETS, start=1):
        print(f"  {i}. {label}")

    while True:
        choice = input("Choose a dataset (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(DATASETS):
            label, url, local_path = DATASETS[int(choice) - 1]
            break
        print(f"Invalid input. Enter a number between 1 and {len(DATASETS)}.")

    # if no url, ask the user for a local file path
    if url is None:
        path = input("Enter path to local CSV file: ").strip().strip('"')
        if not os.path.exists(path):
            print(f"File not found: {path}")
            raise SystemExit(1)
        return path

    # otherwise download it if not already saved
    if not os.path.exists(local_path):
        download_file(url, local_path)
    return local_path

# main loader
def load_sales_data():
    filepath = pick_dataset()

    # load the file
    df, elapsed = load_data(filepath)

    # print stats
    print(f"File loaded successfully in {elapsed:.3f} seconds.")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")

    # replace missing values with 0
    missing_count = df.isnull().sum().sum()
    df = df.fillna(0)
    if missing_count > 0:
        print(f"Note: {missing_count} missing values replaced with 0.")

    # warn if any required columns are missing
    actual_columns = [col.lower() for col in df.columns]
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in actual_columns]
    if missing_cols:
        print(f"[WARNING] Missing columns: {missing_cols}")
        print("Some analytics may not work correctly.")

    return df
if __name__ == "__main__":
    data = load_sales_data()