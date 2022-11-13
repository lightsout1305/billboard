from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Post, Author


class CreateUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username='John',
            email='johndoe@email.com',
        )
        self.assertEqual(user.username, 'John')
        self.assertEqual(user.email, 'johndoe@email.com')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='Dima',
            email='dimaplot@email.com',
            )
        self.assertEqual(superuser.username, 'Dima')
        self.assertEqual(superuser.email, 'dimaplot@email.com')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)


class TestPostDatabase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
            title='Test post',
            content='Test content',
            author=Author.objects.create(
                author=User.objects.create_user(
                    username='Dima',
                    email='dimaplot@email.com',
                )
            )
        )

    def test_post_listing(self):
        self.assertEqual(f'{self.post.title}', 'Test post')
        self.assertEqual(f'{self.post.content}', 'Test content')
        self.assertEqual(f'{self.post.author.author.username}', 'Dima')


class TestHomePage(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'listing/main.html')
        self.assertContains(response, 'Доска объявлений')


class SignupLoginPageTests(TestCase):

    username = "newuser"
    email = "newuser@email.com"

    def test_signup_page_status_code(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_signup_url_by_name(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)

    def test_view_signup_uses_correct_template(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

    def test_login_page_status_code(self):
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_view_login_url_by_name(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)

    def test_view_login_uses_correct_template(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")

    def test_signup_form(self):
        new_user = User.objects.create_user(self.username, self.email)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.all()[0].username, self.username)
        self.assertEqual(User.objects.all()[0].email, self.email)
