from unittest import skip

from django.test import Client
from django.test import TestCase
from django.urls import reverse
import django.urls.exceptions

import catalog.models


class CatalogPageViewsTest(TestCase):
    """test catalog page views"""

    fixtures = ["catalog.json"]

    def test_endpoints_exists(self):
        """test if app endpoints response 200 code"""
        for viewname, args in (
            ("catalog:item-list", []),
            ("catalog:item-detail", [1]),
            ("catalog:re-item-detail", [1]),
            ("catalog:converter-item-detail", [1]),
        ):
            with self.subTest(viewname=viewname, args=args):
                response = Client().get(reverse(viewname, args=args))
                self.assertEqual(response.status_code, 200)

    def test_catalog_item_id_wrong_values(self):
        """test if catalog item detail
        doesn't accept wrong values as id"""
        # we don't test item-detail cause it uses django implementation
        for viewname in (
            "catalog:re-item-detail",
            "catalog:converter-item-detail",
        ):
            for args in (["hello"], [-1], [0], [3.14]):
                with self.subTest(viewname=viewname, args=args):
                    self.assertRaises(
                        django.urls.exceptions.NoReverseMatch,
                        reverse,
                        viewname,
                        args=args,
                    )

    def test_item_list_context_has_correct_key(self):
        """test item detail context has correct key"""
        response = Client().get(reverse("catalog:item-list"))
        self.assertIn("items", response.context)

    def test_item_detail_context_has_correct_key(self):
        """test item detail context has correct key"""
        response = Client().get(reverse("catalog:item-detail", args=[1]))
        self.assertIn("item", response.context)

    def test_item_list_context_cout_item(self):
        """test catalog item list shows context with correct number of items"""
        response = django.test.Client().get(reverse("catalog:item-list"))
        items = response.context["items"]
        self.assertEqual(items.count(), 3)

    def test_item_detail_context_has_correct_model(self):
        """test item detail context has correct model"""
        response = Client().get(reverse("catalog:item-detail", args=[1]))
        self.assertIsInstance(response.context["item"], catalog.models.Item)

    def test_catalog_item_list_context_has_only_necessary_fields(self):
        """test catalog item list context has only necessary fields in item"""
        response = django.test.Client().get(reverse("catalog:item-list"))
        items = response.context["items"]
        necessary_fields = {
            catalog.models.Category: {"id", "name"},
            catalog.models.Item: {
                "text",
                "tags",
                "name",
                "category_id",
                "id",
            },
            catalog.models.Tag: {"id", "name"},
        }
        loaded_fields = items.query.get_loaded_field_names()
        self.assertEqual(loaded_fields, necessary_fields)

    def test_catalog_item_detail_context_item_has_only_necessary_fields(self):
        """test catalog item detail context item has only necessary fields"""
        item_necessary_fields = {"id", "name", "text", "category_id"}
        item_extra_fields = {"is_on_main", "image", "is_published"}

        response = django.test.Client().get(
            reverse("catalog:item-detail", args=[1])
        )
        item = response.context["item"]

        for f in item_necessary_fields:
            self.assertIn(f, item.__dict__)
        for f in item_extra_fields:
            self.assertNotIn(f, item.__dict__)

    def test_catalog_category_detail_context_item_has_only_necessary_fields(
        self,
    ):
        """test catalog item detail context category has only necessary
        fields"""
        category_necessary_fields = {"id", "name"}
        category_extra_fields = {
            "is_published",
            "weight",
            "slug",
            "normilized_name",
        }

        response = django.test.Client().get(
            reverse("catalog:item-detail", args=[1])
        )
        item = response.context["item"]
        category = item.category
        for f in category_necessary_fields:
            self.assertIn(f, category.__dict__)
        for f in category_extra_fields:
            self.assertNotIn(f, category.__dict__)

    def test_catalog_tag_detail_context_item_has_only_necessary_fields(
        self,
    ):
        """test catalog item detail context tag has only necessary
        fields"""
        tag_necessary_fields = {"id", "name"}
        tag_extra_fields = {"is_published", "slug", "normilized_name"}

        response = django.test.Client().get(
            reverse("catalog:item-detail", args=[1])
        )
        item = response.context["item"]
        tag = item.tags.first()
        for f in tag_necessary_fields:
            self.assertIn(f, tag.__dict__)
        for f in tag_extra_fields:
            self.assertNotIn(f, tag.__dict__)

    def test_catalog_gallery_detail_context_item_has_only_necessary_fields(
        self,
    ):
        """test catalog item detail context gallery has only necessary
        fields"""
        gallery_necessary_fields = {"image", "item_id"}

        response = django.test.Client().get(
            reverse("catalog:item-detail", args=[1])
        )
        item = response.context["item"]
        gallery = item.gallery
        for f in gallery_necessary_fields:
            self.assertNotIn(f, gallery.__dict__)


