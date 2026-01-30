import os
import sys

# Ensure this file's folder is on the import path
sys.path.append(os.path.dirname(__file__))

import HandyMath
from HandyMath import max, min
from Ex2 import midpoint
from Ex3 import square_root

num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

mid = midpoint(num1, num2)
root_of_square = square_root(num1 ** 2)
exp_result = HandyMath.exponent(num1, num2)
max_value = max(num1, num2)
min_value = min(num1, num2)

print(f"Midpoint of {num1} and {num2} is {mid}")
print(f"Square root of {num1} squared is {root_of_square}")
print(f"{num1} raised to the power of {num2} is {exp_result}")
print(f"Max of {num1} and {num2} is {max_value}")
print(f"Min of {num1} and {num2} is {min_value}")
