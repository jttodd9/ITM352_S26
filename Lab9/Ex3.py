# read the 1000 lines of taxi data from the taxi csv file
# calculate the total, average, and max trip distance

import csv

filename = "taxi_1000.csv"

with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    total_distance = 0.0
    max_distance = 0.0
    num_rows = 0

    next(reader)  # Skip the header row

    for line in reader:
        trip_distance = float(line[5])  # Trip Miles is the 6th column (index 5)
        total_distance += trip_distance
        if trip_distance > max_distance:
            max_distance = trip_distance
        num_rows += 1

    if num_rows > 0:
        average_distance = total_distance / num_rows

    print(f"Total Trip Distance: {total_distance:.2f}")
    print(f"Average Trip Distance: {average_distance:.2f}")
    print(f"Max Trip Distance: {max_distance:.2f}")

