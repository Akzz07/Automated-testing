# lms_core/api_endpoints/auth.py
from ninja import Schema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken

class AuthSchemaIn(Schema):
    username: str
    password: str

class TokenSchemaOut(Schema):
    access: str
    refresh: str

def add_auth_routes(router):
    @router.post("/sign-in", response=TokenSchemaOut)
    def sign_in(request, auth_in: AuthSchemaIn):
        user = authenticate(username=auth_in.username, password=auth_in.password)
        if user:
            access_token = AccessToken.for_user(user)
            return {"access": str(access_token), "refresh": ""}
        return 401, {"detail": "Invalid credentials"}
