from django import forms
from .models import Master, Appointment, Service
from django.forms import TimeField

# Time selection field for the appointment form.
class TimeSelectField(TimeField):
    widget = forms.Select

    def __init__(self, choices=(), **kwargs):
        super().__init__(**kwargs)
        self.widget.choices = choices

# A form to create an appointment.
class AppointmentForm(forms.ModelForm):
    time = TimeSelectField(choices=[])

    class Meta:
        model = Appointment
        fields = ['service', 'master', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

# Form to create a master.
class MasterForm(forms.ModelForm):
    pass

    class Meta:
        model = Master
        fields = ['name', 'photo', 'description', 'services', 'availability']

# Form to create a sevice.
class ServiceForm(forms.ModelForm):
    pass

    class Meta:
        model = Service
        fields = ['name', 'price', 'duration', ]


