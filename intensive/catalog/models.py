import catalog.validators

import core.models

import django.core.validators
import django.db.models
from django.utils.safestring import mark_safe

from sorl.thumbnail import get_thumbnail


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
    text = django.db.models.TextField(
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


class ItemPreview(django.db.models.Model):
    image = django.db.models.ImageField(
        "Будет приведено к ширине x1280", upload_to="catalog/"
    )

    def get_image_x1280(self):
        return get_thumbnail(self.image, "1280", quality=51)

    def get_image_300x400(self):
        return get_thumbnail(self.image, "400x300", crop="center", quality=51)
    
    def image_tmb(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.image.url}' width=50>"
            )
    
    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True