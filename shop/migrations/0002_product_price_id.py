# Generated by Django 4.1.3 on 2022-11-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="price_id",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
