from django import forms
from .models import Appointment
from .models import Master
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser

class AppointmentForm(forms.ModelForm):
    time = forms.TimeField()

    class Meta:
        model = Appointment
        fields = ['service', 'master', 'date', 'time']



