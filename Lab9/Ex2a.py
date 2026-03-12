#Use the Python csv module to load the CSV file and use the data to calculate the average, maximum, and minimum values for the Annual_Salary field. 

import csv

filename = "Employee_data.csv"

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile)
    salaries = [float(row["Annual_Salary"]) for row in reader]

average_salary = sum(salaries) / len(salaries)
max_salary = max(salaries)
min_salary = min(salaries)

print(f"Average Salary: {average_salary:.2f}")
print(f"Maximum Salary: {max_salary:.2f}")
print(f"Minimum Salary: {min_salary:.2f}")