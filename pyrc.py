import random

# Generate a ciphertext alphabet.
alphabet = []
for i in range(65, 91):
    alphabet.append(chr(i))
random.shuffle(alphabet)

# Read the plaintext message.
input_file = open("message.txt", "r")
plaintext = input_file.read().upper()
input_file.close()

# Generate the ciphertext message.
ciphertext = ''
for plainchar in plaintext:
    if plainchar.isalpha():
        ciphertext = ciphertext + alphabet[ord(plainchar)-65]
    else:
        ciphertext = ciphertext + plainchar

print(ciphertext)
