# the 8 predefined pivot table analytics

import pandas as pd

def show_first_n_rows(df):
    total = len(df)
    print(f"\nEnter rows to display:")
    print(f"  - Enter a number 1 to {total}")
    print(f"  - To see all rows, enter 'all'")
    print(f"  - To skip preview, press Enter")

    choice = input("Your choice: ").strip().lower()

    if choice == "":
        print("Skipping preview.")
    elif choice == "all":
        print(df.to_string())
    elif choice.isdigit() and 1 <= int(choice) <= total:
        print(df.head(int(choice)).to_string())
    else:
        print(f"Invalid input. Enter a number between 1 and {total}, 'all', or press Enter.")

def total_sales_by_region(df):
    pivot = pd.pivot_table(
        df,
        values="unit_price",
        index="sales_region",
        columns="order_type",
        aggfunc="sum",
        fill_value=0
    )
    print("\nTotal Sales by Region and Order Type:")
    print(pivot.to_string())
    return pivot

def avg_sales_by_region(df):
    pivot = pd.pivot_table(
        df,
        values="unit_price",
        index="sales_region",
        columns=["customer_state", "order_type"],
        aggfunc="mean",
        fill_value=0
    )
    print("\nAverage Sales by Region (by State and Sale Type):")
    print(pivot.to_string())
    return pivot

def sales_by_customer_type(df):
    pivot = pd.pivot_table(
        df,
        values="unit_price",
        index=["customer_state", "customer_type", "order_type"],
        aggfunc="sum",
        fill_value=0
    )
    print("\nSales by Customer Type and Order Type, by State:")
    print(pivot.to_string())
    return pivot

def total_sales_qty_price_by_product(df):
    pivot = pd.pivot_table(
        df,
        values=["quantity", "unit_price"],
        index=["sales_region", "product_category"],
        aggfunc="sum",
        fill_value=0
    )
    print("\nTotal Quantity and Sales Price by Region and Product:")
    print(pivot.to_string())
    return pivot

def total_sales_qty_price_by_customer(df):
    pivot = pd.pivot_table(
        df,
        values=["quantity", "unit_price"],
        index=["order_type", "customer_type"],
        aggfunc="sum",
        fill_value=0
    )
    print("\nTotal Quantity and Sales Price by Order Type and Customer Type:")
    print(pivot.to_string())
    return pivot

def max_min_sales_by_category(df):
    pivot = pd.pivot_table(
        df,
        values="unit_price",
        index="product_category",
        aggfunc=["max", "min"],
        fill_value=0
    )
    print("\nMax and Min Sales Price by Category:")
    print(pivot.to_string())
    return pivot

def unique_employees_by_region(df):
    pivot = pd.pivot_table(
        df,
        values="employee_name",
        index="sales_region",
        aggfunc="nunique",
        fill_value=0
    )
    print("\nNumber of Unique Employees by Region:")
    print(pivot.to_string())
    return pivot
