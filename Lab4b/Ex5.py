# Ask the user for a sentence using input and turn it into a list, reverse the list, join the reversed list back into a string

sentence = input("Enter a sentence: ")

# 1. turn string into a list of words
words_list = sentence.split(" ")
print("List of words:", words_list)

# 2. reverse the list
words_list.reverse()
print("Reversed list of words:", words_list)

# 3. join the reversed list back into a string
new_sentence = " ".join(words_list)
print("Reversed sentence:", new_sentence)
