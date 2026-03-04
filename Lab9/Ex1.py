
# Debugged Version
product = {
    "name": 'small gumball', 
    "price": 0.34  # Changed from string to float
}

tax_rate = 0.045

total = product["price"] + product["price"] * tax_rate

print(f"A {product['name']} costs ${total:.2f}")  # Accessed name using dictionary key and formatted total to 2 decimal places