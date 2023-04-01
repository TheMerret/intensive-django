from django.db import models

from catalog.models import Item
from users.models import UserProxy


class RatingManager(models.Manager):
    def available(self):
        return (
            self.get_queryset()
            .select_related("user")
            .only("user__id", "score")
        )

    def statistic_list(self):
        return (
            self.get_queryset()
            .select_related("item")
            .only("item__name")
            .order_by("-score")
        )

    def statistic_detail(self):
        return (
            self.get_queryset()
            .select_related("user", "item")
            .only("score", "item__name", "user__username", "user__id")
        )


class ItemRating(models.Model):
    objects = RatingManager()

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
        ordering = ["-updated_at"]
        verbose_name = "оценка"
        verbose_name_plural = "оценки"
