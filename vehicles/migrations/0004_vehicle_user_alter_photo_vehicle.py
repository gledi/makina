# Generated by Django 4.1.2 on 2022-10-16 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("vehicles", "0003_alter_vehicle_options_vehicle_color_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vehicles",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="photo",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photos",
                to="vehicles.vehicle",
                verbose_name="vehicle",
            ),
        ),
    ]
