from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models

from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_rating(instance, *args, **kwargs):
    title = instance.title
    reviews = title.reviews.all()
    title.rating = reviews.aggregate(models.Avg("score")).get("score__avg")
    title.save(update_fields=["rating"])
    return title.rating
