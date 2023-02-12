from django.test import Client, TestCase


class CatalogPageTest(TestCase):
    """test catalog page"""

    def test_catalog_endpoint_exists(self):
        """test if catalog endpoint responses 200"""
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_item_detail_endpoint_exists(self):
        """test if catalog item detail endpoint responses 200"""
        response = Client().get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

    def test_re_item_detail_endpoint_exists(self):
        """test if catalog item detail with regex endpoint responses 200"""
        response = Client().get("/catalog/re/1/")
        self.assertEqual(response.status_code, 200)

    def test_re_item_detail_string(self):
        """test if catalog item detail with regex
         doesn't accept strings"""
        response = Client().get("/catalog/re/hello/")
        self.assertEqual(response.status_code, 404)

    def test_re_item_detail_negative_number(self):
        """test if catalog item detail with regex
         doesn't accept nigative numbers"""
        response = Client().get("/catalog/re/-1/")
        self.assertEqual(response.status_code, 404)

    def test_re_item_detail_zero(self):
        """test if catalog item detail with regex
         doesn't accept zero"""
        response = Client().get("/catalog/re/0/")
        self.assertEqual(response.status_code, 404)

    def test_converter_item_detail_endpoint_exists(self):
        """test if catalog item detail with coonverter endpoint
         responses 200"""
        response = Client().get("/catalog/converter/1/")
        self.assertEqual(response.status_code, 200)

    def test_converter_item_detail_string(self):
        """test if catalog item detail with regex
         doesn't accept strings"""
        response = Client().get("/catalog/converter/hello/")
        self.assertEqual(response.status_code, 404)

    def test_converter_item_detail_negative_number(self):
        """test if catalog item detail with coonverter
         doesn't accept nigative numbers"""
        response = Client().get("/catalog/converter/-1/")
        self.assertEqual(response.status_code, 404)

    def test_converter_item_detail_zero(self):
        """test if catalog item detail with coonverter
         doesn't accept zero"""
        response = Client().get("/catalog/converter/0/")
        self.assertEqual(response.status_code, 404)
