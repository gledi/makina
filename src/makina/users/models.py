from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = "users"


def _profile_pic_upload(instance, filename):
    return f"profilepics/{instance.user.username}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    telno = models.CharField(_("telno"), max_length=32, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to=_profile_pic_upload)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")
        db_table = "profiles"

    def __str__(self) -> str:
        return self.user.username


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=128)
    is_complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self):
        return reverse("registration-activation", kwargs={"key": self.activation_key})

