country_capitals = {
    "Germany": "Berlin",
    "Canada": "Ottawa",
    "England": "London",}

print(country_capitals)

# print(dictionary_name[key]) to access the value associated with a key The key could be anything even a string or a number
print(country_capitals["Canada"])

# Add a new key-value pair to the dictionary
country_capitals["Italy"] = "Rome"

print(country_capitals)

# Update the value associated with a key
country_capitals["Italy"] = "Milan"
print(country_capitals)

# Key word in and not in to check for existence of a key in a dictionary
print("Germany" in country_capitals)
print("Spain" not in country_capitals)
print("Korea" in country_capitals)