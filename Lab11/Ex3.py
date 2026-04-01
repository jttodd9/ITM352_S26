import pandas as pd
import numpy as np

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "${:,.2f}".format)

df = pd.read_csv(filename, dtype_backend="pyarrow", on_bad_lines="skip")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce", format="mixed")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
df["sales"] = df["quantity"] * df["unit_price"]

pivot = pd.pivot_table(
    df,
    values="sales",
    index=["sales_region", "customer_state"],
    columns="order_type",
    aggfunc=[np.sum, np.mean],
    margins=True,
    margins_name="Total",
    fill_value=0,
)

print(pivot)
