import random
import string
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from auto.models import CarModel, Driver, Enterprise, Vehicle


class Command(BaseCommand):
    COLORS = (
        "Красная",
        "Желтая",
        "Синяя",
        "Белая",
        "Черная",
        "Зеленая",
    )

    def add_arguments(self, parser):
        parser.add_argument("enterprise", type=int)
        parser.add_argument("--count", default=10, type=int)

    def handle(self, *args, **options):
        try:
            enterprise = Enterprise.objects.get(pk=options.get("enterprise"))
        except Enterprise.DoesNotExist:
            raise CommandError("Предприятие с указанным id не существует")

        count = options.get("count")

        for i in range(count):
            model = random.choice(CarModel.objects.all())
            registration_number = self._id_generator(8)

            while Vehicle.objects.filter(registration_number=registration_number).exists():
                registration_number = self._id_generator(8)

            vin = self._id_generator(17)
            while Vehicle.objects.filter(VIN=vin).exists():
                vin = self._id_generator(17)

            if i % 10 == 0:
                current_driver = random.choice(
                    Driver.objects.filter(enterprise=enterprise))
                while Vehicle.objects.filter(current_driver=current_driver).exists():
                    current_driver = random.choice(
                        Driver.objects.filter(enterprise=enterprise))
            else:
                current_driver = None

            Vehicle.objects.create(
                model=model,
                registration_number=registration_number,
                VIN=vin,
                year=random.randint(1990, 2020),
                cost=random.randint(10, 500) * 1000,
                mileage=random.randint(0, 100) * 1000,
                color=random.choice(self.COLORS),
                purchase_date=self._create_random_date(
                    "2000-01-01", "2023-01-01"),
                photo=None,
                enterprise=enterprise,
                current_driver=current_driver,
            )

        self.stdout.write(self.style.SUCCESS(
            f"Успешно добавлены {count} авто для предприятия c id {enterprise}"))

    def _id_generator(self, size: int, chars: str = string.ascii_uppercase + string.digits) -> str:
        return "".join(random.choice(chars) for _ in range(size))

    def _create_random_date(self, start_date_str: str, end_date_str: str) -> str:
        format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date_str, format)
        end_date = datetime.strptime(end_date_str, format)
        random_date = start_date + (end_date - start_date) * random.random()
        return random_date.strftime(format)
