from django.test import TestCase  # Gunakan Django TestCase, bukan unittest
from django.contrib.auth.models import User
from tugaspss12.urls import api  # Import api langsung dari urls.py
from lms_core.models import Course
from django.core.management import call_command
from lms_core.tests.test_client import client


class NegativeAPITestCase(TestCase):
    base_url = '/v1/'


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Buat TestClient sekali untuk seluruh test class
        

    def setUp(self):
        # Jangan buat TestClient baru di sini, gunakan self.client dari setUpClass
        call_command('flush', verbosity=0, interactive=False)
        


        self.teacher_username = 'teacher'
        self.teacher_password = 'password123'
        self.teacher = User.objects.create_user(
            username=self.teacher_username, 
            password=self.teacher_password
        )

        login_teacher_response = self.client.post(
            self.base_url + 'auth/sign-in',
            json={'username': self.teacher_username, 'password': self.teacher_password}
        )
        self.assertEqual(login_teacher_response.status_code, 200)
        self.teacher_token = login_teacher_response.json()['access']
        self.teacher_auth_headers = {
            'Authorization': 'Bearer ' + self.teacher_token
        }
        print("Login response:", login_teacher_response.status_code, login_teacher_response.json())

    def test_create_course_without_name(self):
        incomplete_data = {
            'description': 'Course without name',
            'price': 100
        }
        response = self.client.post(
            self.base_url + 'courses',
            json=incomplete_data,
            headers=self.teacher_auth_headers
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('detail', response.json())

    def test_create_course_with_invalid_price_type(self):
        invalid_data = {
            'name': 'Invalid Course',
            'description': 'Price should be int',
            'price': 'one hundred'
        }
        response = self.client.post(
            self.base_url + 'courses',
            json=invalid_data,
            headers=self.teacher_auth_headers
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertIn('detail', response.json())

    def test_access_protected_route_without_token(self):
        response = self.client.post(
            self.base_url + 'courses',
            json={'name': 'No Token Course', 'description': '...', 'price': 100}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.json())