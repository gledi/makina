from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=32)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Price in EUR",
    )
    price_id = models.CharField(max_length=32, null=True, blank=True)
    photo = models.ImageField(upload_to="products")
    photo_md = ImageSpecField(
        source="photo",
        processors=[ResizeToFill(480, 360)],
        format="JPEG",
        options={"quality": 80},
    )
    photo_thumb = ImageSpecField(
        source="photo",
        processors=[ResizeToFill(120, 90)],
        format="JPEG",
        options={"quality": 80},
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        constraints = [
            models.UniqueConstraint(fields=["code"], name="uix_products_code")
        ]
