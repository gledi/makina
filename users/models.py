from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    telno = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "users"


class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=128)
    is_complete = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("registration-activation", kwargs={"key": self.activation_key})
