from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
