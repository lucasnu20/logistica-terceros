from django.db import models


class Tercero(models.Model):
    nombre = models.CharField(max_length=255)
    cuit = models.CharField(max_length=20, unique=True)
    contacto_principal = models.CharField(max_length=255)
    email = models.EmailField()
    telefono = models.CharField(max_length=50)
    direccion = models.TextField(blank=True)
    region = models.IntegerField(help_text="Código de región/provincia (ej. 1 para Buenos Aires, etc.)")

    def __str__(self):
        return self.nombre