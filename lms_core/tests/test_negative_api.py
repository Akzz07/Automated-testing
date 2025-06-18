# lms_core/tests/test_negative_api.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from lms_core.tests.test_client import client
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client

class NegativeAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = "/api/v1/"

        self.teacher, _ = User.objects.get_or_create(
            username='teacher',
            defaults={'password': make_password('password123')}
        )

        login_response = self.client.post(
            self.base_url + 'auth/sign-in',
            {"username": "teacher", "password": "password123"},
            content_type="application/json"
        )

        print("Login teacher response status:", login_response.status_code)
        print("Login teacher response JSON:", login_response.json())

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
