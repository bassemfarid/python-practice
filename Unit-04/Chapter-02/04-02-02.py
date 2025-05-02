total = 0
with open("Unit-04/Chapter-02/problem txt files/gme-buy.txt", "r") as files:
    for i in files:
        total+=(int(i.rstrip("\n")))
print(total)