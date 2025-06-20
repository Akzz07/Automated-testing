from unittest import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from lms_core.tests.test_client import client  # client ini adalah TestClient(api)
from lms_core.models import Course, CourseMember, CourseContent, Comment
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
import json

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = "/api/v1/"

        # Pastikan user teacher dan student tidak duplikat
        self.teacher, _ = User.objects.get_or_create(
            username='teacher',
            defaults={'password': make_password('password123')}
        )
        self.student, _ = User.objects.get_or_create(
            username='student',
            defaults={'password': make_password('password123')}
        )

        # Login guru
        login_teacher_response = self.client.post(
            self.base_url + 'auth/sign-in',
            {"username": "teacher", "password": "password123"},
            content_type="application/json"
        )

        print("Login teacher response status:", login_teacher_response.status_code)
        print("Login teacher response JSON:", login_teacher_response.json())

        self.assertEqual(login_teacher_response.status_code, 200)
        self.teacher_token = login_teacher_response.json()['access']
        self.teacher_auth_headers = {'Authorization': f'Bearer {self.teacher_token}'}
        

        # Login siswa
        login_student_response = self.client.post(
            self.base_url + 'auth/sign-in',
            {"username": "student", "password": "password123"},
            content_type="application/json"
        )
        print("Login student response status:", login_student_response.status_code)
        print("Login student response JSON:", login_student_response.json())
        self.assertEqual(login_student_response.status_code, 200)
        self.student_token = login_student_response.json()['access']
        self.student_auth_headers = {'Authorization': f'Bearer {self.student_token}'}
        

        # Buat course
        course_data_nested = {
            "course_in": { # <--- Ini kuncinya!
                "name": "Django for Beginners",
                "description": "Learn Django from scratch.",
                "price": 100
            }
        }
        create_course_response = self.client.post(
        self.base_url + 'courses/',
        data={
            "name": "Django for Beginners",
            "description": "Learn Django from scratch.",
            "price": 100
        },
        HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"

        )
        print("Create course response status:", create_course_response.status_code)
        print("Create course response JSON:", create_course_response.json())

        self.assertEqual(create_course_response.status_code, 200)
        self.course = Course.objects.get(id=create_course_response.json()['id'])

        # Buat content
        content_data = {"name": "Introduction to Django", "description": "First lesson"}
        create_content_response = self.client.post(
            f'{self.base_url}courses/{self.course.id}/contents',
            data=json.dumps({"name": "Introduction to Django", "description": "First lesson"}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"

        )
        self.assertEqual(create_content_response.status_code, 200)
        self.content = CourseContent.objects.get(id=create_content_response.json()['id'])
        print("Login response:", login_teacher_response.status_code, login_teacher_response.json())

    def test_list_courses(self):
        response = self.client.get(f'{self.base_url}courses/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], self.course.name)

    def test_create_course(self):
        response = self.client.post(
            self.base_url + 'courses/',
            data={
            "name": "New Course",
            "description": "New Desc",
            "price": 150
        },
        HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"

    )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(name='New Course').exists())

    #  method test_update_course, 
    def test_update_course(self):
        response = self.client.put(
            f'{self.base_url}courses/{self.course.id}/',
            data={  
                "name": "Updated Course",
                "description": "Updated",
                "price": 200
            },
            content_type="multipart/form-data",
            HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Updated Course")

    def test_enroll_course(self):
        response = self.client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            headers=self.student_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CourseMember.objects.filter(course=self.course, user=self.student).exists())


    def test_create_content_comment(self):
        self.client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            HTTP_AUTHORIZATION=f"Bearer {self.student_token}"

        )
        comment_data = {'comment': 'This is a comment'}
        response = self.client.post(
            f'{self.base_url}contents/{self.content.id}/comments',
            data=json.dumps(comment_data),
            content_type="application/json",
            **self.student_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content=self.content, user=self.student).exists())

    def test_delete_comment(self):
        enroll_response = self.client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
             HTTP_AUTHORIZATION=f"Bearer {self.student_token}"
        )
        self.assertEqual(enroll_response.status_code, 200)
        comment_data = {'comment': 'To be deleted'}
        create_response = self.client.post(
            f'{self.base_url}contents/{self.content.id}/comments',
            data=json.dumps(comment_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.student_token}"
        )
        self.assertEqual(create_response.status_code, 200)
        comment_id = create_response.json()['id']

        delete_response = self.client.delete(
            f'{self.base_url}comments/{comment_id}',
            HTTP_AUTHORIZATION=f"Bearer {self.student_token}"
        )
        self.assertEqual(delete_response.status_code, 200)
        
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

