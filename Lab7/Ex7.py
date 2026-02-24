for num in range(1, 11):
    if num == 5:
        continue
    if num == 8:
        print("Reached 8, stopping the loop.")
        break
    print(num)


new_list = [x for x in range(1, 1000) if x != 5 and x != 8 and x % 3 == 0]
print(new_list)