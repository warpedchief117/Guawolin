from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('registro-asistente/', views.registerAssistant, name='register_assistant'),
    path('registro-organizador/', views.registerOrganizer, name='register_organizer'),
    path('mis_tickets/', views.my_tickets, name='my_tickets'),         # Asistente
    path('mis_eventos/', views.my_events, name='my_events'),
    path('eventos/', views.events, name='events'),           # Organizador
    path('reportes/', views.reports, name='reports'),              
]
