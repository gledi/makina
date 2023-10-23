from typing import Final

from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "is_published", "published_on")
    list_filter = ("is_published", "author")
    search_fields = ("title", "body")
    prepopulated_fields: Final[dict[str, tuple[str]]] = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "published_on"
    ordering = ("published_on",)
