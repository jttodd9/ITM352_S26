health = 100

while health > 0:
    print("Current health:", health)
    damage = int(input("Enter damage taken: "))
    health -= damage

print("Game Over!")
