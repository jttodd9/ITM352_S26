#Create a list of lists with test cases for each possible condition. Use this list to test that the code behaves as expected. Tip: try asking ChatGPT to generate the test cases.

#create list of lists with test cases for each possible condition
list_of_lists = [
    [1, 2, 3],                # fewer than 5
    [1, 2, 3, 4, 5],          # between 5 and 10
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # between 5 and 10
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # more than 10
]

#allows the user to test their pick of list and see if the code behaves as expected
user_choice_of_list = int(input("Choose a list to test (1-4): "))

#tests the lists to see if they meet the conditions and prints the appropriate message
if len(list_of_lists[user_choice_of_list - 1]) < 5:
    print("The list contains fewer than 5 elements.")
elif 5 <= len(list_of_lists[user_choice_of_list - 1]) <= 10: 
    print("The list contains between 5 and 10 elements.")
else:
    print("The list contains more than 10 elements.")