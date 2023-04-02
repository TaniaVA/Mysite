from django import forms
from .models import Master, Appointment
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time']
        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput(),
        }

class MasterForm(forms.ModelForm):
    pass

    class Meta:
        model = Master
        fields = ['name', 'photo', 'description', 'services', 'availability']




