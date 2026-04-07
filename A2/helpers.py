# shared helpers for row filtering and excel export

import os

# ask the user which rows to use and return that slice
def filter_rows(df):
    total = len(df)
    print(f"\nThis dataset has {total} rows (0 to {total - 1}).")
    print("Which rows do you want to use?")
    print("  - Press Enter to use ALL rows")
    print("  - Enter a range like 10-50")
    print("  - Enter a comma-separated list like 1,5,9,12")

    while True:
        choice = input("Your choice: ").strip()

        if choice == "":
            return df

        # range like 10-50
        if "-" in choice and "," not in choice:
            parts = choice.split("-")
            if len(parts) == 2 and all(p.strip().isdigit() for p in parts):
                start, end = int(parts[0]), int(parts[1])
                if 0 <= start <= end < total:
                    # +1 because iloc end is exclusive
                    return df.iloc[start:end + 1]

        # list like 1,5,9
        if "," in choice or choice.isdigit():
            parts = [p.strip() for p in choice.split(",")]
            if all(p.isdigit() and 0 <= int(p) < total for p in parts):
                return df.iloc[[int(p) for p in parts]]

        print(f"Invalid input. Use a range (0-{total - 1}), a list, or press Enter.")

# ask if the user wants to export the pivot table to excel
def maybe_export(result):
    if result is None:
        return

    choice = input("\nExport this result to an Excel file? (y/n): ").strip().lower()
    if choice != "y":
        return

    while True:
        filename = input("Enter filename (e.g. report.xlsx): ").strip()
        if filename == "":
            print("Filename cannot be empty.")
            continue
        # add .xlsx if missing
        if not filename.lower().endswith(".xlsx"):
            filename += ".xlsx"
        break

    try:
        result.to_excel(filename)
        print(f"Saved to {os.path.abspath(filename)}")
    except ImportError:
        print("Missing 'openpyxl'. Install it with: pip install openpyxl")
    except Exception as e:
        print(f"Could not save file: {e}")
