from django.db import models


class Aeropuerto(models.Model):
        nombre = models.CharField(max_length=100)
        ciudad = models.CharField(max_length=100)
        pais = models.CharField(max_length=100)

        def __str__(self):
            return f"{self.nombre} ({self.ciudad}, {self.pais})"

class Avion (models.Model):
     modelo = models.CharField(max_length=100)
     capacidad = models.IntegerField()
     fabricante = models.CharField(max_length=100)
     def __str__(self):
          return f"{self.modelo} ({self.fabricante})"


class Vuelo(models.Model):
      codigo = models.CharField(max_length=10, unique=True)
      origen = models.ForeignKey(Aeropuerto, related_name= "salidas", on_delete=models.CASCADE)
      destino = models.ForeignKey(Aeropuerto, related_name= "llegadas", on_delete=models.CASCADE)
      avion = models.ForeignKey(Avion, on_delete=models.SET_NULL, null=True)
      fecha_salida = models.DateTimeField()
      duracion_estimada = models.DurationField()
      precio_base = models.DecimalField(max_digits=10, decimal_places=2)

      def __str__(self):
            return f"{self.codigo}: {self.origen} -> {self.destino}"
      
class Pasajero (models.Model):
      nombre = models.CharField(max_length=100)
      apellido = models.CharField(max_length=100)
      email = models.EmailField()
      telefono = models.CharField(max_length=15)

      def __str__(self):
            return f"{self.nombre} {self.apellido}"
      
class Reserva(models.Model):
      pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
      vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
      fecha_reserva = models.DateTimeField(auto_now_add=True)
      codigo_confirmacion = models.CharField(max_length=12, unique=True)

      def __str__(self):
            return f"Reserva {self.codigo_confirmacion} -> {self.pasajero}"
      
class Asiento (models.Model):
      vuelo = models.ForeignKey(Vuelo,on_delete=models.CASCADE)
      numero = models.CharField(max_length=5)
      clase = models.CharField(max_length=20, choices=[('economica', 'Economica', ), ('ejecutiva', 'Ejecutiva')]) 
      reservado = models.BooleanField(default=False)

      def __str__(self):
          return f"Asiento {self.numero} -> {self.vuelo.codigo}"

class CheckIn(models.Model):
      reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE)
      fecha_checkin = models.DateTimeField(auto_now_add=True)
      asiento = models.OneToOneField(Asiento, on_delete=models.SET_NULL, null=True)

      def __str__(self):
            return f"Check-in de {self.reserva}"

class Equipaje(models.Model):
      checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE)
      peso = models.DecimalField(max_digits=5, decimal_places=2)
      tipo = models.CharField(max_length=20, choices= [('cabina', 'Cabina'), ('documento', 'Documento')])

      def __str__(self):
            return f"{self.tipo} -> {self.peso} kg"
      
      
           
      