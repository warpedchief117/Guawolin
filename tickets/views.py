from urllib import request
from django.shortcuts import render,redirect
from . models import Ticket, Usuario
from django.contrib import messages
from django.shortcuts import render
from .forms import RegisterAssistantForm, RegisterOrganizerForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from tickets import views
from tickets.forms import EventoForm
from .models import Evento


def home(request):
    return render(request, 'guawolin/home.html')

#Funcion para registrar asistentes
    
def registerAssistant(request):
    if request.method == 'POST':
        form = RegisterAssistantForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if Usuario.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif Usuario.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
                user = form.save(commit=False)
                user.rol = 'asistente'
                user.set_password(form.cleaned_data['password'])
                user.save()

                grupo, _ = Group.objects.get_or_create(name='Asistentes')
                user.groups.add(grupo)

                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('login')
    else:
        form = RegisterAssistantForm()

    return render(request, 'tickets/ReAssistant.html', {'form': form})


#Funcion para registrar organizadores

def registerOrganizer(request):
    if request.method == 'POST':
        form = RegisterOrganizerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if Usuario.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            elif Usuario.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado.')
            else:
                user = form.save(commit=False)
                user.rol = 'organizador'
                user.set_password(form.cleaned_data['password'])
                user.save()

                grupo, _ = Group.objects.get_or_create(name='Organizadores')
                user.groups.add(grupo)

                messages.success(request, 'Organizador registrado exitosamente.')
                return redirect('login')
        else:
            messages.error(request, 'Corrige los errores en el formulario.')
    else:
        form = RegisterOrganizerForm()

    return render(request, 'tickets/ReOrganizer.html', {'form': form})



#view para la configuracion del perfil
def profile_settings(request):
    return render(request, 'tickets/profile_settings.html')

#view para mis_eventos
@login_required
def my_events(request):
    if request.user.rol != 'organizador':
        return redirect('home')
    return render(request, 'tickets/mis_eventos.html')

#view para reportes
@login_required
def reports(request):
    if request.user.rol != 'organizador':
        return redirect('home')
    return render(request, 'tickets/reportes.html')

def my_tickets(request):
    if request.user.rol != 'asistente':
        return redirect('home')
    return render(request, 'tickets/mis_tickets.html')

def events(request):
    return render(request, 'tickets/eventos.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # ✅ Asegúrate de que 'home' esté definida en urls.py
  

#view para crear eventos
def create_event_view(request):
    form = EventoForm()
    return render(request, 'eventos/create_event.html', {'form': form})


