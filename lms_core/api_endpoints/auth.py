from ninja import Schema, Router
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError # Import ini!

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            validated_token = AccessToken(token)
            user_id = validated_token['user_id']
            # Penting: Pastikan user_id ini valid dan user aktif
            user = User.objects.get(id=user_id)
            if not user.is_active: # Tambahkan ini jika Anda menangani user aktif/tidak aktif
                return None
            return user
        except Exception:
            return None

class AuthSchemaIn(Schema):
    username: str
    password: str

class TokenSchemaOut(Schema):
    access: str
    refresh: str

def add_auth_routes(router: Router): # Tambahkan type hint Router
    @router.post("/sign-in", response=TokenSchemaOut)
    def sign_in(request, auth_in: AuthSchemaIn):
        user = authenticate(username=auth_in.username, password=auth_in.password)
        if user:
            access_token = AccessToken.for_user(user)
            return {"access": str(access_token), "refresh": ""}
        # Ubah ini menjadi raise HTTPException atau AuthenticationError
        # AuthenticationError akan otomatis menghasilkan status 401
        raise AuthenticationError("Invalid credentials") # <--- Perubahan Kunci!