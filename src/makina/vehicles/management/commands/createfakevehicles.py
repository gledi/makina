import io
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from faker import Faker

from vehicles.models import Vehicle, Photo


User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument("--count", "-c", type=int, default=20)
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        colors = ["White", "Black", "Red", "Blue", "Gray"]
        makes = {
            "Mercedes": ["C200", "S600", "A120"],
            "Ford": ["Focus", "Fiesta", "Mondeo", "Ranger"],
            "Toyota": ["Rav4", "Land Cruiser", "Tacoma", "Hilux"],
            "BMW": ["x6", "x7", "x5"],
            "Audi": ["A8", "Q7", "Q5"],
            "Mazda": ["CX5", "CX7", "MX7"],
            "Volkwagen": ["Passat", "Golf", "Polo"],
            "Volvo": ["S40", "XC60"],
        }
        fake = Faker()
        users = User.objects.all()
        for i in range(options["count"]):
            make = random.choice(list(makes.keys()))
            model = random.choice(makes[make])
            vehicle = Vehicle(
                make=make,
                model=model,
                description=fake.sentence(),
                year=random.randrange(2000, 2023),
                price=random.randrange(10, 1_000) * 100,
                transmission=random.choice(Vehicle.TRANSMISSION_CHOICES)[0],
                fuel=random.choice(Vehicle.FUEL_CHOICES)[0],
                kind=random.choice(Vehicle.KINDS)[0],
                km=random.randrange(0, 300_000),
                color=random.choice(colors),
                user=random.choice(users),
            )

            vehicle.save()

            for j in range(random.randrange(2, 11)):
                pic = ImageFile(
                    io.BytesIO(fake.image((600, 400))), name=f"vehicle_{i}_{j}.png"
                )
                photo = Photo(picture=pic, vehicle=vehicle)
                photo.save()
