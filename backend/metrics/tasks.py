from celery import shared_task

from .analyzer import analyze_api_metric
from .models import APIMetric
from datetime import timedelta

from django.utils import timezone

from .constants import METRICS_RETENTION_DAYS
from .regression_detector import (
    detect_performance_regressions
)
from .recommendation_engine import (
    generate_recommendations
)


@shared_task
def detect_regressions_task():

    detect_performance_regressions()


@shared_task
def analyze_metric_task(api_metric_id):

    api_metric = APIMetric.objects.get(
        id=api_metric_id
    )

    analyze_api_metric(api_metric)

    generate_recommendations(api_metric)


@shared_task
def cleanup_old_metrics():

    cutoff_date = (
        timezone.now()
        - timedelta(days=METRICS_RETENTION_DAYS)
    )

    deleted_count, _ = (
        APIMetric.objects
        .filter(created_at__lt=cutoff_date)
        .delete()
    )

    return deleted_count