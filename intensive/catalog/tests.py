from unittest import skip

from django.test import Client
from django.test import TestCase
from django.urls import reverse
import django.urls.exceptions

import catalog.models


class CatalogPageTest(TestCase):
    """test catalog page"""

    fixtures = ["catalog.json"]  # for item detail

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


class ContextTest(TestCase):
    """test context dictionaries"""

    fixtures = ["catalog.json"]

    def test_homepage_shows_correct_context(self):
        response = Client().get(reverse("homepage:index"))
        self.assertIn("items", response.context)

    def test_nome_count_item(self):
        response = django.test.Client().get(
            reverse("homepage:index")
        )
        items = response.context["items"]
        self.assertEqual(items.count(), 5)
