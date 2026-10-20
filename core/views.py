import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST


@require_GET
def health(request):
    return JsonResponse({"status": "ok", "service": "english-learning-api"})


# A small, transparent rule-based prototype; this is not a complete grammar checker.
WRITING_RULES = [
    {
        "pattern": re.compile(r"\bI\s+am\s+agree\b", re.IGNORECASE),
        "replacement": "I agree",
        "category": "word_choice",
        "explanation": "In English, “agree” is a verb, so it does not need “am”.",
    },
    {
        "pattern": re.compile(r"\b(he|she|it)\s+(go)\b", re.IGNORECASE),
        "replacement_verb": "goes",
        "category": "subject_verb_agreement",
        "explanation": "In the present simple, use “goes” with he, she, or it.",
    },
    {
        "pattern": re.compile(r"\b(he|she|it)\s+(have)\b", re.IGNORECASE),
        "replacement_verb": "has",
        "category": "subject_verb_agreement",
        "explanation": "In the present simple, use “has” with he, she, or it.",
    },
]


@csrf_exempt
@require_POST
def analyze_writing(request):
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": {"code": "invalid_json", "message": "Request body must be valid JSON."}},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": {"code": "invalid_payload", "message": "JSON body must be an object."}},
            status=400,
        )

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        return JsonResponse(
            {"error": {"code": "text_required", "message": "Provide non-empty text to analyze."}},
            status=400,
        )
    if len(text) > 2000:
        return JsonResponse(
            {"error": {"code": "text_too_long", "message": "Text must be 2000 characters or fewer."}},
            status=400,
        )

    errors = []
    for rule in WRITING_RULES:
        for match in rule["pattern"].finditer(text):
            if "replacement" in rule:
                suggestion = rule["replacement"]
            else:
                subject = match.group(1)
                if subject.isupper():
                    subject = subject.upper()
                elif subject[0].isupper():
                    subject = subject.capitalize()
                suggestion = f"{subject} {rule['replacement_verb']}"
            errors.append({
                "category": rule["category"],
                "original": match.group(0),
                "suggestion": suggestion,
                "explanation": rule["explanation"],
                "start": match.start(),
                "end": match.end(),
            })

    errors.sort(key=lambda item: item["start"])
    return JsonResponse({
        "analysis_type": "rule_based_prototype",
        "notice": "This prototype detects only a few patterns and may miss errors.",
        "character_count": len(text),
        "errors": errors,
        "error_count": len(errors),
    })
