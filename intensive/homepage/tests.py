from django.test import Client, TestCase


class HomePageTest(TestCase):
    """test homepage"""

    def test_homepage_endpoint_exists(self):
        """test if homepage endpoint responses 200"""
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_endpoint_exists(self):
        """test if coffee endpoint responses 418"""
        response = Client().get("/coffee/")
        self.assertEqual(response.status_code, 418)

    def test_coffee_endpoint_response(self):
        """test if coffee endpoint responses Я чайник"""
        response = Client().get("/coffee/")
        self.assertContains(response, "Я чайник", status_code=418)
