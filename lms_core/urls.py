# # tugaspss12/urls.py
# from django.contrib import admin
# from django.urls import path, include
# from ninja import NinjaAPI # Import NinjaAPI di sini
# from lms_core.urls import lms_core_main_router # Import router dari lms_core.urls

# # INI ADALAH SATU-SATUNYA TEMPAT DI MANA NinjaAPI diinisialisasi.
# # Gunakan urls_namespace yang jelas dan unik untuk API aplikasi utama Anda.
# api = NinjaAPI(version="1.0.0", urls_namespace="lms_app_api_main")

# # Tambahkan router utama LMS Anda ke API ini.
# # Prefix '/api/' akan ditangani oleh path() Django, dan '/v1/' oleh api.add_router()
# api.add_router("/v1/", lms_core_main_router) # URL akan menjadi /api/v1/...

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include(api.urls)), # Semua endpoint Ninja akan dimulai dengan /api/v1/
# ]