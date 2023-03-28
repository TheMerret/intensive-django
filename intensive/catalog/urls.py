import django.urls

from catalog import converters
from catalog import views


app_name = "catalog"

# N* according to ISO 80000-2
django.urls.register_converter(converters.PositiveInteger, "N*")

urlpatterns = [
    django.urls.path("", views.ItemListView.as_view(), name="item-list"),
    django.urls.path(
        "<int:item_id>", views.ItemDetailView.as_view(), name="item-detail"
    ),
    django.urls.re_path(
        r"^re/(?P<item_id>[1-9]\d*)/$",
        views.ItemDetailView.as_view(),
        name="re-item-detail",
    ),
    django.urls.path(
        "converter/<N*:item_id>/",
        views.ItemDetailView.as_view(),
        name="converter-item-detail",
    ),
    django.urls.path("new", views.NewItemView.as_view(), name="new-items"),
    django.urls.path(
        "friday", views.FridayItemsView.as_view(), name="friday-items"
    ),
    django.urls.path(
        "unverified",
        views.UnverifiedItemsView.as_view(),
        name="unverified-items",
    ),
]
