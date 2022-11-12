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

