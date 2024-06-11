import random
import string


def randomword(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))
