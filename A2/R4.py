"""
R4.py - Custom Pivot Table Builder
Lets the user build their own pivot table by picking rows, columns,
values, and an aggregation function from numbered lists.
"""

import pandas as pd

# Fields the user can pick from in the custom pivot table builder
ROW_COL_FIELDS = ["sales_region", "customer_state", "product_category",
                  "order_type", "customer_type", "employee_name"]
VALUE_FIELDS = ["quantity", "unit_price"]
AGG_FUNCTIONS = ["sum", "mean", "count", "max", "min"]

def pick_from_list(options, prompt, allow_empty=False):
    """Show a numbered list, return the user's selected items as a list of strings."""
    print(f"\n{prompt}")
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")

    while True:
        choice = input("Enter number(s) separated by commas: ").strip()

        if choice == "" and allow_empty:
            return []

        # Split by comma, strip whitespace, validate each is a digit in range
        parts = [p.strip() for p in choice.split(",")]
        if all(p.isdigit() and 1 <= int(p) <= len(options) for p in parts):
            return [options[int(p) - 1] for p in parts]

        print(f"Invalid input. Enter numbers between 1 and {len(options)}.")

def custom_pivot_table(df):
    # 1. Pick row fields (required)
    rows = pick_from_list(ROW_COL_FIELDS, "Select rows:")

    # 2. Pick column fields (optional - press Enter to skip)
    cols = pick_from_list(ROW_COL_FIELDS, "Select columns (optional, press Enter to skip):", allow_empty=True)

    # Remove any column choices that are already row choices to avoid pandas error
    cols = [c for c in cols if c not in rows]

    # 3. Pick value fields (required)
    values = pick_from_list(VALUE_FIELDS, "Select values:")

    # 4. Pick aggregation function (required, just one)
    agg = pick_from_list(AGG_FUNCTIONS, "Select aggregation function:")[0]

    # Build the pivot table
    pivot = pd.pivot_table(
        df,
        values=values,
        index=rows,
        columns=cols if cols else None,
        aggfunc=agg,
        fill_value=0
    )
    print("\nCustom Pivot Table:")
    print(pivot.to_string())
