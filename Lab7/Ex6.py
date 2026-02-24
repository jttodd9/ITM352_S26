greetings = (("hello", 10), ("goodbye", 3), ("goodnight", 5))

new_word = input("Enter a greeting word to add: ")
raw_count = input("Enter a number for that greeting: ")

try:
	new_count = int(raw_count)
	greetings_list = list(greetings)
	greetings_list.append((new_word, new_count))
	greetings = tuple(greetings_list)
except Exception:
	greetings_list = list(greetings)
	greetings_list.append((new_word, raw_count))
	greetings = tuple(greetings_list)

print(greetings)
