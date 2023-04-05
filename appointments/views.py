from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .forms import AppointmentForm, MasterForm, ServiceForm
from .models import Appointment, Master, Service


class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_create.html'

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_update.html'

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('service_list')

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'

class MasterListView(ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'

    def get_queryset(self):
        return Master.objects.filter(services__pk=self.kwargs['service_id']).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        return context


class MasterCreateView(CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_create.html'

class MasterUpdateView(UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_update.html'

class MasterDeleteView(DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('master_list')

class MasterDetailView(DetailView):
    model = Master
    template_name = 'master_detail.html'
    context_object_name = 'master'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        return context

    def post(self, request, *args, **kwargs):
        master = self.get_object()
        service = get_object_or_404(Service, pk=self.kwargs['service_id'])
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.service = service
            appointment.master = master
            appointment.save()
            messages.success(request, 'Запись успешно создана!')
            return redirect('service_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
            return self.render_to_response(self.get_context_data(form=form))


class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_id'] = self.kwargs['service_id']
        context['pk'] = self.kwargs['pk']
        context['date'] = self.request.GET.get('date')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Запись успешно создана!')
            return self.form_valid(form)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
            return self.form_invalid(form)

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.service = get_object_or_404(Service, pk=self.kwargs['service_id'])
        appointment.master = get_object_or_404(Master, pk=self.kwargs['pk'])
        appointment.save()
        return super().form_valid(form)