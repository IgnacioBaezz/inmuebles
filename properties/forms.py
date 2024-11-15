from django import forms
from .models import Property, PropertyPrice, Commune, PropertyType

from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ["owner","active"]
        fields = ["commune","region","property_type","owner","name","description","address","m2_built","m2_totals","active"]
        widgets = {
            "commune": forms.Select(attrs={"class": "form-select"}),
            "region": forms.Select(attrs={"class": "form-select"}),
            "property_type": forms.Select(attrs={"class": "form-select"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la propiedad"}),
            "description": forms.Textarea(attrs={"class": "form-control","rows": 4,"placeholder": "Descripción de la propiedad..."}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Dirección de la propiedad"}),
            "m2_built": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": 0.01}),
            "m2_totals": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": 0.01}),
        }
        labels = {
            "Commune":"Comuna",
            "region":"Region",
            "property_type":"Tipo de Propiedad",
            "name":"Nombre",
            "description":"Descripcion",
            "address":"Dirección",
            "m2_built":"Metros cuadrados construidos",
            "m2_totals":"Metros cuadrados totales",
        }

class PropertyPriceForm(forms.ModelForm):
    class Meta():
        model = PropertyPrice
        exclude = ["property"]
        fields = ["property","monthly_price","sale_price", "status_price"]
        widgets = {
            "property":forms.Select(attrs={"class":"form-select"}),
            "monthly_price":forms.NumberInput(attrs={"class":"form-control"}),
            "sale_price":forms.NumberInput(attrs={"class":"form-control"}),
            "status_price":forms.Select(attrs={"class":"form-select"})
        }
        labels = {
            "property":"Propiedad",
            "monthly_price":"Precio Mensual",
            "sale_price":"Precio de Venta",
            "status":"Estado"
        }

class SearchForm(forms.Form):
    commune = forms.ModelChoiceField(
        queryset=Commune.objects.all(), 
        required=False, 
        label="Comuna", 
        widget= forms.Select(attrs={"class":"form-select"})
    )
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(), 
        required=False, 
        label="Tipo de propiedad",
        widget= forms.Select(attrs={"class":"form-select"})
    )
    max_price = forms.DecimalField(
        required=False, 
        max_digits=10, 
        decimal_places=2, 
        label="Precio máximo",
        widget= forms.NumberInput(attrs={"class":"form-control"})
    )