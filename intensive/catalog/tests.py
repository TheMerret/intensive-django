from django.test import Client, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


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

    def test_re_item_detail_endpoint_exists(self):
        """test if catalog item detail with regex endpoint responses 200"""
        response = Client().get(reverse("re-item-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_re_item_detail_string(self):
        """test if catalog item detail with regex
        doesn't accept strings"""
        self.assertRaises(
            NoReverseMatch, reverse, "re-item-detail", args=["hello"]
        )

    def test_re_item_detail_negative_number(self):
        """test if catalog item detail with regex
        doesn't accept nigative numbers"""
        self.assertRaises(NoReverseMatch, reverse, "re-item-detail", args=[-1])

    def test_re_item_detail_zero(self):
        """test if catalog item detail with regex
        doesn't accept zero"""
        self.assertRaises(NoReverseMatch, reverse, "re-item-detail", args=[0])

    def test_converter_item_detail_endpoint_exists(self):
        """test if catalog item detail with converter endpoint
        responses 200"""
        response = Client().get(reverse("converter-item-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_converter_item_detail_string(self):
        """test if catalog item detail with regex
        doesn't accept strings"""
        self.assertRaises(
            NoReverseMatch, reverse, "converter-item-detail", args=["hello"]
        )

    def test_converter_item_detail_negative_number(self):
        """test if catalog item detail with coonverter
        doesn't accept nigative numbers"""
        self.assertRaises(
            NoReverseMatch, reverse, "converter-item-detail", args=[-1]
        )

    def test_converter_item_detail_zero(self):
        """test if catalog item detail with coonverter
        doesn't accept zero"""
        self.assertRaises(
            NoReverseMatch, reverse, "converter-item-detail", args=[0]
        )
