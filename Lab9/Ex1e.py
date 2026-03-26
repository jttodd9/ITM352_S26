# Open the file names.txt and read it's contents and print the number of names

with open("names.txt") as file_object:
    contents_list = file_object.readlines()

print(contents_list)
print(f"Number of names: {len(contents_list)}")