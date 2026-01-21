#Ask the user for a number between 1 and 100 and print out the square of that number.
#name: Justin Todd
#date: Jan 20, 2026


print("Welcome to the program")
value_entered = input("Please enter a whole number between 1 and 100: ")
print(f"You entered: {value_entered}")

value_as_int = int(value_entered)
squared_value = value_as_int * value_as_int
if value_as_int < 1 or value_as_int > 100:
    print("The value entered is out of range.")
else:
    print(f"The square of {value_entered} is {squared_value}")