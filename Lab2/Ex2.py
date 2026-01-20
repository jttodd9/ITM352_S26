# asks the user to enter their birth year then calculates age.
# name: Justin Todd
# date: Jan 20, 2026

birth_year = input("Please enter your birth year: ")
birth_year_int = int(birth_year)
current_year = 2026
age = current_year - birth_year_int
print(f"You are {age} years old.")