from django.db import models
from django.contrib.auth.models import AbstractUser
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

# Modelo de ticket
class Ticket(models.Model):
    event_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event_name} - {self.user.username}"

