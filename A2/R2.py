# Main entry point for the sales data dashboard.

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
from helpers import filter_rows, maybe_export

def exit_dashboard(df):
    print("Goodbye!")
    raise SystemExit(0)

# skip row filter and export for these
SKIP_FILTER = {show_first_n_rows, exit_dashboard}

# menu items: (label, function)
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
        # print each menu item
        for i, (label, _) in enumerate(MENU_ITEMS, start=1):
            print(f"{i}. {label}")

        choice = input("\nEnter your choice: ").strip()

        # check choice is a valid number
        if not choice.isdigit() or not (1 <= int(choice) <= len(MENU_ITEMS)):
            print(f"Invalid choice. Enter a number between 1 and {len(MENU_ITEMS)}.")
            continue

        # run the picked function
        _, func = MENU_ITEMS[int(choice) - 1]

        if func in SKIP_FILTER:
            func(df)
            continue

        # ask which rows to use, then run the analytic
        working_df = filter_rows(df)
        result = func(working_df)

        # ask if the user wants to save it to excel
        maybe_export(result)

if __name__ == "__main__":
    df = load_sales_data()
    run_menu(df)
