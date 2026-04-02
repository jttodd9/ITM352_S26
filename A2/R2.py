import pandas as pd
from R1 import load_sales_data

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

def sales_by_customer_type(df):
    print("Coming soon: Sales by customer type and order type by state")

def total_sales_qty_price_by_product(df):
    print("Coming soon: Total sales quantity and price by region and product")

def total_sales_qty_price_by_customer(df):
    print("Coming soon: Total sales quantity and price by customer type")

def max_min_sales_by_category(df):
    print("Coming soon: Max and min sales price by category")

def unique_employees_by_region(df):
    print("Coming soon: Number of unique employees by region")

def custom_pivot_table(df):
    print("Coming soon: Custom pivot table")

def exit_dashboard(df):
    print("Goodbye!")
    raise SystemExit(0)

# Tuple of (label, function) pairs, reorder or add items here to change menu
MENU_ITEMS = (
    ("Show the first n rows of sales data",                show_first_n_rows),
    ("Total sales by region and order_type",               total_sales_by_region),
    ("Average sales by region with average by state",      avg_sales_by_region),
    ("Sales by customer type and order type by state",     sales_by_customer_type),
    ("Total sales quantity and price by region/product",   total_sales_qty_price_by_product),
    ("Total sales quantity and price by customer type",    total_sales_qty_price_by_customer),
    ("Max and min sales price by category",                max_min_sales_by_category),
    ("Number of unique employees by region",               unique_employees_by_region),
    ("Create a custom pivot table",                        custom_pivot_table),
    ("Exit",                                               exit_dashboard),
)

def run_menu(df):
    while True:
        print("\n--- Sales Data Dashboard ---")
        # Print each item with its number, generated from position
        for i, (label, _) in enumerate(MENU_ITEMS, start=1):
            print(f"{i}. {label}")

        choice = input("\nEnter your choice: ").strip()

        # Validate: must be a number within range
        if not choice.isdigit() or not (1 <= int(choice) <= len(MENU_ITEMS)):
            print(f"Invalid choice. Enter a number between 1 and {len(MENU_ITEMS)}.")
            continue

        # Call the function paired with the chosen menu item
        _, func = MENU_ITEMS[int(choice) - 1]
        func(df)

if __name__ == "__main__":
    df = load_sales_data()
    run_menu(df)