from django.urls import path
from .views import *


urlpatterns = [
    path("", root),
    path("inicio/", index_view, name="index-url"),
    path("cliente/", client_about, name="client-url")
]
