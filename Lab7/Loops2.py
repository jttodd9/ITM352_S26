prices = [100, 50 , 20, 356]

total = 0
item_count = 0


for price in prices:
    item_count += 1
    if item_count > 2:
        discounted_price = price * 0.9 # Apply a 10% discount to each price after the second item
    else:
        discounted_price = price # Apply no discount to the first two items
    total += discounted_price

rounded_total = round(total, 2) # Round the total to 2 decimal places
print(f"Total price = {rounded_total:.2f}")