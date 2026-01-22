#  Modify the code in Exercise 2.3 to round the values reported to the user to two decimal places (use the round built-in function).
# asks the user to enter a value 1-100 with a decimal and convets the input to a float then squares it. Uses the round function to limit decimal places.
# name: Justin Todd
# date: Jan 22, 2026

print("Welcome to the program")
value_entered = input("Please enter a number between 1 and 100 (decimals allowed): ")
# Converting the input to a float
value_as_float = float(value_entered)
# Displaying the entered value
print(f"You entered: {round(value_as_float, 2)}")
# Squaring the value
squared_value = value_as_float ** 2
# Making sure the value is within range to continue operations
if value_as_float < 1 or value_as_float > 100:
    print("The value entered is out of range.")
else:
    print(f"The square of {round(value_as_float, 2)} is {round(squared_value, 2)}")