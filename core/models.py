from django.db.models import Model, EmailField, CharField, TextField

class ContactForm(Model):
    customer_email = EmailField(verbose_name="Correo Cliente")
    customer_name = CharField(max_length=64)
    message = TextField(verbose_name="Mensaje")

    class Meta():
        verbose_name = "Formulario de Contacto"
        verbose_name_plural = "Formularios de Contacto"