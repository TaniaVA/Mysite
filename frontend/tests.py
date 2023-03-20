from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class HomePageTests(TestCase):
    def test_url_exists_at_correct_location_homepage(self):

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
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, "Home")

