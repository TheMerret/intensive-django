import django.shortcuts
import django.urls
import django.views.generic

import catalog.models
from rating.forms import ItemRatingForm
from rating.models import ItemRating


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/list.html"
    queryset = catalog.models.Item.objects.on_list()
    context_object_name = "items"


class ItemDetailView(
    django.views.generic.edit.FormMixin,
    django.views.generic.edit.ProcessFormView,
    django.views.generic.DetailView,
):
    template_name = "catalog/item_detail.html"
    queryset = catalog.models.Item.objects.detailed()
    context_object_name = "item"
    pk_url_kwarg = "item_id"
    form_class = ItemRatingForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        medium_value = 0
        all_rating = ItemRating.objects.filter(item=self.object)
        for i in all_rating:
            medium_value += i.score
        all_score = all_rating.count()
        medium_value /= all_score or 1
        if request.user.is_authenticated:
            form = ItemRatingForm(
                None,
                instance=self.object.ratings.filter(user=request.user).first(),
            )
            self.extra_context = {
                "form": form,
                "score": medium_value,
                "all_score": all_score,
            }
        else:
            self.extra_context = {
                "score": medium_value,
                "all_score": all_score,
            }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form = ItemRatingForm(
            self.request.POST or None,
            instance=self.object.ratings.filter(
                user=self.request.user
            ).first(),
        )
        if form.instance is not None:
            if "delete" in self.request.POST:
                ItemRating.objects.get(
                    item=self.object, user=self.request.user
                ).delete()
            else:
                print("hello")
                rating = form.save(commit=False)
                rating.user = self.request.user
                rating.item = self.object
                rating.save()
        else:
            score = form.cleaned_data["score"]
            rating = ItemRating.objects.create(
                user=self.request.user, item=self.object, score=score
            )
            rating.clean()
            rating.save()
        return django.shortcuts.redirect(
            "catalog:item-detail", item_id=self.object.id
        )


class NewItemView(django.views.generic.ListView):
    template_name = "catalog/list_date.html"
    queryset = catalog.models.Item.objects.new()
    context_object_name = "items"


class FridayItemsView(django.views.generic.ListView):
    template_name = "catalog/list_date.html"
    queryset = catalog.models.Item.objects.friday()
    context_object_name = "items"


class UnverifiedItemsView(django.views.generic.ListView):
    template_name = "catalog/list_date.html"
    queryset = catalog.models.Item.objects.unverified()
    context_object_name = "items"
