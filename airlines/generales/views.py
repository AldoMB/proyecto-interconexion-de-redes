from django.shortcuts import render


# Create your views here.
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.utils import timezone
from vuelos.models import Vuelo, Avion, Aeropuerto
from django.views.generic import ListView
from django.db.models import Count, Sum, Avg, Min, Max


class prueba1(TemplateView):
    template_name = "prueba1.html"

class prueba2(TemplateView):
    template_name = "prueba2.html"

class prueba3(TemplateView):
    template_name = "prueba3.html"

class prueba4(TemplateView):
    template_name = "prueba4.html"

class prueba5(TemplateView):
    template_name = "prueba5.html"


class HomeView(TemplateView):
   template_name = 'home.html'


   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       ahora = timezone.now()


       # Próximos 5 vuelos ordenados por fecha de salida
       context['proximos_vuelos'] = (
           Vuelo.objects
                .filter(fecha_salida__gte=ahora)
                .select_related('origen', 'destino', 'avion')
                .order_by('fecha_salida')[:5]
       )


       # Flota: todos los aviones
       context['flota'] = Avion.objects.all()


       # Aeropuertos (únicos por ciudad–país)
       context['aeropuertos'] = Aeropuerto.objects.all()


       return context

class FlightListView(ListView):
   model               = Vuelo
   template_name       = "flight_list.html"
   context_object_name = "vuelos"
   paginate_by         = 10
 

   # ——— Filtra solo vuelos futuros —
   def get_queryset(self):
       return (super()
               .get_queryset()
               .filter(fecha_salida__gte=timezone.now())
               .select_related("origen", "destino", "avion")
               .order_by("fecha_salida"))


   # ——— Datos extra para la plantilla —
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       qs = self.object_list  # ya filtrado


       context.update({
           "total_vuelos": qs.count(),
           "precio_min": qs.aggregate(mi=Min("precio_base"))["mi"],
           "precio_max": qs.aggregate(ma=Max("precio_base"))["ma"],


           # Ciudades únicas para un posible filtro rápido
           "origenes":  qs.values("origen__ciudad", "origen__pais").distinct(),
           "destinos": qs.values("destino__ciudad", "destino__pais").distinct(),
       })
       return context

class AircraftListView(ListView):
    model               = Avion
    template_name       = "aircraft_list.html"
    context_object_name = "aviones"
    paginate_by         = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list

        context.update({
            "total_aviones": qs.count(),
            "capacidad_total": qs.aggregate(total=Sum("capacidad"))["total"],
            "capacidad_promedio": qs.aggregate(avg=Avg("capacidad"))["avg"],
            # Para mostrar cuántos modelos por fabricante
            "fabricantes": qs.values("fabricante")  # Cambio de 'value' a 'values'
                            .annotate(total=Count("id"))
                            .order_by("-total"),
        })
        return context
    
class AirportListView(ListView):
    model = Aeropuerto
    template_name = "airport_list.html"
    context_object_name = "aeropuertos"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.object_list

        context.update({
            "total_aeropuertos": qs.count(),
            "paises": qs.values("pais")
                        .annotate(total=Count("id"))
                        .order_by("pais"),
        })
        return context