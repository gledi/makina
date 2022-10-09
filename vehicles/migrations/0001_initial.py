# Generated by Django 4.1.2 on 2022-10-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vehicle",
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
                ("make", models.CharField(max_length=255)),
                ("model", models.CharField(max_length=255)),
                ("description", models.TextField(null=True)),
            ],
        ),
    ]
