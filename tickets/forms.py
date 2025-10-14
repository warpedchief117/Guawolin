from django import forms
from .models import Usuario
from .models import Evento


class RegisterAssistantForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label='Contraseña'
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Usuario',
            'email': 'Correo electrónico',
        }

class RegisterOrganizerForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        label='Contraseña'
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Usuario',
            'email': 'Correo electrónico',
        }

class EventoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'datetime-local' , 'class': 'input-fecha'})
    )

    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha', 'lugar', 'imagen']



def create_event_view(request):
    form = EventoForm()
    return render(request, 'tickets/create_event.html', {'form': form})


