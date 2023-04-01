import django.urls

import statistic.views

app_name = "statistic"

urlpatterns = [
    django.urls.path(
        "users/",
        statistic.views.UserListView.as_view(),
        name="users",
    ),
    django.urls.path(
        "user/<int:user_id>/",
        statistic.views.UserStatistic.as_view(),
        name="user-statistic",
    ),
    django.urls.path(
        "my_item_list/",
        statistic.views.UserItemStatisticListView.as_view(),
        name="my_item_list",
    ),
    django.urls.path(
        "item/<int:item_id>/",
        statistic.views.ItemStatistic.as_view(),
        name="item-statistic",
    ),
    django.urls.path(
        "item_list/",
        statistic.views.ItemStatisticListView.as_view(),
        name="item_list",
    ),
]
