import django.views.generic


class AboutView(django.views.generic.TemplateView):
    template_name = "about/about.html"
