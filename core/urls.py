from django.urls import path

from .views import analyze_writing, health

urlpatterns = [
    path("health/", health, name="health"),
    path("writing/analyze/", analyze_writing, name="analyze-writing"),
]
