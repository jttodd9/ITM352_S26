searchMe = [2, 5, 7, 11, 15, 22, 27, 30, 34, 41, 55, 57, 58, 60, 77]

target = int(input("Enter a number to search for: "))

found = False
for number in searchMe:
    if number == target:
        found = True
        break  # stop searching once found

if found:
    print(f"{target} was found in the array.")
else:
    print(f"{target} was NOT found in the array.")