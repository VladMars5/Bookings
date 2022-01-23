from django.urls import path

from . import views

urlpatterns =[
    path("", views.get, name="index"),
    path("about/",  views.about),
    path("contacts/",  views.contacts),
    path("<int:pk>/",  views.AddTicket.as_view(), name="add_ticket"),
    path("<slug:slug>/",  views.FlyDetailView.as_view(), name="flight_detail"),
]