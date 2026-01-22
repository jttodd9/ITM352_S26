# asks the user to enter a weight in pounds and converts it to kilograms.
# name: Justin Todd
# date: Jan 22, 2026

(lambda w: print(f"You entered: {round(w, 2)} pounds\nThe equivalent weight in kilograms is: {round(w * 0.453592, 2)} kg"))(float(input("Please enter a weight in pounds: ")))