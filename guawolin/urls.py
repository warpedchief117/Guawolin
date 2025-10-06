from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from tickets.views import home
from tickets.views import register
from tickets.views import dashboard_view


urlpatterns = [
    path('', home, name='home'),  # Esto hace que la raíz muestre tu pantalla principal
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),  # ← esta línea conecta la app de tickets
    path('accounts/', include('django.contrib.auth.urls')),  # ← esta línea es clave para usuarios no identifcados
    path('register/', register, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),# ← esta línea es clave para la vinculación al menu  
    path('tickets/', include('tickets.urls')),
]
