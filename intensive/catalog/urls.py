import django.urls

from catalog import converters
from catalog import views


app_name = "catalog"

# N* according to ISO 80000-2
django.urls.register_converter(converters.PositiveInteger, "N*")

urlpatterns = [
    django.urls.path("", views.item_list, name="item-list"),
    django.urls.path("<int:item_id>", views.item_detail, name="item-detail"),
    django.urls.path("new", views.new_items, name="new-items"),
    django.urls.path("friday", views.friday_items, name="friday-items"),
    django.urls.path(
        "unverified", views.unverified_items, name="unverified-items"
    ),
    django.urls.path("tag", views.tag_create, name="tag-create"),
    django.urls.path(
        "tag/<int:item_id>/delete", views.tag_delete, name="tag-delete"
    ),
    django.urls.path(
        "tag/<int:item_id>/update", views.tag_create, name="tag-update"
    ),
    django.urls.path("feedback", views.feedback, name="feedback"),
]
