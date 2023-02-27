import catalog.validators

import core.models

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe

from django_resized import ResizedImageField

from tinymce.models import HTMLField


class Tag(core.models.CatalogCommon, core.models.CatalogGroupCommon):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(core.models.CatalogCommon, core.models.CatalogGroupCommon):
    # PositiveSmallIntegerField
    weight = django.db.models.IntegerField(
        "Вес",
        help_text="Насколько весома категория",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Item(core.models.CatalogCommon):
    text = HTMLField(
        "Описание",
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
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def image_tmb(self):
        if self.preview:
            return mark_safe(f"<img src='{self.preview.image.url}' width=50>")

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


class Preview(django.db.models.Model):
    image = ResizedImageField(
        "Превью",
        size=[300, 300],
        crop=["middle", "center"],
        upload_to="catalog/",
    )
    item = django.db.models.OneToOneField(
        Item,
        verbose_name=Item._meta.verbose_name,
        help_text="Какому товару принадлежит превью",
        on_delete=django.db.models.CASCADE,
        related_name="preview",
    )

    class Meta:
        verbose_name = "Превью"
        verbose_name_plural = "Превьюшки"

    def __str__(self):
        return self.image.url


class Gallery(django.db.models.Model):
    image = ResizedImageField(
        "Фото",
        size=[300, 300],
        crop=["middle", "center"],
        upload_to="catalog/",
    )
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        verbose_name=Item._meta.verbose_name,
        help_text="Какому товару принадлежит фото",
        related_name="gallery",
    )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотогалерея"

    def __str__(self):
        return self.image.url
