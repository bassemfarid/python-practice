lists = []
with open("Unit-04/Chapter-02/problem txt files/pizza-toppings.txt", "r") as files:
    for i in files:
        lists.append(i.rstrip("\n"))
lists.sort()
for i in lists:
    print(i)