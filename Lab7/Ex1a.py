#Write Python code that uses a Python for-statement to create a list of elements that are the odd numbers between 1 and 50.

odd_numbers = []
for i in range(1, 51, 2):
    if i% 2 == 1:
        odd_numbers.append(i)

print(odd_numbers)