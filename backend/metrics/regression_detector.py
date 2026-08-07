from datetime import timedelta

from django.db.models import Avg
from django.utils import timezone

from .models import (
    APIMetric,
    PerformanceIssue
)

REGRESSION_MULTIPLIER = 2


def detect_performance_regressions():

    now = timezone.now()

    recent_cutoff = now - timedelta(hours=1)

    historical_cutoff = now - timedelta(days=1)

    unique_paths = (
        APIMetric.objects
        .values_list("path", flat=True)
        .distinct()
    )

    for path in unique_paths:

        recent_avg = (
            APIMetric.objects
            .filter(
                path=path,
                created_at__gte=recent_cutoff
            )
            .aggregate(
                Avg("response_time_ms")
            )["response_time_ms__avg"]
        )

        historical_avg = (
            APIMetric.objects
            .filter(
                path=path,
                created_at__gte=historical_cutoff,
                created_at__lt=recent_cutoff
            )
            .aggregate(
                Avg("response_time_ms")
            )["response_time_ms__avg"]
        )

        if not recent_avg or not historical_avg:
            continue

        if recent_avg > (
            historical_avg * REGRESSION_MULTIPLIER
        ):

            latest_metric = (
                APIMetric.objects
                .filter(path=path)
                .latest("created_at")
            )

            PerformanceIssue.objects.create(
                api_metric=latest_metric,
                issue_type="regression",
                severity="critical",
                message=(
                    f"Performance regression detected "
                    f"for {path}. "
                    f"Historical avg: "
                    f"{historical_avg:.2f} ms, "
                    f"Recent avg: "
                    f"{recent_avg:.2f} ms"
                )
            )