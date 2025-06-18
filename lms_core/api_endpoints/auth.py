# lms_core/api_endpoints/auth.py

from ninja import Schema, Router
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError  # ✅ Tambahan penting

# ✅ FIXED: Gunakan JWT validation sesuai dengan SimpleJWT
class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            validated_token = AccessToken(token)  # ✅ Decode & verify JWT
            user_id = validated_token['user_id']
            user = User.objects.get(id=user_id)
            if not user.is_active:  # ✅ Tambahan keamanan
                return None
            return user
        except Exception:
            return None

# ✅ Schema login request dan response
class AuthSchemaIn(Schema):
    username: str
    password: str

class TokenSchemaOut(Schema):
    access: str
    refresh: str

# ✅ FIXED: Gunakan raise AuthenticationError alih-alih return 401 manual
def add_auth_routes(router: Router):
    @router.post("/sign-in", response=TokenSchemaOut)
    def sign_in(request, auth_in: AuthSchemaIn):
        print("Trying login:", auth_in.username)
        try:
            user = User.objects.get(username=auth_in.username)
            print("✅ Found user:", user)
            print("🔒 Password input:", auth_in.password)
            print("🔐 Stored hash:", user.password)
            if not user.check_password(auth_in.password):
                print("❌ Wrong password!")
                raise AuthenticationError("Wrong password")

            access_token = AccessToken.for_user(user)
            return {"access": str(access_token), "refresh": ""}
        except User.DoesNotExist:
            print("❌ User not found!")
            raise AuthenticationError("User not found")
