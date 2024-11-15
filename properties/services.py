from .models import Property, Region, Commune

def export_properties_from_commune(save_file=False) -> dict:
    properties = Property.objects.filter(active=True).select_related("commune","price")
    properties_from_commune = {}
    
    for property in properties:
        commune = property.commune
        if commune.name not in properties_from_commune:
            properties_from_commune[commune.name] = []
        properties_from_commune[commune.name].append({
            "commune":commune.name,
            "id":property.id,
            "name": property.name,
            "description": property.description,
            "monthly_price":property.price.monthly_price,
            "sale_price":property.price.sale_price,
            "status_price":property.price.status_price
        })

    if save_file is True:
        with open("data_management/consultas/properties_from_commune.txt", "w", encoding="utf-8") as archivo:
            for commune_name, properties in properties_from_commune.items():
                archivo.write(f"---Commune: {commune_name}\n")
                for idx, prop in enumerate(properties, 1):
                    archivo.write(f"Property {idx}\n -Name: {prop['name']}\n -Description: {prop["description"]}\n")
                archivo.write("\n")

    return properties_from_commune


def export_properties_from_region(save_file=False) -> dict:
    properties = Property.objects.filter(active=True).select_related("region", "price")
    properties_from_region = {}
    
    for property in properties:
        region = property.region
        if region.name not in properties_from_region:
            properties_from_region[region.name] = []
        properties_from_region[region.name].append({
            "region":region.name,
            "id":property.id,
            "name": property.name,
            "description": property.description,
            "monthly_price": property.price.monthly_price,
            "sale_price": property.price.sale_price,
            "status_price":property.price.status_price
        })

    if save_file is True:
        with open('data_management/consultas/properties_from_region.txt', 'w', encoding='utf-8') as archivo:
            for region_name, properties in properties_from_region.items():
                archivo.write(f"---Region: {region_name}\n")
                for idx, prop in enumerate(properties, 1):
                    archivo.write(f"Property {idx}\n -Name: {prop['name']}\n -Description: {prop["description"]}\n")
                    archivo.write(f" -Monthly Price: {prop["monthly_price"]}\n -Sale Price: {prop["sale_price"]}\n")
                archivo.write("\n")

    return properties_from_region
