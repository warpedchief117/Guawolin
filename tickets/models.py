from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

# Modelo personalizado de usuario
class Usuario(AbstractUser):
    email = models.EmailField(unique=True)

    ROLES = (
        ('organizador', 'Organizador'),
        ('asistente', 'Asistente'),
    )
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.username} ({self.rol})"

# Modelo de evento
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='eventos_creados')  # ✅

    def __str__(self):
        return self.titulo

# Modelo de ticket
class Ticket(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='tickets')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirmado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} – {self.evento.titulo}"


