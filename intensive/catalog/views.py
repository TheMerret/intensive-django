import django.shortcuts

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
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.detailed(), pk=item_id
    )
    template = "catalog/item_detail.html"
    context = {"item": item}
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
