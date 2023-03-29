import django.db.models
import django.shortcuts
import django.views.generic


import users.models


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
            user.item_rating.filter(score=max_score)
            .only("item__name")
            .order_by("-updated_at")
            .first()
        )
        context["worst_rating"] = (
            user.item_rating.filter(score=min_score)
            .only("item__name")
            .order_by("-updated_at")
            .first()
        )
        context["rating_count"] = user.item_rating.count()
        context["rating_mean"] = user.item_rating.aggregate(
            django.db.models.Avg("score")
        ).get("score__avg")
        return context
