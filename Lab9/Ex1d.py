#Open a file names.txt and read it's contents and print the number of names

with open("names.txt") as file_object:
    while (line := file_object.readline()):
        print(line.strip())

