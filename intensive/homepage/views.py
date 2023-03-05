from django.http import HttpResponse
from django.shortcuts import render

import catalog.models


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.all().order_by("text", "name")
    context = {
        "items": items,
    }
    return render(request, template, context)


def coffee(request):
    return HttpResponse("<body>Я чайник</body>", status=418)
