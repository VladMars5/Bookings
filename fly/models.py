from django.db import models
from django.core.validators import RegexValidator

from django.urls import reverse
# Create your models here.
SERVISE = (
    ('E', 'Economy'),
    ('C', 'Comfort'),
    ('B', 'Business'),
)

class Bookings(models.Model):
    """Бронирование"""
    book_ref = models.CharField("Номер бронирования",\
                                validators=[RegexValidator(regex='^\w{6}$', \
                                message='Номер должен содержать 6 символов', code='nomatch')],\
                                primary_key=True, unique=True, max_length=6)
    book_date = models.DateTimeField("Дата бронирования", auto_now_add=True)
    total_amount = models.DecimalField("Полная сумма", max_digits=10 , decimal_places=2)

    def __str__(self):
        return self.book_ref #вернет строку о представлении нашей модели

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

class Tickets(models.Model):
    """Билеты"""
    ticket_id = models.AutoField("Идентификатор", primary_key=True)
    ticket_no = models.CharField("Номер билета",\
                                validators=[RegexValidator(regex='^\d{13}$', \
                                message='Номер должен содержать 13 символов', code='nomatch')],\
                                unique=True, max_length=13)
    flight_id = models.ForeignKey('Flights', verbose_name="Рейс", related_name="id_flight", on_delete=models.CASCADE)
    book_ref = models.ForeignKey(Bookings, verbose_name="Номер бронирования", related_name="no_booking", on_delete=models.CASCADE)
    passenger_last_name = models.TextField("Фамилия пассажира", max_length=30)
    passenger_name = models.TextField("Имя пассажира")
    contact_data = models.CharField("Контактные данные пассажира", max_length=12)
    seat_no = models.CharField("Номер места", max_length=3)
    fare_conditions = models.CharField("Класс обслуживания", max_length=1, choices=SERVISE)
    amount_ticket = models.DecimalField("Стоимость билета", max_digits=10, decimal_places=2)


    def __str__(self):
        return self.ticket_no

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

class Flights(models.Model):
    """Рейсы"""
    flight_id = models.AutoField("Идентификатор", primary_key=True)
    flight_no = models.CharField("Номер рейса", max_length=6)
    scheduled_departure_date = models.DateField("Дата вылета", default='')
    scheduled_departure_time = models.TimeField("Время вылета", default='')
    scheduled_arrival = models.DateTimeField("Время прилета по расписанию")
    departure_airport = models.ForeignKey('Airports', verbose_name='Аэропорт вылета', related_name='flight_iz_airport',\
                                          on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey('Airports', verbose_name='Аэропорт прилета', related_name='flight_v_airport',\
                                          on_delete=models.CASCADE)
    status = models.CharField("Статус рейса", max_length=20)
    aircraft_code = models.ForeignKey('Aircrafts', verbose_name='Код самолета', related_name='code_aircraft_flight',\
                                          on_delete=models.CASCADE)

    def __str__(self):
        ans ="Из " + str(self.departure_airport) + " в " + str(self.arrival_airport)
        return ans

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        unique_together = ("flight_id", "flight_no")

class Airports(models.Model):
    """Аэропорты"""
    airport_code = models.CharField("Код аэропорта",\
                                primary_key=True, unique=True, max_length=10)
    airport_name = models.TextField("Название аэропорта", unique=True)
    city = models.TextField("Город")

    def __str__(self):
        return self.airport_code

    class Meta:
        verbose_name = "Аэропорт"
        verbose_name_plural = "Аэропорты"


class Aircrafts(models.Model):
    """Самолеты"""
    aircraft_code = models.CharField("Код самолета", primary_key=True, max_length=10)
    model = models.TextField("Модель самолета")
    range = models.PositiveIntegerField("Дальность")

    def __str__(self):
        ans = str(self.model) + "(" + str(self.aircraft_code) + ")"
        return ans

    class Meta:
        verbose_name = "Самолет"
        verbose_name_plural = "Самолеты"

STATUS_SEAT = (
    ('F', 'Free'),
    ('B', 'Busy'),
)

class Seats(models.Model):
    """Места"""
    aircraft_code = models.ForeignKey('Aircrafts', verbose_name='Код самолета', related_name='code_aircraft_seat',\
                                          on_delete=models.CASCADE)
    seat_no = models.CharField("Номер места в самолете", max_length=3)
    fare_conditions = models.CharField("Класс обслуживания", max_length=10, choices=SERVISE)
    amount_seat = models.DecimalField("Стоимость места", max_digits=10 , decimal_places=2)
    status = models.CharField("Статус места", max_length=1, choices=STATUS_SEAT)

    def __str__(self):
        ans1 = "Место: " + str(self.seat_no)
        ans2 = "Класс: " + str(self.fare_conditions)
        ans3 = "Стоимость: " + str(self.amount_seat)
        return str(ans1+','+ans2+','+ans3)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"
        unique_together = (("aircraft_code", "seat_no"),)
