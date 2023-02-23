import core.utils

import django.core.exceptions
import django.db.models


class CatalogCommon(django.db.models.Model):
    name = django.db.models.CharField(
        "Имя", help_text="Назовите объект", max_length=150
    )
    is_published = django.db.models.BooleanField(
        "Опубликовано", help_text="Опубликован ли объект", default=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class CatalogGroupCommon(django.db.models.Model):
    slug = django.db.models.SlugField(
        "Строковый идентификатор",
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
        if self._meta.model.objects.filter(
            normilized_name=self.normilized_name
        ).exists():
            raise django.core.exceptions.ValidationError(
                {"name": "Похожее имя уже существует"}
            )
        return super().validate_unique(exclude)
