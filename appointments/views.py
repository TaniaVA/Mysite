from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

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
    success_url = reverse_lazy('master_list')


class MasterUpdateView(UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_update.html'
    success_url = reverse_lazy('master_list')

    def get_object(self):
        return get_object_or_404(Master, pk=self.kwargs['pk'])

    def form_valid(self, form):
        master = form.save(commit=False)
        photo = form.cleaned_data['photo']
        if photo:
            file_name = default_storage.save(photo.name, ContentFile(photo.read()))
            master.photo = file_name
        master.save()
        return super().form_valid(form)


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
        master = self.get_object()
        schedule_dict = master.get_schedule_dict()
        context['schedule_dict'] = schedule_dict
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
    template_name = 'appointment_create.html'
    success_url = reverse_lazy('appointment_create_success')

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # добавляем время в контекст шаблона
        context['time'] = self.request.POST.get('time')
        return self.render_to_response(context)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {
            'master': self.get_object(),
            'service': get_object_or_404(Service, pk=self.kwargs['service_id'])
        }
        return kwargs

    def get_object(self):
        return get_object_or_404(Master, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Запись успешно создана!')
            return self.form_valid(form)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.object:
            return reverse('appointment_create_success', kwargs={'pk': self.object.pk})
        else:
            return reverse_lazy('appointment_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['service_id'])
        master = get_object_or_404(Master, pk=self.kwargs['pk'])
        schedule_dict = master.get_schedule_dict()
        context['schedule_dict'] = schedule_dict

        # let's add time options for the time form field
        available_times = []
        for schedule in schedule_dict.values():
            for time, status in schedule.items():
                if status == 'available':
                    available_times.append((time, time))
        context['form'].fields['time'].widget.choices = available_times

        context['object'] = self.object

        return context

class AppointmentCreateSuccessView(TemplateView):
    model = Appointment
    template_name = 'appointments/appointment_create_success.html'
