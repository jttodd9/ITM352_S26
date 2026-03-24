# Create a list of tuples that are percentiles of houshold income

import numpy as np

hh_income = [
    (10, 14629),
    (20, 25600),
    (30, 37002),
    (40, 50000),
    (50, 63179),
    (60, 79542),
    (70, 100162),
    (80, 130000),
    (90, 184292)
]

hh_income_array = np.array(hh_income)

# Report the dimensions of the array and the number of elements.
print(f"Dimensions: {hh_income_array.ndim}")
print(f"Shape of the array: {hh_income_array.shape}")
print(f"Number of elements: {hh_income_array.size}")


print(f"{'Percentile':<15}{'Income':>10}")
for row in hh_income_array:
    print(f"{int(row[0]):<15}{int(row[1]):>10}")
    