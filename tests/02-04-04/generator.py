number = int(input())
if not number % 3:
    print("Fizz Buzz" if not number % 5 else "Fizz")
elif not number % 5:
    print("Buzz")
else: print(number)