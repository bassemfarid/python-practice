num = int(input())
for i in range(num, 0, -1):
    for j in range(i, 0, -1):
        if i == j: print(j, end="")
        else: print("", j, end="")
    print("")