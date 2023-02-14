from django.test import Client, TestCase
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
