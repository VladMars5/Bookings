from django import forms

from .models import Tickets, Bookings

class AddTicketForm(forms.ModelForm):
    """Форма добавления пассажира"""
    class Meta:
        model = Tickets
        fields = ("passenger_id", "passenger_name", "contact_data", "seat_no", "fare_conditions", "amount_ticket")


