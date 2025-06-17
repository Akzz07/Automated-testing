# lms_core/apps.py
from django.apps import AppConfig

class LmsCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms_core'

    def ready(self):
        # Hapus SEMUA logika impor dan add_router di sini
        # Logika ini sekarang ada di tugaspss12/urls.py
        pass # Tidak ada yang perlu dilakukan di sini untuk menambahkan router API