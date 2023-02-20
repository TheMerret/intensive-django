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

    class Meta:
        abstract = True
