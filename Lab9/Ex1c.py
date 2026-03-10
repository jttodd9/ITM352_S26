# Open the file names.txt and read it's contents and print number of names

file_object = open("names.txt")
contents = file_object.read()
print(contents)
file_object.close()
print(f"Number of names: {len(contents.splitlines())}")