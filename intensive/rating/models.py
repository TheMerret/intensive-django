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
        verbose_name="пользователь",
        help_text="Кто написал отзыв",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="товар",
        help_text="Товар для которого предназначен отзыва",
    )
    score = models.SmallIntegerField(
        choices=Score.choices,
        verbose_name="оценка товара",
        help_text="Насколько вы оцениваете товар",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
