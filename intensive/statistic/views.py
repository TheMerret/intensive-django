import django.db.models
import django.shortcuts
import django.views.generic

import catalog.models
import rating.models
import users.models


class UserItemStatisticListView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.ListView,
):
    template_name = "statistic/my_item_list.html"
    context_object_name = "item_rating"

    def get_queryset(self):
        return rating.models.ItemRating.objects.statistic_list().filter(
            user_id=self.request.user.id
        )


class ItemStatisticListView(django.views.generic.ListView):
    template_name = "statistic/my_item_list.html"
    context_object_name = "item_rating"

    def get_queryset(self):
        return rating.models.ItemRating.objects.statistic_list()


class ItemStatistic(django.views.generic.DetailView):
    template_name = "statistic/item_detail.html"
    model = catalog.models.Item
    context_object_name = "item"
    pk_url_kwarg = "item_id"

    def get(self, request, *args, **kwargs):
        self.object = catalog.models.Item.objects.only("name").get(
            pk=kwargs["item_id"]
        )
        all_rating = (
            rating.models.ItemRating.objects.statistic_detail().filter(
                item=self.object
            )
        )
        max_min_avg = all_rating.aggregate(
            django.db.models.Max("score"),
            django.db.models.Min("score"),
            django.db.models.Avg("score"),
        )
        max_score = max_min_avg.get("score__max")
        min_score = max_min_avg.get("score__min")
        if min_score == max_score:
            score = all_rating.filter(score=max_score).first()
            self.extra_context = {
                "score": max_min_avg.get("score__avg"),
                "all_score": all_rating.count(),
                "max_score": score,
                "min_score": score,
            }
        else:
            self.extra_context = {
                "score": max_min_avg.get("score__avg"),
                "all_score": all_rating.count(),
                "max_score": all_rating.filter(score=max_score).first(),
                "min_score": all_rating.filter(score=min_score).first(),
            }
        return super().get(request, *args, **kwargs)


class UserListView(django.views.generic.ListView):
    template_name = "statistic/user_list.html"
    queryset = users.models.UserProxy.objects.list_users()
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
        max_min_avg = user.item_rating.aggregate(
            django.db.models.Max("score"),
            django.db.models.Min("score"),
            django.db.models.Avg("score"),
        )
        max_score = max_min_avg.get("score__max")
        min_score = max_min_avg.get("score__min")
        item = catalog.models.Item.objects.only("name")
        if min_score == max_score:
            rating_score = item.filter(ratings__score=max_score).first()
            context["best_rating"] = rating_score
            context["worst_rating"] = rating_score
        else:
            context["best_rating"] = item.filter(
                ratings__score=max_score
            ).first()
            context["worst_rating"] = item.filter(
                ratings__score=min_score
            ).first()
        context["rating_count"] = rating.models.ItemRating.objects.filter(
            user_id=user.id
        ).count()
        context["rating_mean"] = max_min_avg.get("score__avg")
        return context
