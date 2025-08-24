from django.db import models
from django.core.exceptions import ValidationError


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
    

class UnidadMedida(models.TextChoices):
    KILOGRAMOS = 'kg', 'Kilogramos'
    LITROS = 'lt', 'Litros'
    UNIDADES = 'un', 'Unidades'
    CAJAS = 'cj', 'Cajas'

class Material(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, db_index=True)
    descripcion = models.TextField(blank=True, null=True)
    
    tercero = models.ForeignKey(
        'Tercero', 
        on_delete=models.CASCADE, 
        related_name="materiales"
    )
    categoria = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    
    unidad_medida = models.CharField(
        max_length=20, 
        choices=UnidadMedida.choices, 
        default=UnidadMedida.UNIDADES
    )
    
    peso_neto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    peso_bruto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    volumen = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    alto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    largo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    condiciones_almacenamiento = models.CharField(max_length=100, blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True, unique=True)
    valor_declarado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=10, default="ARS")
    
    activo = models.BooleanField(default=True, db_index=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.tercero.nombre})"

    def clean(self):
        """Validaciones automáticas antes de guardar"""
        # Peso bruto no puede ser menor que el neto
        if self.peso_bruto and self.peso_neto and self.peso_bruto < self.peso_neto:
            raise ValidationError("El peso bruto no puede ser menor al peso neto.")
        
        # Si se definen dimensiones, volumen se calcula automáticamente (en m³)
        if self.alto and self.ancho and self.largo:
            calculated_volume = self.alto * self.ancho * self.largo / 1000000  # mm³ -> m³
            if not self.volumen or abs(self.volumen - calculated_volume) > 0.001:
                self.volumen = calculated_volume