# tugaspss12/urls.py
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from lms_core.api import create_lms_router

api = NinjaAPI(
    version="1.0.0",
    urls_namespace="lms_app_api_main"  # JANGAN gunakan uuid atau gonta-ganti
)

lms_core_main_router = create_lms_router()
api.add_router("/v1/", lms_core_main_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
