from django.test import Client, TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


class CatalogPageTest(TestCase):
    """test catalog page"""

    def test_endpoints_exists(self):
        """test if app endpoints response 200 code"""
        for viewname, args in (
            ("item-list", []),
            ("item-detail", [1]),
            ("re-item-detail", [1]),
            ("converter-item-detail", [1]),
        ):
            with self.subTest(viewname=viewname, args=args):
                response = Client().get(reverse(viewname, args=args))
                self.assertEqual(response.status_code, 200)

    def test_catalog_item_id_wrong_values(self):
        """test if catalog item detail
        doesn't accept wrong values as id"""
        # we don't test item-detail cause it uses django implementation
        for viewname in ("re-item-detail", "converter-item-detail"):
            for args in (["hello"], [-1], [0]):
                with self.subTest(viewname=viewname, args=args):
                    self.assertRaises(
                        NoReverseMatch, reverse, viewname, args=args
                    )
