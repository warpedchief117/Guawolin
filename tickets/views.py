from django.shortcuts import render,redirect
from .forms import TicketForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'guawolin/home.html')

@login_required
def purchase_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Asigna el usuario actual
            ticket.save()
            return redirect('ticket_confirmation')
    else:
        form = TicketForm()
    return render(request, 'tickets/purchase_form.html', {'form': form})

@login_required
def ticket_confirmation(request):
    return render(request, 'tickets/confirmation.html')

@login_required
def my_tickets(request):
    tickets = request.user.ticket_set.order_by('-purchase_date')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})

def register(request):
    form = UserCreationForm()
    return render(request, 'guawolin/register.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'evento/dashboard.html')

def ticket_purchase(request):
    return render(request, 'tickets/comprar.html')

def concursos_view(request):
    return render(request, 'tickets/concursos.html')

def noticias_view(request):
    return render(request, 'tickets/noticias.html')

def foro_view(request):
    return render(request, 'tickets/foro.html')