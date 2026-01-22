# Asks user to enter a temperature in Fahrenheit and converts it to Celsius in float format
# name: Justin Todd
# date: Jan 22, 2026

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5.0/9.0 
    

fahrenheit_input = input("Please enter a temperature in Fahrenheit: ")
fahrenheit_value = float(fahrenheit_input)
celsius_value = fahrenheit_to_celsius(fahrenheit_value)
print(f"The temperature in Celsius is: {round(celsius_value, 2)} °C")