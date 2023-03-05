from django.test import Client, TestCase
from django.urls import reverse


class AboutPageTest(TestCase):
    """test about page"""

    def test_about_endpoint_exists(self):
        """test if about endpoint responses 200"""
        response = Client().get(reverse("about:about"))
        self.assertEqual(response.status_code, 200)
