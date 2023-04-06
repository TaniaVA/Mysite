from django.test import TestCase

from datetime import timedelta
from django.urls import reverse, resolve
from appointments.models import Service, Master
from .views import ServiceListView, MasterListView
from accounts.models import CustomUser


class ServiceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = Service.objects.create(
            name='New Service',
            price=10,
            duration=timedelta(minutes=30)
        )

    def test_service_model(self):
        """
        Test for checking Service model attributes
        """
        self.assertEqual(self.service.name, 'New Service')
        self.assertEqual(self.service.price, 10)
        self.assertEqual(str(self.service), 'New Service')
        self.assertEqual(self.service.get_absolute_url(), reverse('service_list'))


    def test_service_listview(self):
        """
        Test for checking service list view page rendering
        """
        response = self.client.get(reverse('service_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Service')
        self.assertTemplateUsed(response, 'service_list.html')

    def test_list_url_resolve_view(self):
        view = resolve(reverse('service_list'))
        self.assertEqual(view.func.view_class, ServiceListView)

    def test_service_createview(self):
        """
        Test for checking service creation using CreateView
        """
        response = self.client.post(
            reverse('service_create'),
            {
                'name': 'New Service',
                'price': 20,
                'duration': timedelta(minutes=50)
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Service.objects.last().name, 'New Service')
        self.assertEqual(Service.objects.last().price, 20)

    def test_service_updateview(self):
        """
        Test for checking service update using UpdateView
        """
        response = self.client.post(
            reverse('service_update', args=[self.service.pk]),
            {
                'name': 'Updated Service',
                'price': 30,
                'duration': timedelta(minutes=40)
            },
        )
        self.assertEqual(response.status_code, 302)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Updated Service')
        self.assertEqual(self.service.price, 30)

    def test_service_deleteview(self):
        """
        Test for checking service delete using DeleteView
        """
        response = self.client.post(
            reverse('service_delete', args=[self.service.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Service.objects.count(), 0)

    def test_service_detailview(self):
        """
        Test for checking service detail view page rendering
        """
        response = self.client.get(reverse('service_detail', kwargs={'pk': self.service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New Service')
        self.assertTemplateUsed(response, 'service_detail.html')
        no_response = self.client.get(reverse('service_detail', kwargs={'pk': 10000}))

class MasterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(email='test@example.com', password='test123')
        cls.service = Service.objects.create(name='Test Service', price=20, duration=timedelta(minutes=30))
        cls.master = Master.objects.create(
            name='Test Master',
            user=cls.user,
            description='Test description',
            schedule='path/to/schedule.pdf'
        )
        cls.master.services.add(cls.service)

    def test_master_model(self):

        """
        Test for checking Master model attributes
        """

        self.assertEqual(str(self.master), 'Test Master')
        self.assertEqual(self.master.name, 'Test Master')
        self.assertEqual(self.master.user.email, 'test@example.com')
        self.assertEqual(self.master.description, 'Test description')
        self.assertEqual(self.master.schedule, 'path/to/schedule.pdf')
        self.assertIn(self.service, self.master.services.all())

    def test_master_listview(self):
        """
        Test for checking master list view page rendering
        """
        response = self.client.get(reverse('master_list', kwargs={'service_id': self.service.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Master')
        self.assertTemplateUsed(response, 'master_list.html')

    def test_list_url_resolve_view(self):
        view = resolve(reverse('master_list', kwargs={'service_id': self.service.pk}))
        self.assertEqual(view.func.view_class, MasterListView)

