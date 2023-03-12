from django.urls import path

from feedback import views


app_name = "feedback"

urlpatterns = [
    path("", views.feedback_view, name="feedback"),
]
