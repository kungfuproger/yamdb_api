from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


from users.models import User


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
#    title = models.ForeignKey(
#        Title,
#        on_delete=models.CASCADE,
#        related_name='reviews',
#        verbose_name='Произведение',
#    )
    text = models.TextField(
        'Отзыв',
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Поставьте оценку от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='к этому отзыву',
    )
    text = models.TextField(
        'Комментарий',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
