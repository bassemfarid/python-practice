letter = input()
print(f"{letter}'s code point is {ord(letter)}")
print(f"before {letter} is {chr(ord(letter)-1)}, code point {ord(letter)-1}")
print(f"after {letter} is {chr(ord(letter)+1)}, code point {ord(letter)+1}")