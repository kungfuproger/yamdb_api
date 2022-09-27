from django.contrib.auth.tokens import PasswordResetTokenGenerator

CODE_EMAIL = "confirmation_code@yamdb.yandex"
from django.core.mail import send_mail


def code_sender(user):
    """Генерирует и отправляет код заданому юзеру."""
    code = PasswordResetTokenGenerator().make_token(user)
    send_mail(
        "Api_Yamdb confirmation_code",
        f"confirmation_code: {code}",
        CODE_EMAIL,
        [user.email],
        fail_silently=False,
    )
