import mistune
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_("title"), max_length=255, null=False, blank=False)
    slug = models.SlugField(_("slug"), max_length=255, null=False, blank=False)
    body = models.TextField(_("body"), null=False, blank=False)
    published_on = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("author"),
        null=False,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    is_published = models.BooleanField(default=False)
    tags = models.CharField(max_length=255)

    class Meta:
        db_table = "posts"
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self) -> str:
        return self.title

    @property
    def body_html(self) -> str:
        return mistune.markdown(self.body)
