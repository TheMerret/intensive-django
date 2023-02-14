from django.urls import include, path

from . import settings

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
