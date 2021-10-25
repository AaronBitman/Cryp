import random

def violates_like_exclusion(alphabet, plaintext):
    """ Determine if a letter in the alphabet violates
        like-exclusion and if that letter is in the plaintext. """

    # First of all, we might not even WANT like-exclusion; if so, forget it.
    #return False
    # If we DO want like-exclusion, comment out the line above.

    # Now, loop through all the letters of the cipher
    # alphabet to check for a coinciding letter.
    for index, val in enumerate(alphabet):
        # If there is such a coincidence, see
        # if that letter is in the plaintext.
        if chr(index+65) == val:
            if val in plaintext:
                return True
    # Otherwise, we're good.
    return False

# Read the plaintext message.
input_file = open("message.txt", "r")
plaintext = input_file.read().upper()
input_file.close()

while True:
    # Generate a ciphertext alphabet.
    alphabet = []
    for i in range(65, 91):
        alphabet.append(chr(i))
    random.shuffle(alphabet)
    if not violates_like_exclusion(alphabet, plaintext):
        break

# Generate the ciphertext message.
ciphertext = ''
for plainchar in plaintext:
    if plainchar.isalpha():
        ciphertext = ciphertext + alphabet[ord(plainchar)-65]
    else:
        ciphertext = ciphertext + plainchar

print(ciphertext)
