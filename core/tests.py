from django.test import TestCase


class HealthEndpointTests(TestCase):
    def test_health_endpoint_returns_ok(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "ok",
            "service": "english-learning-api",
        })

    def test_health_endpoint_rejects_post(self):
        response = self.client.post("/api/health/")
        self.assertEqual(response.status_code, 405)
