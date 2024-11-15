from django.shortcuts import render
from django.http import JsonResponse
from properties.models import Property

def autocomplete_search(request):
    context = {
        "title": "Busqueda | Báez Inmobiliaria"
    }
    query = request.GET.get("q")
    if query:
        results = Property.objects.filter(name__icontains=query)
        context.update = {
            "query":query,
            "results":results
        }
        return render(request, "core/search.html", context)
    context["query"] = []
    return render(request, "core/search.html", context)
