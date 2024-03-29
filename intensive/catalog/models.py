import datetime
import random

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField

import catalog.validators
import core.models


class TagManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)


class Tag(core.models.CatalogCommon, core.models.CatalogGroupCommon):
    objects = TagManager()

    class Meta:
        ordering = ("slug",)
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(core.models.CatalogCommon, core.models.CatalogGroupCommon):
    # PositiveSmallIntegerField
    weight = django.db.models.IntegerField(
        "вес",
        help_text="Насколько весома категория",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        ordering = ("weight", "id")
        verbose_name = "категория"
        verbose_name_plural = "категории"


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .filter(category__is_published=True)
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags", queryset=Tag.objects.published().only("name")
                )
            )
        )

    def on_list(self):
        return (
            self.published()
            .order_by("category__name")
            .only("name", "category__name", "text", "tags__name")
        )

    def on_main_page(self):
        return (
            self.published()
            .filter(is_on_main=True)
            .only("name", "category__name", "text", "tags__name")
        )

    def detailed(self):
        return (
            self.published()
            .prefetch_related(
                django.db.models.Prefetch(
                    "gallery",
                    queryset=Gallery.objects.only("image"),
                )
            )
            .only(
                "name",
                "preview",
                "text",
                "category__name",
                "tags__name",
            )
        )

    def new(self):
        week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        limit = 5
        items_last_week = self.on_list().filter(
            creation_date__date__gte=week_ago
        )
        if not items_last_week:
            return items_last_week
        ids = items_last_week.values_list("id", flat=True)
        rand_ids = random.choices(ids, k=limit)
        rand_items = self.get_queryset().filter(id__in=rand_ids)
        return rand_items

    def friday(self):
        weekday = 6
        limit = 5
        return self.on_list().filter(update_date__week_day=weekday)[:limit]

    def unverified(self):
        return self.on_list().filter(
            django.db.models.Q(
                creation_date__lt=django.db.models.F("update_date")
                + datetime.timedelta(seconds=1)
            )
            & django.db.models.Q(
                update_date__lt=django.db.models.F("creation_date")
                + datetime.timedelta(seconds=1)
            )
        )


class Item(core.models.CatalogCommon):
    objects = ItemManager()

    text = HTMLField(
        "описание",
        help_text="Введите описание объекта",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
    )
    is_on_main = django.db.models.BooleanField(
        "на главной ли",
        help_text="Сделайте это поле положительным, "
        "если хотите видеть товар на главной странице",
        default=False,
    )

    category = django.db.models.ForeignKey(
        Category,
        verbose_name=Category._meta.verbose_name,
        help_text="Введите категорию",
        on_delete=django.db.models.CASCADE,
        related_name="catalog_items",
    )
    tags = django.db.models.ManyToManyField(
        Tag, verbose_name=Tag._meta.verbose_name
    )

    creation_date = django.db.models.DateTimeField(
        "дата создания", auto_now_add=True
    )
    update_date = django.db.models.DateTimeField(
        "дата изменения", auto_now=True
    )

    class Meta:
        ordering = ("name", "id")
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def image_tmb(self):
        if self.preview:
            thumbnail = self.preview.get_thumbnail("50x50")
            return mark_safe(f"<img src='{thumbnail.url}'>")

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class Preview(core.models.ImageCommon):
    item = django.db.models.OneToOneField(
        Item,
        verbose_name=Item._meta.verbose_name,
        help_text="Какому товару принадлежит превью",
        on_delete=django.db.models.CASCADE,
        related_name="preview",
    )

    class Meta:
        ordering = ("image",)
        verbose_name = "превью"
        verbose_name_plural = "превьюшки"

    def __str__(self):
        return self.image.url


class Gallery(core.models.ImageCommon):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name=Item._meta.verbose_name,
        help_text="Какому товару принадлежит фото",
        related_name="gallery",
    )

    class Meta:
        ordering = ("image",)
        verbose_name = "фото"
        verbose_name_plural = "фотогалерея"

    def __str__(self):
        return self.image.url
