from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    class Transmission(models.TextChoices):
        AUTOMATIC = "A", _("Automatic")
        MANUAL = "M", _("Manual")

    class Fuel(models.TextChoices):
        DIESEL = "diesel", _("Diesel")
        GASOLINE = "gasoline", _("Gasoline")
        ELECTRIC = "eletric", _("Electric")

    class Kind(models.TextChoices):
        SEDAN = "sedan", _("Sedan")
        COUPET = "coupet", _("Coupet")
        HATCHBACK = "hatchback", _("Hatchback")
        SUV = "suv", _("SUV")
        TRUCK = "truck", _("Truck")

    make = models.CharField(max_length=255, null=False, blank=False)
    model = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(help_text=_("Price in Euros"))
    transmission = models.CharField(max_length=1, choices=Transmission.choices)
    fuel = models.CharField(max_length=32, choices=Fuel.choices)
    plates = models.CharField(max_length=32, default="Albanian")
    kind = models.CharField(max_length=32, choices=Kind.choices, blank=True)
    km = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=32, blank=True)
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
        permissions = (
            ("publish_vehicle", "Can publish vehicle"),
        )

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

    def __str__(self) -> str:
        return self.picture.name
