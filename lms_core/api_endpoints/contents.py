# lms_core/api_endpoints/contents.py
from ninja import Schema
from lms_core.models import Course, CourseContent
from django.shortcuts import get_object_or_404
from ninja_jwt.authentication import JWTAuth
from django.contrib.auth.models import User
from ninja.errors import HttpError

# Schemas
class CourseContentSchemaIn(Schema):
    name: str
    description: str

class CourseContentSchemaOut(Schema):
    id: int
    course_id: int
    name: str
    description: str

def add_contents_routes(router):
    @router.post("/{course_id}/contents", response=CourseContentSchemaOut, auth=JWTAuth())
    def create_course_content(request, course_id: int, content_in: CourseContentSchemaIn):
        # JWT Authentication will automatically populate request.auth with the user
        user = request.auth
        
        if not user:
            raise HttpError(401, "Authentication required")

        course = get_object_or_404(Course, id=course_id)

        if course.teacher != user:
            raise HttpError(403, "You are not the teacher of this course")

        content = CourseContent.objects.create(
            course=course, 
            name=content_in.name,
            description=content_in.description
        )
        return {
            "id": content.id,
            "course_id": content.course.id,
            "name": content.name,
            "description": content.description
        }