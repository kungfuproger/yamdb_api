from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Review(models.Model):
    """Модель отзыва."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    #    title = models.ForeignKey(
    #        Title,
    #        on_delete=models.CASCADE,
    #        related_name='reviews',
    #        verbose_name='Произведение',
    #    )
    text = models.TextField(
        "Отзыв",
    )
    score = models.IntegerField(
        "Оценка",
        help_text="Поставьте оценку от 1 до 10",
        validators=[MaxValueValidator(10), MinValueValidator(1)],
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.author} на произведение {self.title}"


class Comment(models.Model):
    """Модель кооментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="к этому отзыву",
    )
    text = models.TextField(
        "Комментарий",
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = "Комментарии"

    def __str__(self):
        review = str(self.review)[6:]
        return f"Комментарий {self.author} к отзыву {review}"
