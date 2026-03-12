#Look up the documentation on this package and use it to open the file only if it exists and is readable and print out some file information such as size.


import csv
import os

Employee_data_file = "Employee_data.csv"

#File Size (in bytes)
if os.path.exists(Employee_data_file):
    file_size = os.path.getsize(Employee_data_file)
    print(f"File Size: {file_size} bytes")
else:
    print("File does not exist or is not readable.")