from catalog import converters, views

from django.urls import path, re_path, register_converter

# N* according to ISO 80000-2
register_converter(converters.PositiveInteger, "N*")

urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("<int:item_id>", views.item_detail, name="item-detail"),
    re_path(
        r"^re/(?P<item_id>[1-9]\d*)/$",
        views.item_detail,
        name="re-item-detail",
    ),
    path(
        "converter/<N*:item_id>/",
        views.item_detail,
        name="converter-item-detail",
    ),
]
