from django.shortcuts import get_object_or_404
from django.shortcuts import render

import catalog.models


def item_list(request):
    template = "catalog/list.html"
    items = catalog.models.Item.objects.on_list()
    context = {
        "items": items,
    }
    return render(request, template, context)


def item_detail(request, item_id):
    item = get_object_or_404(
        catalog.models.Item.objects.detailed(), pk=item_id
    )
    template = "catalog/item_detail.html"
    context = {"item": item}
    return render(request, template, context)


def new_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.new()
    context = {
        "items": items,
    }
    return render(request, template, context)


def friday_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.friday()
    context = {
        "items": items,
    }
    return render(request, template, context)


def unverified_items(request):
    template = "catalog/list_date.html"
    items = catalog.models.Item.objects.unverified()
    context = {
        "items": items,
    }
    return render(request, template, context)
