def multiply(first_num, second_num):
    # Change 1: Start at 0 and use repeated addition to compute multiplication.
    product = 0

    # Change 2: Use a separate loop variable so function parameters are not overwritten.
    for _ in range(second_num):
        product += first_num

    # Change 3: Return the computed product (not the input value).
    return product


# Change 4: Convert input strings to integers before math.
first = int(input("Enter the first number: "))
second = int(input("Enter the second number: "))
prod = multiply(first, second)

print(f"The product of {first}, {second} is {prod}")
