"""
R2.py - Sales Data Dashboard Menu
Main entry point for the dashboard. Loads the data via R1, then runs
the interactive menu that calls into R3 (predefined analytics) and
R4 (custom pivot table builder).
"""

from R1 import load_sales_data
from R3 import (
    show_first_n_rows,
    total_sales_by_region,
    avg_sales_by_region,
    sales_by_customer_type,
    total_sales_qty_price_by_product,
    total_sales_qty_price_by_customer,
    max_min_sales_by_category,
    unique_employees_by_region,
)
from R4 import custom_pivot_table

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
