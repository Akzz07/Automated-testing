from ninja import Schema, File, Form, Body
from ninja.files import UploadedFile
from lms_core.models import Course, CourseMember
from django.shortcuts import get_object_or_404
from typing import List
from django.contrib.auth.models import User
from lms_core.api_endpoints.auth import GlobalAuth


# Schemas untuk response
class UserSchema(Schema):
    username: str

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

class CourseUpdateSchema(Schema):
    name: str
    description: str
    price: int

def add_courses_routes(router):
    @router.get("", response=List[CourseSchemaOut])
    def list_courses(request):
        return Course.objects.all()

    @router.post("", response=CourseSchemaOut, auth=GlobalAuth())
    def create_course(
        request,
        name: str = Form(...),
        description: str = Form(...),
        price: int = Form(...),
        file: UploadedFile = File(None)
    ):
        if not request.auth:
            raise ValueError("Authentication required")
        course = Course.objects.create(
            name=name,
            description=description,
            price=price,
            teacher=request.auth,
        )
        return course

    @router.put("/{course_id}", response=CourseSchemaOut, auth=GlobalAuth())
    def update_course(request, course_id: int, data: CourseUpdateSchema = Body(...)):
        course = get_object_or_404(Course, id=course_id)
        if course.teacher != request.auth:
            raise ValueError("You are not the teacher of this course")
        course.name = data.name
        course.description = data.description
        course.price = data.price
        course.save()
        return course

    @router.post("/{course_id}/enroll", response=CourseMemberSchemaOut, auth=GlobalAuth())
    def enroll_course(request, course_id: int):
        if not request.auth:
            raise ValueError("Authentication required")
        course = get_object_or_404(Course, id=course_id)
        course_member, created = CourseMember.objects.get_or_create(
            course_id=course.id, 
            user=request.auth
    )

        return course_member
