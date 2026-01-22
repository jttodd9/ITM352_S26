# Write Python code that uses the input built-in function to ask the user to enter a sentence of their choosing. Use the len built-in function to determine how many characters were in the string entered and report this information back to the user.
# asks the user to enter a sentence and reports the number of characters in it.
# name: Justin Todd
# date: Jan 22, 2026

print("Welcome to the program")
user_string = input("Please enter a sentence of your choosing: ")
string_length = len(user_string)
print(f"The sentence you entered has {string_length} characters.")
