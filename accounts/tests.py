from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your tests here.
class SignupPageTests(TestCase):
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






