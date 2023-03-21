import pathlib
import time

from django.contrib.auth.models import User, UserManager
from django.db import models
import sorl.thumbnail


class UserProfileManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("profile")
            .filter(is_active=True)
        )


class UserProxy(User):
    object = UserProfileManager()

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
