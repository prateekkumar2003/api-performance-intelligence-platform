import time

from django.db import connection
import random

from .constants import REQUEST_SAMPLING_RATE

from .models import APIMetric, SQLQueryMetric
# from .analyzer import analyze_api_metric
from .tasks import analyze_metric_task


class MetricsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        should_sample = (
            random.random() < REQUEST_SAMPLING_RATE
        )

        initial_query_count = len(connection.queries)

        start_time = time.time()

        response = self.get_response(request)

        end_time = time.time()

        response_time_ms = (end_time - start_time) * 1000

        if not should_sample:
            return response
        api_metric = APIMetric.objects.create(
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            response_time_ms=response_time_ms
        )

        executed_queries = connection.queries[initial_query_count:]

        for query_data in executed_queries:

            query_sql = query_data.get("sql")

            execution_time = float(query_data.get("time")) * 1000

            SQLQueryMetric.objects.create(
                api_metric=api_metric,
                query=query_sql,
                execution_time_ms=execution_time
            )

        analyze_metric_task.delay(api_metric.id)

        return response