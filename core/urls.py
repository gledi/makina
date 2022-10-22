from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("", include("vehicles.urls")),
    path("posts/", include("blog.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
