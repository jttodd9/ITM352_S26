#3. Write Python code that executes a for loop that examines every element of the tuple (“hello,” 10; “goodbye,” 3; “goodnight,” 5). Within the loop, use an if statement to count how many of the elements are strings. After the loop completes, print out a message stating how many strings are in the tuple.

greetings = (("hello", 10), ("goodbye", 3), ("goodnight", 5))
starting_count = 0
for item in greetings:
    if isinstance(item[0], str):  # Check if the first element of the tuple is a string
        starting_count += 1
print(f"There are {starting_count} strings in the tuple.")