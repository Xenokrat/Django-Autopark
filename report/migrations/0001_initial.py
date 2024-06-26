# Generated by Django 4.2 on 2023-04-09 18:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Показатель')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['object_id'],
            },
        ),
        migrations.CreateModel(
            name='CarMileageReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(choices=[('день', 'День'), ('месяц', 'Месяц'), ('год', 'Год')], max_length=10, verbose_name='Временной период')),
                ('start_date', models.DateField(verbose_name='Начальная дата')),
                ('end_date', models.DateField(verbose_name='Конечная дата')),
                ('report_type', models.CharField(default='Отчет по пробегу за период', max_length=50, verbose_name='Тип отчета')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auto.vehicle')),
            ],
            options={
                'verbose_name': 'Отчет по пробегу автомобиля за период',
                'verbose_name_plural': 'Отчеты по пробегу автомобиля за период',
            },
        ),
    ]
