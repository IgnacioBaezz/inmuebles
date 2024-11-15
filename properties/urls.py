from django.urls import path
from .views import *
from core.views import autocomplete_search

urlpatterns = [
    path("mis-propiedades/", owner_properties, name="owner-properties"),
    path("lista/", properties_list, name="properties-list"),
    path("detalle/<int:id>/", property_detail, name="property-detail"),
    path("añadir/", property_add, name="property-add"),
    path("editar/<int:pk>", property_edit, name="property-edit"),
    path("eliminar/<int:pk>", property_delete, name="property-delete"),
    path("busqueda/", autocomplete_search, name="search-url"),
    path("obtener-comunas/", get_communes, name="obtener-comunas"),
    path("panel-de-control/", dashboard, name="dashboard"),
    path("Busqueda/", property_search, name="property-search"),
]
