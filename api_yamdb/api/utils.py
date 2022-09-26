import string
from random import choice, shuffle

from django.core.mail import send_mail


CODE_EMAIL = "confirmation_code@yamdb.yandex"


def code_generator(length):
    """Возвращает код заданой длинны."""
    characters = list(string.ascii_lowercase + string.digits)
    shuffle(characters)
    code = []
    for i in range(length):
        code.append(choice(characters))
    shuffle(code)
    return "".join(code)


def code_sender(user):
    """Генерирует и отправляет код заданому юзеру."""
    code = code_generator(10)
    user.confirmation_code = code
    user.save()

    send_mail(
        "Api_Yamdb confirmation_code",
        f"confirmation_code: {code}",
        CODE_EMAIL,
        [user.email],
        fail_silently=False,
    )
