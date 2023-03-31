import django.db.models
import django.shortcuts
import django.views.generic

import catalog.models
import rating.models
import users.models


class ItemStatisticListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "statistic/item_list.html"
    context_object_name = "item_rating"

    def get_queryset(self):
        return (
            rating.models.ItemRating.objects
            .statistic_list()
            .filter(user_id=self.request.user.id)
        )


class ItemStatistic(django.views.generic.DetailView):
    template_name = "statistic/item_detail.html"
    queryset = catalog.models.Item.objects.only("name")
    context_object_name = "item"
    pk_url_kwarg = "item_id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        all_rating = (
            rating.models.ItemRating.objects.statistic_detail().filter(
                item_id=self.object.id
            )
        )
        average = all_rating.aggregate(django.db.models.Avg("score")).get(
            "score__avg"
        )
        max_min = all_rating.aggregate(
            django.db.models.Max("score"), django.db.models.Min("score")
        )
        max_score = max_min.get("score__max")
        min_score = max_min.get("score__min")
        self.extra_context = {
            "score": average,
            "all_score": all_rating.count(),
            "max_score": all_rating.filter(score=max_score)
            .first()
            .user.username,
            "min_score": all_rating.filter(score=min_score)
            .first()
            .user.username,
        }
        return super().get(request, *args, **kwargs)


class UserListView(django.views.generic.ListView):
    template_name = "statistic/user_list.html"
    queryset = users.models.UserProxy.objects.simple_list_users()
    context_object_name = "users"


class UserStatistic(django.views.generic.TemplateView):
    template_name = "statistic/user_statistic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        user = django.shortcuts.get_object_or_404(
            users.models.UserProxy.objects.only("username"), pk=user_id
        )
        context["user"] = user
        max_min = user.item_rating.aggregate(
            django.db.models.Max("score"), django.db.models.Min("score")
        )
        max_score = max_min.get("score__max")
        min_score = max_min.get("score__min")
        item = catalog.models.Item.objects.only("name")
        context["best_rating"] = item.filter(ratings__score=max_score).first()
        context["worst_rating"] = item.filter(ratings__score=min_score).first()
        context["rating_count"] = (
            rating.models.ItemRating.objects.filter(user_id=user.id)
            .only("id")
            .count()
        )
        context["rating_mean"] = user.item_rating.aggregate(
            django.db.models.Avg("score")
        ).get("score__avg")
        return context
