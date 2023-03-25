from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
import django.contrib.auth.urls
from django.urls import include
from django.urls import path

import users.urls

urlpatterns = [
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
    path("feedback/", include("feedback.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include(users.urls)),
    path("auth/", include(django.contrib.auth.urls)),
    path("tinymce/", include("tinymce.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
