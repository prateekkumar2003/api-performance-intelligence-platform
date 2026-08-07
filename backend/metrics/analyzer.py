from .models import PerformanceIssue
from collections import Counter

from .query_utils import normalize_query


SLOW_API_THRESHOLD_MS = 1000
SLOW_QUERY_THRESHOLD_MS = 200
HIGH_QUERY_COUNT_THRESHOLD = 10


def analyze_api_metric(api_metric):

    # Slow API detection
    if api_metric.response_time_ms > SLOW_API_THRESHOLD_MS:

        PerformanceIssue.objects.create(
            api_metric=api_metric,
            issue_type="slow_api",
            message=(
                f"API took "
                f"{api_metric.response_time_ms:.2f} ms"
            ),
            severity="critical"
        )

    sql_queries = api_metric.sql_queries.all()

    # High query count detection
    if sql_queries.count() > HIGH_QUERY_COUNT_THRESHOLD:

        PerformanceIssue.objects.create(
            api_metric=api_metric,
            issue_type="high_query_count",
            message=(
                f"API executed "
                f"{sql_queries.count()} queries"
            ),
            severity="warning"
        )

    # Slow query detection
    for query in sql_queries:

        if query.execution_time_ms > SLOW_QUERY_THRESHOLD_MS:

            PerformanceIssue.objects.create(
                api_metric=api_metric,
                issue_type="slow_query",
                message=(
                    f"Slow query detected "
                    f"({query.execution_time_ms:.2f} ms)"
                ),
                severity="warning"
            )
    detect_n_plus_one(api_metric)


def detect_n_plus_one(api_metric):

    sql_queries = api_metric.sql_queries.all()

    normalized_queries = []

    for query in sql_queries:

        normalized = normalize_query(query.query)

        normalized_queries.append(normalized)

    query_counter = Counter(normalized_queries)

    for query_pattern, count in query_counter.items():

        if count >= 5:

            PerformanceIssue.objects.create(
                api_metric=api_metric,
                issue_type="n_plus_one",
                message=(
                    f"Potential N+1 detected. "
                    f"Repeated query executed {count} times."
                ),
                severity="critical"
            )