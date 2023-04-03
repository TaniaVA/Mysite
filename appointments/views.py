from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Service, Master, Appointment
from .forms import AppointmentForm, MasterForm
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.http import HttpResponseRedirect


class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_pk'] = self.kwargs.get('service_pk')
        return context

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    template_name = 'service_edit.html'
    fields = ['name', 'price', 'duration', ]

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff


class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    template_name = "service_new.html"
    fields = ['name', 'price', 'duration', ]

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
    success_url = reverse_lazy('appointment_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_pk'] = self.kwargs.get('service_pk')
        return context

class MasterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Master
    template_name = 'master_edit.html'
    form_class = MasterForm
    success_url = reverse_lazy('master_list')

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

    def form_valid(self, form):
        # Получаем объект мастера из базы данных
        master = form.save(commit=False)
        # Получаем загруженное изображение из формы
        photo = form.cleaned_data['photo']
        # Если загружено изображение, то сохраняем его в файловой системе
        if photo:
            file_name = default_storage.save(photo.name, ContentFile(photo.read()))
            master.photo = file_name
        # Сохраняем изменения в базе данных
        master.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('master_list', args=[self.kwargs['service_id']])


    def get_available_dates(request):
        service_id = request.GET.get('service_id')
        master_id = request.GET.get('master_id')
        master = Master.objects.get(id=master_id)
        dates = master.get_available_dates(service_id)
        return JsonResponse({'dates': dates})


class MasterCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Master
    template_name = "master_new.html"
    fields = ['name', 'photo', 'description', 'services']

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

    def form_valid(self, form):
        # Получаем объект мастера из базы данных
        master = form.save(commit=False)
        # Получаем загруженное изображение из формы
        photo = form.cleaned_data['photo']
        # Если загружено изображение, то сохраняем его в файловой системе
        if photo:
            file_name = default_storage.save(photo.name, ContentFile(photo.read()))
            master.photo = file_name
        # Установить создателя мастера
        master.user = self.request.user
        # Сохраняем изменения в базе данных
        master.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('master_list')


class MasterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Master
    template_name = 'master_delete.html'
    success_url = reverse_lazy('service_list')

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('master_list', kwargs={'service_id': self.object.service.id})
        self.object.delete()
        return HttpResponseRedirect(success_url)

class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = "appointment_detail.html"

    def appointment_create(request, pk):
        service = get_object_or_404(Service, pk=pk)

        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appointment = form.save(commit=False)
                appointment.service = service
                if appointment.is_available():
                    appointment.save()
                    return render(request, 'appointments/appointment_detail.html', {'object': service, 'appointment': appointment})
        else:
            form = AppointmentForm()

        return render(request, 'appointments/appointment_create.html', {'form': form, 'service': service})

class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_create.html'
    fields = ['date', 'time', 'master', 'service']
    success_url = reverse_lazy('appointment_detail')

    def form_valid(self, form):
        master = get_object_or_404(Master, pk=self.kwargs['master_pk'])
        service = get_object_or_404(Service, pk=self.kwargs['service_pk'])
        form.instance.master = master
        form.instance.service = service
        return super().form_valid(form)

    def test_func(self):
        """
        Test whether the user is a staff member.
        """
        return self.request.user.is_staff

    def get_initial(self):
        # Получаем выбранные пользователем параметры
        service_id = self.request.GET.get('service_id')
        master_id = self.request.GET.get('master_id')
        date = self.request.GET.get('date')

        # Подготавливаем словарь с начальными значениями полей формы
        initial = {}
        if service_id:
            service = Service.objects.get(id=service_id)
            initial['service'] = service
        if master_id:
            master = Master.objects.get(id=master_id)
            initial['master'] = master
        if date:
            initial['date'] = date
        return initial

    def get_available_times(request):
        master_id = request.GET.get('master_id')
        date = request.GET.get('date')
        master = Master.objects.get(id=master_id)
        times = master.get_available_times(date)
        return JsonResponse({'times': times})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master_id = self.request.GET.get('master_id')
        master = Master.objects.get(id=master_id)
        availability = master.get_availability('2023-04-03', '2023-04-07')
        context['availability'] = availability
        return context

class AppointmentListView(ListView):
    model = Appointment

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
