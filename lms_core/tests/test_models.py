# /tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from lms_core.models import Course, CourseMember # Sesuaikan import path jika berbeda
from django.core.management import call_command

class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher1', password='password123')
        self.student = User.objects.create_user(username='student1', password='password123')
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.user
        )

    def test_course_creation(self):
        self.assertEqual(self.course.name, "Django for Beginners")
        self.assertEqual(self.course.description, "Learn Django from scratch.")
        self.assertEqual(self.course.price, 100)
        self.assertEqual(self.course.teacher, self.user)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Django for Beginners")

    def test_is_member(self):
        self.assertFalse(self.course.is_member(self.student))
        CourseMember.objects.create(course_id=self.course, user_id=self.student)
        self.assertTrue(self.course.is_member(self.student))

class CourseMemberModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher1', password='password123')
        self.student = User.objects.create_user(username='student1', password='password123')
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.user
        )
        self.course_member = CourseMember.objects.create(
            course_id=self.course,
            user_id=self.student,
            roles='std'
        )

    def test_course_member_creation(self):
        self.assertEqual(self.course_member.course_id, self.course)
        self.assertEqual(self.course_member.user_id, self.student)
        self.assertEqual(self.course_member.roles, 'std')

    def test_course_member_str(self):
        self.assertEqual(str(self.course_member), f"{self.course}: {self.student}")

    def test_course_member_role_options(self):
        # Pastikan ROLE_OPTIONS didefinisikan di model CourseMember
        # from lms_core.models import ROLE_OPTIONS
        self.assertIn(self.course_member.roles, dict(CourseMember.ROLE_OPTIONS).keys())