from unittest import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from lms_core.tests.test_client import client  # client ini adalah TestClient(api)
from lms_core.models import Course, CourseMember, CourseContent, Comment


class APITestCase(TestCase):
    base_url = '/api/v1/'


    def setUp(self):
        
        call_command('flush', verbosity=0, interactive=False)

        # Buat user guru dan siswa
        self.teacher = User.objects.create_user(username='teacher', password='password123')
        self.student = User.objects.create_user(username='student', password='password123')

        # Login guru
        login_teacher_response = client.post(
            self.base_url + 'auth/sign-in',
            json={'username': 'teacher', 'password': 'password123'}
        )
        print("Login teacher response status:", login_teacher_response.status_code)
        print("Login teacher response JSON:", login_teacher_response.json())
        self.assertEqual(login_teacher_response.status_code, 200)
        self.teacher_token = login_teacher_response.json()['access']
        self.teacher_auth_headers = {'Authorization': f'Bearer {self.teacher_token}'}
        

        # Login siswa
        login_student_response = client.post(
            self.base_url + 'auth/sign-in',
            json={'username': 'student', 'password': 'password123'}
        )
        print("Login student response status:", login_student_response.status_code)
        print("Login student response JSON:", login_student_response.json())
        self.assertEqual(login_student_response.status_code, 200)
        self.student_token = login_student_response.json()['access']
        self.student_auth_headers = {'Authorization': f'Bearer {self.student_token}'}
        

        # Buat course
        course_data = {
            "name": "Django for Beginners",
            "description": "Learn Django from scratch.",
            "price": 100
        }
        create_course_response = client.post(
            self.base_url + 'courses',
            json=course_data,
            headers=self.teacher_auth_headers
        )
        self.assertEqual(create_course_response.status_code, 200)
        self.course = Course.objects.get(id=create_course_response.json()['id'])

        # Buat content
        content_data = {"name": "Introduction to Django", "description": "First lesson"}
        create_content_response = client.post(
            f'{self.base_url}courses/{self.course.id}/contents',
            json=content_data,
            headers=self.teacher_auth_headers
        )
        self.assertEqual(create_content_response.status_code, 200)
        self.content = CourseContent.objects.get(id=create_content_response.json()['id'])
        print("Login response:", login_teacher_response.status_code, login_teacher_response.json())

    def test_list_courses(self):
        response = client.get(f'{self.base_url}courses')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], self.course.name)

    def test_create_course(self):
        data = {"name": "New Course", "description": "New Desc", "price": 150}
        response = client.post(
            self.base_url + 'courses',
            json=data,
            headers=self.teacher_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Course.objects.filter(name='New Course').exists())

    # Di method test_update_course, ubah POST menjadi PUT/PATCH:
    def test_update_course(self):
        updated = {"name": "Updated Course", "description": "Updated", "price": 200}
        response = client.put(  # Ubah dari post ke put
        f'{self.base_url}courses/{self.course.id}/',
         json=updated,
         headers=self.teacher_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, "Updated Course")

    def test_enroll_course(self):
        response = client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            headers=self.student_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CourseMember.objects.filter(course=self.course, user=self.student).exists())

    def test_create_content_comment(self):
        # Enroll student dulu
        client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            headers=self.student_auth_headers
        )
        comment_data = {'comment': 'This is a comment'}
        response = client.post(
            f'{self.base_url}contents/{self.content.id}/comments',
            json=comment_data,
            headers=self.student_auth_headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content=self.content, user=self.student).exists())

    def test_delete_comment(self):
        client.post(
            f'{self.base_url}courses/{self.course.id}/enroll',
            headers=self.student_auth_headers
        )
        comment_data = {'comment': 'To be deleted'}
        create_response = client.post(
            f'{self.base_url}contents/{self.content.id}/comments',
            json=comment_data,
            headers=self.student_auth_headers
        )
        comment_id = create_response.json()['id']

        delete_response = client.delete(
            f'{self.base_url}comments/{comment_id}',
            headers=self.student_auth_headers
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())
