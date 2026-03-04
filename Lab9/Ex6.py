# BUGGED CODE (notes)
# for x in range(10):
#     if x != 5:
#         print(x)
#         continue
#     if x == 8:
#         print("done!")
#         break
#
# Why it is bugged:
# 1) range(10) loops 0-9, but the requirement says 1-10.
# 2) if x != 5: continue runs for almost every value, so x == 8 check is never reached.



# Change 1: Use range(1, 11) to loop from 1 to 10.
# Change 2: Check x == 5 first, then continue to skip printing 5.
# Change 3: Check x == 8 before printing so the loop stops at 8 and prints "done!".
for x in range(1, 11):
    if x == 5:
        continue
    if x == 8:
        print("done!")
        break
    print(x)
