num = int(input())
for i in range(num, 0, -1):
    print(" " * (2 * abs(num-i)), end="")
    for j in range(1, i):
        print(j, end=" ")
    print(i, end="")
    for j in range(i-1, 0, -1):
        print("", j, end="")
    print("")