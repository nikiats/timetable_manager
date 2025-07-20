from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from web.models import Timetable


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.signup_url = reverse('web:signup')
        self.login_url = reverse('web:login')
        self.logout_url = reverse('web:logout')
        self.timetable_url = reverse('web:timetable')
        self.index_url = reverse('web:index')
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Timetable.objects.create(user=self.user)


    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/signup.html')


    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/login.html')
        

    def test_signup_post_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'password': '123456',
            'password_repeat': '123456'
        }, follow=True)
        
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Timetable.objects.filter(user__username='newuser').exists())

        self.assertRedirects(response, self.timetable_url)


    def test_login_post_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        }, follow=True)
        self.assertRedirects(response, self.timetable_url)


    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, self.index_url)


    def test_timetable_view_requires_login(self):
        response = self.client.get(self.timetable_url)
        redirect_url = f"{self.login_url}?next={self.timetable_url}"
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, redirect_url)


    def test_timetable_view_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.timetable_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'web/timetable.html')


class TimetableUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.timetable = Timetable.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        
        self.update_url = reverse('web:update_timetable')


    def test_update_timetable_valid(self):
        body = {
            'day_index': 0,
            'hour': 8,
            'value': 'Анна Python 2000',
        }
        response = self.client.post(self.update_url, body)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)


    def test_update_timetable_invalid(self):
        body = {
            'day_index': 'invalid',
            'hour': 25,
            'value': 'Анна Python 2000',
        }
        response = self.client.post(self.update_url, body)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)


class ImageAvailableViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.svg_url = reverse('web:svg_image_available')
        self.png_url = reverse('web:png_image_available')
        self.login_url = reverse('web:login')
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.timetable = Timetable.objects.create(user=self.user)


    def test_svg_image_requires_login(self):
        response = self.client.get(self.svg_url)
        expected_login_url = f"{self.login_url}?next={self.svg_url}"
        self.assertRedirects(response, expected_login_url)


    def test_png_image_requires_login(self):
        response = self.client.get(self.png_url)
        expected_login_url = f"{self.login_url}?next={self.png_url}"
        self.assertRedirects(response, expected_login_url)


    def test_svg_image_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.svg_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/svg+xml')
        
        self.assertIn(b'<svg', response.content)


    def test_png_image_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.png_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        
        self.assertIn('timetable.png', response['Content-Disposition'])

        # Проверка формата PNG по специальному префиксу
        self.assertTrue(response.content.startswith(b'\x89PNG'))
