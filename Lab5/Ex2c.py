trip_durations = [1.1, 0.8, 2.5, 2.6]
trip_fares = (6.25, 5.25, 10.50, 8.05)

# List of dictionaries where each dictionary represents a trip
trips = [
    {"duration": trip_durations[0], "fare": trip_fares[0]},
    {"duration": trip_durations[1], "fare": trip_fares[1]},
    {"duration": trip_durations[2], "fare": trip_fares[2]},
    {"duration": trip_durations[3], "fare": trip_fares[3]}
]
print("List of trip dictionaries:")
print(trips)
# Alternative: Create using zip
# trips = [{"duration": duration, "fare": fare} for duration, fare in zip(trip_durations, trip_fares)]

trip_num = input("What trip do you want to see? (1-4) ")
trip_index = int(trip_num) - 1
print(f"Duration: {trips[trip_index]['duration']} miles")
print(f"Fare: ${trips[trip_index]['fare']:.2f}")
