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
from django.http import HttpResponse
from tickets.decoradores import solo_organizadores
from tickets.decoradores import solo_asistentes
from django.shortcuts import get_object_or_404 #detalle de evento
from django.contrib import messages #eliminar evento


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
@solo_organizadores
def create_event_view(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        print("Método:", request.method)
        print("Datos POST:", request.POST)
        print("Archivos:", request.FILES)
        print("Formulario válido:", form.is_valid())
        print("Errores:", form.errors)
        if form.is_valid():
            nuevo_evento = form.save(commit=False)
            nuevo_evento.organizador = request.user

            print("Evento creado:", nuevo_evento.titulo)
            print("Organizador asignado:", nuevo_evento.organizador)
            print("Rol del usuario:", getattr(request.user, 'rol', 'sin rol'))

            nuevo_evento.save()
            return redirect('my_events')
    else:
        form = EventoForm()
    return render(request, 'eventos/create_event.html', {'form': form})


#Vista para el panel asistentes
@solo_asistentes
def panel_asistente(request):
    eventos = Evento.objects.filter(fecha__gte=timezone.now()).order_by('fecha')
    return render(request, 'tickets/panel_asistente.html', {'eventos': eventos})


#Vista para el panel organizador
@solo_organizadores
def panel_organizador(request):
    eventos = Evento.objects.filter(organizador=request.user).order_by('-fecha')
    return render(request, 'panel_organizador.html', {'eventos': eventos})


#Vista para usuario no autorizado
def no_autorizado(request):
    return HttpResponse(" No tienes permiso para acceder a esta vista.", status=403)

@solo_asistentes
def mis_boletos(request):
    boletos = Ticket.objects.filter(usuario=request.user).select_related('evento').order_by('-fecha_registro')
    return render(request, 'mis_boletos.html', {'boletos': boletos})

#Vista de Mis Eventos 
@solo_organizadores
def mis_eventos(request):
    eventos = Evento.objects.filter(organizador=request.user).order_by('-fecha')
    return render(request, 'eventos/mis_eventos.html', {'eventos': eventos})

#Vista de detalle de evento 
@solo_organizadores
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
    return render(request, 'eventos/detalle_evento.html', {'evento': evento})


#Eliminar los eventos creados
@solo_organizadores
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, organizador=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado correctamente.')
        return redirect('my_events')
    return render(request, 'eventos/eliminacion_evento.html', {'evento': evento})

#Acceso a los eventos disponibles
@solo_asistentes  
def eventos_disponibles(request):
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'eventos/eventos_disponibles.html', {'eventos': eventos})

#comprar boleto
@solo_asistentes
def comprar_boleto(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        Boleto.objects.create(evento=evento, usuario=request.user)
        messages.success(request, '¡Boleto comprado exitosamente!')
        return redirect('eventos_disponibles')
    return render(request, 'eventos/confirmar_compra.html', {'evento': evento})




    



