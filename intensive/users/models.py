import pathlib
import time

from django.contrib.auth.models import User, UserManager
from django.db import models
import django.utils.timezone
import sorl.thumbnail

import users.utils


class UserProfileManager(UserManager):
    @classmethod
    def normalize_email(cls, email):
        email = users.utils.normilize_email(email)
        return email

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("profile")
            .filter(is_active=True)
        )

    def birthdays(self):
        today = django.utils.timezone.localtime().date()
        return (
            self.get_queryset()
            .select_related("profile")
            .filter(
                profile__birthday__day=today.day,
                profile__birthday__month=today.month,
            )
            .only("profile__birthday", "username", "email")
        )

    def list_users(self):
        return (
            self.get_queryset()
            .select_related("profile")
            .only("username", "date_joined", "profile__id")
        )


class UserProxy(User):
    objects = UserProfileManager()

    class Meta:
        proxy = True


def get_user_media_path(instance, filename):
    creation_timestamp = int(time.time())
    filename = pathlib.Path(filename)
    basename, suffix = filename.stem, filename.suffix
    filename = f"{basename}_{creation_timestamp}{suffix}"
    media_path = pathlib.Path("users") / str(instance.user.id) / filename
    return media_path


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    birthday = models.DateField("дата рождения", blank=True, null=True)
    image = sorl.thumbnail.ImageField(
        "фото", upload_to=get_user_media_path, blank=True, null=True
    )
    coffee_count = models.PositiveIntegerField(
        "количество выпитых кофе", default=0
    )

    def get_thumbnail(self):
        if self.image:
            return sorl.thumbnail.get_thumbnail(
                self.image, "300x300", crop="center", quality=51
            )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"
