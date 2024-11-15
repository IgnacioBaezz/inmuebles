from django.urls import reverse_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Property, Commune, Region, PropertyPrice
from .services import export_properties_from_commune, export_properties_from_region
from django.core.paginator import Paginator
from .forms import PropertyForm, PropertyPriceForm, SearchForm
from users.decorators import group_required
from users.models import User
from django.http import JsonResponse

@login_required
def owner_properties(request):
    pk_owner = request.user.id
    username = request.user.username
    properties = Property.objects.filter(owner_id=pk_owner, active=True)
    context = {
        "title":f"Inmuebles {username} | Inmobiliaria Báez",
        "properties": properties
    }
    return render(request, "properties/properties_owner.html", context)

@login_required
def property_delete(request, pk):
    property_instance = Property.objects.get(pk=pk)
    property_instance.active = False
    property_instance.save()
    return redirect(owner_properties)

@login_required
def property_add(request):
    if request.method == "POST":
        property_form = PropertyForm(request.POST)
        price_form = PropertyPriceForm(request.POST)
        
        if property_form.is_valid() and price_form.is_valid():
            property_instance = property_form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()
            price_instance = price_form.save(commit=False)
            price_instance.property = property_instance
            price_instance.save()
            return redirect(owner_properties)
    else:
        prop_form = PropertyForm()
        price_form = PropertyPriceForm()

    regiones = Region.objects.all()
    comunas = Commune.objects.all()
    comunas_por_region = {
        region.id: [{"id": comuna.id, "nombre": comuna.name} for comuna in comunas if comuna.region_id == region.id]
        for region in regiones
    }
    context = {
        "title": "Agregar Inmueble | Báez Inmobiliaria",
        "prop_form": prop_form,
        "price_form": price_form,
        "comunas_por_region":comunas_por_region
    }
    return render(request, "properties/property_add.html", context)

@login_required
def property_edit(request, pk):
    prop_instance = get_object_or_404(Property, pk=pk)
    prop_price_instance = get_object_or_404(PropertyPrice, property=pk)
    regiones = Region.objects.all()
    comunas = Commune.objects.all()
    comunas_por_region = {
        region.id: [{"id": comuna.id, "nombre": comuna.name} for comuna in comunas if comuna.region_id == region.id]
        for region in regiones
    }
    if request.method == "POST":
        prop_form = PropertyForm(request.POST, instance=prop_instance)
        price_form = PropertyPriceForm(request.POST, instance=prop_price_instance)
        if prop_form.is_valid() and price_form.is_valid():
            prop_form.active = True
            prop_form.save()
            price_form.save()
            return redirect(owner_properties)
    else:
        prop_form = PropertyForm(instance=prop_instance)
        price_form = PropertyPriceForm(instance=prop_price_instance)

    context = {
        "title":f"Editar {prop_instance.name} | Báez Inmobiliaria",
        "property":prop_instance,
        "prop_form": prop_form,
        "price_form": price_form,
        "comunas_por_region":comunas_por_region
    }
    return render(request, "properties/property_edit.html", context)

def properties_list(request):
    if request.method == "GET":
        filter_prop = request.GET.get("filter", None)
        page = request.GET.get("page", 1)

        if filter_prop == "region":
            properties_dict = export_properties_from_region() 
            properties = []
            for region_props in properties_dict.values():
                properties.extend(region_props)  
        elif filter_prop == "comuna":
            properties_dict = export_properties_from_commune() 
            properties = []  
            for commune_props in properties_dict.values():
                properties.extend(commune_props)  
        else:
            properties = Property.objects.filter(active=True)

        if not isinstance(properties, list):
            paginator = Paginator(properties, 6)
        else:
            paginator = Paginator(properties, 6)
        try:
            properties = paginator.get_page(page)
        except:
            properties = paginator.page(1)
        
        context = {
            "title": "Inmuebles | Inmobiliaria Báez",
            "propiedades": properties,
            "filter": filter_prop
        }

        return render(request, "properties/properties_list.html", context)

@login_required
def property_detail(request, id):
    property = get_object_or_404(Property, id=id)
    context = {
        "title":f"Detalle {property.name} | Inmobiliaria Báez",
        "property":property
    }
    return render(request, 'properties/property_detail.html', context)

@login_required
def dashboard(request):
    user = request.user
    try:
        group = user.groups.get(name="arrendadores")
    except:
        group = "lala"
    form = SearchForm()
    properties = Property.objects.filter(owner_id=user.id, active=True)
    sell_properties = []
    lease_properties = []
    for x in properties:
        if x.price.status_price == "sell":
            sell_properties.append(x)
        elif x.price.status_price == "lease":
            lease_properties.append(x)
    context = {
        "title": "Panel de control | Inmobiliaria Báez",
        "properties":properties[:5],
        "properties_data":[len(properties),len(sell_properties), len(lease_properties)],
        "user_group":group,
        "form":form
    }
    return render(request, "properties/dashboard.html", context) 
    
def property_search(request):
    form = SearchForm(request.GET)
    properties = Property.objects.all()
    context = {
        "title": "Busqueda | Inmobiliaria Báez",
        "form": form,
    }
    commune = request.GET.get('commune', None)
    property_type = request.GET.get('property_type', None)
    max_price = request.GET.get('max_price', None)
    if commune is not None:
        properties = properties.filter(commune=commune)
    if property_type is not None:
        properties = properties.filter(property_type=property_type)
    if max_price is not None:
        properties = properties.filter(price__sale_price__lte=max_price)
    context["properties"] = properties

    return render(request, "properties/property_search.html", context)
    
def get_communes(request):
    region_id = request.GET.get("region_id")
    comunas = Commune.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(comunas), safe=False)


def property_proposal(request, id_user, id_property):
    pass