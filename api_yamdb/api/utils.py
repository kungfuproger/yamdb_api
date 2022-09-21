import string
from random import choice, shuffle


def code_generator(length):
    """Возвращает код заданой длинны."""
    characters = list(string.ascii_lowercase + string.digits)
    shuffle(characters)
    code = []
    for i in range(length):
        code.append(choice(characters))
    shuffle(code)
    return "".join(code)
