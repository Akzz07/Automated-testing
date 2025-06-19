# lms_core/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
# Sesuaikan import path jika berbeda - pastikan CourseMember diimpor
from lms_core.models import Course, CourseMember

class CourseModelTest(TestCase):
    def setUp(self):
        """
        Setup data awal untuk setiap pengujian CourseModel.
        Membuat pengguna 'teacher1' dan 'student1', serta satu kursus.
        """
        self.user = User.objects.create_user(username='teacher1', password='password123')
        self.student = User.objects.create_user(username='student1', password='password123')
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.user
        )

    def test_course_creation(self):
        """
        Memastikan objek Course dapat dibuat dengan benar
        dan atributnya sesuai.
        """
        self.assertEqual(self.course.name, "Django for Beginners")
        self.assertEqual(self.course.description, "Learn Django from scratch.")
        self.assertEqual(self.course.price, 100)
        self.assertEqual(self.course.teacher, self.user)

    def test_course_str(self):
        """
        Memastikan representasi string dari objek Course
        sesuai dengan yang diharapkan.
        """
        self.assertEqual(str(self.course), "Django for Beginners")

    def test_is_member(self):
        """
        Menguji metode is_member pada model Course.
        Memastikan itu mengembalikan False jika siswa bukan anggota,
        dan True setelah siswa ditambahkan sebagai anggota.
        """
        self.assertFalse(self.course.is_member(self.student))
        # Menambahkan siswa sebagai anggota kursus melalui CourseMember
        CourseMember.objects.create(course=self.course, user=self.student, roles='std')
        self.assertTrue(self.course.is_member(self.student))

class CourseMemberModelTest(TestCase):
    def setUp(self):
        """
        Setup data awal untuk setiap pengujian CourseMemberModel.
        Membuat pengguna, kursus, dan satu entri CourseMember.
        """
        self.user = User.objects.create_user(username='teacher1', password='password123')
        self.student = User.objects.create_user(username='student1', password='password123')
        self.course = Course.objects.create(
            name="Django for Beginners",
            description="Learn Django from scratch.",
            price=100,
            teacher=self.user
        )
        self.course_member = CourseMember.objects.create(
            course=self.course, # Gunakan objek Course langsung, bukan course_id
            user=self.student,   # Gunakan objek User langsung, bukan user_id
            roles='std'
        )

    def test_course_member_creation(self):
        """
        Memastikan objek CourseMember dapat dibuat dengan benar
        dan atributnya sesuai.
        """
        self.assertEqual(self.course_member.course, self.course)
        self.assertEqual(self.course_member.user, self.student)
        self.assertEqual(self.course_member.roles, 'std')

    def test_course_member_str(self):
        """
        Memastikan representasi string dari objek CourseMember
        sesuai dengan yang diharapkan.
        """
        # Perbarui ekspektasi string karena metode __str__ di CourseMember diperbarui
        self.assertEqual(str(self.course_member), f"{self.course}: {self.student.username} (Student)")

    def test_course_member_role_options(self):
        """
        Memastikan bahwa peran yang ditetapkan untuk CourseMember
        terdapat dalam opsi peran yang valid.
        """
        # ROLE_OPTIONS diimpor dari model lms_core.models
        from lms_core.models import ROLE_OPTIONS
        self.assertIn(self.course_member.roles, dict(ROLE_OPTIONS).keys())

