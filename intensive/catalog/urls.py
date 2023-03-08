import django.urls

from catalog import converters
from catalog import views


app_name = "catalog"

# N* according to ISO 80000-2
django.urls.register_converter(converters.PositiveInteger, "N*")

urlpatterns = [
    django.urls.path("", views.item_list, name="item-list"),
    django.urls.path("<int:item_id>", views.item_detail, name="item-detail"),
    django.urls.re_path(
        r"^re/(?P<item_id>[1-9]\d*)/$",
        views.item_detail,
        name="re-item-detail",
    ),
    django.urls.path(
        "converter/<N*:item_id>/",
        views.item_detail,
        name="converter-item-detail",
    ),
    django.urls.path("new", views.new_items, name="new-items"),
    django.urls.path("friday", views.friday_items, name="friday-items"),
    django.urls.path(
        "unverified", views.unverified_items, name="unverified-items"
    ),
]
