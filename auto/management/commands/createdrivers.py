import random
import string
from datetime import datetime

from auto.models import CarModel, Driver, Enterprise, Vehicle
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    FIRST_NAMES = (
        "Александр",
        "Алексей",
        "Андрей",
        "Артем",
        "Арсений",
        "Владислав",
        "Денис",
        "Дмитрий",
        "Евгений",
        "Егор",
        "Иван",
        "Игорь",
        "Илья",
        "Кирилл",
        "Максим",
        "Матвей",
        "Михаил",
        "Никита",
        "Роман",
        "Руслан",
        "Сергей",
        "Тимофей",
        "Тимур",
        "Ярослав",
    )
    SECOND_NAMES = (
        "Иванов",
        "Смирнов",
        "Кузнецов",
        "Попов",
        "Васильев",
        "Петров",
        "Соколов",
        "Михайлов",
    )

    def add_arguments(self, parser):
        parser.add_argument("enterprise", type=int)
        parser.add_argument("--count", default=10, type=int)

    def handle(self, *args, **options):
        try:
            enterprise = Enterprise.objects.get(pk=options.get("enterprise"))
        except Enterprise.DoesNotExist:
            CommandError("Предприятие с указанным id не существует")

        count = options.get("count")
        for _ in range(count):
            vehicle = random.choice(Vehicle.objects.filter(enterprise=enterprise))
            Driver.objects.create(
                first_name=random.choice(self.FIRST_NAMES),
                second_name=random.choice(self.SECOND_NAMES),
                salary=random.randint(10, 100) * 1000,
                driving_experience=random.randint(0, 30),
                enterprise=enterprise,
                vehicle=vehicle,
            )

        self.stdout.write(self.style.SUCCESS(f"Успешно добавлены {count} водителей для предприятия c id {enterprise}"))
