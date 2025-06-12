msg = input()
keys = [int(input()) for _ in range(3)]

new_msg = ""

index = 0
for i in range(len(msg)):
    if msg[i] == " ":
        new_msg += " "
        continue
    if msg[i].isupper():
        new_msg += chr((ord(msg[i]) - ord('A') + keys[index%3]) % 26 + ord('A'))
        index += 1
    elif msg[i].islower():
        new_msg += chr((ord(msg[i]) - ord('a') + keys[index%3]) % 26 + ord('a'))
        index += 1
    else:
        new_msg += msg[i]

print(new_msg)