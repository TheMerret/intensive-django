from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = "catalog/list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, item_id):
    return HttpResponse("<body>Подробно элемент</body>")
