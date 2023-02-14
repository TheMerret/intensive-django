from catalog import views

from django.urls import path

urlpatterns = [
    path("", views.item_list, name="item-list"),
    path("<int:item_id>", views.item_detail, name="item-detail"),
]
