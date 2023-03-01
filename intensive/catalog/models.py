import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe
from tinymce.models import HTMLField

import catalog.validators
import core.models


class Tag(core.models.CatalogCommon, core.models.CatalogGroupCommon):
    class Meta:
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
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(core.models.CatalogCommon):
    text = HTMLField(
        "описание",
        help_text="Введите описание объекта",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
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

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def image_tmb(self):
        if self.preview:
            thumbnail = self.preview.get_thumbnail()
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
        verbose_name = "фото"
        verbose_name_plural = "фотогалерея"

    def __str__(self):
        return self.image.url
