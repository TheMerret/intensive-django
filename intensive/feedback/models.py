import django.db.models


class Feedback(django.db.models.Model):
    class Status(django.db.models.TextChoices):
        RECEIVED = "received"
        PROCESSING = "processing"
        ANSWERED = "answered"

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
