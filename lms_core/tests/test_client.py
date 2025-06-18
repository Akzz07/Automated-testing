# lms_core/tests/test_client.py
from ninja import NinjaAPI
from ninja.testing import TestClient
from lms_core.api import create_lms_router
from lms_core.api_endpoints.auth import GlobalAuth

# Gunakan version & namespace unik agar tidak bentrok
test_api = NinjaAPI(version="test-v1", urls_namespace="test_namespace", auth=GlobalAuth())
test_api.add_router("/api/v1/", create_lms_router())

# TestClient global — gunakan ini di test manapun
client = TestClient(test_api)
