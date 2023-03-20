import datetime
from unittest import mock

import django.test
import django.urls
import django.utils.timezone

import users.models


@django.test.override_settings(IS_USER_ACTIVE=False)
class UserTest(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.signup_data = {
            "username": "test",
            "email": "test@yandex.ru",
            "password1": "Hardpwd1",
            "password2": "Hardpwd1",
        }
        return super().setUpTestData()

    def test_signup_activate(self):
        """test after signup user could be activated"""
        mocked_time = django.utils.timezone.localtime() - datetime.timedelta(
            hours=12
        )
        username = self.signup_data["username"]
        client = django.test.Client()
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=mocked_time)
        ):
            client.post(
                django.urls.reverse("users:signup"),
                data=self.signup_data,
                follow=True,
            )
            activate_link = django.urls.reverse(
                "users:activate", kwargs=dict(username=username)
            )
            response = client.get(activate_link)
        self.assertEqual(response.status_code, 200)
        user = users.models.User.objects.get(username=username)
        self.assertTrue(user.is_active)

    def test_signup_activate_delayed(self):
        """test after signup user couldn't be activated after 12 hours"""
        mocked_time = django.utils.timezone.localtime() - datetime.timedelta(
            hours=12, seconds=1
        )
        username = self.signup_data["username"]
        client = django.test.Client()
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=mocked_time)
        ):
            client.post(
                django.urls.reverse("users:signup"),
                data=self.signup_data,
                follow=True,
            )
            activate_link = django.urls.reverse(
                "users:activate", kwargs=dict(username=username)
            )
            response = client.get(activate_link)
        self.assertEqual(response.status_code, 410)
        user = users.models.User.objects.get(username=username)
        self.assertFalse(user.is_active)