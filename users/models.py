from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    description = models.CharField(max_length=1000, default="", null=True, blank=True, verbose_name="Descripcion")
    # utype = models.CharField(max_length=30, choices=[("member","socio"),("customer","cliente")])

    class Meta():
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username}"
       
    def get_complete_name(self):
        return f"{self.first_name} {self.last_name}"