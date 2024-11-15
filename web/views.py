from django.contrib.auth.decorators import login_required
from users.decorators import user_passes_test
from users.models import User
from django.shortcuts import render, redirect


def root(request):
    return redirect(index_view)


def index_view(request):
    context = {
        "title":"Inicio | Inmobiliaria Báez"
    }
    return render(request, "web/index.html", context)


def client_about(request):
    user_type = request.GET.get("user_type", None)
    context = {"user_type":user_type}
    title = "Acerca | Inmobiliaria Báez"
    if user_type is not None:
        if context["user_type"] == "member": 
            title = "Acerca de los socios | Inmobiliaria Báez"
        elif context["user_type"] == "customer":
            title = "Acerca de los clientes | Inmobiliaria Báez"
    
    context.update({
                "title":title,
            })
    
    return render(request, "web/about.html", context)



