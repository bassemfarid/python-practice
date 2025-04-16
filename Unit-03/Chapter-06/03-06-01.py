ASCII_OFFSET_CAP = 64
msg = input()
key = int(input())
encrypted = ""

for each in msg:
    if each == " ":
        encrypted += " "
        continue
    if (ord(each) - ASCII_OFFSET_CAP + key) % 26 == 0:
        encrypted += chr(ASCII_OFFSET_CAP + 26)
    else:
        encrypted += chr((ord(each) - ASCII_OFFSET_CAP + key) % 26 + ASCII_OFFSET_CAP)

print(encrypted)