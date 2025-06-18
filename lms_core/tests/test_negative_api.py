# lms_core/tests/test_negative_api.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from lms_core.tests.test_client import client


class NegativeAPITestCase(TestCase):
    base_url = '/api/v1/'

    def setUp(self):
        call_command('flush', verbosity=0, interactive=False)

        # Buat user guru
        self.teacher = User.objects.create_user(username='teacher', password='password123')

        # Login guru
        login_response = client.post(
            self.base_url + 'auth/sign-in',
            json={'username': 'teacher', 'password': 'password123'}
        )
        self.assertEqual(login_response.status_code, 200)
        self.teacher_token = login_response.json()['access']
        self.teacher_auth_headers = {'Authorization': f'Bearer {self.teacher_token}'}

    def test_create_course_without_name(self):
        # Kirim request tanpa nama
        data = {
            'description': 'No name',
            'price': 100
        }
        response = client.post(self.base_url + 'courses', json=data, headers=self.teacher_auth_headers)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('detail', response.json())

    def test_create_course_with_invalid_price_type(self):
        data = {
            'name': 'Invalid Price',
            'description': 'Wrong type',
            'price': 'seratus'
        }
        response = client.post(self.base_url + 'courses', json=data, headers=self.teacher_auth_headers)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('detail', response.json())

    def test_access_protected_route_without_token(self):
        data = {
            'name': 'No Token',
            'description': 'Should fail',
            'price': 150
        }
        response = client.post(self.base_url + 'courses', json=data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.json())
