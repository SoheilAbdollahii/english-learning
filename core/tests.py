import json
import os
import subprocess
import sys

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

    def test_rejects_non_object_json_payload(self):
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps(["not", "an", "object"]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "invalid_payload")

    def test_returns_no_errors_for_unrecognized_patterns(self):
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps({"text": "The weather is nice today."}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["error_count"], 0)
        self.assertEqual(response.json()["errors"], [])

    def test_returns_multiple_issues_in_text_order(self):
        text = "He go to school. I am agree."
        response = self.client.post(
            "/api/writing/analyze/",
            data=json.dumps({"text": text}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["error_count"], 2)
        self.assertEqual(
            [issue["suggestion"] for issue in body["errors"]],
            ["He goes", "I agree"],
        )
        self.assertEqual(
            [issue["start"] for issue in body["errors"]],
            sorted(issue["start"] for issue in body["errors"]),
        )


class ProductionSettingsTests(TestCase):
    def _load_settings_with_environment(self, overrides):
        env = os.environ.copy()
        for key, value in overrides.items():
            if value is None:
                env.pop(key, None)
            else:
                env[key] = value
        return subprocess.run(
            [sys.executable, "-c", "import config.settings"],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_production_rejects_default_secret_key(self):
        env = {
            "DJANGO_DEBUG": "False",
            "DJANGO_ALLOWED_HOSTS": "example.com",
            "DJANGO_SECRET_KEY": None,
        }
        result = self._load_settings_with_environment(env)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY", result.stderr)

    def test_production_rejects_wildcard_allowed_hosts(self):
        result = self._load_settings_with_environment({
            "DJANGO_DEBUG": "False",
            "DJANGO_SECRET_KEY": "test-only-secret-value",
            "DJANGO_ALLOWED_HOSTS": "*",
        })
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_ALLOWED_HOSTS", result.stderr)
