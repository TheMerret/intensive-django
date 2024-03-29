import pathlib
import time

import django.core.exceptions
import django.db.models
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import ImageField

import core.utils


class CatalogCommon(django.db.models.Model):
    name = django.db.models.CharField(
        "имя", help_text="Назовите объект", max_length=150
    )
    is_published = django.db.models.BooleanField(
        "опубликовано", help_text="Опубликован ли объект", default=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class CatalogGroupCommon(django.db.models.Model):
    slug = django.db.models.SlugField(
        "строковый идентификатор",
        help_text="Человекопонятный URL для объекта",
        max_length=200,
        unique=True,
    )
    normilized_name = django.db.models.CharField(
        unique=True,
        editable=False,
        max_length=150,
    )

    class Meta:
        abstract = True

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.normilized_name = core.utils.normilize_name(self.name)
        return super().save(force_insert, force_update, using, update_fields)

    def validate_unique(self, exclude):
        self.normilized_name = core.utils.normilize_name(self.name)
        if (
            self._meta.model.objects.filter(
                normilized_name=self.normilized_name
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                {"name": "Похожее имя уже существует"}
            )
        return super().validate_unique(exclude)


def get_item_media_path(instance, filename):
    creation_timestamp = int(time.time())
    filename = pathlib.Path(filename)
    basename, suffix = filename.stem, filename.suffix
    filename = f"{basename}_{creation_timestamp}{suffix}"
    media_path = pathlib.Path("catalog") / str(instance.item.id) / filename
    return media_path


class ImageCommon(django.db.models.Model):
    image = ImageField(
        "фото",
        upload_to=get_item_media_path,
    )

    def get_thumbnail(self, size="300x300"):
        return get_thumbnail(self.image, size, crop="center", quality=51)

    class Meta:
        abstract = True

    def __str__(self):
        return self.image.url
