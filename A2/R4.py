# create a custom pivot table

import pandas as pd

# fields the user can pick from
ROW_COL_FIELDS = ["sales_region", "customer_state", "product_category",
                  "order_type", "customer_type", "employee_name"]
VALUE_FIELDS = ["quantity", "unit_price"]
AGG_FUNCTIONS = ["sum", "mean", "count", "max", "min"]

# show a numbered list and return the user's picks
def pick_from_list(options, prompt, allow_empty=False):
    print(f"\n{prompt}")
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt}")

    while True:
        choice = input("Enter number(s) separated by commas: ").strip()

        if choice == "" and allow_empty:
            return []

        # check each number is valid
        parts = [p.strip() for p in choice.split(",")]
        if all(p.isdigit() and 1 <= int(p) <= len(options) for p in parts):
            return [options[int(p) - 1] for p in parts]

        print(f"Invalid input. Enter numbers between 1 and {len(options)}.")

def custom_pivot_table(df):
    # pick rows
    rows = pick_from_list(ROW_COL_FIELDS, "Select rows:")

    # pick columns (optional)
    cols = pick_from_list(ROW_COL_FIELDS, "Select columns (optional, press Enter to skip):", allow_empty=True)

    # drop any column that's already a row
    cols = [c for c in cols if c not in rows]

    # pick values
    values = pick_from_list(VALUE_FIELDS, "Select values:")

    # pick one aggregation function
    agg = pick_from_list(AGG_FUNCTIONS, "Select aggregation function:")[0]

    # build the pivot table
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
    return pivot
