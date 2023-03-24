import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Service(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    duration = models.DurationField(default=0)

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    availability = models.JSONField(default=list)

    def __str__(self):
        return self.name

    def update_availability(self, days, time):
        """
        Метод, который будет обновлять поле availability на основе
        выбранных мастером дней и времени выполнения услуг
        """
        # days - список дней, в которые доступен мастер
        # time - время выполнения услуги
        availability = []
        for day in days:
            start_time = timezone.make_aware(
                timezone.datetime.combine(day, time)
            )
            end_time = start_time + self.services.first().duration
            availability.append(
                (day, start_time.time(), end_time.time())
            )
        self.availability = availability
        self.save()

    def is_available(self, day, time):
        """
        Метод, который проверяет, доступен ли мастер в определенный день и время
        """
        start_time = timezone.make_aware(
            timezone.datetime.combine(day, time)
        )
        end_time = start_time + self.services.first().duration
        appointments = Appointment.objects.filter(
            master=self,
            date=day,
            time__gte=start_time.time(),
            time__lt=end_time.time()
        )
        if appointments.exists():
            return False
        else:
            return True


class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f'{self.service} with {self.master} on {self.date} at {self.time}'


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
