def get_element(values, index):
    # Added bounds check to prevent IndexError for invalid indexes.
    if -len(values) <= index < len(values):
        return values[index]
    # Changed behavior: return a message instead of crashing.
    return "Index out of range"


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
# This call is intentionally out of range to show the safe handling.
print(get_element(my_list, 5)) 
