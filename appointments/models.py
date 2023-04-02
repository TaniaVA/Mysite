import datetime
from django.db import models
from django.utils import timezone
from django.urls import reverse
import json
from datetime import datetime



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

    def load_master_schedule(master_id, start_date, end_date):
        try:
            master = Master.objects.get(id=master_id)
        except Master.DoesNotExist:
            print(f'Master with id {master_id} does not exist')
            return

        with open('schedule.py', 'r') as f:
            schedule_data = json.load(f)

        for date_str, services_schedule in schedule_data.items():
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date < start_date or date > end_date:
                continue

            for service_id, start_time_str in services_schedule.items():
                service = Service.objects.get(id=service_id)
                start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()

                if not master.is_available(date, start_time):
                    continue

                master_schedule = master.schedule.get(str(date), {})
                master_schedule[str(service_id)] = start_time.strftime('%H:%M:%S')
                master.schedule[str(date)] = master_schedule

        master.update_availability(start_date, end_date)

    def get_availability(self, date_range):
        # переменная для хранения пустых слотов
        availability = []
        # Итерируем по всем датам
        for day in date_range:
            day_schedule = self.schedule.get(str(day.date()), {})
            print(f"Schedule for day {day.date()}: {day_schedule}")
            # Итерируем по всем услугам
            for service in self.services.all():
                # Получаем из get запроса дату начала услуги
                start_time = day_schedule.get(str(service.id))
                if not start_time:
                    continue
                    #  Высчитаем окончание добавив к начальному времени продолжительность
                start_time = timezone.make_aware(
                    datetime.datetime.combine(day.date(), datetime.time.fromisoformat(start_time)))
                end_time = start_time + service.duration
                # Если мастер не доступен пропускаем эту итерацию
                if not self.is_available(day.date(), start_time.time()):
                    continue
                    # Составляем список из дат, начала выполнения услуги и окончания
                availability.append((day.date(), start_time.time(), end_time.time()))
        return availability


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