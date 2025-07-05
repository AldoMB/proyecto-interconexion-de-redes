from django.db import models

# Create your models here.
class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
       return f"{self.nombre} - {self.email}"
