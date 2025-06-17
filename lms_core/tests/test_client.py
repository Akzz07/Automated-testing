from ninja import NinjaAPI
from ninja.testing import TestClient
from lms_core.api import create_lms_router

# Buat Test API dengan versi & namespace unik
test_api = NinjaAPI(
    version="tempik_999",
    urls_namespace="tempik_namespace_999"
)
test_api.add_router("/v1/", create_lms_router())

# Ini yang dipakai semua test
client = TestClient(test_api)
