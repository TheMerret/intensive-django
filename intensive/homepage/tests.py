import django.test
from django.urls import reverse


class HomePageTest(django.test.TestCase):
    """test homepage"""

    def test_endpoints_exists(self):
        """test if app endpoints response corresponding code"""
        for viewname, status_code in (
            ("homepage:index", 200),
            ("homepage:coffee", 418),
        ):
            with self.subTest(viewname=viewname, status_code=status_code):
                response = django.test.Client().get(reverse(viewname))
                self.assertEqual(response.status_code, status_code)

    def test_coffee_endpoint_response(self):
        """test if coffee endpoint responses Я чайник"""
        response = django.test.Client().get(reverse("homepage:coffee"))
        self.assertContains(response, "Я чайник", status_code=418)


@django.test.override_settings(REVERSE_REQUEST_COUNT=10)
class MiddlewareTest(django.test.TestCase):
    """test reverse middleware"""

    def test_reversing_words_every_n_request(self):
        """test if middleware reversing russian words after n requests"""
        n = 10
        for viewname, text, status_code in (
            ("homepage:index", "яанвалГ", 200),  # одно слово
            ("homepage:coffee", "Я кинйач", 418),  # несколько
        ):
            with self.subTest(
                viewname=viewname, text=text, status_code=status_code
            ):
                client = django.test.Client()
                response = client.get(reverse(viewname))
                for _ in range(n - 1):
                    response = client.get(reverse(viewname))
                self.assertContains(response, text, status_code=status_code)

    @django.test.override_settings(REVERSE_REQUEST_COUNT=0)
    def test_disabling_middleware(self):
        """test if middleware could be disabed"""
        n = 10
        client = django.test.Client()
        response = client.get(reverse("homepage:index"))
        for _ in range(n - 1):
            response = client.get(reverse("homepage:index"))
        self.assertContains(response, "Главная")
