import django.db.models


class Feedback(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        RECEIVED = "received", "получено"
        PROCESSING = "processing", "в обработке"
        ANSWERED = "answered", "ответ дан"

    text = django.db.models.TextField(
        "текст обратной связи",
        help_text="Что вы хотите сообщить нам",
    )
    created_on = django.db.models.DateTimeField(
        "дата создания", auto_now_add=True
    )
    email = django.db.models.EmailField(
        "почта", help_text="Ваша почта", max_length=150
    )
    status = django.db.models.CharField(
        "статус обработки",
        max_length=16,
        choices=Status.choices,
        default=Status.RECEIVED,
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"

    def __str__(self):
        return self.text[:15]
