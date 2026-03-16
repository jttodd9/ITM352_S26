# Modify Ex3 to calculate total fares, average fare, and max trip distance
# for records with fares greater than $10

import csv

filename = "taxi_1000.csv"

with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    total_fares = 0.0
    max_distance = 0.0
    num_rows = 0

    next(reader)  # Skip the header row

    for line in reader:
        fare = float(line[10])  # Fare is the 11th column (index 10)
        if fare > 10:
            total_fares += fare
            trip_distance = float(line[5])  # Trip Miles is the 6th column (index 5)
            if trip_distance > max_distance:
                max_distance = trip_distance
            num_rows += 1

    if num_rows > 0:
        average_fare = total_fares / num_rows

    print(f"Total Fares (over $10): ${total_fares:.2f}")
    print(f"Average Fare (over $10): ${average_fare:.2f}")
    print(f"Max Trip Distance (fares over $10): {max_distance:.2f} miles")
