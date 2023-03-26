import django.views.generic

import catalog.models


class ItemListView(django.views.generic.ListView):
    template_name = "catalog/list.html"
    queryset = catalog.models.Item.objects.on_list()
    context_object_name = "items"


class ItemDetailView(django.views.generic.DetailView):
    template_name = "catalog/item_detail.html"
    queryset = catalog.models.Item.objects.detailed()
    context_object_name = "item"
    pk_url_kwarg = "item_id"


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
