from django.test import TestCase
from django.test import TestCase
from unittest.mock import Mock
from .views import AppointmentCreateView

class MyTest(TestCase):
    def test_get_form_kwargs(self):
        # Создаем объекты, необходимые для тестирования
        view = AppointmentCreateView()
        view.object = Mock()
        view.request = Mock()
        view.request.GET = {'date': '2022-04-05'}

        # Вызываем функцию
        kwargs = view.get_form_kwargs()

        # Проверяем результат
        self.assertEqual(kwargs['master'], view.object)
        self.assertIsNotNone(kwargs['availability'])

