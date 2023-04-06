from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Blog


# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="testBlog",
            email="test12@example.com",
            password="test12pass123",
        )
        cls.blog = Blog.objects.create(
            title="Blog Title",
            body="This is a body content for this blog post.",
            author=cls.user,
        )

    def test_blog_model(self):
        """
        Test for checking Blog model attributes
        """
        self.assertEqual(self.blog.title, "Blog Title")
        self.assertEqual(self.blog.body, "This is a body content for this blog post.")
        self.assertEqual(self.blog.author.username, "testBlog")
        self.assertEqual(str(self.blog), "Blog Title")
        self.assertEqual(self.blog.get_absolute_url(), "/blog/1")

    def test_url_exists_at_correct_location_blog(self):
        """
        Test for checking blog url exists at the correct location
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detail(self):
        """
        Test for checking blog detail url exists at the correct location
        """
        response = self.client.get("/blog/1")
        self.assertEqual(response.status_code, 200)

    def test_blog_listview(self):
        """
        Test for checking blog list view page rendering
        """
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a body content for this blog post.")
        self.assertTemplateUsed(response, "blog_list.html")

    def test_blog_detailview(self):
        """
        Test for checking blog detail view page rendering
        """
        response = self.client.get(reverse("blog_detail", kwargs={'pk': self.blog.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog Title")
        self.assertTemplateUsed(response, "blog_detail.html")
        no_response = self.client.get

    def test_blog_deleteview(self):
        """
        Test for checking blog delete using DeleteView
        """
        response = self.client.post(
            reverse("blog_delete", args="1"))
        self.assertEqual(response.status_code, 302)
