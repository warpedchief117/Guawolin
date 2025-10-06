from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    event_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.event_name} - {self.user.username}"

    class Meta:
        app_label = 'tickets'

