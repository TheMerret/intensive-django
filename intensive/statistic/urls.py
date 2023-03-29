import django.urls

import statistic.views

app_name = "statistic"

urlpatterns = [
    django.urls.path(
        "users",
        statistic.views.UserListView.as_view(),
        name="users",
    ),
    django.urls.path(
        "user/<int:user_id>",
        statistic.views.UserStatistic.as_view(),
        name="user-statistic",
    ),
]
