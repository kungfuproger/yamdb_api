from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)
class User(AbstractUser):
    
    email = models.EmailField(
        blank=False, max_length=254, verbose_name="Email"
    )
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    role = models.CharField(choices=ROLES, max_length=20)
