from django.shortcuts import render


def item_list(request):
    template = "catalog/list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, item_id):
    template = "catalog/item_detail.html"
    context = {
        "item_id": item_id
    }
    return render(request, template, context)
