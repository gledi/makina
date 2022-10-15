from django.db import models
from django.db.models import Manager


"""
CREATE TABLE vehicles_vehicle (
    id  integer      not null constraint vehicles_pk primary key autoincrement,
    make        varchar(255) not null,
    model       varchar(255) not null,
    description text
)
"""


class Vehicle(models.Model):  # vehicles_vehicle
    make = models.CharField(max_length=255, null=False)
    model = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    year = models.IntegerField(null=True)
