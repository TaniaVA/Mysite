import datetime
from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone


class Service(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    duration = models.DurationField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("service_list")


class Master(models.Model):
    name = models.CharField(max_length=150)
    photo = models.ImageField(upload_to='users/', default='users/profile_placeholder.jpg', blank=True)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    availability = models.JSONField(default=list)
    description = models.CharField(max_length=255, default='Мастер по маникюру и педикюру')
    schedule = models.FileField(upload_to='schedules/', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("master_list")

    def get_schedule_dict(self):
        # получаем все записи по данному мастеру
        appointments = Appointment.objects.filter(master=self)

        # создаем словарь с расписанием
        schedule_dict = {}
        for i in range(10):
            # вычисляем дату i-го дня от сегодняшней даты
            date = timezone.now().date() + timedelta(days=i)
            # создаем словарь для расписания на эту дату
            schedule = {}
            for j in range(9, 20):
                # проверяем, что j находится в нужном диапазоне
                if j < 9 or j >= 19:
                    continue
                # вычисляем время j-го часа
                dt = datetime(year=2023, month=4, day=6, hour=j)
                time = dt.time()
                # проверяем, свободно ли это время
                is_available = True
                for appointment in appointments:
                    if appointment.date == date and appointment.time == time:
                        is_available = False
                        break
                # добавляем запись в словарь расписания
                schedule[str(time)] = 'available' if is_available else 'unavailable'
            # добавляем словарь расписания на эту дату в общий словарь
            schedule_dict[str(date)] = schedule
        return schedule_dict

        return schedule_dict



class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


    def __str__(self):
        return f'{self.service} with {self.master} on {self.date} at {self.time}'

    def get_absolute_url(self):
        return reverse("appointment_detail", kwargs={"pk": self.pk})


class Availability(models.Model):
    master = models.ForeignKey(
        to=Master,
        on_delete=models.CASCADE,
        related_name='master_availability',
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.master} on {self.date} from {self.start_time} to {self.end_time}'
