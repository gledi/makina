from rest_framework import serializers

from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = (
            "id",
            "make",
            "model",
            "description",
            "year",
            "price",
            "transmission",
            "fuel",
            "plates",
            "kind",
            "km",
            "color",
            "created_at",
            "updated_at",
        )
