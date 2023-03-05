from django.shortcuts import get_object_or_404
from django.shortcuts import render

import catalog.models


def item_list(request):
    template = "catalog/list.html"
    items = catalog.models.Item.objects.published()
    context = {
        "items": items,
    }
    return render(request, template, context)


def item_detail(request, item_id):
    item = get_object_or_404(
        catalog.models.Item.objects.filter(is_published=True), pk=item_id
    )
    template = "catalog/item_detail.html"
    context = {"item": item}
    return render(request, template, context)
