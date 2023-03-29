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
        return rating.models.ItemRating.objects.filter(
            user=self.request.user
        ).order_by("-score")


class ItemStatistic(django.views.generic.DetailView):
    template_name = "statistic/item_detail.html"
    queryset = catalog.models.Item.objects.only("name")
    context_object_name = "item"
    pk_url_kwarg = "item_id"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        medium_value = 0
        max_score, min_score = [0, None], [6, None]
        all_rating = rating.models.ItemRating.objects.filter(item=self.object)
        for i in all_rating:
            medium_value += i.score
            if i.score > max_score[0]:
                max_score[0] = i.score
                max_score[1] = i.user.username
            if i.score < min_score[0]:
                min_score[0] = i.score
                min_score[1] = i.user.username
        all_score = all_rating.count()
        medium_value /= all_score or 1
        self.extra_context = {
            "score": medium_value,
            "all_score": all_score,
            "max_score": max_score[1],
            "min_score": min_score[1],
        }
        return super().get(request, *args, **kwargs)


class UserListView(django.views.generic.ListView):
    template_name = "statistic/user_list.html"
    model = users.models.UserProxy
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
        context["best_rating"] = (
            user.item_rating.filter(score=max_score).only("item__name").first()
        )
        context["worst_rating"] = (
            user.item_rating.filter(score=min_score).only("item__name").first()
        )
        context["rating_count"] = user.item_rating.count()
        context["rating_mean"] = user.item_rating.aggregate(
            django.db.models.Avg("score")
        ).get("score__avg")
        return context
