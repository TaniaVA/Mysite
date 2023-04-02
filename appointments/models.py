import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, timedelta
from django.http import JsonResponse


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

    def get_availability(self, start_date_str, end_date_str):
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        availability = []
        for available_date in self.availability:
            date = datetime.strptime(available_date[0], '%Y-%m-%d').date()
            start_times = available_date[1:]

            if start_date <= date <= end_date:
                for start_time in start_times:
                    start = datetime.strptime(f'{date}T{start_time}', '%Y-%m-%dT%H:%M')
                    end = start + timedelta(hours=3)  # appointment duration is 3 hours

                    if self.is_available(start):
                        availability.append({
                            'start': start.isoformat(),
                            'end': end.isoformat()
                        })

        return JsonResponse({'availability': availability})

    def update_availability(self, start_date, end_date):
        """
        Метод, который будет обновлять поле availability на основе
        выбранных мастером дней и времени выполнения услуг
        """
        # days - список дней, в которые доступен мастер
        # time - время выполнения услуги
        availability = []
        for d in range((end_date - start_date).days + 1):
            day = start_date + datetime.timedelta(days=d)
            day_schedule = self.schedule.get(str(day), {})
            for service in self.services.all():
                start_time = day_schedule.get(str(service.id), '09:00')
                start_time = timezone.make_aware(
                    datetime.datetime.combine(day, datetime.time.fromisoformat(start_time)))
                end_time = start_time + service.duration
                availability.append((day, start_time.time(), end_time.time()))
        self.availability = availability
        self.save()



class Appointment(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    # AVAILABLE = 'AV'
    # BOOKED = 'BK'
    # STATUS_CHOICES = [
    #     (AVAILABLE, 'Available'),
    #     (BOOKED, 'Booked')
    # ]
    # status = models.CharField(
    #     max_length=2,
    #     choices=STATUS_CHOICES,
    #     default=AVAILABLE
    # )

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
