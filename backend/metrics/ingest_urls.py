from django.urls import path

from .ingest_views import (
    TelemetryIngestAPIView
)

urlpatterns = [
    path(
        "ingest/",
        TelemetryIngestAPIView.as_view()
    ),
]