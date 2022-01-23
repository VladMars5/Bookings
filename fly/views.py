from django.shortcuts import render, redirect
from .models import Flights, Airports, Aircrafts, Seats, Tickets, Bookings
from django.views.generic.base import View
from datetime import date

from django.views.generic import ListView, DetailView

import string
import random

from django.contrib import messages

# Create your views here.

def get(request):
    num_visits = request.session.get('num_visits', 0)#подсчет кол-ва подключений к сервису всего через сессии
    request.session['num_visits'] = num_visits + 1

    all_fly_10 = Flights.objects.all()[:10]

    if request.method == 'POST':
        iz_goroda = request.POST['iz_goroda']
        v_gorod = request.POST['v_gorod']
        date = request.POST['date']
        iz_city = Airports.objects.get(city__iexact = iz_goroda).airport_code
        v_city = Airports.objects.get(city__iexact = v_gorod).airport_code
        print(iz_city,v_city)
        
        flyits = Flights.objects.filter(departure_airport = iz_city, arrival_airport=v_city, scheduled_departure_date=date)
        
        if flyits == None:
            return render(request, "fly/index.html", {'num_visits': num_visits})
        else:
            return render(request, "fly/index.html", {"flights": flyits, 'num_visits': num_visits , 'all_fly_10': all_fly_10})
    return render(request, "fly/index.html", {'num_visits': num_visits, 'all_fly_10': all_fly_10})


class FlyDetailView(View):
    """Полное описание полета"""
    def get(self, request, slug):
        slug = slug.split("_")
        fly = Flights.objects.get(flight_id = slug[0], flight_no = slug[1])#некоторое число которое передаем через url
        
        seats = Seats.objects.filter(aircraft_code = fly.aircraft_code, status = 'F')
        
        if not seats.exists(): #проверяет queryset на пустоту
            return render(request, "fly/book.html", {"fly": fly, "seats": seats , "seats_none": "Мест нет"})
        else:
            return render(request, "fly/book.html", {"fly": fly, "seats": seats})

class AddTicket(View):
    """Добавление билета после отправки формы"""
    def post(self, request, pk):

        fly_id = Flights.objects.get(flight_id=pk)
        last_name = request.POST['last name']
        first_name = request.POST['first name']
        contact_data =request.POST['contact']
        seat_no = str(request.POST['seat']).split(",")[0].split(" ")[1]
        fare_conditions = str(request.POST['seat']).split(",")[1].split(" ")[1]
        amount_ticket = str(request.POST['seat']).split(",")[2].split(" ")[1]

        book_ref_gen = 6
        book_ref_gen_str = str(''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=book_ref_gen)))

        ticket_no_gen = 13
        ticket_no_gen_str = str(''.join(random.choices(string.digits, k=ticket_no_gen)))

        Bookings.objects.create(book_ref=book_ref_gen_str, total_amount=amount_ticket)
        book_ref_id = Bookings.objects.get(book_ref=book_ref_gen_str)
        Tickets.objects.create(ticket_no=ticket_no_gen_str, flight_id = fly_id, book_ref=book_ref_id, passenger_last_name=last_name,\
                               passenger_name=first_name, contact_data = contact_data, seat_no = seat_no,\
                               fare_conditions = fare_conditions, amount_ticket = amount_ticket)

        #Обновляет запись в бд о статусе места в самолете
        aircraft = fly_id.aircraft_code
        obj_seat = Seats.objects.get(aircraft_code= aircraft, seat_no = seat_no)
        obj_seat.status ='B'
        obj_seat.save()

        messages.info(request, f'Ваш билет успешно оформлен. Номер вышего билета {ticket_no_gen_str}. Номер брони: {book_ref_gen_str}')
        return redirect("/")


def about(request):
    return render(request, 'fly/safety.html')

def contacts(request):
    return render(request, 'fly/contacts.html')