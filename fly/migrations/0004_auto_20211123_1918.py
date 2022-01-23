# Generated by Django 3.2.8 on 2021-11-23 16:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fly', '0003_flights_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flights',
            name='url',
        ),
        migrations.AddField(
            model_name='seats',
            name='amount_seat',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Стоимость места'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='amount_ticket',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Стоимость билета'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='fare_conditions',
            field=models.CharField(choices=[('E', 'Economy'), ('C', 'Comfort'), ('B', 'Business')], default='B', max_length=1, verbose_name='Класс обслуживания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='flight_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='id_flight', to='fly.flights', verbose_name='Рейс'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='seat_no',
            field=models.CharField(default='1B', max_length=3, verbose_name='Номер места'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tickets',
            name='ticket_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False, verbose_name='Идентификатор'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='ticket_no',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Номер должен содержать 13 символов', regex='^\\d{13}$')], verbose_name='Номер билета'),
        ),
        migrations.DeleteModel(
            name='Ticket_flights',
        ),
    ]
