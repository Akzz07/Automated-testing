from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_member(self, user):
        return CourseMember.objects.filter(course=self, user=user).exists()


class CourseMember(models.Model):
    ROLE_OPTIONS = (
        ('std', 'Student'),
        ('ta', 'Teaching Assistant'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.CharField(max_length=3, choices=ROLE_OPTIONS, default='std')

    def __str__(self):
        role_display = dict(self.ROLE_OPTIONS).get(self.roles, self.roles)
        return f"{self.course}: {self.user.username} ({role_display})"


class CourseContent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.course.name}"


class Comment(models.Model):
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.name}"
