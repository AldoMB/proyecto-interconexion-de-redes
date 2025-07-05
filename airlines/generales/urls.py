# generales/urls.py
from django.urls import path
from . import views


urlpatterns = [
   path('', views.HomeView.as_view(), name='home'),
   path("vuelos/", views.FlightListView.as_view(),   name="flight_list"),
   path("aircraft/", views.AircraftListView.as_view(), name="aircraft_list"),
   path("airport/", views.AirportListView.as_view(), name="airport_list"),
   path('prueba1', views.prueba1.as_view(), name='prueba1'),
   path('prueba2', views.prueba2.as_view(), name='prueba2'),
   path('prueba3', views.prueba3.as_view(), name='prueba3'),
   path('prueba4', views.prueba4.as_view(), name='prueba4'),
   path('prueba5', views.prueba5.as_view(), name='prueba5'),
]

