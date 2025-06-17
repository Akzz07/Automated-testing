#/models.py
from django.db import models
from django.contrib.auth.models import User
# from lms_core.models import Course, CourseMember

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_member(self, user):
        return CourseMember.objects.filter(course_id=self, user_id=user).exists()

class CourseMember(models.Model):
    ROLE_OPTIONS = (
        ('std', 'Student'),
        ('ta', 'Teaching Assistant'),
    )
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=3, choices=ROLE_OPTIONS, default='std')

    def __str__(self):
        return f"{self.course_id}: {self.user_id}"

# Tambahkan model lain jika diperlukan untuk Integration Testing, misal:
class CourseContent(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Comment(models.Model):
    content_id = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user_id.username} on {self.content_id.name}"