from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):  # vehicles_vehicle
    TRANSMISSION_AUTOMATIC = "A"
    TRANSMISSION_MANUAL = "M"
    TRANSMISSION_CHOICES = [
        (TRANSMISSION_AUTOMATIC, "Automatic"),
        (TRANSMISSION_MANUAL, "Manual"),
    ]

    DIESEL = "Diesel"
    PETROL = "Petrol"
    ELECTRIC = "Electric"
    FUEL_CHOICES = [
        (DIESEL, DIESEL),
        (PETROL, PETROL),
        (ELECTRIC, ELECTRIC),
    ]

    SEDAN = "Sedan"
    COUPET = "Coupet"
    HATCHBACK = "Hatchback"
    SUV = "SUV"
    TRUCK = "Truck"
    KINDS = [
        (SEDAN, SEDAN),
        (COUPET, COUPET),
        (HATCHBACK, HATCHBACK),
        (SUV, SUV),
        (TRUCK, TRUCK),
    ]

    make = models.CharField(max_length=255, null=False, blank=False)
    model = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(help_text=_("Price in Euros"))
    transmission = models.CharField(max_length=1, choices=TRANSMISSION_CHOICES)
    fuel = models.CharField(max_length=32, choices=FUEL_CHOICES)
    plates = models.CharField(max_length=32, default="Albanian")
    kind = models.CharField(max_length=32, choices=KINDS, null=True, blank=True)
    km = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=32, null=True, blank=True)
    is_published = models.BooleanField(_("is published?"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehicles",
    )

    class Meta:
        db_table = "vehicles"
        verbose_name = _("vehicle")
        verbose_name_plural = _("vehicles")
        permissions = [
            ("publish_vehicle", "Can publish vehicle"),
        ]

    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model} {self.get_transmission_display()}/{self.fuel}"

    def get_absolute_url(self):
        return reverse("vehicle-detail", kwargs={"pk": self.pk})


class Photo(models.Model):
    picture = models.ImageField(_("picture"))
    vehicle = models.ForeignKey(
        Vehicle,
        verbose_name=_("vehicle"),
        on_delete=models.CASCADE,
        related_name="photos",
    )

    class Meta:
        db_table = "photos"
        verbose_name = _("photo")
        verbose_name_plural = _("photos")
