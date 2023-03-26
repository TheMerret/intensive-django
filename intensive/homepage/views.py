from django.http import HttpResponse
import django.views.generic

import catalog.models


class HomeView(django.views.generic.ListView):
    template_name = "homepage/home.html"
    queryset = catalog.models.Item.objects.on_main_page()
    context_object_name = "items"


class CoffeeView(django.views.generic.View):

    def get(self, request):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()
        return HttpResponse("<body>Я чайник</body>", status=418)
