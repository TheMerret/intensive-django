from django.urls import path

from homepage import views

urlpatterns = [
    path("", views.home, name="index"),
    path("coffee/", views.coffee)
]
