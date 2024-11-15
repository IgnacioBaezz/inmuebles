from django.core.exceptions import ValidationError
from django.db import models
from users.models import User

class PositiveFieldsMixin:
    def validate_positive_fields(self, *fields):
        for field in fields:
            value = getattr(self, field, None)
            if value is not None and value < 0:
                raise ValidationError(f"El valor del campo {field} no puede ser negativo.")
            
            
class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "Región"
        verbose_name_plural = "Regiones"

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"

    def __str__(self):
        return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    class Meta:
        verbose_name = "Tipo de inmueble"
        verbose_name_plural = "Tipos de inmuebles"

    def __str__(self):
        return self.name

class PropertyStatus(models.TextChoices):
    AVAILABLE = "available", "Disponible"
    RENTED = "rented", "Arrendado"
    SOLD = "sold", "Vendido"

class Property(models.Model, PositiveFieldsMixin):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, verbose_name="Comuna")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Region")
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, verbose_name="Tipo de propiedad")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Propietario")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    address = models.CharField(max_length=200, verbose_name="Dirección")
    m2_built = models.FloatField(verbose_name="Metros cuadrados construidos")
    m2_totals = models.FloatField(verbose_name="Metros cuadrados totales")
    active = models.BooleanField(default=True, verbose_name="Activo")
    status = models.CharField(max_length=20, choices=PropertyStatus.choices, default=PropertyStatus.AVAILABLE, verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de última actualización", null=True, blank=True)

    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"
    
    def __str__(self):
        return self.name

    def clean(self):
        self.validate_positive_fields("m2_built", "m2_totals")
        if self.m2_built > self.m2_totals:
            raise ValidationError("Los metros cuadrados construidos no pueden ser mayores que los metros cuadrados totales.")

class PropertyPrice(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='price')
    status_price = models.CharField(max_length=30 ,choices=[("sell","venta"), ("lease","arriendo")], default="lease")
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio mensual")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Precio de venta")

    class Meta:
        verbose_name = "Precio de Propiedad"
        verbose_name_plural = "Precios de Propiedades"

    def __str__(self):
        return f"Precios de {self.property.name}"

class Proposal(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="proposals")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals")
    message = models.TextField(verbose_name="Mensaje", default="", null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("pending", "Pendiente"), ("accepted", "Aceptada"), ("rejected", "Rechazada")], default="pending")
    date_sent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Propuesta"
        verbose_name_plural = "Propuestas"

    def __str__(self):
        return f"Propuesta para {self.property.name} por {self.client.username}"