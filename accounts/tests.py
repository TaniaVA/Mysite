from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class SignupPageTests(TestCase):
    def test_url_exists_at_correct_location(self):

        """Этот тест проверяет, что при запросе к signup
        возвращает код состояния
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


class HomePageTests(TestCase):
    def setUp(self):

        """функция setUp запускается перед выполнением каждого теста и
        создает пользователя, используя метод
        get_user_model().objects.create_user"""

        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

    def test_home_page_status_code(self):

        """Этот тест проверяет, что при запросе к домашней странице
        возвращается код состояния
        :return: 200 (успех)
        """

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):

        """В этом тесте проверяем, что при запросе к домашней странице
        используются шаблоны base.html и home.html"""

        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_content_authenticated(self):

        """Тест проверяет, что при запросе к домашней странице от авторизованного
        пользователя выводится сообщение приветствия с его именем и ссылка на выход
         из системы"""

        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'Здравствуйте, {self.user.username}.')
        self.assertContains(response, f'<a href="{reverse("logout")}">Выйти</a>')

    def test_home_page_content_not_authenticated(self):

        """Тест проверяет, что при запросе к домашней странице от неавторизованного
        пользователя выводится сообщение о том, что пользователь не вошел в систему, и
         ссылки страницы входа и регистрации"""

        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Вы не вошли в систему.')
        self.assertContains(response, f'<a href="{reverse("login")}">Войти</a>')
        self.assertContains(response, f'<a href="{reverse("signup")}">Регистрация</a>')