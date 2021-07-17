import random
import string


def create_confirmation_code(length=10):
    letters = string.printable
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
