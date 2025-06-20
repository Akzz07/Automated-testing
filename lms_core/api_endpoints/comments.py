# lms_core/api_endpoints/comments.py
# Hapus 'Router' dari import di sini
from ninja import Schema
from lms_core.models import CourseContent, Comment, CourseMember
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from lms_core.api_endpoints.auth import GlobalAuth

# Schemas (biarkan ini)
class CommentSchemaIn(Schema):
    comment: str

class CommentSchemaOut(Schema):
    id: int
    content_id: int
    user_id: int
    comment: str
    created_at: datetime

def add_comments_routes(router): # Menerima instance Router DI SINI
    @router.post("/{content_id}/comments", response=CommentSchemaOut, auth=GlobalAuth())
    def create_content_comment(request, content_id: int, comment_in: CommentSchemaIn):
        if not request.auth:
            raise ValueError("Authentication required")
        content = get_object_or_404(CourseContent, id=content_id)
        is_member = CourseMember.objects.filter(course_id=content.course_id, user_id=request.auth).exists()
        if not is_member:
            raise ValueError("You are not a member of this course")
        comment = Comment.objects.create(content_id=content, user_id=request.auth, **comment_in.dict())
        return comment

    @router.delete("/{comment_id}", response={200: str}, auth=GlobalAuth())
    def delete_comment(request, comment_id: int):
        if not request.auth:
            raise ValueError("Authentication required")
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.user_id != request.auth:
            raise ValueError("You are not the owner of this comment")
        comment.delete()
        return "Comment deleted successfully"