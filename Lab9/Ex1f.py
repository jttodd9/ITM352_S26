#Now add your own name to the end of the file and print the entire contents of the file. ​​What steps are necessary to ensure that the new name is added to the end of the file without losing the existing names? Discuss the pros and cons of appending the file versus overwriting the file.

with open("names.txt") as file_object:
    contents_list = file_object.readlines()

print(contents_list)


with open("names.txt", "a") as file_object:  # "a" mode opens the file for appending
    print("Appending a new name to the file...")
    file_object.write("Todd, Justin\n")  # Replace "Your Name" with your actual 
    contents_list.append("Todd, Justin\n")  # Add the new name to the list for printing
    print(f"Number of names: {len(contents_list)}")