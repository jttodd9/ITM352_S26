def fibonacci(values):
    # Added guard: prevents errors and returns 0 for an empty list.
    if not values:
        return 0

    # Changed setup: start total at the first list item.
    total = values[0]
    # Changed loop: add each remaining value to build the final total.
    for val in values[1:]:
        total = total + val
    # Returns the computed total.
    return total

my_list = [1, 2, 3, 4, 5]
# Test call for the updated function.
print(fibonacci(my_list)) 

