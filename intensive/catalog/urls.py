from catalog import views

from django.urls import path

urlpatterns = [
    path("", views.item_list),
    path("<int:item_id>", views.item_detail),
]
