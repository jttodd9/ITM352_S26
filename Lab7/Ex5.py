celebrities = (
	"Taylor Swift",
	"Lionel Messi",
	"The Weeknd",
	"Keanu Reeves",
	"Angelina Jolie",
)
ages = (36, 38, 36, 61, 50)

new_celebrity = input("Enter a celebrity name to add: ")
updated_celebrities = celebrities + (new_celebrity,)
print(updated_celebrities)

celebrity_data = {
	"celebrities": list(celebrities),
	"ages": list(ages),
}

print(celebrity_data)
