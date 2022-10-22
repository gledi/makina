from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    telno = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        db_table = "users"
