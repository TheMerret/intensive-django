from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

import users.models


class AuthenticationEmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()  # noqa:N806
        if username is None or password is None:
            return
        email = username
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, "is_active", False) and user.check_password(
                password
            ):
                return user
        return

    def get_user(self, user_id):
        try:
            return users.models.UserProxy.objects.get(pk=user_id)
        except users.models.UserProxy.DoesNotExist:
            return None