class ModelTest(TestCase):
    """test catalog models"""

    fixtures = ["catalog.json"]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.category = catalog.models.Category.objects.first()
        cls.tag = catalog.models.Tag.objects.first()
        cls.abiguous_category = catalog.models.Category(
            name="ПРИВЕТ",
            is_published=True,
            slug="hello-slug",
            weight=200,
        )
        cls.abiguous_category.save()
        cls.abiguous_tag = catalog.models.Tag(
            name="ПРИВЕТ",
            is_published=True,
            slug="hello-slug",
        )
        cls.abiguous_tag.save()

    def setUp(self):
        super().setUp()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            text="превосходно",
            is_published=True,
            category=ModelTest.category,
        )
        self.tag = catalog.models.Tag(
            name="Тестовый тег",
            is_published=True,
            slug="test-tag-slug",
        )
        self.category = catalog.models.Category(
            name="Тестовый тег",
            is_published=True,
            slug="test-tag-slug",
            weight=200,
        )

    def test_create_item_excellently_luxurious(self):
        """test if item could be created if data is valid"""
        for text in ("превосходно", "роскошно"):
            item_count = catalog.models.Item.objects.count()
            with self.subTest(text=text):
                item = catalog.models.Item.objects.create(
                    name="Тестовый товар",
                    text="превосходно",
                    is_published=True,
                    category=ModelTest.category,
                )
                item.tags.add(ModelTest.tag)
                item.full_clean()
                item.save()
                self.assertEqual(
                    catalog.models.Item.objects.count(), item_count + 1
                )

    def test_create_tag_with_valid_data(self):
        """test if tag could be created if data is valid"""
        tag_count = catalog.models.Tag.objects.count()

        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

    def test_create_category_with_valid_data(self):
        """test if category could be created if data is valid"""
        category_count = catalog.models.Category.objects.count()

        self.category.full_clean()
        self.category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(), category_count + 1
        )

    @skip
    def test_wrong_id_for_objects(self):
        """test if wrong ids for objects couldn't be passed"""
        for obj in (self.item, self.tag, self.category):
            for id_ in (0, -1):
                with self.subTest(obj=obj, id_=id_):
                    obj_count = obj.__class__.objects.count()
                    obj.id = id_
                    with self.assertRaises(
                        django.core.exceptions.ValidationError
                    ):
                        obj.full_clean()
                        obj.save()
                self.assertEqual(obj.__class__.objects.count(), obj_count)

    def test_wrong_name_for_objects(self):
        """test if wrong names for objects couldn't be passed"""
        for obj in (self.item, self.tag, self.category):
            name = "a" * 151  # max is 150
            with self.subTest(obj=obj, name=name):
                obj_count = obj.__class__.objects.count()
                obj.name = name
                with self.assertRaises(django.core.exceptions.ValidationError):
                    obj.full_clean()
                    obj.save()
                self.assertEqual(obj.__class__.objects.count(), obj_count)

    def test_fuzzy_name_for_objects(self):
        """test if similiar names for tag and category couldn't be passed"""
        for obj in (self.tag, self.category):
            for name in (
                "!ПРИВЕТ?",
                "ПРИ ВЕ Т",
                "ПриВет",
                "ПPИBET",
                "!пP иBE T?",
            ):
                with self.subTest(obj=obj, name=name):
                    obj_count = obj.__class__.objects.count()
                    obj.name = name
                    with self.assertRaises(
                        django.core.exceptions.ValidationError
                    ):
                        obj.full_clean()
                        obj.save()
                    self.assertEqual(obj.__class__.objects.count(), obj_count)

    def test_wrong_text_for_item(self):
        """test if wrong text for item couldn't be passed"""
        item_count = catalog.models.Item.objects.count()

        self.item.text = "неправильный текст"

        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item.full_clean()
            self.item.save()

        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    def test_wrong_slug_for_objects(self):
        """test if wrong slug for objects couldn't be passed"""
        for obj, slug_prev in (
            (self.tag, ModelTest.tag.slug),  # slug unique for each table
            (self.category, ModelTest.category.slug),
        ):
            for slug in ("a" * 201, "1]%}бабочка{%[2", slug_prev):
                obj_count = obj.__class__.objects.count()
                with self.subTest(obj=obj, slug=slug):
                    obj.slug = slug
                    with self.assertRaises(
                        django.core.exceptions.ValidationError
                    ):
                        obj.full_clean()
                        obj.save()
                    self.assertEqual(obj.__class__.objects.count(), obj_count)

    def test_wrong_weights_for_category(self):
        """test if wrong weights for category couldn't be passed"""
        for weight in (-1, 32768):
            with self.subTest(weight=weight):
                category_count = catalog.models.Category.objects.count()
                self.category.weight = weight

                with self.assertRaises(django.core.exceptions.ValidationError):
                    self.category.full_clean()
                    self.category.save()
                self.assertEqual(
                    catalog.models.Category.objects.count(), category_count
                )
