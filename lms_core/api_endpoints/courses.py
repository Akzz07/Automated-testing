# lms_core/api_endpoints/courses.py
# Hapus 'Router' dari import di sini
from ninja import Schema, File
from ninja.files import UploadedFile
from lms_core.models import Course, CourseMember
from django.shortcuts import get_object_or_404
from typing import List
from django.contrib.auth.models import User
from lms_core.api_endpoints.auth import GlobalAuth


# Schemas (biarkan ini)
class UserSchema(Schema):
    username: str

class CourseSchemaIn(Schema):
    name: str
    description: str
    price: int

class CourseSchemaOut(Schema):
    id: int
    name: str
    description: str
    price: int
    teacher: UserSchema

class CourseMemberSchemaOut(Schema):
    id: int
    course_id: int
    user_id: int
    roles: str

def add_courses_routes(router): # Menerima instance Router DI SINI
    @router.get("", response=List[CourseSchemaOut])
    def list_courses(request):
        courses = Course.objects.all()
        return courses

    @router.post("", response=CourseSchemaOut, auth=GlobalAuth())
    def create_course(request, course_in: CourseSchemaIn, file: UploadedFile = File(None)):
        if not request.auth:
            raise ValueError("Authentication required")
        course = Course.objects.create(**course_in.dict(), teacher=request.auth)
        return course

    @router.put("/{course_id}", response=CourseSchemaOut, auth=GlobalAuth())
    def update_course(request, course_id: int, course_in: CourseSchemaIn, file: UploadedFile = File(None)):
        if not request.auth:
            raise ValueError("Authentication required")
        course = get_object_or_404(Course, id=course_id)
        if course.teacher != request.auth:
            raise ValueError("You are not the teacher of this course")
        for attr, value in course_in.dict().items():
            setattr(course, attr, value)
        course.save()
        return course

    @router.post("/{course_id}/enroll", response=CourseMemberSchemaOut, auth=GlobalAuth())
    def enroll_course(request, course_id: int):
        if not request.auth:
            raise ValueError("Authentication required")
        course = get_object_or_404(Course, id=course_id)
        course_member, created = CourseMember.objects.get_or_create(
            course_id=course, user_id=request.auth
        )
        return course_member