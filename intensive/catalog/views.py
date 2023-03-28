import django.shortcuts
import django.urls
from rating.forms import ItemRatingForm
from rating.models import ItemRating

import catalog.forms
import catalog.models


def item_list(request):
    template = "catalog/list.html"
    items = catalog.models.Item.objects.on_list()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def item_detail(request, item_id):
    template = "catalog/item_detail.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.detailed(), pk=item_id
    )
    medium_value = 0
    all_rating = ItemRating.objects.filter(item=item)
    for i in all_rating:
        medium_value += i.score
    medium_value /= (all_rating.count() or 1)
    form = ItemRatingForm(
        request.POST or None,
        instance=item.ratings.filter(user=request.user).first(),
    )
    if form.is_valid():
        if form.instance is not None:
            rating = form.save(commit=False)
            rating.user = request.user
            rating.item = item
            rating.save()
        else:
            score = form.cleaned_data["score"]
            rating = ItemRating.objects.create(
                user=request.user, item=item, score=score
            )
            rating.clean()
            rating.save()
        return django.shortcuts.redirect(
            "catalog:item-detail", item_id=item_id
        )
    context = {
        "item": item,
        "form": form,
        "score": medium_value,
    }
    return django.shortcuts.render(request, template, context)


def new_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.new()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def friday_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.friday()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def unverified_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.unverified()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def tag_create(request):
    template = "catalog/tag_create.html"
    form = catalog.forms.TagCreateForm(request.POST or None)
    if form.is_valid():
        is_published = form.cleaned_data["is_published"]
        name = form.cleaned_data["name"]
        slug = form.cleaned_data["slug"]
        catalog.models.Tag.objects.create(
            is_published=is_published,
            name=name,
            slug=slug,
        )
        return django.shortcuts.redirect("catalog:tag-create")
    context = {"form": form}
    return django.shortcuts.render(request, template, context)


def tag_delete(request, item_id):
    tag = django.shortcuts.get_object_or_404(catalog.models.Tag, pk=item_id)
    if request.method == "POST":
        tag.delete()
    template = "catalog/tag_delete.html"
    context = {"tag": tag}
    return django.shortcuts.render(request, template, context)


def tag_update(request, item_id):
    template = "catalog/tag_update.html"
    tag = django.shortcuts.get_object_or_404(catalog.models.Tag, pk=item_id)
    form = catalog.forms.TagUpdateForm(request.POST or None)
    if form.is_valid():
        tag.slug = form.cleaned_data["slug"]
        tag.save(update_fields=["slug"])
    context = {"tag": tag}
    return django.shortcuts.render(request, template, context)


def feedback(request):
    template = "catalog/feedback.html"
    form = catalog.forms.ItemForm(request.POST or None)

    if form.is_valid():
        name = form.cleaned_data.get("name")
        django.shortcuts.get_object_or_404send_mail(
            "Subject here",
            name,
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )

        return django.shortcuts.redirect("catalog:item-list")

    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)


def item_create(request):
    template = "create.html"
    form = catalog.forms.ItemForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data["name"]
        catalog.models.Item.objects.create(name=name)
    context = {
        "form": form,
    }
    return django.shortcuts.render(request, template, context)
