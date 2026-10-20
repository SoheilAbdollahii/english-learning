import json

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


class WritingAnalysisEndpointTests(TestCase):
    def test_detects_known_pattern_and_returns_original_offsets(self):
        text = "Yesterday I am agree."
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps({"text": text}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["analysis_type"], "rule_based_prototype")
        self.assertEqual(body["error_count"], 1)
        issue = body["errors"][0]
        self.assertEqual(text[issue["start"]:issue["end"]], issue["original"])
        self.assertEqual(issue["suggestion"], "I agree")
        self.assertEqual(issue["category"], "word_choice")

    def test_rejects_empty_text(self):
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps({"text": "  "}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "text_required")

    def test_rejects_text_over_limit(self):
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps({"text": "a" * 2001}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "text_too_long")

    def test_rejects_invalid_json(self):
        response = self.client.post(
            "/api/writing/analyze/",
            data="{invalid",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "invalid_json")
