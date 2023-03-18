import django.db.models


class Feedback(django.db.models.Model):
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

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратная связь"
