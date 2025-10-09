from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('comprar/', views.purchase_ticket, name='purchase_ticket'),
    path('confirmacion/', views.ticket_confirmation, name='ticket_confirmation'),
    path('mis-tickets/', views.my_tickets, name='my_tickets'),
    path('concursos/', views.concursos_view, name='concursos'),
    path('noticias/', views.noticias_view, name='noticias'),
    path('foro/', views.foro_view, name='foro'),
]
