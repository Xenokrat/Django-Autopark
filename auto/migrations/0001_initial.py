# Generated by Django 4.2 on 2023-04-09 18:13

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255, unique=True, verbose_name='Бренд')),
                ('car_type', models.CharField(max_length=255, verbose_name='Тип авто')),
                ('load_capacity', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Грузоподъемность, кг')),
                ('seats_number', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Количество мест')),
                ('fuel_tank_volume', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Объем бака, куб.см')),
                ('drive_type', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тип привода')),
                ('max_speed', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Максимальная скорость, км/ч')),
            ],
            options={
                'verbose_name': 'Бренд авто',
                'verbose_name_plural': 'Бренды авто',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('second_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('salary', models.PositiveIntegerField(blank=True, null=True, verbose_name='Зарплата, руб')),
                ('driving_experience', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Водительский стаж')),
            ],
            options={
                'verbose_name': 'Водитель',
                'verbose_name_plural': 'Водители',
            },
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название предприятия')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('timezone', models.CharField(blank=True, choices=[('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Europe/Moscow', 'Europe/Moscow'), ('Europe/Kirov', 'Europe/Kirov'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Europe/Saratov', 'Europe/Saratov'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Europe/Samara', 'Europe/Samara'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Asia/Omsk', 'Asia/Omsk'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Asia/Barnaul', 'Asia/Barnaul'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Asia/Chita', 'Asia/Chita'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Asia/Magadan', 'Asia/Magadan'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Asia/Anadyr', 'Asia/Anadyr')], default='UTC', max_length=32, verbose_name='Часовой пояс')),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер регистрации')),
                ('VIN', models.CharField(max_length=17, unique=True)),
                ('year', models.PositiveSmallIntegerField(verbose_name='Год выпуска')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='Цвет')),
                ('purchase_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время покупки')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')),
                ('current_driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicles', to='auto.driver', verbose_name='Активный водитель')),
                ('enterprise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='auto.enterprise', verbose_name='Предприятие')),
                ('model', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='auto.carmodel', verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='manager', serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Учетная запись')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('second_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('enterprise', models.ManyToManyField(blank=True, related_name='manager', to='auto.enterprise', verbose_name='Предприятия')),
            ],
            options={
                'verbose_name': 'Менеджер',
                'verbose_name_plural': 'Менеджеры',
            },
        ),
        migrations.CreateModel(
            name='GPSData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='GPS положение')),
                ('timestamp', models.DateTimeField(null=True, verbose_name='Время записи')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gps_data', to='auto.vehicle', verbose_name='Авто')),
            ],
            options={
                'verbose_name': 'GPS данные',
                'verbose_name_plural': 'GPS данные',
            },
        ),
        migrations.CreateModel(
            name='GPSAutoTrack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track', django.contrib.gis.db.models.fields.LineStringField(srid=4326, verbose_name='GPS путь')),
                ('timestamp_start', models.DateTimeField(null=True, verbose_name='Время отправления')),
                ('timestamp_end', models.DateTimeField(null=True, verbose_name='Время прибытия')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gps_auto_track', to='auto.vehicle', verbose_name='Авто')),
            ],
            options={
                'verbose_name': 'GPS Трек',
                'verbose_name_plural': 'GPS Треки',
            },
        ),
        migrations.AddField(
            model_name='driver',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to='auto.enterprise', verbose_name='Предприятие'),
        ),
        migrations.AddField(
            model_name='driver',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to='auto.vehicle', verbose_name='Автомобиль'),
        ),
        migrations.CreateModel(
            name='AutoRide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='Время начала поездки')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Время окончания поездки')),
                ('start_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, verbose_name='Точка начала поездки')),
                ('end_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, verbose_name='Точка окончания поездки')),
                ('distance', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Пробег, км')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auto_rides', to='auto.vehicle', verbose_name='Авто')),
            ],
            options={
                'verbose_name': 'Поездка',
                'verbose_name_plural': 'Поездки',
            },
        ),
    ]
