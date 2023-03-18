import pathlib
import time

import django.db.models


class Contact(django.db.models.Model):
    email = django.db.models.EmailField(
        "почта", help_text="Ваша почта", max_length=150
    )

    class Meta:
        verbose_name = "контакты"
        verbose_name_plural = "контакты"


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
    contact = django.db.models.ForeignKey(
        Contact,
        on_delete=django.db.models.CASCADE,
        verbose_name=Contact._meta.verbose_name,
        related_name="feedbacks",
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


def get_file_media_path(instance, filename):
    creation_timestamp = int(time.time())
    filename = pathlib.Path(filename)
    basename, suffix = filename.stem, filename.suffix
    filename = f"{basename}_{creation_timestamp}{suffix}"
    media_path = pathlib.Path("uploads") / str(instance.feedback.id) / filename
    return media_path


class Attachment(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
        verbose_name=Feedback._meta.verbose_name,
        related_name="attachments",
    )
    file = django.db.models.FileField(
        "файл",
        upload_to=get_file_media_path,
        help_text="Прикрепите, если нужно, файлы",
    )

    def __str__(self):
        return self.text[:15]
