species = {}
with open("Unit-04/Chapter-02/problem txt files/bird-store.txt", "r") as files:
    for i in files:
        i = i.rstrip("\n")
        if i not in species:
            species[i] = 1
        else:
            species[i] += 1
print(str(species["chicken"]) + ", " + str(species["goose"]) + ", " + str(species["dodo"]) + ", " + str(species["ostrich"]) + ", " + str(species["parrot"]))