from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from tickets.views import home
from tickets.views import register
from tickets.views import dashboard_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),  # Esto hace que la raíz muestre tu pantalla principal
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),# ← esta línea es clave para la vinculación al menu  
    path('tickets/', include('tickets.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='guawolin/login.html'), name='login'),
]
