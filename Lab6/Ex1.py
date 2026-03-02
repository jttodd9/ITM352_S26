# creates a tuple of emotions and checks if the last emotion is "happy" and if there is more than 3 emotions then prints if true or false

emotions = ("happy", "sad", "fear", "surprise")
condition = emotions[-1] == "happy" and len(emotions) > 3
print(condition)#should return false

