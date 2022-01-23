from django.contrib import admin
from .models import Bookings,Tickets, Flights,Airports,Aircrafts,Seats



@admin.register(Flights)
class FlightsAdmin(admin.ModelAdmin):
    list_display = ("flight_id","flight_no", "departure_airport", "arrival_airport","scheduled_departure_date")

@admin.register(Seats)
class SeatsAdmin(admin.ModelAdmin):
    list_display = ("seat_no", "aircraft_code", "status")

# Register your models here.
admin.site.register(Bookings)
admin.site.register(Tickets)
# admin.site.register(Flights)
admin.site.register(Airports)
admin.site.register(Aircrafts)
# admin.site.register(Seats)

