from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("makina.users.urls")),
    path("", include("makina.pages.urls")),
    path("shop/", include("makina.shop.urls")),
    path("vehicles/", include("makina.vehicles.urls")),
    path("posts/", include("makina.blog.urls")),
]


if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
