from django.test import Client, TestCase, modify_settings
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


@modify_settings(
    MIDDLEWARE={
        "append": "intensive.middleware.ReverseMiddleware",
    }
)
class MiddlewareTest(TestCase):
    """test reverse middleware"""

    def test_reversing_words_every_n_request(self):
        """test if middleware reversing russian words after n requests"""
        n = 10
        for viewname, text, status_code in (
            ("index", "яанвалГ", 200),  # одно слово
            ("coffee", "Я кинйач", 418),  # несколько
        ):
            with self.subTest(
                viewname=viewname, text=text, status_code=status_code
            ):
                client = Client()
                response = client.get(reverse(viewname))
                for _ in range(n - 1):
                    response = client.get(reverse(viewname))
                print(response.content.decode())
                self.assertContains(response, text, status_code=status_code)

    @modify_settings(
        MIDDLEWARE={
            "remove": "intensive.middleware.ReverseMiddleware",
        }
    )
    def test_disabling_middleware(self):
        """test if middleware could be disabed"""
        n = 10
        client = Client()
        response = client.get(reverse("index"))
        for _ in range(n - 1):
            response = client.get(reverse("index"))
        self.assertContains(response, "Главная")
