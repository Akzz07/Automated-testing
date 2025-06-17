# lms_core/api_endpoints/contents.py
# Hapus 'Router' dari import di sini
from ninja import Schema
from lms_core.models import Course, CourseContent
from django.shortcuts import get_object_or_404

# Schemas (biarkan ini)
class CourseContentSchemaIn(Schema):
    name: str
    description: str

class CourseContentSchemaOut(Schema):
    id: int
    course_id: int
    name: str
    description: str

def add_contents_routes(router): # Menerima instance Router DI SINI
    @router.post("/{course_id}/contents", response=CourseContentSchemaOut)
    def create_course_content(request, course_id: int, content_in: CourseContentSchemaIn):
        if not request.auth:
            raise ValueError("Authentication required")
        course = get_object_or_404(Course, id=course_id)
        if course.teacher != request.auth:
            raise ValueError("You are not the teacher of this course")
        content = CourseContent.objects.create(course_id=course, **content_in.dict())
        return content