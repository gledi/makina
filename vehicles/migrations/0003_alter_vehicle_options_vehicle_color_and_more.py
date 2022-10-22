# Generated by Django 4.1.2 on 2022-10-16 10:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0002_vehicle_year"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="vehicle",
            options={"verbose_name": "vehicle", "verbose_name_plural": "vehicles"},
        ),
        migrations.AddField(
            model_name="vehicle",
            name="color",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vehicle",
            name="fuel",
            field=models.CharField(
                choices=[
                    ("Diesel", "Diesel"),
                    ("Petrol", "Petrol"),
                    ("Electric", "Electric"),
                ],
                default="Diesel",
                max_length=32,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vehicle",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="is published?"),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Sedan", "Sedan"),
                    ("Coupet", "Coupet"),
                    ("Hatchback", "Hatchback"),
                    ("SUV", "SUV"),
                    ("Truck", "Truck"),
                ],
                max_length=32,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="km",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="plates",
            field=models.CharField(default="Albanian", max_length=32),
        ),
        migrations.AddField(
            model_name="vehicle",
            name="price",
            field=models.IntegerField(default=5000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vehicle",
            name="transmission",
            field=models.CharField(
                choices=[("A", "Automatic"), ("M", "Manual")], default="M", max_length=1
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vehicle",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterModelTable(
            name="vehicle",
            table="vehicles",
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("picture", models.ImageField(upload_to="", verbose_name="picture")),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vehicles.vehicle",
                        verbose_name="vehicle",
                    ),
                ),
            ],
            options={
                "verbose_name": "photo",
                "verbose_name_plural": "photos",
                "db_table": "photos",
            },
        ),
    ]