from django.http import HttpResponse
from django.shortcuts import render

import catalog.models
import homepage.forms


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main_page()
    form = homepage.forms.FeedbackForm()
    context = {
        "form": form,
        "items": items,
    }
    if request.method == "POST" and form.is_valid():
        name = request.POST.get("name")
        print(name)
    return render(request, template, context)


def coffee(request):
    return HttpResponse("<body>Я чайник</body>", status=418)
