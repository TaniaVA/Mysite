from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from accounts.forms import CustomUserCreationForm
from accounts.views import SignUpView


# Create your tests here.
class SignupPageTests(TestCase):
    """
     Тесты для страницы регистрации.

     Methods
     -------
     test_url_exists_at_correct_location()
         Проверяет, что при запросе к странице регистрации возвращает статус 200.

     test_signup_view_reverse()
         Проверяет, что при запросе к странице регистрации используется шаблон signup.html.

     test_signup_form()
         Отправляет POST запрос в форму регистрации с некоторыми данными.
         Проверяет, что код состояния ответа равен 302 (перенаправление),
         количество пользователей в базе, а имя и email пользователя соответствуют ожидаемым значениям.

     test_signup_form_class()
         Проверяет, что класс формы на странице регистрации является CustomUserCreationForm
         и содержит токен csrf.

     test_signup_view()
         Проверяет, что функция представления SignUpView используется для страницы регистрации.
     """

    def test_url_exists_at_correct_location(self):

        """Этот тест проверяет, что при запросе к signup
        возвращается код состояния
        :return: 200 (успех)
        """

        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_reverse(self):

        """Тест проверяет, что при запросе к signup
        используется шаблон signup.html"""

        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):

        """Тест отправляет POST запрос в форму регистрации с
        некоторыми данными. Затем проверяет, что код состояния ответа
        равен 302 (перенаправление), количество пользователей
        в базе, а имя и email пользователя соответствуют ожидаемым
        значениям"""

        response = self.client.post(
            reverse("signup"),
            {
                "username": "testuser",
                "email": "testuser@mail.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, "testuser")
        self.assertEqual(get_user_model().objects.all()[0].email, "testuser@mail.com")

    def test_signup_view(self):

        """Тест проверяет, что функция представления SignUpView
        используется для страницы регистрации."""

        view = resolve(reverse('signup'))
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__
        )


class CustomUserTests(TestCase):
    """
    Тесты для модели CustomUser.
    """

    def test_create_user(self):
        """
        Тест создания обычного пользователя.
        """
        User = get_user_model()
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='testpass123',
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """
        Тест создания суперпользователя.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admintest123',
        )
        self.assertEqual(admin_user.username, 'admin')
        self.assertEqual(admin_user.email, 'admin@test.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class PasswordResetTests(TestCase):
    """
    Тесты для сброса пароля.
    """

    def setUp(self):

        """
        Тесты для проверки начальных конфигураций
        """

        User = get_user_model()
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="testpass123",
        )
        self.url = reverse('password_reset')
        self.responce = self.client.get(self.url)

    def test_view_by_url(self):

        """
        Тесты сброса пароля по url
        """

        responce = self.client.get('/accounts/password_reset/')
        self.assertEqual(responce.status_code, 200)

    # test password reset page
    def test_view(self):

        """Тест проверяет, страницу сброса пароля."""

        self.assertEqual(self.responce.status_code, 200)
        self.assertTemplateUsed(self.responce, 'registration/password_reset_form.html')
        self.assertContains(self.responce, 'Сброс моего пароля')
        self.assertNotContains(self.responce, 'Email Sent')

    def test_password_reset_post(self):

        """Тестовый POST-запрос на сброс пароля."""

        responce = self.client.post(self.url, data={
            'email': "test@example.com",
        })
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(responce.url, reverse("password_reset_done"))