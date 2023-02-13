from unittest import skip

from django.test import Client, TestCase, override_settings
from django.urls import reverse


class HomePageTest(TestCase):
    """test homepage"""

    def test_endpoints_exists(self):
        """test if app endpoints response corresponding code"""
        for viewname, status_code in (("index", 200), ("coffee", 418)):
            with self.subTest(viewname=viewname, status_code=status_code):
                response = Client().get(reverse(viewname))
                self.assertEqual(response.status_code, status_code)

    def test_coffee_endpoint_response(self):
        """test if coffee endpoint responses Я чайник"""
        response = Client().get(reverse("coffee"))
        self.assertContains(response, "Я чайник", status_code=418)


class MiddlewareTest(TestCase):
    """test reverse middleware"""

    def test_reversing_every_n_request(self):
        """test if middleware reversing russian words after n requests"""
        n = 10
        client = Client()
        response = client.get("/")
        for _ in range(n - 1):
            response = client.get("/")
        self.assertContains(response, "Главная"[::-1])

    def test_reversing_multiple_words(self):
        """test if middleware reversing multiple
        russian words after n requests"""
        n = 10
        client = Client()
        response = client.get("/coffee", follow=True)
        for _ in range(n - 1):
            response = client.get("/coffee", follow=True)
        self.assertContains(response, "Я кинйач", status_code=418)

    @skip  # TODO
    def test_reversing_nothing(self):
        """test if middleware reversing none
        russian words after n requests"""

        n = 10
        client = Client()
        response = client.get("/")
        for _ in range(n - 1):
            response = client.get("/")
        self.assertContains(response, "")

    @skip  # TODO
    @override_settings(REVERSE_MIDDLEWARE=False)
    def test_disabling_middleware(self):
        """test if middleware could be disabed"""
        n = 10
        client = Client()
        response = client.get("/")
        for _ in range(n - 1):
            response = client.get("/")
        self.assertContains(response, "Главная")
