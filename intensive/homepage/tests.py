from django.test import Client, TestCase


class HomePageTest(TestCase):
    """test homepage"""

    def test_homepage_endpoint_exists(self):
        """test if homepage endpoint responses 200"""
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
