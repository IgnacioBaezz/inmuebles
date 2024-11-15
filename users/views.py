from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy as _
from django.contrib import messages

from .services import asign_group_member, asign_group_customer
from .forms import UserRegisterForm, UserProfileForm, UserLoginForm
from web.views import index_view
from .models import User
from time import sleep
from properties.views import dashboard
# Vista basada en función


def register_user(request):
    user_type = request.GET.get("user_type", None)
    context = {"user_type":user_type}
    if user_type is not None:
        if context["user_type"] == "member": 
            message1 = "Únete a nuestro grupo de socios"
            message2 = "Gestiona tus propiedades"
            title = "Registro Socio | Inmobilaria Báez"
        elif context["user_type"] == "customer":
            message1 = "Hazte cliente"
            message2 = "Obtén beneficios exclusivos y promociones"
            title = "Registro Cliente | Inmobilaria Báez"
    else: 
        return redirect("client-url")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        context["form"] = form
        if form.is_valid():
            user = form.save()
            if user_type == "member":
                asign_group_member(user)
            elif user_type == "customer":
                asign_group_customer(user)
            else:
                return redirect('error_page') # No implementado
            context["form"] = form
            login(request, user)
            return redirect(dashboard)
    else:
        context["form"] = UserRegisterForm

    context.update({
                "title":title,
                "message1":message1,
                "message2":message2,
            })
    return render(request, "users/register.html", context)

@login_required
def logout_user(request):
    logout(request)
    return redirect(dashboard)


def login_user(request):
    context = {
        "form":UserLoginForm,
        "title":"Login",
        "error":"El usuario o contraseña son incorrectos"
    }
    if request.method == "GET":
        return render(request, "users/login.html", context)
    else:
        username = request.POST["username"]
        user = User.objects.get(username=username)
        user.password == request.POST["password"]
        # user = authenticate(request,username=request.POST["username"],password=request.POST["password"])
        if user == None:
            return render(request, "web/index.html", context)
        else:
            login(request, user)
            return redirect(dashboard)

@login_required
def profile_user(request):
    user = request.user
    form = UserProfileForm(instance=user)
    user_groups = user.groups.all()
    user_keys = ["Nombre de usuario", "Nombre", "Apellido", "Correo electrónico", "Descripción"]
    user_list = [user.username, user.first_name, user.last_name, user.email, user.description]
    usuario_info = dict(zip(user_keys, user_list))

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, "Tu perfil ha sido actualizado exitosamente.")
                return redirect(profile_user)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")

    context = {
        "title": f"Perfil {user.username} | Báez Inmobiliaria",
        "usuario_info": usuario_info,
        "user_groups": user_groups,
        "form": form,
    }
    return render(request, "users/profile.html", context)