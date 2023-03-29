from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from .models import Appointment, Master, Service
from .forms import AppointmentForm, MasterForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    template_name = 'service_edit.html'
    fields = ['name', 'price', 'duration',]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    template_name = "service_new.html"
    fields = ['name', 'price', 'duration',]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')

class MasterListView(ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'

class MasterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Master
    template_name = 'master_edit.html'
    form_class = MasterForm

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

class MasterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Master
    template_name = "master_new.html"
    fields = ['image', 'name',]

class MasterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('master_list')

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointment_detail.html"

class AppointmentCreateView(CreateView):
    model = Appointment
    fields = ['service', 'master', 'date', 'time']
    success_url = reverse_lazy('appointment_list')

class AppointmentListView(ListView):
    model = Appointment

@login_required
def appointment_create(request):
    AppointmentFormSet = formset_factory(AppointmentForm, extra=0)

    if request.method == 'POST':
        formset = AppointmentFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                appointment = form.save(commit=False)
                appointment.user = request.user
                appointment.save()
            messages.success(request, 'Appointments have been created.')
            return redirect('appointment_list')
    else:
        formset = AppointmentFormSet()

    return render(request, 'appointments/appointment_create.html', {'formset': formset})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ['service', 'master', 'date', 'time']
    success_url = reverse_lazy('appointment_list')

class AppointmentDeleteView(DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointment_list')

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk, user=request.user)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment has been deleted.')
        return redirect('appointment_list')
    return render(request, 'appointments/appointment_delete.html', {'appointment': appointment})
