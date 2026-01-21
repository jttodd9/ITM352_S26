# Expressions Tutorial
# Justin Todd
# Date: Jan 21, 2026

print("Hello, Today I will help you create a professional email address!")
name = input("Please enter your first and last name: ")
major = input("Please enter your major (e.g., Computer Science): ")
grad_year = input("Please enter your graduation year (e.g., 2026): ")
name_parts = name.split()
first_name = name_parts[0].lower()
last_name = name_parts[-1].lower()
email_address = f"{first_name}.{last_name}.{major.replace(' ', '').lower()}{grad_year}@university.edu"
print(f"Your professional email address is: {email_address}")




