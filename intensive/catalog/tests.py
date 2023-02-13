from django.test import Client, TestCase
from django.urls import reverse


class CatalogPageTest(TestCase):
    """test catalog page"""

    def test_catalog_endpoint_exists(self):
        """test if catalog endpoint responses 200"""
        response = Client().get(reverse("item-list"))
        self.assertEqual(response.status_code, 200)

    def test_item_detail_endpoint_exists(self):
        """test if catalog item detail endpoint responses 200"""
        response = Client().get(reverse("item-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
