from django.db import models

from catalog.models import Item
from users.models import UserProxy


class ItemRating(models.Model):
    class Score(models.IntegerChoices):
        HATRED = 1, "ненависть"
        NEPRIYAZN = 2, "неприязнь"
        NEUTRAL = 3, "нейтрально"
        ADORATION = 4, "обожание"
        LOVE = 5, "любовь"

    user = models.ForeignKey(
        UserProxy,
        on_delete=models.CASCADE,
        related_name="item_rating",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="ratings",
    )
    score = models.SmallIntegerField(
        "оценка товара",
        choices=Score.choices,
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("updated_at", )
