from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.

class Objetivo(models.Model):
    descripcion = models.CharField(max_length=50)
    fecha_inicio = models.DateField(default=datetime.now)
    fecha_fin = models.DateField(default=datetime.now)
    # contador cuenta las veces que se ha completado el objetivo
    contador = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.descripcion