i = int(input())
num = 2
prime = True
while num <= i**(1/2) and i != 1:
    if i % num == 0: prime = False
    num+=1
print(prime)