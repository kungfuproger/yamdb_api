from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from .validators import custom_year_validator


class Category(models.Model):
    """Модель категории произведения."""

    name = models.CharField(
        "название категории",
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        "slug категории",
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанра произведения."""

    name = models.CharField(
        "название жанра",
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        "slug жанра",
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        "название",
        max_length=200,
        unique=True,
    )
    year = models.PositiveIntegerField(
        "год выпуска",
        validators=(custom_year_validator,)
    )
    rating = models.IntegerField(
        "рейтинг",
        default=0,
    )
    description = models.TextField(
        "описание",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        default=None,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


# @receiver(post_save, sender="reviews.Review")
# @receiver(post_delete, sender="reviews.Review")
# def update_rating(instance, *args, **kwargs):
#     title = instance.title
#     reviews = title.reviews.all()
#     title.rating = reviews.aggregate(models.Avg("score")).get("score__avg")
#     title.save(update_fields=["rating"])
#     return title.rating


class Review(models.Model):
    """Модель отзыва."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
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
