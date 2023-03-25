import datetime
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.db import transaction
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

        cls.user = User.objects.create_user(
            username="testuser",
            email="testuser@yandex.ru",
            password="testpswd",
            is_active=True,
        )
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

    def test_login_username(self):
        """test can login with username"""
        login_data = {"username": self.user.username, "password": "testpswd"}
        client = django.test.Client()
        client.post(django.urls.reverse("users:login"), data=login_data)
        user = get_user(client)
        self.assertTrue(user.is_authenticated)

    def test_login_email(self):
        """test can login with username"""
        login_data = {"username": self.user.email, "password": "testpswd"}
        client = django.test.Client()
        client.post(django.urls.reverse("users:login"), data=login_data)
        user = get_user(client)
        self.assertTrue(user.is_authenticated)

    def test_email_normalization(self):
        """test user email is normilized"""
        for email, normilized_email in (
            ("someone+sometag+another@example.com", "someone@example.com"),
            ("someone@ya.ru", "someone@yandex.ru"),
            ("SomeOne@MaIL.rU", "someone@mail.ru"),
            ("some.test@gmail.com", "sometest@gmail.com"),
            ("some.test@yandex.ru", "some-test@yandex.ru"),
        ):
            with self.subTest(email=email, normilized_email=normilized_email):
                with transaction.atomic():
                    user = users.models.UserProxy.objects.create_user(
                        username="test", email=email, password="testpswd"
                    )
                self.assertEqual(user.email, normilized_email)
                user.delete()

    def test_ban_on_too_many_fails(self):
        """test user couldn't login affter too many failed attempts"""
        max_attempts = settings.AXES_FAILURE_LIMIT
        client = django.test.Client()
        login_data = {"username": self.user.username, "password": "wrongpswd"}
        for _ in range(max_attempts - 1):
            resp = client.post(
                django.urls.reverse("users:login"), data=login_data
            )
            self.assertEqual(resp.status_code, 200)
        resp = client.post(django.urls.reverse("users:login"), data=login_data)
        self.assertEqual(resp.status_code, 403)
        self.assertFalse(
            User.objects.get(username=self.user.username).is_active
        )

    @mock.patch("users.lockout.send_reactivate_email")
    def test_reactivate_after_ban(self, mock_reactivate_email):
        """test user could reactivate accout after login too many attempts"""
        mocked_time = django.utils.timezone.localtime() - datetime.timedelta(
            days=6
        )
        max_attempts = settings.AXES_FAILURE_LIMIT
        client = django.test.Client()
        login_data = {"username": self.user.username, "password": "wrongpswd"}
        with mock.patch(
            "django.utils.timezone.localtime",
            mock.Mock(return_value=mocked_time),
        ):
            for _ in range(max_attempts):
                client.post(
                    django.urls.reverse("users:login"), data=login_data
                )
        reactivate_url = mock_reactivate_email.call_args.args[2]
        client.get(reactivate_url)
        self.assertTrue(
            User.objects.get(username=self.user.username).is_active
        )

    @mock.patch("users.lockout.send_reactivate_email")
    def test_reactivate_delayed_after_ban(self, mock_reactivate_email):
        """test user couldn't reactivate accout after login
        with too many attempts after week"""
        mocked_time = django.utils.timezone.localtime() - datetime.timedelta(
            days=8
        )
        max_attempts = settings.AXES_FAILURE_LIMIT
        client = django.test.Client()
        login_data = {"username": self.user.username, "password": "wrongpswd"}
        with mock.patch(
            "django.utils.timezone.localtime",
            mock.Mock(return_value=mocked_time),
        ):
            for _ in range(max_attempts):
                client.post(
                    django.urls.reverse("users:login"), data=login_data
                )
        reactivate_url = mock_reactivate_email.call_args.args[2]
        resp = client.get(reactivate_url)
        self.assertEqual(resp.status_code, 401)
        self.assertFalse(
            User.objects.get(username=self.user.username).is_active
        )
