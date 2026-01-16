def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y

if __name__ == '__main__':
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        operation = input("Choose operation (add, subtract, multiply, divide): ").strip().lower()

        if operation == 'add':
            print(f'Result: {add(num1, num2)}')
        elif operation == 'subtract':
            print(f'Result: {subtract(num1, num2)}')
        elif operation == 'multiply':
            print(f'Result: {multiply(num1, num2)}')
        elif operation == 'divide':
            print(f'Result: {divide(num1, num2)}')
        else:
            print("Invalid operation!")
    except ValueError as e:
        print(f'Error: {e}')